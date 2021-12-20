#!/usr/bin/env python
# -*- coding: utf-8 -*-

BCC_TOTAL = 18577726082


def yield_bcc_freq_words():
    with open('raw/bcc/bcc.txt') as fin:
        for line in fin:
            line = line.rstrip().split('\t')
            word = line[1]
            freq = float(line[2]) * 1e6 / BCC_TOTAL
            yield (freq, word)
