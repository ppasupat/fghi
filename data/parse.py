#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil, re, argparse, json, gzip
from collections import defaultdict, Counter
import xml.etree.ElementTree as ET


def parse_svg(char):
    filename = 'raw/makemeahanzi/svgs-still/{}-still.svg'.format(ord(char))
    tree = ET.parse(filename)
    root = tree.getroot()
    paths = []
    for x in root[1]:
        if x.tag.endswith('}path'):
            paths.append(x.attrib['d'])
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if not os.path.exists('vocab'):
        os.makedirs('vocab')

    print('Reading words and chars')
    char_to_words = defaultdict(list)
    hsk = [None] * 8
    hsk_so_far = set()
    for level in (1,2,3,4,5,6):
        print('HSK level', level)
        hsk[level] = set()
        with open('raw/hskhsk/{}.tsv'.format(level)) as fin:
            for line in fin:
                line = line.rstrip().split('\t')
                line[2] = level
                word = line[0]
                for char in set(word):
                    char_to_words[char].append(line)
                    if char not in hsk_so_far:
                        hsk[level].add(char)
        hsk_so_far.update(hsk[level])

    # Read the extra characters
    with open('hsk.json') as fin:
        all_chars = set(''.join(json.load(fin).values()))
    for level in (1,2,3,4,5,6):
        all_chars -= set(hsk[level])
    hsk[7] = sorted(all_chars)

    print('Reading characters')
    for level, chars in enumerate(hsk):
        if chars is None:
            continue
        print('HSK level {} ({} chars)'.format(level, len(chars)))
        for char in chars:
            paths = parse_svg(char)
            info = {
                'char': char,
                'level': level,
                'words': char_to_words[char],
                'strokes': paths,
            }
            with open('vocab/{}.json'.format(ord(char)), 'w') as fout:
                json.dump(info, fout, ensure_ascii=False)
    

if __name__ == '__main__':
    main()

