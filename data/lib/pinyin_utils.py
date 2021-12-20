#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


# https://stackoverflow.com/a/21488584
pinyinToneMarks = {
    'a': 'āáǎà', 'e': 'ēéěè', 'i': 'īíǐì',
    'o': 'ōóǒò', 'u': 'ūúǔù', 'ü': 'ǖǘǚǜ',
    'A': 'ĀÁǍÀ', 'E': 'ĒÉĚÈ', 'I': 'ĪÍǏÌ',
    'O': 'ŌÓǑÒ', 'U': 'ŪÚǓÙ', 'Ü': 'ǕǗǙǛ'
}


def _convert_pinyin_callback(m):
    tone = int(m.group(3)) % 5
    r = m.group(1)
    # for multple vowels, use first one if it is a/e/o, otherwise use second one
    pos = 0
    if len(r) > 1 and not r[0] in 'aeoAEO':
        pos = 1
    if tone != 0:
        r = r[0:pos] + pinyinToneMarks[r[pos]][tone-1] + r[pos+1:]
    return r + m.group(2)


def decode_pinyin(s):
    s = s.replace('u:', 'ü').replace('U:', 'Ü').replace('v', 'ü').replace('V', 'Ü')
    return re.sub(r'([aeiouüÜ]{1,3})(n?g?r?)([012345])',
            _convert_pinyin_callback, s, flags=re.IGNORECASE).replace('r5', 'r')
