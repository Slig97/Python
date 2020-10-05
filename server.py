import socket
import threading


class Server:

    def __init__(self):
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)
        self.port = 8080
        self.udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = 0
        self.clients = []
        self.tcpsocket.bind((self.ip_address, self.port))
        self.tcpsocket.listen()
        thread1 = threading.Thread(target=self.send_ip_port_to_new_client)
        thread1.start()

    def send_ip_port_to_new_client(self):  # sending the ip and port via udp to new client
        self.udpsocket.bind((self.ip_address, self.port))
        print("Server running...")
        while True:
            data, self.clientaddr = self.udpsocket.recvfrom(1024)
            data = self.ip_address + ":" + str(self.port)
            self.udpsocket.sendto(bytes(data, "utf-8"), self.clientaddr)

    def broadcast(self, msg):  # sending message to all clients connected
        for i in self.clients:
            i.send(msg)

    def receiving_messages(self, clientsock, clientaddr, username):  # thread for receiving messages from all clients
        while True:
            try:
                msg = clientsock.recv(1024)
                self.broadcast(msg)

            except:
                self.connections -= 1
                self.clients.remove(clientsock)
                print("client left: ", username)
                value = username + " left the chat"
                self.broadcast(bytes(value, "utf-8"))
                print("Connections: ", self.connections)
                return

    def run_tcpserver(self):
        while True:
            (clientsock, clientaddr) = self.tcpsocket.accept()  # accept connection
            self.clients.append(clientsock)
            self.connections += 1
            print("Connections: ", self.connections)
            username = clientsock.recv(1024)  # receive username and store it
            username = username.decode()
            value = username + " has entered the chat"
            self.broadcast(bytes(value, "utf-8"))
            thread = threading.Thread(target=self.receiving_messages, args=(clientsock, clientaddr,
                                                                            username))  # starting thread to the server can receive messages and send his ip at the same time
            thread.start()


server = Server()
server.run_tcpserver()


