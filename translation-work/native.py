"""Sacred 2 L10C v258 + English name-generator resources, stdlib only."""
import collections
import heapq
import re
import struct

RES = 'locale/en_UK/global.res'
CSV_NAMES = ('AppendBonus', 'AppendMaterial', 'AppendRare', 'DescriptionBonus',
             'DescriptionMaterial', 'DescriptionRare', 'Itemnames', 'Optional')
PATHS = (RES,) + tuple(f'locale/en_UK/{n}.csv' for n in CSV_NAMES)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_res(data):
    require(len(data) >= 20, 'Truncated RES')
    magic, version, nh, nd = struct.unpack_from('<4sIII', data)
    require(magic == b'L10C' and version == 258, 'Only L10C version 258 is supported')
    p = 16 + 4 * nh
    require(p + nd * 12 + 4 <= len(data), 'Invalid RES table bounds')
    hashes = list(struct.unpack_from(f'<{nh}I', data, 16))
    require(len(set(hashes)) == len(hashes), 'Duplicate hash-list keys')
    descriptors = list(struct.iter_unpack('<III', data[p:p + 12 * nd]))
    require(len({d[0] for d in descriptors}) == nd, 'Duplicate RES text keys')
    p += nd * 12
    nn, = struct.unpack_from('<I', data, p)
    p += 4
    require(nn <= 65536 and p + nn * 8 <= len(data), 'Invalid Huffman tree bounds')
    nodes = list(struct.iter_unpack('<HHHH', data[p:p + nn * 8]))
    for i, (left, right, char, pad) in enumerate(nodes):
        # Unused uint16 + leaf child fields contain nonzero opaque data in the
        # original. Proven community codec and the tested game ignore them.
        if char == 0:
            require(left < nn and right < nn, 'Invalid Huffman child')
    payload = memoryview(data)[p + nn * 8:]
    pairs = []
    for key, off, length in descriptors:
        require(length <= 1000000 and off + length <= len(payload) * 8,
                f'Invalid string bounds: {key}')
        units = bytearray()
        for _ in range(length):
            index, steps = 0, 0
            while nodes[index][2] == 0:
                require(off < len(payload) * 8 and steps <= nn, 'Truncated/cyclic Huffman stream')
                index = nodes[index][(payload[off >> 3] >> (off & 7)) & 1]
                off += 1
                steps += 1
            units.extend(struct.pack('<H', nodes[index][2]))
        pairs.append((key, units.decode('utf-16le', errors='strict')))
    return hashes, pairs


def write_res(hashes, pairs):
    require(len(set(hashes)) == len(hashes), 'Duplicate hash-list keys')
    require(len({k for k, _ in pairs}) == len(pairs), 'Duplicate RES text keys')
    encoded = [(k, list(struct.unpack(f'<{len(t.encode("utf-16le")) // 2}H',
                                     t.encode('utf-16le')))) for k, t in pairs]
    frequency = collections.Counter(c for _, units in encoded for c in units)
    require(0 not in frequency, 'NUL cannot be a Huffman leaf')
    serial = 0
    heap = []
    for char, count in sorted(frequency.items()):
        heapq.heappush(heap, (count, serial, char))
        serial += 1
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, (a[0] + b[0], serial, (a[2], b[2])))
        serial += 1
    table, codes = [], {}

    def visit(node, code):
        index = len(table)
        table.append(None)
        if isinstance(node, int):
            table[index] = (0, 0, node, 0)
            codes[node] = code
        else:
            left = visit(node[0], code + (0,))
            right = visit(node[1], code + (1,))
            table[index] = (left, right, 0, 0)
        return index

    if heap:
        visit(heap[0][2], (0,) if isinstance(heap[0][2], int) else ())
    require(len(table) <= 65536, 'Too many Huffman nodes')
    payload, descriptors, bit = bytearray(), [], 0
    for key, units in encoded:
        descriptors.append((key, bit, len(units)))
        for char in units:
            for value in codes[char]:
                if bit % 8 == 0:
                    payload.append(0)
                payload[-1] |= value << (bit % 8)
                bit += 1
    # Engine archives contain trailing padding; make it deterministic.
    payload.extend(b'\0\0')
    result = bytearray(struct.pack('<4sIII', b'L10C', 258, len(hashes), len(pairs)))
    for h in hashes:
        result.extend(struct.pack('<I', h))
    for descriptor in descriptors:
        result.extend(struct.pack('<III', *descriptor))
    result.extend(struct.pack('<I', len(table)))
    for node in table:
        result.extend(struct.pack('<HHHH', *node))
    result.extend(payload)
    return bytes(result)


def csv_units(path, data):
    """Stable scope = native row key + alternative slot; never fuzzy-match slots."""
    text = data.decode('cp1252', errors='strict')
    units, seen = [], set()
    for row, line in enumerate(text.splitlines(keepends=True)):
        cells = line.rstrip('\r\n').split(';')
        if not line.strip() or cells[0] == 'hasGender=false':
            continue
        require(cells[0] and len(cells) > 1, f'Unknown CSV grammar: {path}:{row + 1}')
        if not any(cells[1:]):
            continue  # Preserve native empty rows, including the duplicate RESISTANCE row.
        require(cells[0] not in seen, f'Duplicate CSV key: {path}:{cells[0]}')
        seen.add(cells[0])
        for slot, value in enumerate(cells[1:], 1):
            if not value:
                continue
            suffix = ''
            if path.endswith('/Itemnames.csv'):
                match = re.fullmatch(r'(.*)(,[0-9]+)', value)
                require(match is not None, f'Unknown item-name suffix: {value}')
                value, suffix = match.groups()
            units.append((f'{cells[0]}:{slot}', value,
                          {'row': row, 'slot': slot, 'suffix': suffix, 'scope': cells[0]}))
    return units


def records(path, data):
    if path == RES:
        _, pairs = read_res(data)
        units = [(str(k), t, {'row': i}) for i, (k, t) in enumerate(pairs)]
    else:
        require(path in PATHS, f'Unsupported source resource: {path}')
        units = csv_units(path, data)
    return [dict(id=f'{path}#{key}', key=key, source_file=path, EN=text,
                 PTBR='', **metadata) for key, text, metadata in units]


def rebuild(path, data, translations):
    if path == RES:
        hashes, pairs = read_res(data)
        if all(translations[f'{path}#{k}'] == text for k, text in pairs):
            return data  # Preserve every opaque byte on a no-op build.
        result = write_res(hashes, [(k, translations[f'{path}#{k}']) for k, _ in pairs])
        require(read_res(result) == (hashes, [(k, translations[f'{path}#{k}']) for k, _ in pairs]),
                'Native RES reconstruction mismatch')
        return result
    lines = data.decode('cp1252').splitlines(keepends=True)
    for key, _, loc in csv_units(path, data):
        row, slot = loc['row'], loc['slot']
        old = lines[row]
        ending = '\r\n' if old.endswith('\r\n') else '\n' if old.endswith('\n') else ''
        cells = old.rstrip('\r\n').split(';')
        text = translations[f'{path}#{key}']
        require(not any(c in text for c in ';\r\n'), 'CSV delimiter/newline in translation')
        cells[slot] = text + loc['suffix']
        lines[row] = ';'.join(cells) + ending
    result = ''.join(lines).encode('cp1252', errors='strict')
    expected = [(key, translations[f'{path}#{key}'], loc) for key, _, loc in csv_units(path, data)]
    require(csv_units(path, result) == expected, 'Native CSV reconstruction mismatch')
    return result


# Preserve native tags exactly, including legacy unbalanced markup. Unknown angle
# annotations are conservative review constraints, not inferred spoken dialogue.
TOKENS = re.compile(r'<[^>]*>|%\{[^}]*\}\d+|%(?:\d+\$)?[-+0 #]*\d*(?:\.\d+)?[sdifugxX]|%\d+|\{\d+\}|https?://[^\s<>]+')


def validate_translation(record):
    text = record['PTBR']
    require(isinstance(text, str), f'PTBR must be a string: {record["id"]}')
    if not text:
        return
    require(text.strip(), f'Whitespace-only PTBR: {record["id"]}')
    require(not any(ord(c) < 32 and c not in '\r\n\t' for c in text), 'Forbidden control character')
    require(all(text.count(c) == record['EN'].count(c) for c in '\r\n\t'),
            f'Native line-break/tab counts changed: {record["id"]}')
    require(collections.Counter(TOKENS.findall(text)) == collections.Counter(TOKENS.findall(record['EN'])),
            f'Protected syntax changed: {record["id"]}')
    # Tag order is structural; printf order may be grammatical only for indexed tokens.
    require(re.findall(r'<[^>]*>', text) == re.findall(r'<[^>]*>', record['EN']),
            f'Tag order changed: {record["id"]}')
    plain_printf = r'%(?:[-+0 #]*\d*(?:\.\d+)?[sdifugxX])'
    require(re.findall(plain_printf, text) == re.findall(plain_printf, record['EN']), 'Unindexed printf order changed')
    if record['source_file'] != RES:
        require(not any(c in text for c in ';\r\n'), 'CSV delimiter/newline in translation')
        text.encode('cp1252', errors='strict')
    else:
        text.encode('utf-16le', errors='strict')
