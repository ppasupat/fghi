#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re


LEVELS = {
    '==一级字表==': '1',
    '==二级字表==': '2',
    '==三级字表==': '3',
}


def get_standard():
    with open('raw/standard/standard.json') as fin:
        data = json.load(fin)
    content = data['query']['pages']['195151']['revisions'][0]['slots']['main']['*']
    standard = {}
    current_level = None
    for line in content.split('\n'):
        if line.startswith('=='):
            current_level = LEVELS.get(line)
            if current_level:
                standard[current_level] = []
        elif current_level and re.match(':\d+ .', line):
            char = line.split(maxsplit=1)[1]
            match = re.match(r'{{!\|(.)', char)
            if match:
                char = match.group(1)
            standard[current_level].append(char[0])
    return standard
