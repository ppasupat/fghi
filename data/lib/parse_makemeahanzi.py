#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


def get_svg_paths(char):
    filename = 'raw/makemeahanzi/svgs-still/{}-still.svg'.format(ord(char))
    tree = ET.parse(filename)
    root = tree.getroot()
    paths = []
    for x in root[1]:
        if x.tag.endswith('}path'):
            paths.append(x.attrib['d'])
    return paths
