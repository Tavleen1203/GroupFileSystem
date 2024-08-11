# server/file_server.py

import socket
import threading
from .group_manager import GroupManager
from .utils import handle_client, send_multicast
from shared.constants import MULTICAST_PORT, MULTICAST_GROUP, FILE_TRANSFER_PORT

class FileServer:
    def __init__(self):
        self.group_manager = GroupManager()
        self.group_manager.create_group("Developers")
        self.group_manager.create_group("Designers")

    def start_server(self):
        print("Starting server...")
        multicast_thread = threading.Thread(target=self.listen_for_multicast)
        multicast_thread.start()
        self.start_file_transfer_server()

    def listen_for_multicast(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', MULTICAST_PORT))
            mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            while True:
                data, address = sock.recvfrom(1024)
                print(f"Received multicast request from {address}: {data.decode()}")
                handle_client(data.decode(), address, self.group_manager)

    def start_file_transfer_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', FILE_TRANSFER_PORT))
            server_socket.listen(5)
            print(f"File transfer server listening on port {FILE_TRANSFER_PORT}...")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Accepted connection from {addr}")

                client_thread = threading.Thread(target=self.handle_file_transfer, args=(client_socket,))
                client_thread.start()

    def handle_file_transfer(self, client_socket):
        try:
            requested_file = client_socket.recv(1024).decode()
            print(f"Client requested file: {requested_file}")

            with open(requested_file, 'rb') as file:
                file_data = file.read()
                client_socket.sendall(file_data)

            print("File transfer complete.")
        except Exception as e:
            print(f"Error during file transfer: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = FileServer()
    server.start_server()
