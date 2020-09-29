import socket
import threading


clients=[]


def thread_func(conn,addr):
    while True:
        try:
            msg = conn.recv(1024)
            msg=str(msg, "utf-8")
            message=msg.split(":")[-1]
            print(message)
            if(message==" exit"):
                clients.remove(conn)
                break
            broadcast(msg) #send the message to every client so he can see it
        except:
            clients.remove(conn)

    conn.close()



class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.INADDR_ANY)  # socket erzeugen
        self.server_ip = socket.gethostbyname(socket.gethostname())
        print("Server-IP-Adresse: ",self.server_ip)
        self.port = 5050  # port angeben
        self.socket.bind((self.server_ip, self.port))  # server binden
        self.socket.listen() # warten...

        print("Server läuft...")

    def listen(self):
        while True:
            (conn, addr) = self.socket.accept()  # accept connection
            clients.append(conn) #append client to list


            print("ACTIVE CONNECTIONS: ", threading.active_count())


            thread = threading.Thread(target=thread_func, args=(conn, addr))  # thread erzeugen
            thread.start()  # thread starten




def broadcast(msg):
    for i in clients:
        i.send(bytes(msg,"utf-8"))


server=Server()
server.listen()


