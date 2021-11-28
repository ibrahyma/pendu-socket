import threading, socket, time

class Client():
    def __init__(self, server, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.listening = True

    def recv_data_handler(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
       
    def listen(self):
        self.listen_thread = threading.Thread(target = self.recv_data_handler)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):
        try:
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("unable to send message")
   
    def quit(self):
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        if data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()
        else:
            print(data)

if __name__ == "__main__":
    try:
        client = Client('127.0.0.1', 4321)
        client.listen()
        message = ""

        while (message != "QUIT"):
            message = input()
            if (message != ""):
                client.send(message)
    except KeyboardInterrupt:
        quit(0)