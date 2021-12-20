#!/usr/bin/env python
# -*- coding: utf-8 -*-


def yield_subtlex_freq_chars():
    with open('raw/subtlex-ch/SUBTLEX-CH-CHR.utf8') as fin:
        header = '"'
        while header.startswith('"'):
            header = fin.readline().rstrip('\n')
        header = header.split('\t')
        for line in fin:
            line = dict(zip(header, line.rstrip('\n').split('\t')))
            char = line['Character']
            freq = float(line['CHR/million'])
            yield (freq, char)


def yield_subtlex_freq_words():
    with open('raw/subtlex-ch/SUBTLEX_CH_131210_CE.utf8', encoding='utf-8-sig') as fin:
        header = fin.readline().rstrip('\n').split('\t')
        for line in fin:
            line = dict(zip(header, line.rstrip('\n').split('\t')))
            word = line['Word']
            freq = float(line['W.million'])
            yield (freq, word)
