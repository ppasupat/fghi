#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json

from lib import parse_commonuse
from lib import parse_hsk30
from lib import parse_junda
from lib import parse_subtlex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--top-char-limit', type=int, default=1000,
            help='Number of characters for the lists of top characters')
    args = parser.parse_args()

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
    print('Wrote cats:')
    for key, value in char_cats.items():
        print(key, len(value))
    

if __name__ == '__main__':
    main()

