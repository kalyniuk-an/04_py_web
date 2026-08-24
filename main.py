import os
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from datetime import datetime

HOST = "127.0.0.1"

HTTP_PORT = 3000
SOCKET_PORT = 5000

def read_file(filename):
    # file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, "rb") as file:
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
    def do_POST(self):
        if self.path == "/message":
            content_length = int(self.headers.get("Content-Length", 0))

            body = self.rfile.read(content_length)
            body = body.decode("utf-8")
            form_data = parse_qs(body)

            username = form_data.get("username", [""])[0]
            message = form_data.get("message", [""])[0]

            print(username)
            print(message)

            data = { 
                "username": username,
                "message": message
            }

            send_to_socket_server(data)

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

def http_server():
    server = HTTPServer((HOST, HTTP_PORT), HttpServer)
    print(f"HTTP server started on http://{HOST}:{HTTP_PORT}")
    server.serve_forever()

def send_to_socket_server(data):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    message = json.dumps(data, ensure_ascii = False)

    client_socket.sendto(message.encode("utf-8"), (HOST, SOCKET_PORT))

    client_socket.close()

def save_message(data):
    storage_dir = "storage"
    data_file = os.path.join(storage_dir, "data.json")

    os.makedirs(storage_dir, exist_ok=True)

    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as file:
            message = json.load(file)
    else:
        message = {}

    timestamp = str(datetime.now())

    message[timestamp] = {
        "username": data["username"],
        "message": data["message"]
    }

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(message, file, ensure_ascii=False, indent=2)

def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST,SOCKET_PORT))

    print(f"Socket server started on {HOST}:{SOCKET_PORT}")

    while True:
        data, address = server_socket.recvfrom(4096)

        print("Receided:", data)

        message = json.loads(data.decode("utf-8"))

        save_message(message)

if __name__ == "__main__":
    http_thread = threading.Thread(target = http_server)
    socked_thread = threading.Thread(target = socket_server)

    http_thread.start()
    socked_thread.start()

    http_thread.join()
    socked_thread.join()

# print(read_file("index.html"))