import http.server
import socketserver
import os

PORT = 8000
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/cgi-bin"]

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"CGI Server running at http://localhost:{PORT}")
    httpd.serve_forever()
