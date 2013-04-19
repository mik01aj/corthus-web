"""

A snippet for later.

import os

for fn in os.listdir('.'):
    s = open(fn).read()
    if s.startswith('\xef\xbb\xbf'):
        open(fn, 'w').write(s[3:])

"""

print __doc__