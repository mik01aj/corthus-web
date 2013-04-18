#!/usr/bin/python

"""
Usage:

./import_ponomar.py <Ponomar project root>
"""

import sys
import os
from shutil import copytree

RELATIONS = [
    ('Ponomar/languages/ar/bible/svd', 'texts_ponomar/ar'),
    ('Ponomar/languages/cu/bible/elis', 'texts_ponomar/cu'),
    ('Ponomar/languages/el/bible/spt', 'texts_ponomar/el'),
    ('Ponomar/languages/en/bible/kjv', 'texts_ponomar/en'),
    ('Ponomar/languages/fr/bible/ls', 'texts_ponomar/fr'),
    ('Ponomar/languages/la/bible/vulgate', 'texts_ponomar/la'),
    ('Ponomar/languages/zh/Hans/bible/cuv', 'texts_ponomar/zh-Hans'),
    ('Ponomar/languages/zh/Hant/bible/cuv', 'texts_ponomar/zh-Hant'),
]

if __name__ == '__main__':

    def get_path_pair(src, dest):
        return os.path.join(ponomar_root, src), dest

    try:
        [ponomar_root] = sys.argv[1:]
        for src, dest in RELATIONS:
            src, dest = get_path_pair(src, dest)
            assert os.path.isdir(src), "%s does not exist" % src
            assert os.path.isdir(os.path.dirname(dest)), "%s does not exist" % os.path.dirname(dest)
    except (ValueError, AssertionError) as e:
        print e
        print >> sys.stderr, __doc__
        sys.exit(1)

    for src, dest in RELATIONS:
        src, dest = get_path_pair(src, dest)
        print 'Copying %s to %s' % (src, dest)
        copytree(src, dest)
