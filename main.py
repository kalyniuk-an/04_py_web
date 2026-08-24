import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"

HTTP_PORT = 3000
SOCKET_PORT = 5000