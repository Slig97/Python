import socket
import threading

class Client:
    def __init__(self):
        self.udpsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcpsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_ip_port(self):
        self.udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udpsocket.sendto(b"DISCOVER", ("<broadcast>", 8080))
        recv=self.udpsocket.recv(1024)
        recv=recv.decode("utf-8")
        self.server_ip_address=recv.split(":")[0]
        self.server_port=int(recv.split(":")[1])
        self.udpsocket.close()

    def connect_to_server(self):
        try:
            self.tcpsocket.connect((self.server_ip_address,self.server_port))
        except RuntimeError as e:
            print(e)
            exit(-1)
    def chat(self):
        self.name=input("Type in your username: ")
        self.tcpsocket.send(bytes(self.name, "utf-8"))
        thread=threading.Thread(target=self.send)
        thread.start()
        thread1=threading.Thread(target=self.receive)
        thread1.start()
        thread.join()
        thread1.join()


    def send(self):
        while True:
            value=input("")
            value=self.name+": "+value
            try:
                self.tcpsocket.send(bytes(value,"utf-8"))
            except:
                print("Server no longer reachable")
                self.tcpsocket.close()
                return

    def receive(self):
        while True:
            try:
                data=self.tcpsocket.recv(1024)
                print(data.decode())
            except:
                print("Server no longer reachable")
                self.tcpsocket.close()
                return



client=Client()
client.receive_ip_port()
client.connect_to_server()
client.chat()
