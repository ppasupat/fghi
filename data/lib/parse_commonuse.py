#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re


LEVELS = {
    '==一级字表==': '1',
    '==二级字表==': '2',
    '==三级字表==': '3',
}


def get_commonuse():
    with open('raw/commonuse/commonuse.json') as fin:
        data = json.load(fin)
    content = data['query']['pages']['195151']['revisions'][0]['slots']['main']['*']
    commonuse = {}
    current_level = None
    for line in content.split('\n'):
        if line.startswith('=='):
            current_level = LEVELS.get(line)
            if current_level:
                commonuse[current_level] = []
        elif current_level and re.match(':\d+ .', line):
            char = line.split(maxsplit=1)[1]
            match = re.match(r'{{!\|(.)', char)
            if match:
                char = match.group(1)
            commonuse[current_level].append(char[0])
    return commonuse
