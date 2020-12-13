#!/usr/bin/env python3
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


def is_legal(char):
  x = ord(char)
  return 0x4e00 <= x <= 0x9fff


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
    with open('raw/hskhsk/{}.tsv'.format(level), encoding='utf-8-sig') as fin:
      for line in fin:
        line = line.strip().split('\t')
        line[2] = level
        word = line[0]
        for char in set(word):
          if not is_legal(char):
            print('Skipping "{}" (U+{})'.format(char, hex(ord(char))))
            continue
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
        'info': char_to_infos[char],
        'words': char_to_words[char],
        'strokes': paths,
      }
      with open('vocab/{}.json'.format(ord(char)), 'w') as fout:
        json.dump(info, fout, ensure_ascii=False)
  

if __name__ == '__main__':
  main()

