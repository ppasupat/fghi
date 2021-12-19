#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, shutil, re, argparse, json, gzip
from collections import defaultdict, Counter
import xml.etree.ElementTree as ET
from pinyin_utils import decode_pinyin


BCC_TOTAL = 18577726082


HSK_WORDS_NOT_IN_CEDICT = {
    '纽扣儿': [['niu3 kou4 r5', 'button']],
    '打篮球': [['da3 lan2 qiu2', 'to play basketball']],
    '系领带': [['xi4 ling3 dai4', 'to tie a necktie']],
    '踢足球': [['ti1 zu2 qiu2', 'to play soccer']],
    '放暑假': [['fang4 shu3 jia4', 'to have a summer vacation']],
    '弹钢琴': [['tan2 gang1 qin2', 'to play the piano']],
}


def parse_svg(char):
    filename = 'raw/makemeahanzi/svgs-still/{}-still.svg'.format(ord(char))
    tree = ET.parse(filename)
    root = tree.getroot()
    paths = []
    for x in root[1]:
        if x.tag.endswith('}path'):
            paths.append(x.attrib['d'])
    return paths


def is_legal_char(char):
    x = ord(char)
    return 0x4e00 <= x <= 0x9fff


def yield_from_subtlex():
    with open('raw/subtlex-ch/SUBTLEX_CH_131210_CE.utf8', encoding='utf-8-sig') as fin:
        header = fin.readline().rstrip('\n').split('\t')
        for line in fin:
            line = dict(zip(header, line.rstrip('\n').split('\t')))
            word = line['Word']
            freq = float(line['W.million'])
            yield (freq, word)


def yield_from_bcc():
    with open('raw/bcc/bcc.txt') as fin:
        for line in fin:
            line = line.rstrip().split('\t')
            word = line[1]
            freq = float(line[2]) * 1e6 / BCC_TOTAL
            yield (freq, word)


def yield_common_words():
    """Yields (freq-per-million, word) in decreasing order."""
    s1 = iter(yield_from_subtlex())
    s2 = iter(yield_from_bcc())
    f1, w1 = next(s1)
    f2, w2 = next(s2)
    while f1 > 0 or f2 > 0:
        if f1 > f2:
            yield f1, w1
            try:
                f1, w1 = next(s1)
            except StopIteration:
                f1, w1 = -1, None
        else:
            yield f2, w2
            try:
                f2, w2 = next(s2)
            except StopIteration:
                f2, w2 = -1, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-m', '--min-common-word-freq', type=float, default=5.,
            help='Common word filter: minimum number of occurrences per 1 million words')
    args = parser.parse_args()

    if not os.path.exists('vocab'):
        os.makedirs('vocab')

    # Read HSK words and characters
    print('Reading words and chars')
    hsk = [None] * 9
    hsk_so_far = set()
    char_to_words = defaultdict(list)
    used_words = set()
    with open('raw/chinese-lexicon/statistics/hsk.json') as fin:
        hsk_raw = json.load(fin)
    for level in (1,2,3,4,5,6):
        print('HSK level', level)
        hsk[level] = set()
        for word in hsk_raw[level - 1]:
            line = [word, level]
            used_words.add(word)
            for char in set(word):
                if not is_legal_char(char):
                    print('Skipping "{}" (U+{})'.format(char, hex(ord(char))))
                    continue
                char_to_words[char].append(line)
                if char not in hsk_so_far:
                    hsk[level].add(char)
        hsk_so_far.update(hsk[level])
    print('Added {} chars + {} words.'.format(len(hsk_so_far), len(used_words)))

    # Read the extra characters
    with open('cats.json') as fin:
        # The keys beyond 1, ..., 6 are extra characters
        all_chars = set(''.join(json.load(fin).values()))
    for level in (1,2,3,4,5,6):
        all_chars -= set(hsk[level])
    hsk[7] = sorted(all_chars)
    print('Added {} extra chars.'.format(len(hsk[7])))

    # At least cover all characters from grid-fghi
    with open('grid-fghi.json') as fin:
        grid_chars = set(''.join(x[1] for x in json.load(fin)))
    for level in (1,2,3,4,5,6,7):
        grid_chars -= set(hsk[level])
    hsk[8] = sorted(grid_chars)
    print('Added {} extra extra chars.'.format(len(hsk[8])))
    print('    ({})'.format(', '.join(hsk[8])))

    # Read Unihan
    char_to_infos = defaultdict(dict)
    with open('raw/unihan/Unihan_Readings.txt') as fin:
        for line in fin:
            if line[0] == '#' or not line.strip():
                continue
            tokens = line.rstrip().split('\t')
            assert len(tokens) == 3, '||'.join(tokens)
            code, key, value = tokens
            char = chr(int(code[2:], 16))
            if key == 'kDefinition':
                char_to_infos[char]['gloss'] = value
            elif key == 'kTGHZ2013':
                char_to_infos[char]['pron'] = ', '.join(x.split(':')[-1] for x in value.split())

    # Read CEDict
    print('Reading CEDict')
    cedict = defaultdict(list)
    with open('raw/cc-cedict/cedict_ts.u8') as fin:
        fin.readline()        # Avoid the BOM
        for line in fin:
            if line[0] == '#':
                continue
            m = re.match(r'^(\S+) (\S+) \[([^]]+)\] /(.*)/$', line.rstrip('\n'))
            assert m is not None, line
            _, word, pron, gloss = m.groups()
            pron = decode_pinyin(pron)
            gloss = gloss.replace('/', '; ')
            cedict[word].append([pron, gloss])
    print('Read {} words.'.format(len(cedict)))

    # Add pronunciations and glosses to the HSK words
    for char, words in char_to_words.items():
        words_copy = words[:]
        words.clear()
        for word, level in words_copy:
            pron_gloss_list = (cedict[word] if word in cedict
                    else HSK_WORDS_NOT_IN_CEDICT.get(word))
            if not pron_gloss_list:
                print('Warning: HSK word {} not in CEDICT'.format(word))
                words.append([word, level, '???', '???'])
            else:
                for pron, gloss in pron_gloss_list:
                    words.append([word, level, pron, gloss])

    # Read common words
    char_to_extra_words = defaultdict(list)
    num_extra_words = 0
    for freq, word in yield_common_words():
        if freq < args.min_common_word_freq:
            break
        if word in used_words or word not in cedict or len(word) == 1:
            continue
        for pron, gloss in cedict[word]:
            line = [word, round(freq, 2), pron, gloss]
            for char in set(word):
                if is_legal_char(char):
                    char_to_extra_words[char].append(line)
        used_words.add(word)
        num_extra_words += 1
    print('Added {} extra words.'.format(num_extra_words))

    print('Writing information to vocab/ ...')
    for level, chars in enumerate(hsk):
        if chars is None:
            continue
        print('HSK level {} ({} chars)'.format(level, len(chars)))
        for char in chars:
            paths = parse_svg(char)
            info = {
                    'char': char,
                    'level': level,
                    'info': char_to_infos[char],
                    'words': char_to_words[char],
                    'extraWords': char_to_extra_words[char],
                    'strokes': paths,
                    }
            with open('vocab/{}.json'.format(ord(char)), 'w') as fout:
                json.dump(info, fout, ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main()

