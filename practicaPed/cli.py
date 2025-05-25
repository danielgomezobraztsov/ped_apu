import socket
import os
import sys

def run_client(server_path, command):
    client_path = f"/tmp/client_{os.getpid()}.sock"
    if os.path.exists(client_path):
        os.unlink(client_path)
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client_socket.bind(client_path)
    try:
        client_socket.sendto(command.encode(), server_path)
        response, _ = client_socket.recvfrom(128)
        print(response.decode())
    finally:
        client_socket.close()
        if os.path.exists(client_path):
            os.unlink(client_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cli.py SERVER_PATH COMMAND")
        sys.exit(1)
    run_client(sys.argv[1], sys.argv[2])
