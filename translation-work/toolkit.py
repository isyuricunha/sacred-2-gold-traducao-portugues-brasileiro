#!/usr/bin/env python3
"""Offline manual-localization workflow. All writes confined to this repository."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import uuid
import zipfile

from native import PATHS, RES, records, rebuild, require, validate_translation

ROOT = Path(__file__).resolve().parent.parent
WORK = 'translation-work/'
TRANSLATIONS = WORK + 'translations'
SNAPSHOT = WORK + 'accepted-sources'
REPORTS = WORK + 'reports'
BUILD = WORK + 'build-manifest.json'
STATE = WORK + '.state'
SCHEMA = 1


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf8')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(value):
    return sha(blob(value))


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def safe(root, rel):
    p = PurePosixPath(rel)
    require(rel and not p.is_absolute() and '\\' not in rel and ':' not in rel
            and all(x not in ('', '.', '..') for x in rel.split('/')), f'Unsafe path: {rel}')
    root = root.absolute()
    require(not root.is_symlink() and not (hasattr(root, 'is_junction') and root.is_junction()), f'Linked root: {root}')
    target = root / rel
    require(target.resolve().is_relative_to(root.resolve()), f'Escaping path: {target}')
    for part in [target, *target.parents]:
        if part == root.parent:
            break
        require(not part.is_symlink() and not (hasattr(part, 'is_junction') and part.is_junction()),
                f'Linked path: {part}')
    return target


def inventory(root):
    if not root.exists():
        return {}
    require(root.is_dir() and not root.is_symlink(), f'Invalid root: {root}')
    found, folded = {}, set()
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(parent) / name
            rel = p.relative_to(root).as_posix()
            safe(root, rel)
            require(rel.casefold() not in folded, f'Case collision: {rel}')
            folded.add(rel.casefold())
        for name in files:
            p = Path(parent) / name
            require(p.is_file(), f'Not a regular file: {p}')
            found[p.relative_to(root).as_posix()] = sha(p.read_bytes())
    return dict(sorted(found.items()))


def read_sources(root):
    inv = inventory(root)
    require(set(inv) == set(PATHS), f'Incomplete/unknown sources; expected exactly: {list(PATHS)}; found {list(inv)}')
    return {p: safe(root, p).read_bytes() for p in PATHS}


def source_records(sources):
    result = []
    for path, data in sources.items():
        result.extend(records(path, data))
    require(len({r['id'] for r in result}) == len(result), 'Duplicate native identity')
    for r in result:
        r['source_fingerprint'] = fingerprint({k: v for k, v in r.items() if k not in ('PTBR', 'row')})
    return result


def source_inventory(sources):
    return {p: sha(data) for p, data in sorted(sources.items())}


def durable(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def atomic_json(path, obj):
    tmp = path.with_suffix('.tmp')
    durable(tmp, blob(obj))
    os.replace(tmp, path)


class Project:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()

    def path(self, rel):
        return safe(self.root, rel)

    def state_inventory(self):
        result = {}
        for rel in ('EN', TRANSLATIONS, SNAPSHOT, REPORTS, 'PTBR'):
            result[rel] = inventory(self.path(rel))
        p = self.path(BUILD)
        result[BUILD] = sha(p.read_bytes()) if p.exists() else None
        return result

    def interrupted(self):
        p = self.path(STATE + '/journal.json')
        return p.exists()

    @contextlib.contextmanager
    def lock(self):
        p = self.path(STATE + '/operation.lock')
        p.parent.mkdir(parents=True, exist_ok=True)
        f = p.open('a+b')
        try:
            if os.name == 'nt':
                import msvcrt
                f.seek(0)
                if f.read(1) == b'':
                    f.write(b'0')
                    f.flush()
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            f.close()
            raise ValueError('Another toolkit operation holds the lock')
        try:
            yield
        finally:
            f.close()

    def recover(self):
        journal = self.path(STATE + '/journal.json')
        if not journal.exists():
            return {'status': 'no-interrupted-transaction'}
        j = read_json(journal)
        base = self.path(STATE + '/transactions/' + j['transaction'])
        # Inspect every affected live tree before recovery, never overwrite edits.
        for rel in j['targets']:
            target = self.path(rel)
            current = self.tree_digest(target)
            require(current in (j['before'][rel], j['after'][rel], None),
                    f'Recovery conflict: {rel}; preserve edits before recovery')
        for rel in j['targets']:
            target, old = self.path(rel), safe(base / 'old', rel)
            if old.exists():
                if target.exists():
                    saved = safe(base / 'aborted', rel)
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    if saved.exists():
                        require(self.tree_digest(target) == j['before'][rel], 'Recovery conflict')
                        continue
                    os.replace(target, saved)
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(old, target)
            elif j['before'][rel] is None and target.exists():
                saved = safe(base / 'aborted', rel)
                saved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(target, saved)
        journal.unlink()
        return {'status': 'rolled-back-interrupted-transaction', 'snapshot': str(base)}

    @staticmethod
    def tree_digest(path):
        if not path.exists():
            return None
        return fingerprint(inventory(path)) if path.is_dir() else sha(path.read_bytes())

    def transaction(self, files, targets, expected, fail_after=None):
        require(not self.interrupted(), 'Interrupted transaction; run recover')
        tx = uuid.uuid4().hex
        base = self.path(STATE + '/transactions/' + tx)
        stage = base / 'new'
        for name, data in files.items():
            require(any(name == t or name.startswith(t + '/') for t in targets), 'Unowned transaction file')
            durable(safe(stage, name), data)
        # Empty target directories (e.g. zero records) are supported explicitly.
        for rel in targets:
            if not safe(stage, rel).exists():
                safe(stage, rel).mkdir(parents=True)
        require(self.state_inventory() == expected, 'Concurrent edits detected; nothing was promoted')
        j = {'transaction': tx, 'targets': targets,
             'before': {t: self.tree_digest(self.path(t)) for t in targets},
             'after': {t: self.tree_digest(safe(stage, t)) for t in targets}}
        atomic_json(self.path(STATE + '/journal.json'), j)
        # Deliberately leave the journal on failure: recovery rolls back all roots.
        for index, rel in enumerate(targets):
            target, old = self.path(rel), safe(base / 'old', rel)
            if target.exists():
                old.parent.mkdir(parents=True, exist_ok=True)
                os.replace(target, old)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(safe(stage, rel), target)
            if fail_after == index:
                raise RuntimeError('Injected interrupted promotion')
        for rel in targets:
            require(self.tree_digest(self.path(rel)) == j['after'][rel], 'Promotion mismatch; run recover')
        atomic_json(base / 'receipt.json', j)
        self.path(STATE + '/journal.json').unlink()
        return tx

    def load(self, allow_en_changed=False):
        require(not self.interrupted(), 'Interrupted transaction: run toolkit.py recover before reading state')
        manifest = read_json(self.path(TRANSLATIONS + '/manifest.json'))
        require(manifest['schema'] == SCHEMA, 'Unsupported manifest schema')
        sources = read_sources(self.path(SNAPSHOT))
        require(source_inventory(sources) == manifest['sources'], 'Accepted snapshot fingerprints mismatch')
        require(fingerprint(manifest['sources']) == manifest['generation'], 'Invalid generation')
        if not allow_en_changed:
            require(inventory(self.path('EN')) == manifest['sources'], 'EN differs from accepted generation: run sync')
        canonical = {r['id']: r for r in source_records(sources)}
        batches, seen = {}, set()
        expected_names = set(manifest['batches']) | {'manifest.json'}
        require(set(inventory(self.path(TRANSLATIONS))) == expected_names, 'Unexpected/missing batch files')
        for name in manifest['batches']:
            require(name.startswith('batch-') and name.endswith('.jsonl') and '/' not in name, 'Unsafe batch name')
            rows = [json.loads(line) for line in self.path(TRANSLATIONS + '/' + name).read_text(encoding='utf8').splitlines()]
            require(len(rows) <= 500, 'Batch exceeds 500 entries')
            for r in rows:
                rid = r['id']
                require(rid in canonical and rid not in seen, f'Unknown/duplicate ID: {rid}')
                seen.add(rid)
                require({k: v for k, v in r.items() if k not in ('PTBR', 'history')}
                        == {k: v for k, v in canonical[rid].items() if k != 'PTBR'},
                        f'Immutable source fields edited: {rid}')
                require(isinstance(r.get('history', []), list), 'Invalid history')
                validate_translation(r)
            batches[name] = rows
        require(seen == set(canonical) and len(seen) == manifest['records'], 'Missing/extra records')
        return manifest, sources, batches

    def generation_fingerprint(self):
        # Raw JSONL bytes include all manual edits and their exact batch membership.
        return fingerprint(inventory(self.path(TRANSLATIONS)))

    def sync(self, sources=None, initial=False, dry_run=False):
        expected = self.state_inventory()
        exists = self.path(TRANSLATIONS + '/manifest.json').exists()
        require(not initial or not exists, 'Extraction refuses to overwrite existing progress; use sync')
        require(initial or exists, 'No accepted generation; run extract first')
        oldm, old_sources, old_batches = ({}, {}, {}) if initial else self.load(allow_en_changed=True)
        sources = sources if sources is not None else read_sources(self.path('EN'))
        require(set(sources) == set(PATHS), 'Incomplete source import')
        canonical = source_records(sources)
        sources_inv = source_inventory(sources)
        generation = fingerprint(sources_inv)
        policy = self.path(WORK + 'source-policy.json')
        if policy.exists():
            require(generation not in read_json(policy).get('rejected', []), 'Known translated source; supply original English')
        old_records = {r['id']: (name, r) for name, rows in old_batches.items() for r in rows}
        new_ids = {r['id'] for r in canonical}
        batches = {name: [] for name in old_batches}
        changes = []
        counts = dict(added=0, modified=0, removed=0, moved=0, unchanged=0, preserved_translations=0)
        new = []
        for record in canonical:
            prior = old_records.get(record['id'])
            if prior is None:
                new.append(record)
                counts['added'] += 1
                changes.append(dict(kind='added', id=record['id'], source_file=record['source_file'],
                                    previous_EN=None, EN=record['EN'], previous_PTBR=''))
                continue
            batch, old = prior
            kind = 'unchanged'
            record['history'] = old.get('history', [])
            if record['source_fingerprint'] == old['source_fingerprint']:
                record['PTBR'] = old['PTBR']
                counts['preserved_translations'] += bool(old['PTBR'])
                if record['row'] != old['row']:
                    kind = 'moved'
            else:
                kind = 'modified'
                record['history'] = record['history'] + [dict(generation=oldm['generation'],
                                                            EN=old['EN'], PTBR=old['PTBR'])]
            counts[kind] += 1
            if kind != 'unchanged':
                changes.append(dict(kind=kind, id=record['id'], source_file=record['source_file'],
                                    previous_EN=old['EN'], EN=record['EN'], previous_PTBR=old['PTBR'], batch=batch))
            batches[batch].append(record)
        for rid, (batch, old) in old_records.items():
            if rid not in new_ids:
                counts['removed'] += 1
                changes.append(dict(kind='removed', id=rid, source_file=old['source_file'],
                                    previous_EN=old['EN'], EN=None, previous_PTBR=old['PTBR'], batch=batch,
                                    archived_record=old))
        # Preserve physical batch order, even if native rows have moved.
        for name, rows in batches.items():
            order = {r['id']: i for i, r in enumerate(old_batches[name])}
            rows.sort(key=lambda r: order[r['id']])
        for record in new:
            last = next(reversed(batches), None)
            if last is None or len(batches[last]) >= 500:
                last = f'batch-{len(batches) + 1:04d}.jsonl'
                batches[last] = []
            batches[last].append(record)
        manifest = dict(schema=SCHEMA, game='Sacred 2 Gold / Ice & Blood', native='L10C-258',
                        sources=sources_inv, generation=generation, records=len(canonical), batch_size=500,
                        batches=list(batches), deployment='EN/<path> -> PTBR/<path>',
                        profile='single-English-baseline', provenance='Explicit verified original resource catalog')
        assignments = {r['id']: name for name, rows in batches.items() for r in rows}
        for c in changes:
            c.setdefault('batch', assignments.get(c['id']))
        source_changes = {p: dict(before=oldm.get('sources', {}).get(p), after=h)
                          for p, h in sources_inv.items() if oldm.get('sources', {}).get(p) != h}
        report = dict(status='proposed' if dry_run else 'accepted', previous_generation=oldm.get('generation'),
                      generation=generation, counts=counts, source_changes=source_changes, changes=changes,
                      affected_batches=sorted({c['batch'] for c in changes}),
                      existing_pending=sum(not r['PTBR'] for _, r in old_records.values()),
                      pending=sum(not r['PTBR'] for rows in batches.values() for r in rows),
                      warnings=['CSV alternative slots are contextual IDs; insertion/reordering within a row requires review.'],
                      next_action='Ella: review diff, research briefing, translate pending entries.')
        if oldm.get('sources') == sources_inv:
            if expected['EN'] == sources_inv:
                return dict(status='unchanged', generation=generation, counts=counts)
        if dry_run:
            return report
        files = {}
        for path, data in sources.items():
            files['EN/' + path] = data
            files[SNAPSHOT + '/' + path] = data
        files[TRANSLATIONS + '/manifest.json'] = blob(manifest)
        for name, rows in batches.items():
            files[TRANSLATIONS + '/' + name] = b''.join(
                (json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n').encode('utf8') for r in rows)
        # Keep removed records and diffs versioned beyond the latest sync.
        for path in inventory(self.path(REPORTS)):
            files[REPORTS + '/' + path] = self.path(REPORTS + '/' + path).read_bytes()
        report['recovery'] = 'translation-work/.state/transactions (local); accepted-sources and history are versioned'
        files[REPORTS + '/sync-latest.json'] = blob(report)
        files[REPORTS + '/history/' + generation + '.json'] = blob(report)
        files[REPORTS + '/sync-latest.md'] = (
            '# Sincronização aceita\n\nGeração: `' + generation + '`\n\n' +
            '\n'.join(f'- {k}: {v}' for k, v in counts.items()) +
            '\n\nDetalhes e IDs: sync-latest.json. Ella deve revisar os registros pendentes.\n').encode('utf8')
        # Validate staged catalog and all translations before publishing anything.
        require(len(assignments) == len(canonical), 'Staged membership mismatch')
        for rows in batches.values():
            for r in rows:
                validate_translation(r)
        report['transaction'] = self.transaction(files, ['EN', SNAPSHOT, TRANSLATIONS, REPORTS], expected)
        return report

    def apply(self, payload, replace=False):
        expected = self.state_inventory()
        manifest, _, batches = self.load()
        require(set(payload) == {'generation', 'entries'}, 'Payload requires only generation and entries')
        require(payload['generation'] == manifest['generation'], 'Wrong source generation')
        require(isinstance(payload['entries'], list), 'entries must be an array')
        by_id = {r['id']: r for rows in batches.values() for r in rows}
        seen, accepted, rejected = set(), [], []
        # Identity errors invalidate the complete payload before accepting partial text updates.
        for item in payload['entries']:
            require(set(item) == {'id', 'source_fingerprint', 'PTBR'}, 'Only ID, fingerprint and PTBR may be supplied')
            rid = item['id']
            require(rid in by_id and rid not in seen, f'Duplicate/unknown ID: {rid}')
            require(item['source_fingerprint'] == by_id[rid]['source_fingerprint'], f'Stale source: {rid}')
            seen.add(rid)
        for item in payload['entries']:
            old = by_id[item['id']]
            try:
                require(isinstance(item['PTBR'], str) and item['PTBR'] != '', 'PTBR cannot be empty')
                require(not old['PTBR'] or old['PTBR'] == item['PTBR'] or replace, 'Existing PTBR: use --replace after review')
                validate_translation(dict(old, PTBR=item['PTBR']))
                if old['PTBR'] != item['PTBR']:
                    if old['PTBR']:
                        old.setdefault('history', []).append(dict(generation=manifest['generation'], EN=old['EN'], PTBR=old['PTBR']))
                    old['PTBR'] = item['PTBR']
                    accepted.append(item['id'])
            except (ValueError, UnicodeError) as error:
                rejected.append({'id': item['id'], 'reason': str(error)})
        if accepted:
            files = {TRANSLATIONS + '/manifest.json': blob(manifest)}
            for name, rows in batches.items():
                files[TRANSLATIONS + '/' + name] = b''.join((json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n').encode('utf8') for r in rows)
            self.transaction(files, [TRANSLATIONS], expected)
        return dict(accepted=accepted, rejected=rejected, status='partial' if rejected else 'ok')

    def status(self):
        manifest, _, batches = self.load(allow_en_changed=True)
        rows = [r for batch in batches.values() for r in batch]
        try:
            self.verify_output()
            output = 'current'
        except (ValueError, OSError, KeyError) as error:
            output = 'absent/stale: ' + str(error)
        latest = self.path(REPORTS + '/sync-latest.json')
        counts = read_json(latest)['counts'] if latest.exists() else {}
        return dict(generation=manifest['generation'], files=len(manifest['sources']), records=len(rows),
                    batches=len(batches), completed=sum(bool(r['PTBR']) for r in rows),
                    pending=sum(not r['PTBR'] for r in rows), output=output,
                    latest_changes=counts,
                    en_changed=inventory(self.path('EN')) != manifest['sources'])

    def build(self):
        expected = self.state_inventory()
        manifest, sources, batches = self.load()
        rows = [r for batch in batches.values() for r in batch]
        require(all(r['PTBR'] for r in rows), f'Incomplete translation: {sum(not r["PTBR"] for r in rows)} pending; PTBR unchanged')
        translations = {r['id']: r['PTBR'] for r in rows}
        outputs = {p: rebuild(p, data, translations) for p, data in sources.items()}
        # Deep native validation is performed above, not in CI.
        output_hashes = source_inventory(outputs)
        receipt = dict(schema=SCHEMA, producer='sacred2-toolkit-build-v1', generation=manifest['generation'],
                       sources=manifest['sources'], translation_fingerprint=self.generation_fingerprint(),
                       records=len(rows), completed=len(rows), pending=0, outputs=output_hashes,
                       native_validation='parse-rebuild-parse-all-records', tooling=self.tooling_fingerprint())
        receipt['receipt_hash'] = fingerprint(receipt)
        if self.path(BUILD).exists() and read_json(self.path(BUILD)) == receipt and inventory(self.path('PTBR')) == output_hashes:
            return {'status': 'unchanged', 'outputs': output_hashes}
        files = {'PTBR/' + p: data for p, data in outputs.items()}
        files[BUILD] = blob(receipt)
        self.transaction(files, ['PTBR', BUILD], expected)
        self.verify_output()
        return dict(status='built', outputs=output_hashes, records=len(rows))

    def tooling_fingerprint(self):
        return fingerprint({name: sha(self.path(WORK + name).read_bytes()) for name in ('native.py', 'toolkit.py')})

    def verify_output(self):
        require(not self.interrupted(), 'Interrupted transaction; recover first')
        require(self.path(BUILD).is_file(), 'No successful build manifest')
        receipt = read_json(self.path(BUILD))
        keys = {'schema', 'producer', 'generation', 'sources', 'translation_fingerprint', 'records',
                'completed', 'pending', 'outputs', 'native_validation', 'tooling', 'receipt_hash'}
        require(set(receipt) == keys, 'Invalid/incomplete build receipt')
        require(receipt['schema'] == SCHEMA and receipt['producer'] == 'sacred2-toolkit-build-v1', 'Invalid producer')
        require(receipt['receipt_hash'] == fingerprint({k: v for k, v in receipt.items() if k != 'receipt_hash'}), 'Build receipt mismatch')
        manifest = read_json(self.path(TRANSLATIONS + '/manifest.json'))
        require(receipt['generation'] == manifest['generation'] == fingerprint(manifest['sources']), 'Stale source generation')
        require(receipt['sources'] == manifest['sources'] == inventory(self.path('EN')) == inventory(self.path(SNAPSHOT)), 'Stale/missing original sources')
        require(receipt['translation_fingerprint'] == self.generation_fingerprint(), 'Stale translation generation')
        require(receipt['tooling'] == self.tooling_fingerprint(), 'Tooling changed: rebuild required')
        require(receipt['records'] == receipt['completed'] == manifest['records'] and receipt['pending'] == 0, 'Incomplete build')
        require(receipt['native_validation'] == 'parse-rebuild-parse-all-records', 'Missing native validation')
        require(set(receipt['outputs']) == set(PATHS), 'Invalid output inventory')
        require(inventory(self.path('PTBR')) == receipt['outputs'], 'Missing/extra/modified output files')
        return dict(status='verified', files=len(receipt['outputs']), generation=receipt['generation'])

    def package(self):
        self.verify_output()
        approved = inventory(self.path('PTBR'))
        target = self.path('PTBR.zip')
        temp = self.path(STATE + '/PTBR.zip')
        temp.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in approved:
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, safe(self.path('PTBR'), name).read_bytes())
        with zipfile.ZipFile(temp) as archive:
            require(archive.namelist() == list(approved) and archive.testzip() is None, 'Invalid ZIP inventory')
            require({name: sha(archive.read(name)) for name in archive.namelist()} == approved, 'ZIP content mismatch')
        self.verify_output()
        os.replace(temp, target)
        return dict(status='packaged', file='PTBR.zip', sha256=sha(target.read_bytes()), members=list(approved))

    def candidate(self, args):
        if args.source_file:
            require(Path(args.source_file).name in ('global.res', 'original.res'), 'Only a RES source-file is supported')
            sources = read_sources(self.path('EN'))
            sources[RES] = Path(args.source_file).read_bytes()
            return sources
        if args.source_root:
            p = Path(args.source_root).resolve()
            require(not p.is_relative_to(self.path('PTBR')), 'PTBR cannot be an original source')
            return read_sources(p)
        if args.game_root or args.command == 'update-sources':
            candidates = []
            if args.game_root:
                candidates = [Path(args.game_root)]
            else:
                local = self.path(STATE + '/machine.json')
                if local.exists():
                    candidates = [Path(read_json(local)['game_root'])]
                else:
                    # Bounded metadata search: Steam AppID 225640, never entire-drive scanning.
                    steam = Path(os.environ.get('ProgramFiles(x86)', '/nonexistent')) / 'Steam/steamapps'
                    libraries = [steam]
                    vdf = steam / 'libraryfolders.vdf'
                    if vdf.exists():
                        import re
                        libraries += [Path(p.replace('\\\\', '\\')) / 'steamapps' for p in re.findall(r'"path"\s+"([^"]+)"', vdf.read_text(encoding='utf8'))]
                    for lib in libraries:
                        acf = lib / 'appmanifest_225640.acf'
                        if acf.exists():
                            import re
                            match = re.search(r'"installdir"\s+"([^"]+)"', acf.read_text(encoding='utf8'))
                            if match:
                                candidates.append(lib / 'common' / match[1])
            require(len(set(p.resolve() for p in candidates)) == 1,
                    'No unique verified installation. Use update-sources --game-root "GAME ROOT" (untouched English originals)')
            p = candidates[0].resolve()
            require(p != self.root and not p.is_relative_to(self.root), 'Expected external game installation')
            require((p / 'system/sacred2.exe').is_file(), 'Not Sacred 2: missing system/sacred2.exe')
            # Read ONLY managed resources, not an entire installation subtree.
            sources = {name: safe(p, name).read_bytes() for name in PATHS}
            source_records(sources)
            approved = read_json(self.path(WORK + 'source-policy.json'))
            digest = fingerprint(source_inventory(sources))
            require(digest not in approved.get('rejected', []), 'Known translated installation; use original resources')
            require(digest in approved['trusted'] or args.approve_source == digest,
                    f'Unrecognized original/modded source; cannot prove English provenance. Inspect it, then explicitly attest with --approve-source {digest}')
            if not args.dry_run:
                self._verified_game_root = str(p)
            return sources
        return None


def main(argv=None):
    # Windows consoles and redirected streams may default to cp1252; reports are UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['extract', 'sync', 'update-sources', 'check', 'diff', 'status',
                                          'apply', 'build', 'verify-output', 'package', 'recover', 'rollback'])
    parser.add_argument('--source-root')
    parser.add_argument('--source-file')
    parser.add_argument('--game-root')
    parser.add_argument('--approve-source')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--payload')
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--snapshot')
    args = parser.parse_args(argv)
    project = Project()
    try:
        require(sum(bool(v) for v in (args.source_root, args.source_file, args.game_root)) <= 1, 'Choose a single source input')
        require(not (args.source_root or args.source_file or args.game_root or args.approve_source)
                or args.command in ('extract', 'sync', 'update-sources', 'diff'), 'Source flags do not apply to this command')
        require(not args.dry_run or args.command in ('extract', 'sync', 'update-sources', 'diff'), '--dry-run is a source-operation flag')
        require(not args.replace or args.command == 'apply', '--replace is only supported by apply')
        require(not args.payload or args.command == 'apply', '--payload is only supported by apply')
        mutates = args.command in ('extract', 'sync', 'update-sources', 'apply', 'build', 'package', 'recover', 'rollback') and not args.dry_run
        with project.lock() if mutates else contextlib.nullcontext():
            if project.interrupted() and mutates and args.command != 'recover':
                project.recover()
            if args.command in ('extract', 'sync', 'update-sources'):
                result = project.sync(project.candidate(args), initial=args.command == 'extract', dry_run=args.dry_run)
                if hasattr(project, '_verified_game_root'):
                    atomic_json(project.path(STATE + '/machine.json'), {'game_root': project._verified_game_root})
            elif args.command == 'check':
                project.load()
                result = project.status()
            elif args.command == 'status':
                result = project.status()
            elif args.command == 'diff':
                candidate = project.candidate(args)
                result = {'mode': 'read-only', 'report': project.sync(candidate, dry_run=True) if candidate is not None else read_json(project.path(REPORTS + '/sync-latest.json'))}
            elif args.command == 'apply':
                require(args.payload, 'apply requires --payload FILE.json')
                result = project.apply(read_json(Path(args.payload)), args.replace)
            elif args.command == 'build':
                result = project.build()
            elif args.command == 'verify-output':
                result = project.verify_output()
            elif args.command == 'package':
                result = project.package()
            elif args.command == 'recover':
                result = project.recover()
            else:
                require(args.snapshot and len(args.snapshot) == 32 and all(c in '0123456789abcdef' for c in args.snapshot), 'rollback requires --snapshot TRANSACTION_ID')
                base = project.path(STATE + '/transactions/' + args.snapshot)
                receipt = read_json(base / 'receipt.json')
                require(all(project.tree_digest(project.path(t)) == receipt['after'][t] for t in receipt['targets']), 'Rollback would overwrite newer progress; preserve it first')
                files = {}
                require(all(receipt['before'][t] is not None for t in receipt['targets']), 'Initial extraction has no earlier generation to restore')
                for rel in receipt['targets']:
                    old = safe(base / 'old', rel)
                    require(project.tree_digest(old) == receipt['before'][rel], 'Damaged rollback snapshot')
                    if old.is_file():
                        files[rel] = old.read_bytes()
                    else:
                        for name in inventory(old):
                            files[rel + '/' + name] = safe(old, name).read_bytes()
                result = {'status': 'rolled-back', 'transaction': project.transaction(files, receipt['targets'], project.state_inventory())}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result.get('rejected') else 0
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print(json.dumps({'status': 'error', 'message': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
