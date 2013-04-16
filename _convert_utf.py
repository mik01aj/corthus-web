
from __future__ import unicode_literals
from corthus.toolkit.translit import hip2unicode

f=open('corthus-web/texts/kanon_izr.pt')
f2=open('corthus-web/texts/kanon_izr.pt2', 'w')

for line in f:
	line = line.decode('utf-8')
	if line.startswith('cu '):
		f2.write((line[:3] + hip2unicode(line[3:])).encode('utf-8'))
	else:
		f2.write(line.encode('utf-8'))

f.close()
f2.close()

