# server/utils.py

import socket
from shared.constants import MULTICAST_GROUP, MULTICAST_PORT

def send_multicast(message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
    print(f"Multicast message sent to group {MULTICAST_GROUP}")

def handle_client(request, client_address, group_manager):
    request_parts = request.split()
    command = request_parts[0]

    if command == "LIST_GROUPS":
        groups = group_manager.list_groups()
        response = f"Available groups: {', '.join(groups)}"
        send_response(response, client_address)

    elif command == "JOIN_GROUP":
        group_name = request_parts[1]
        group_manager.add_user_to_group(group_name, client_address)
        response = f"Successfully joined group {group_name}."
        send_response(response, client_address)

    elif command == "SEND_FILE":
        # This would be used by an admin or an automated process to send files
        group_name = request_parts[1]
        file_path = request_parts[2]
        send_file_to_group(file_path, group_name, group_manager)

def send_response(response, client_address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(response.encode(), client_address)

def send_file_to_group(file_path, group_name, group_manager):
    group_members = group_manager.get_group_members(group_name)
    if not group_members:
        print(f"No members in group '{group_name}' to send the file.")
        return

    with open(file_path, "rb") as file:
        file_data = file.read()

    for member in group_members:
        send_file_via_tcp(file_data, member)

def send_file_via_tcp(file_data, recipient_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((recipient_address[0], FILE_TRANSFER_PORT))
        sock.sendall(file_data)
        print(f"File sent to {recipient_address[0]}:{recipient_address[1]}")
