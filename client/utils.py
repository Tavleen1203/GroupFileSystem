# client/utils.py

import os
from shared.constants import BUFFER_SIZE

def receive_file(connection):
    file_data = b''
    while True:
        data = connection.recv(BUFFER_SIZE)
        if not data:
            break
        file_data += data
    save_file(file_data)

def save_file(file_data):
    with open("received_file", "wb") as file:
        file.write(file_data)
    print("File received and saved as 'received_file'")
