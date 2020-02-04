import socket
from threading import Thread


def receiving(conn):
    while True:
        msg = str(conn.recv(2048), encoding="utf-8")
        if msg == "/exit":
            print("\nServer closed the connetion\n")
            break
        print("\nServer: " + msg + "\n")


def sending(conn):
    while True:
        msg = input()
        if msg == "/exit":
            print("Closing connection...")
            conn.send(bytes(msg, encoding="utf-8"))
            break
        conn.send(bytes(msg, encoding="utf-8"))


sock = socket.socket()
sock.connect((input("Server's IP: "), 6668))
recv = Thread(target=receiving, args=(sock,))
send = Thread(target=sending, args=(sock,))
recv.start()
send.start()
recv.join()
send.join()
sock.close()

