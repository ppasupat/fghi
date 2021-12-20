#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from collections import defaultdict


def get_word_to_pron_gloss():
    cedict = defaultdict(list)
    with open('raw/cc-cedict/cedict_ts.u8') as fin:
        fin.readline()        # Avoid the BOM
        for line in fin:
            if line[0] == '#':
                continue
            m = re.match(r'^(\S+) (\S+) \[([^]]+)\] /(.*)/$', line.rstrip('\n'))
            assert m is not None, line
            _, word, pron, gloss = m.groups()
            pron = pinyin_utils.decode_pinyin(pron)
            gloss = gloss.replace('/', '; ')
            cedict[word].append([pron, gloss])
    return dict(cedict)
