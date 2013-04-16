from bottle import route, run, static_file
from itertools import izip_longest

# http://stackoverflow.com/questions/14431012/how-to-convert-sass-on-the-fly-to-css-in-python
# import subprocess
# process = subprocess.Popen("compass --watch ./css/main.sass:./css/main.css".split(), stdout=subprocess.PIPE)

@route('/')
def hello():
    return open('index.html').read()

@route('/gen/<name>/<chapter>')
def gen_text(name, chapter):

    def get_chapter(filename, chapter):
        with open(filename) as f:
            result = []
            on = False
            for line in f:
                if not on and line.startswith('#') and line[1:].strip() == chapter:
                    on = True
                elif on:
                    if line.startswith('#'):
                        break
                    result.append(line.split('|')[1])  # a hackish way to get rid of numbers
            return result

    langs = ['el', 'cu', 'en', 'fr', 'la']

    def gen_response():
        chapters = [get_chapter('texts_ponomar/%s/%s.text' % (lang, name), chapter)
                    for lang in langs]
        for fragments in izip_longest(*chapters):
            for lang, fragment in zip(langs, fragments):
                if fragment:  # we may receive nulls from izip_longest
                    yield lang + ' ' + fragment.strip()
            yield ''

    return '\n'.join(gen_response())

@route('/<filename:path>')
def send_static(filename):
    extension = filename.split('.')[-1]
    mimetype = {
        'eot': 'font/opentype',
        'ttf': 'font/ttf',
        'pt': 'text/plain',
    }.get(extension, 'auto')
    return static_file(filename, root='./', mimetype=mimetype)

# @route('/js/<filename:re:.*\.js>')
# def send_static_js(filename):
#     return static_file(filename, root='js/')

run(host='localhost', port=8080, debug=True)
