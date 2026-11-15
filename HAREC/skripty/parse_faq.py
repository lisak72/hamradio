"""Parse ČTÚ question bank text (pdftotext -layout) – class A part only."""
import re, json, sys

PUA = {'': 'Ω', '': '°', '': 'λ', '': '∞', '': '%', '': 'μ'}


def clean(s):
    for k, v in PUA.items():
        s = s.replace(k, v)
    return s


def parse(path):
    lines = [clean(l.rstrip('\n')) for l in open(path, encoding='utf-8')]
    # class A: from "(1) Průkaz HAREC" to "(2) Průkaz NOVICE"
    start = next(i for i, l in enumerate(lines) if 'Průkaz HAREC operátora třídy A' in l)
    end = next(i for i, l in enumerate(lines) if 'Průkaz NOVICE operátora třídy N' in l)
    lines = lines[start:end]

    parts = []          # [{title, sections:[{label,title,items:[{n,q,a}] , raw:[]}], dist:[(label,count)], total}]
    part = sec = item = None
    mode = 'q'          # 'q' normal, 'dist' distribution table
    state = None        # 'q' collecting question, 'a' collecting answer
    for l in lines:
        s = l.strip()
        if not s or re.fullmatch(r'\d+ / \d+', s):
            continue
        m = re.match(r'Zkušební otázky a správné odpovědi pro třídu A\s*[–-]\s*(.*?):?$', s)
        if m:
            part = {'title': m.group(1).strip(' :'), 'sections': [], 'dist': [], 'total': None}
            parts.append(part)
            sec = item = None
            mode = 'q'
            continue
        if part is None:
            continue
        if s.startswith('Zkušební otázky jsou členěny') or re.match(r'Oddíl\s+Počet', s):
            mode = 'dist'
            part['dist_text'] = s
            continue
        if mode == 'dist':
            for lab, cnt in re.findall(r'([a-j])\)\s+(\d+)', s):
                part['dist'].append((lab, int(cnt)))
            m = re.match(r'Celkem\s+(\d+)', s)
            if m:
                part['total'] = int(m.group(1))
            continue
        m = re.match(r'^([a-j])\)\s+(.*)$', s)
        if m and not re.match(r'^\d', m.group(2)):
            sec = {'label': m.group(1), 'title': m.group(2).strip(), 'items': [], 'raw': []}
            part['sections'].append(sec)
            item = None
            state = None
            continue
        if sec is None:
            continue
        m = re.match(r'^(\d+)\.\s+(.*)$', s)
        if m:
            item = {'n': int(m.group(1)), 'q': m.group(2).strip(), 'a': ''}
            sec['items'].append(item)
            state = 'q'
            # answer on same line after "Country: X"
            mm = re.match(r'^(.*?:)\s+(\S.*)$', item['q'])
            if mm and not item['q'].endswith(':'):
                item['q'], item['a'] = mm.group(1), mm.group(2)
                state = 'a'
            continue
        if item is None:
            sec['raw'].append(s)
            continue
        if state == 'q':
            if s.startswith('-') or re.search(r'[:?]$', item['q']):
                state = 'a'
                item['a'] = re.sub(r'^-\s*', '', s)
            else:
                item['q'] += ' ' + s
        else:
            item['a'] = (item['a'] + ' ' + s).strip()
    return parts


if __name__ == '__main__':
    parts = parse(sys.argv[1])
    json.dump(parts, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for p in parts:
        print('PART', p['title'], p['dist'], p['total'])
        for s in p['sections']:
            print('  ', s['label'], s['title'], len(s['items']), 'raw', len(s['raw']))
