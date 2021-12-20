#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json

from lib import parse_standard
from lib import parse_hsk30
from lib import parse_junda
from lib import parse_subtlex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    # HSK 1-6 and unified advanced (7-9; indexed as "7")
    char_cats = parse_hsk30.get_hsk_chars()
    # Top characters from books and movies
    char_cats['B'] = [char for _, char in parse_junda.yield_junda_freq_chars()]
    char_cats['M'] = [char for _, char in parse_subtlex.yield_subtlex_freq_chars()]
    # Table of General Standard Chinese Characters
    standard = parse_standard.get_standard()
    char_cats['F'] = standard['1']     # frequent (3500)
    char_cats['C'] = standard['2']     # common (6500)
    char_cats['S'] = standard['3']     # standard (8105)
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

