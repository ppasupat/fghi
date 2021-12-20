#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict


def get_char_to_infos():
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
    return dict(char_to_infos)
