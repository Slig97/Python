import socket
import threading

SERVER_IP=socket.gethostbyname(socket.gethostname()) #IP from server

class Client:

    def __init__(self):
        self.server_ip = input("Type in the IP-Address of the Server: ")
        name=input("Type in your name: ")
        self.name=name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5050
        self.server_addr = (self.server_ip, self.port)
        self.socket.connect(self.server_addr)
        self.thread1=threading.Thread(target=self.write)
        self.thread2=threading.Thread(target=self.receive)
        self.thread1.start()
        self.thread2.start()
        print("Welcome to the Chatroom!")

    def write(self): #writing thread
        while True:
            self.chat = input("")
            self.chat=self.name+": "+self.chat
            self.socket.send(bytes(self.chat, "utf-8"))

    def receive(self): #waiting thread
        while True:
            self.msg = self.socket.recv(1024)
            self.msg = str(self.msg, "utf-8")
            print(self.msg)

client=Client()

