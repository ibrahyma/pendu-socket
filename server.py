import socket, signal, sys, random, json

from clientListener import ClientListener

class Server():
    def __init__(self, port):
        self.mots = ["pizza", "salade", "donner", "bonjour", "calme", "paisible", "pluie", "mer", "eau",
         "tomate", "oignon", "dune", "dictionnaire", "malinois", "chien", "chat", "pension", "amour", "programmation",
         "legume", "rap", "cookie", "class", "informatique", "acrimonie", "achaler", "acrostiche", "ambages", "aplacophore",
         "babiller", "bome", "bamboche", "bonzesse",, "callipyge", "calter", "capitation", "dessiccateur","distal", "doxa", "ductile",
         "epacte", "entropie", "epithalame", "ensiforme", "eburne", "equanamite", "febricule", "flagorner", "fustet", "faix", "glose",
         "glairer", "gambit", "gabarre", "gone", "grigne", "covid", "dragon", "ball", "griffe", "haret", "hyphe", "holisme", "hypocondarique",
         "hypotypose", "hellenisation", "incube", "infundubuliforme", "impavide", "intertidal", "jactance", "janotisme",
         "jobastre", "jaculatoire", "kaolin", "kaon", "kenophobie", "kraken", "lacunaire", "lallation", "lege", "lacustre",
         "lavure", "liponombre", "lipopremier", "macache", "makimono", "meson", "mas", "maltose", "mandala", "mediocratie", "miston",
         "misogyne", "misandre", "mistoufle", "merzlota", "mentisme", "mirliflore", "matefaim", "metonymie", "mezigue", "mutant",
         "modenature", "moderateur", "muance", "nadir", "notule", "nasarde", "nife", "nervation", "nanan", "nib", "nervi", "nubile",
         "objectivation", "objuration", "obvie", "onagre", "oekoumene", "onychophagie", "orant", "ovalie", "opprobre",
         "pasquin", "peguer", "perissologie", "phenakistiscope", "peronnelle", "paratexte", "planification", "perle", "parangon",
         "petuner", "petiole", "pica","piauler", "pioupiou", "succube", "sphinge", "satyiasis", "tuple", "tautologie", "tétraktys",
         "triskaidekaphobie", "valetudinaire", "zebre", "paix", "peace", "love", "hate", "pendu", "navigateur", "pikachu"]
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

    def str_add_spaces_between_chars(self, str: str):
        return " ".join(str)

    def str_remove_spaces(self, str: str):
        return str.replace(' ', '')

    def run(self):
        while True:
            try:
                print("En attente de joueurs...")
                try:
                    (client_socket, client_adress) = self.listener.accept()
                except socket.error:
                    sys.exit('Connexion aux joueurs impossible')
                self.clients_sockets.append(client_socket)
                print("Start the thread for client:", client_adress)
                client_thread = ClientListener(self, client_socket, client_adress)
                client_thread.start()
            except KeyboardInterrupt:
                quit(0)

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

    def echo(self, data: dict):
        dataToSend = json.dumps(data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(dataToSend.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")

if __name__ == "__main__":
    server = Server(1234)
    server.run()
