import socket, threading, re, time

class ClientListener(threading.Thread):
    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server = server
        self.socket = socket
        self.address = address
        self.listening = True

    def run(self):
        while self.listening:
            self.server.echo(f"\n\nModèle du mot : {self.server.modele_du_mot}\n")
            self.server.echo(f"Lettres utilisées : {str(self.server.lettres_proposees)}\n")

            data = ""
            try:
                data: str = self.socket.recv(1024).decode('UTF-8')
                letter = data[0].lower()

                if letter == "":
                    raise Exception()
                if letter in self.server.mot_secret:
                    if not letter in self.server.lettres_proposees:	
                        self.server.points += self.server.mot_secret.count(letter)
                        self.server.echo("\n\nExact. Vous avez " + str(self.server.points) + " points.\n")

                        for x in [m.start() for m in re.finditer(letter, self.server.mot_secret)]:
                            modele = self.server.str_remove_spaces(self.server.modele_du_mot)
                            nouveau_modele = self.server.replacer(modele, letter, x)
                            self.server.modele_du_mot = self.server.str_add_spaces_between_chars(nouveau_modele)
                            self.server.echo(f"\n\nModèle du mot : {self.server.modele_du_mot}")

                        if self.server.points == len(self.server.mot_secret):
                            self.server.echo("\nGG !!!")
                            exit(0)
                    else:
                        self.server.echo("Cette lettre a déjà été proposée...")
                else:
                    self.server.essais_restants -= 1
                    if self.server.essais_restants == 0:
                        self.server.echo("Perdu. Le mot était '" + self.server.mot_secret + "'.")
                        exit(0)

                    self.server.echo(f"Faux. Il reste {str(self.server.essais_restants)} essais.")

                if not letter in self.server.lettres_proposees:
                    self.server.lettres_proposees.append(letter)

            except socket.error:
                print("Unable to receive data")
            except Exception:
                print()
            self.handle_msg(data)
            time.sleep(0.1)

    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)

    def handle_msg(self, data):
        print(self.address, "sent :", data)
        if data == "QUIT" or data == "":
            self.quit()
        else:
            self.server.echo(data)