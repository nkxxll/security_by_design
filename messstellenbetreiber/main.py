from bottle import route, run, template

PORT = 8080

@route('/hello/<name>')
def random_function_name(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=PORT)