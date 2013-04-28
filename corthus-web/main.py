from bottle import route, static_file, default_app, response
from itertools import izip_longest
import json
import os

# http://stackoverflow.com/questions/14431012/how-to-convert-sass-on-the-fly-to-css-in-python
# import subprocess
# process = subprocess.Popen("compass --watch ./css/main.sass:./css/main.css".split(), stdout=subprocess.PIPE)


os.chdir(os.path.dirname(__file__))


class use_json(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        response.content_type = 'application/json'
        return json.dumps(self.f(*args, **kwargs),
                          ensure_ascii=False,
                          sort_keys=True,
                          indent=2)


@route('/')
def hello():
    return open('index.html').read()


INDEX_BASE_LANG = 'el'


@route('/api/<name>/<chapter_num:re:[0-9]+>')
@use_json
def text(name, chapter_num):
    # reading text from Ponomar db
    def get_chapter(filename, chapter):
        with open(filename) as f:
            result = []
            on = False
            for line in f:
                # chapter titles start with hash - "#{chapter_num}"
                # line format: "{verse number}| {verse text}"
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

    all_langs = ['ar', 'cu', 'el', 'en', 'fr', 'la', 'zh-Hans', 'zh-Hant']

    rungs = []
    langs = []

    for lang in all_langs:
        try:
            chapter = get_chapter('texts_ponomar/%s/%s.text' % (lang, name), chapter_num)
        except IOError:
            continue
        langs.append(lang)
        for i, fragment in enumerate(chapter):
            if len(rungs) < i+1:
                rungs.append({})
            rungs[i][lang] = [fragment.strip()]

    return {'langs': langs,
            'rungs': rungs}


@route('/api/<name>/index')
@use_json
def book_index(name):
    with open('texts_ponomar/%s/%s.text' % (INDEX_BASE_LANG, name)) as f:
        return [line[1:].strip()
                for line in f if line.startswith('#')]


@route('/api/index')
def index():
    """Dynamic file listing (currently not used in favor of index.json)"""
    return [fn[:-5]
            for fn in os.listdir('texts_ponomar/%s' % INDEX_BASE_LANG)
            if fn.endswith('.text')]


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