from bottle import route, run, static_file, response

# http://stackoverflow.com/questions/14431012/how-to-convert-sass-on-the-fly-to-css-in-python
# import subprocess
# process = subprocess.Popen("compass --watch ./css/main.sass:./css/main.css".split(), stdout=subprocess.PIPE)

@route('/')
def hello():
    return open('index.html').read()

@route('/<filename:path>')
def send_static(filename):
    extension = filename.split('.')[-1]
    response.content_type = {
        'eot' : ''
    }
    return static_file(filename, root='./')

# @route('/js/<filename:re:.*\.js>')
# def send_static_js(filename):
#     return static_file(filename, root='js/')

run(host='localhost', port=8080, debug=True)
