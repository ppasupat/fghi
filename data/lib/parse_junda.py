#!/usr/bin/env python
# -*- coding: utf-8 -*-


def yield_junda_freq_chars():
    prev_cumul_freq = 0
    with open('raw/junda/CharFreq-utf8.tsv') as fin:
        for line in fin:
            line = line.strip().split('\t')
            char = line[1]
            cumul_freq = float(line[3]) * 1e4
            yield (cumul_freq - prev_cumul_freq, char)
            prev_cumul_freq = cumul_freq
