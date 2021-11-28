import socket, signal, sys, time, random

from clientListener import ClientListener

class Server():
    def __init__(self, port):
        self.mots = ["hello"]
        # self.mots = ["pizza", "salade", "donner", "bonjour", "calme", "paisible", "pluie", "mer", "eau", "tomate", "oignon"]
        self.mot_secret = self.mots[random.randrange(0, len(self.mots))]
        self.essais_restants = 13
        self.points = 0
        self.modele_du_mot = self.str_add_spaces_between_chars("_" * len(self.mot_secret))
        self.lettres_proposees = []

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        self.clients_sockets = []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.listener.close()
        self.echo("QUIT")

    def str_add_spaces_between_chars(self, str: str):
        return " ".join(str)

    def str_remove_spaces(self, str: str):
        return str.replace(' ', '')

    def run(self):
        while True:
            print("En attente de joueurs...")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread = ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)

    def replacer(self, s, newstring, index, nofail=False):
        if not nofail and index not in range(len(s)):
            raise ValueError("index outside given string")
        if index < 0:
            return newstring + s
        if index > len(s):
            return s + newstring

        return s[:index] + newstring + s[index + 1:]

    def is_already_tried(self, lettre: str) -> bool:
        return lettre in self.lettres_proposees

    def remove_socket(self, socket):
        self.client_sockets.remove(socket)

    def echo(self, data):
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")

if __name__ == "__main__":
    try:
        server = Server(4321)
        server.run()
    except KeyboardInterrupt:
        quit(0)