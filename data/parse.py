#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, shutil, re, argparse, json, gzip
from collections import defaultdict, Counter

from lib import parse_bcc
from lib import parse_cedict
from lib import parse_commonuse
from lib import parse_hsk30
from lib import parse_junda
from lib import parse_makemeahanzi
from lib import parse_subtlex
from lib import parse_unihan
from lib import pinyin_utils


def is_legal_char(char):
    x = ord(char)
    return 0x4e00 <= x <= 0x9fff


def yield_common_words():
    """Yields (freq-per-million, word) in decreasing order.

    The words are unified from:
    - SUBTLEX-CH (movie subtitles)
    - BCC (BLCU Chinese Corpus)
    """
    s1 = iter(parse_subtlex.yield_subtlex_freq_words())
    s2 = iter(parse_bcc.yield_bcc_freq_words())
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
    parser.add_argument('-M', '--max-total-words', type=int, default=3,
            help='Keep adding less common words up to this number of total words')
    parser.add_argument('-t', '--top-char-limit', type=int, default=1000,
            help='Number of characters for the lists of top characters')
    args = parser.parse_args()

    if not os.path.exists('vocab'):
        os.makedirs('vocab')

    # Read characters (grouped into categories)
    print('Reading characters')
    # HSK 1-6 and unified advanced (7-9; indexed as "7")
    char_cats = parse_hsk30.get_hsk_chars()
    # Top characters from books and movies
    char_cats['B'] = []
    for _, char in parse_junda.yield_junda_freq_chars():
        char_cats['B'].append(char)
        if len(char_cats['B']) == args.top_char_limit:
            break
    char_cats['M'] = []
    for _, char in parse_subtlex.yield_subtlex_freq_chars():
        char_cats['M'].append(char)
        if len(char_cats['M']) == args.top_char_limit:
            break
    # Common use characters
    commonuse = parse_commonuse.get_commonuse()
    char_cats['C'] = commonuse['1']
    char_cats['C2'] = commonuse['2']
    char_cats['C3'] = commonuse['3']
    # Write to cats.json
    char_cats = {key: ''.join(value) for (key, value) in char_cats.items()}
    with open('cats.json', 'w') as fout:
        json.dump(char_cats, fout, indent=0, ensure_ascii=False)
        fout.write('\n')

    # Read Unihan
    print('Reading Unihan')
    char_to_infos = parse_unihan.get_char_to_infos() 
    print('Read {} characters from Unihan'.format(len(char_to_infos)))

    # Read CEDict
    print('Reading CEDict')
    cedict = parse_cedict.get_word_to_pron_gloss()
    print('Read {} words from CEDict.'.format(len(cedict)))

    # Read HSK words
    # For simplicity, ignore the annotated POS and senses
    char_to_words = defaultdict(list)
    used_words = set()
    for level, words in parse_hsk30.get_hsk_words().items():
        for word in parse_hsk30.gen_processed_words(words):
            if word in used_words:
                continue
            pron_glosses = parse_cedict.lookup_cedict(cedict, word, verbose=args.verbose)
            for char in set(word):
                if not is_legal_char(char):
                    continue
                for pron, gloss in pron_glosses:
                    line = [word, int(level), pron, gloss]
                    char_to_words[char].append(line)
            used_words.add(word)
    print('Added {} HSK words.'.format(len(used_words)))

    # Read common words
    char_to_extra_words = defaultdict(list)
    num_extra_words = 0
    for freq, word in yield_common_words():
        if word in used_words:
            continue
        pron_glosses = parse_cedict.lookup_cedict(cedict, word, verbose=args.verbose)
        for char in set(word):
            if not is_legal_char(char):
                continue
            if freq < args.min_common_word_freq and (
                    len(char_to_words[char]) + len(char_to_extra_words[char])
                    >= args.max_total_words):
                continue
            for pron, gloss in pron_glosses:
                line = [word, round(freq, 2), pron, gloss]
                char_to_extra_words[char].append(line)
        used_words.add(word)
        num_extra_words += 1
    print('Added {} extra words.'.format(num_extra_words))

    print('Writing information to vocab/ ...')
    written_chars = set()
    for level in ('1', '2', '3', '4', '5', '6', '7', 'C', 'C2', 'C3'):
        num_chars_in_level = 0
        for char in char_cats[level]:
            if char in written_chars:
                continue
            try:
                paths = parse_makemeahanzi.get_svg_paths(char)
            except FileNotFoundError:
                print('WARNING: SVG for {} not found'.format(char))
                paths = []
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
            written_chars.add(char)
            num_chars_in_level += 1
        print('Written {} characters for Level {}'.format(
            num_chars_in_level, level))


if __name__ == '__main__':
    main()

