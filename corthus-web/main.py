from bottle import route, run, static_file

# import subprocess
# process = subprocess.Popen("compass --watch ./css/main.sass:./css/main.css".split(), stdout=subprocess.PIPE)

@route('/')
def hello():
    return open('index.html').read()

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

@route('/js/<filename:re:.*\.js>')
def send_static_js(filename):
    return static_file(filename, root='js/')

run(host='localhost', port=8080, debug=True)
