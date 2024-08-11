# client/file_client.py

import socket
import threading
from .utils import receive_file
from shared.constants import MULTICAST_GROUP, MULTICAST_PORT, FILE_TRANSFER_PORT

class FileClient:
    def __init__(self):
        self.multicast_thread = threading.Thread(target=self.listen_for_multicast)
        self.file_thread = threading.Thread(target=self.listen_for_file_transfer)

    def start_client(self):
        self.multicast_thread.start()
        self.file_thread.start()

    def listen_for_multicast(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', MULTICAST_PORT))
            mreq = socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            print(f"Listening for multicast messages on {MULTICAST_GROUP}:{MULTICAST_PORT}")
            while True:
                try:
                    data, _ = sock.recvfrom(1024)
                    print(f"Multicast message received: {data.decode()}")
                except TimeoutError:
                    print("No multicast message received within the timeout period.")

    def request_group_list(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = "LIST_GROUPS"
            sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))

    def join_group(self, group_name):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = f"JOIN_GROUP {group_name}"
            sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))

    def listen_for_file_transfer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('0.0.0.0', FILE_TRANSFER_PORT))
            sock.listen(5)
            print(f"Listening for file transfers on port {FILE_TRANSFER_PORT}")
            while True:
                conn, addr = sock.accept()
                threading.Thread(target=receive_file, args=(conn,)).start()

if __name__ == "__main__":
    client = FileClient()
    client.start_client()
    
    # Request to see all groups
    client.request_group_list()

    # Request to join a group (e.g., "Developers")
    client.join_group("Developers")
