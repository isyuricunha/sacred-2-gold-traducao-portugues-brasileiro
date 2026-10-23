#!/usr/bin/env python3
"""Plan a verified PT-BR GitHub Release without changing repository state.

Runs after toolkit.py verify-output and package. GitHub Actions provides a list
of *published* releases; tags are fetched by checkout with fetch-depth: 0.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'translation-work'
VERSION_RE = re.compile(r'^v(\d+)\.(\d+)\.(\d+)$')
BATCH_RE = re.compile(r'^translation-work/translations/batch-\d{4}\.jsonl$')


def git(*args, check=True):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.decode(errors='replace').strip()}")
    return result


def revisions(releases):
    accepted = []
    for release in releases:
        if release.get('isDraft') or release.get('isPrerelease'):
            continue
        name = release.get('tagName', '')
        match = VERSION_RE.fullmatch(name)
        if match:
            accepted.append((tuple(map(int, match.groups())), name))
    accepted.sort()
    return accepted[-1][1] if accepted else None


def source_rows(revision):
    """Read approved PTBR strings from the tagged/current JSONL snapshots."""
    names = git('ls-tree', '-r', '--name-only', revision,
                '--', 'translation-work/translations/').stdout.decode().splitlines()
    result = {}
    for path in names:
        if not BATCH_RE.fullmatch(path):
            continue
        payload = git('show', f'{revision}:{path}').stdout
        for line in payload.splitlines():
            item = json.loads(line)
            rid = item['id']
            if rid in result:
                raise ValueError(f'Duplicate localization unit: {rid}')
            result[rid] = item['PTBR']
    return result


def native_files(revision='HEAD'):
    result = git('ls-tree', '-r', '--name-only', revision, '--', 'PTBR/').stdout.decode().splitlines()
    result = [name.removeprefix('PTBR/') for name in result if name.startswith('PTBR/')]
    if not result:
        raise ValueError('No PTBR resources committed; a complete build must be committed first')
    return sorted(result)


def plan(releases, repo):
    head = git('rev-parse', 'HEAD').stdout.decode().strip()
    current_files = native_files()
    previous = revisions(releases)
    if previous:
        tagged = git('rev-parse', '--verify', f'refs/tags/{previous}^{{commit}}').stdout.decode().strip()
        ancestor = git('merge-base', '--is-ancestor', tagged, head, check=False)
        if ancestor.returncode:
            raise ValueError(f'Published release {previous} is not an ancestor of this commit')
        unchanged = git('diff', '--quiet', previous, 'HEAD', '--', 'PTBR/', check=False)
        if unchanged.returncode not in (0, 1):
            raise ValueError('Could not compare deployed PTBR resources')
        if unchanged.returncode == 0:
            return {'publish': False, 'tag': previous, 'previous': previous,
                    'reason': 'PTBR files are identical to the latest published release'}
        major, minor, patch = map(int, VERSION_RE.fullmatch(previous).groups())
        tag = f'v{major}.{minor}.{patch + 1}'
    else:
        tag = 'v1.0.0'

    # Guard against a tag existing for another commit (e.g. a stale failed run).
    existing = git('rev-parse', '--verify', '--quiet', f'refs/tags/{tag}^{{commit}}', check=False)
    if existing.returncode == 0 and existing.stdout.decode().strip() != head:
        raise ValueError(f'Version tag {tag} exists at a different commit; refusing to retag')
    if existing.returncode not in (0, 1):
        raise ValueError(f'Could not inspect version tag {tag}')

    receipt = json.loads((WORK / 'build-manifest.json').read_text(encoding='utf-8'))
    if receipt.get('pending') != 0 or receipt.get('completed') != receipt.get('records'):
        raise ValueError('Build receipt is not complete')
    zip_path = ROOT / 'PTBR.zip'
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    with zipfile.ZipFile(zip_path) as archive:
        members = sorted(archive.namelist())
        if members != current_files:
            raise ValueError('ZIP contents do not match committed PTBR resources')

    if previous:
        before = source_rows(previous)
        after = source_rows('HEAD')
        added = [key for key in after if key not in before]
        removed = [key for key in before if key not in after]
        edited = [key for key in after if key in before and before[key] != after[key]]
        modified = git('diff', '--name-only', previous, 'HEAD', '--', 'PTBR/').stdout.decode().splitlines()
        notes = [
            f'# Sacred 2 Gold — Tradução PT-BR {tag}',
            '',
            f'Atualização automática sobre a versão **{previous}**.',
            '',
            '## Changelog',
            f'- **{len(edited)}** textos revisados/alterados.',
            f'- **{len(added)}** novas unidades de tradução.',
            f'- **{len(removed)}** unidades removidas.',
            f'- **{len(modified)}** arquivos nativos modificados.',
            '',
            '### Recursos atualizados',
            *[f'- `{p.removeprefix("PTBR/")}`' for p in modified],
            '',
        ]
        if not (edited or added or removed):
            notes.append('As alterações ocorreram nos recursos nativos/empacotamento sem mudanças detectadas nos valores PT-BR dos JSONL.')
            notes.append('')
        notes.append(f'[Comparar commits desde {previous}](https://github.com/{repo}/compare/{previous}...{tag})')
    else:
        notes = [
            f'# Sacred 2 Gold — Tradução PT-BR {tag}',
            '',
            '## Primeira versão',
            f'- **{receipt["records"]:,}** entradas localizadas em português brasileiro.'.replace(',', '.'),
            f'- **{len(current_files)}** recursos nativos do idioma `en_UK` para instalação.',
            '- Inclui Sacred 2 Gold / Ice & Blood conforme a base inglesa documentada neste projeto.',
            '',
            'Esta é a primeira publicação integral da tradução.',
        ]
    notes += [
        '',
        '## Instalação',
        'Baixe **PTBR.zip** nos arquivos desta Release. Com o jogo fechado, faça backup dos arquivos originais; '
        'extraia o ZIP e copie o conteúdo de `locale/` para a raiz da instalação, preservando os caminhos.',
        'Consulte o [README](../) para compatibilidade e instruções completas.',
        '',
        '## Integridade',
        f'- SHA-256 de `PTBR.zip`: `{digest}`',
        f'- Commit: `{head}`',
        f'- Entradas verificadas: {receipt["completed"]:,}'.replace(',', '.'),
        '',
        '*A verificação técnica do pacote não substitui o teste de instalação e jogabilidade.*',
        ''
    ]
    return dict(publish=True, tag=tag, previous=previous, sha=head, zip_sha256=digest,
                notes='\n'.join(notes), files=len(current_files))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['plan'])
    parser.add_argument('--releases-json', required=True)
    parser.add_argument('--notes-file', required=True)
    parser.add_argument('--plan-file', required=True)
    parser.add_argument('--github-output')
    parser.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY',
                                                         'isyuricunha/sacred-2-gold-traducao-portugues-brasileiro'))
    args = parser.parse_args()
    published = json.loads(Path(args.releases_json).read_text(encoding='utf-8'))
    if not isinstance(published, list):
        raise ValueError('Expected GitHub release list')
    result = plan(published, args.repo)
    notes = result.pop('notes', '')
    Path(args.notes_file).write_text(notes, encoding='utf-8')
    Path(args.plan_file).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n',
                                    encoding='utf-8')
    if args.github_output:
        with Path(args.github_output).open('a', encoding='utf-8') as out:
            out.write(f'publish={str(result["publish"]).lower()}\n')
            if result['publish']:
                out.write(f'tag={result["tag"]}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as err:
        print(f'Erro no planejamento da Release: {err}', file=sys.stderr)
        raise SystemExit(1)
