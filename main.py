import os
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"

HTTP_PORT = 3000
SOCKET_PORT = 5000

def read_file(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, "rb") as file:
        return file.read()

class HttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # print("GET request:", self.path)
        if self.path == "/":
            content = read_file("index.html")

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(content)
        elif self.path == "/message.html":
            content = read_file("message.html")
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            self.wfile.write(content)
        elif self.path == "/logo.png":
            content = read_file("logo.png")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        else: 
            content = read_file("error.html")
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content)

def http_server():
    server = HTTPServer((HOST, HTTP_PORT), HttpServer)
    print(f"HTTP server started on http://{HOST}:{HTTP_PORT}")
    server.serve_forever()

if __name__ == "__main__":
    http_server()

# print(read_file("index.html"))