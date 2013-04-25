from bottle import route, static_file, default_app, response
from itertools import izip_longest
import json
import os

# http://stackoverflow.com/questions/14431012/how-to-convert-sass-on-the-fly-to-css-in-python
# import subprocess
# process = subprocess.Popen("compass --watch ./css/main.sass:./css/main.css".split(), stdout=subprocess.PIPE)


os.chdir(os.path.dirname(__file__))


@route('/')
def hello():
    return open('index.html').read()


INDEX_BASE_LANG = 'el'


@route('/api/<name>/<chapter:re:[0-9]+>')
def text(name, chapter):
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
                    if '|' in line:
                        result.append(line.split('|')[1])  # a hackish way to get rid of numbers
                    else:
                        result.append(line)
            return result

    langs = ['ar', 'cu', 'el', 'en', 'fr', 'la', 'zh-Hans', 'zh-Hant']

    def gen_response():
        chapters = [get_chapter('texts_ponomar/%s/%s.text' % (lang, name), chapter)
                    for lang in langs]
        for fragments in izip_longest(*chapters):
            for lang, fragment in zip(langs, fragments):
                if fragment:  # we may receive nulls from izip_longest
                    yield lang + ' ' + fragment.strip()
            yield ''

    response.content_type = 'text/plain'
    return '\n'.join(gen_response())


@route('/api/<name>/index')
def book_index(name):
    with open('texts_ponomar/%s/%s.text' % (INDEX_BASE_LANG, name)) as f:
        return json.dumps([line[1:].strip()
                           for line in f if line.startswith('#')])


@route('/api/index')
def index():
    """Dynamic file listing (currently not used in favor of index.json)"""
    return json.dumps([fn[:-5]
                       for fn in os.listdir('texts_ponomar/%s' % INDEX_BASE_LANG)
                       if fn.endswith('.text')])


@route('/<filename:path>')
def send_static(filename):
    extension = filename.split('.')[-1]
    mimetype = {
        'eot': 'font/opentype',
        'ttf': 'font/ttf',
        'pt': 'text/plain',
    }.get(extension, 'auto')
    return static_file(filename, root='./', mimetype=mimetype)


application = default_app()
#run(host='localhost', port=8080, debug=True)
