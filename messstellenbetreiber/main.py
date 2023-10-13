import http.server as hserver
def run(server_port=8080, server_class=hserver.HTTPServer, handler_class=hserver.BaseHTTPRequestHandler):
    server_address = ('', server_port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run(8080)