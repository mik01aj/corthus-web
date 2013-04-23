"""

A snippet for later.

import os

for fn in os.listdir('.'):
    s = open(fn).read()
    if s.startswith('\xef\xbb\xbf'):
        open(fn, 'w').write(s[3:])





for d, ds, fs in os.walk('corthus-web'):
    for f in fs:
        if f.endswith('.text'):
            s = open(d + '/' + f).read()
            assert s
            if s.startswith('\xef\xbb\xbf'):
                open(f, 'w').write(s[3:])



for d, ds, fs in os.walk('corthus-web'):
    for f in fs:
        if f.endswith('.text'):
            s = open(d + '/' + f).read()
            assert s
            if not s.startswith('#'):
                print d + '/' + f
                print s.splitlines()[0]





"""

print __doc__