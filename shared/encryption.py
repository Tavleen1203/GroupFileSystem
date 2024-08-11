from cryptography.fernet import Fernet

# Utility functions for encryption and decryption
def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data)
