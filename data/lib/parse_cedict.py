#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from collections import defaultdict

from lib import pinyin_utils


def _clean_gloss(gloss):
    gloss = gloss.replace('/', '; ')
    gloss = re.sub(r'\[([A-Za-z0-9: ]+)\]',
            lambda m: '[{}]'.format(pinyin_utils.decode_pinyin(m.group(1))),
            gloss)
    gloss = re.sub(r'([|\u4e00-\u9fff]+)\[([^\]]+)\]',
            lambda m: '{}[{}]'.format(
                m.group(1).split('|')[-1], m.group(2)),
            gloss)
    return gloss


def _verify_gloss(word, gloss):
    if (gloss.startswith('variant of ' + word) and
            re.match('variant of ' + word + '\[[^\]]+\]$', gloss)):
        return False
    if (gloss.startswith('old variant of ' + word) and
            re.match('old variant of ' + word + '\[[^\]]+\]$', gloss)):
        return False
    return True


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
            gloss = _clean_gloss(gloss)
            if _verify_gloss(word, gloss):
                cedict[word].append([pron, gloss])
    return dict(cedict)


def lookup_cedict(cedict, word, verbose=False):
    """Returns a list of (pron, gloss)."""
    if word[-1] == '儿':
        if word not in cedict or (
                len(cedict[word]) == 1 and cedict[word][0][1].startswith('erhua variant')):
            if verbose:
                print('Try looking up {} --> {}'.format(word, word[:-1]))
            result = lookup_cedict(cedict, word[:-1], verbose=verbose)
            if result != [['???', '???']]:
                result = [(pron + ' r', gloss) for (pron, gloss) in result]
            return result
    if word not in cedict:
        if verbose:
            print('WARNING: "{}" not in CEDICT'.format(word))
        return [['???', '???']]
    return cedict[word]
