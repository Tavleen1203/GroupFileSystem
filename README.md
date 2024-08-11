# Group File Sharing Tool 📂

This repository contains a Python-based file distribution tool designed for managing groups and distributing files within an organization. The system includes both server and client components, allowing for the efficient management of user groups and secure file transfers.

## **Features**

### **1. Group Management**
- **Group Creation**: The server automatically creates predefined groups (e.g., "Developers", "Designers") upon startup.
- **List Groups**: Clients can request a list of all available groups from the server.
- **Join Groups**: Clients can join specific groups, and the server manages and tracks group memberships.
- **Server Acknowledgment**: The server sends a confirmation response to the client after processing group-related requests.

### **2. File Transfer**
- **File Distribution**: The server can distribute files to all members of a specified group using reliable TCP connections.
- **Secure File Reception**: Clients receive and securely save files sent by the server.
- **Authorization**: Files are only sent to authorized group members.

### **3. Client-Server Communication**
- **Multicast Messaging (UDP)**: Used for client requests like listing groups and joining groups, enabling efficient communication across the network.
- **TCP/IP File Transfer**: Ensures reliable and secure file delivery from the server to the client.

### **4. Scalability and Flexibility**
- **Socket Reuse**: Both the server and client are designed to quickly reuse ports, avoiding port conflicts during repeated operations.
- **Modular Design**: The code is organized into modules (`server`, `client`, `shared`), making it easy to extend or modify features independently.

## **Technology Stack**

### **1. Python**
- The core of the application is built using Python, leveraging its powerful standard libraries for networking, threading, and file handling.

### **2. Socket Programming**
- **UDP (User Datagram Protocol)**: Utilized for multicast messaging, allowing the server to communicate efficiently with multiple clients.
- **TCP (Transmission Control Protocol)**: Used for reliable file transfers, ensuring that data is securely delivered to the intended recipients.

### **3. Threading**
- The server and client use Python's `threading` module to handle multiple operations concurrently, such as listening for messages and managing file transfers.

### **4. Network Programming**
- **Multicast Communication**: Enables the server to broadcast messages to all clients, such as group listings or join confirmations.
- **TCP Sockets**: Used for secure and reliable file transfer between the server and clients.

### **5. File I/O**
- **File Handling**: The server reads files from disk to send to clients, while the client writes received files to disk, ensuring data integrity.

### **6. Modular Design**
- The project is organized into distinct modules (`server`, `client`, `shared`), promoting easy maintenance and scalability.

Server Side Shell:
![image](https://github.com/user-attachments/assets/9c9069f5-d044-424a-bee2-534f4f4e421a)


Client Side:
![image](https://github.com/user-attachments/assets/4e3233c5-68b2-4cab-a9c2-ac5d51cfc693)


## **Installation and Setup**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/file-distribution-tool.git
   cd file-distribution-tool
   ```

2. **Install Dependencies:**
   Ensure Python is installed on your system. No additional dependencies are required for this project as it uses Python's standard library.

3. **Run the Server:**
   ```bash
   python -m server.file_server
   ```

4. **Run the Client:**
   In a separate terminal window:
   ```bash
   python -m client.file_client
   ```

## **Usage**

- **Group Management:** The client will automatically request a list of groups and join a specified group. The server handles these requests and updates group membership accordingly.
- **File Transfer:** Once the client joins a group, the server can be configured to send files to the client.

