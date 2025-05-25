import socket
import os
import sys
from datetime import datetime


def run_server(socket_path):
    if os.path.exists(socket_path):
        os.unlink(socket_path)
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_socket.bind(socket_path)
    try:
        while True:
            message, client_address = server_socket.recvfrom(128)
            if message == b"TIME":
                response = datetime.now().strftime("%H:%M:%S").encode()
            elif message == b"DATE":
                response = datetime.now().strftime("%Y-%m-%d").encode()
            else:
                response = b"ERROR"
            server_socket.sendto(response, client_address)
    finally:
        server_socket.close()
        if os.path.exists(socket_path):
            os.unlink(socket_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python serv.py SOCKET_PATH")
        sys.exit(1)
    run_server(sys.argv[1])
