#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

NUMBERS = {
    '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7',
}


def _parse_hsk30(filename, section_header):
    results = {}
    current_level = None
    with open('raw/hsk30/' + filename) as fin:
        for line in fin:
            line = line.strip()
            if not line:
                current_level = None
            elif re.match(section_header, line):
                current_level = NUMBERS[line[0]]
                results[current_level] = []
            elif current_level and re.match('\d+\s+.*', line):
                results[current_level].append(line.split(maxsplit=1)[1])
    return results


def get_hsk_chars():
    return _parse_hsk30('charlist.txt', '.*级汉字表')


def get_hsk_words():
    return _parse_hsk30('wordlist.txt', '.*级词汇表')
