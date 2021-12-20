#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json


def _group(stuff, chars_per_line):
    for i in range(0, len(stuff), chars_per_line):
        yield stuff[i:i+chars_per_line]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    # Read character categories
    print('Reading characters')
    with open('cats.json') as fin:
        char_cats = json.load(fin)
    print('Available cats: {}'.format(list(char_cats.keys())))

    # HSK
    print('Writing grid-hsk.json')
    with open('grids/grid-hsk.json', 'w') as fout:
        print('[', file=fout)
        for level in '1234567':
            print('["#","HSK {}"],'.format('7-9' if level == '7' else level), file=fout)
            for line in _group(char_cats[level], 15):
                print('["","{}"],'.format(line), file=fout)
        print('[]]', file=fout)

    # Character frequency
    print('Writing grid-book.json')
    with open('grids/grid-book.json', 'w') as fout:
        print('[', file=fout)
        for i, line in enumerate(_group(char_cats['B'], 10)):
            print('["{}","{}"],'.format(i, line), file=fout)
        print('[]]', file=fout)
    print('Writing grid-movie.json')
    with open('grids/grid-movie.json', 'w') as fout:
        print('[', file=fout)
        for i, line in enumerate(_group(char_cats['M'], 10)):
            print('["{}","{}"],'.format(i, line), file=fout)
        print('[]]', file=fout)
    

if __name__ == '__main__':
    main()

