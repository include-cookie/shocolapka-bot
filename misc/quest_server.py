import socket

HOST = '0.0.0.0'
PORT = 65432

DATA = b"Hello, World!\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        conn.sendall(DATA)
        conn.close()
