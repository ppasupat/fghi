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
  parser.add_argument('-r', '--subtlexch-max-rank', type=int, default=999999,
      help='Maximum rank of common words from SUBTLEX-CH')
  parser.add_argument('-c', '--subtlexch-max-per-char', type=int, default=10,
      help='Maximum number of common words from SUBTLEX-CH')
  args = parser.parse_args()

  if not os.path.exists('vocab'):
    os.makedirs('vocab')

  # Read HSK words and characters
  print('Reading words and chars')
  hsk = [None] * 8
  hsk_so_far = set()
  seen_words = set()
  char_to_words = defaultdict(list)
  for level in (1,2,3,4,5,6):
    print('HSK level', level)
    hsk[level] = set()
    with open('raw/hskhsk/{}.tsv'.format(level), encoding='utf-8-sig') as fin:
      for line in fin:
        # simp, trad, pinyin_num, pinyin_tone, meaning
        line = line.strip().split('\t')
        word, pron, gloss = line[0], line[3], line[4]
        seen_words.add(word)
        line = [word, level, pron, gloss]
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
    # The keys beyond 1, ..., 6 are extra characters
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

  # Read common words
  char_to_extra_words = defaultdict(list)
  with open('raw/subtlex-ch/SUBTLEX_CH_131210_CE.utf8', encoding='utf-8-sig') as fin:
    header = fin.readline().rstrip('\n').split('\t')
    for ii, line in enumerate(fin):
      if ii >= args.subtlexch_max_rank:
        break
      line = dict(zip(header, line.rstrip('\n').split('\t')))
      word = line['Word']
      pron = line['Pinyin']
      gloss = line['Eng.Tran.'].replace('/', '; ')
      if gloss == '#':
        continue
      line = [word, ii, pron, gloss]
      if word not in seen_words:
        seen_words.add(word)
        for char in set(word):
          if not is_legal(char):
            print('Skipping "{}" (U+{})'.format(char, hex(ord(char))))
            continue
          if len(char_to_extra_words[char]) < args.subtlexch_max_per_char:
            char_to_extra_words[char].append(line)

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

