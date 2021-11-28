import re, random
from tkinter import *
from tkinter.messagebox import *

def str_add_spaces_between_chars(str: str):
	return " ".join(str)

def str_remove_spaces(str: str):
	return str.replace(' ', '')

class Pendu:
	def __init__(self, window) -> None:
		self.mots = ["pizza", "salade", "donner", "bonjour", "calme", "paisible", "pluie", "mer", "eau", "tomate", "oignon"]
		self.mot_secret = self.mots[random.randrange(0, len(self.mots))]
		self.essais_restants = 13
		self.points = 0
		self.modele_du_mot = str_add_spaces_between_chars("_" * len(self.mot_secret))
		self.lettres_proposees = []

		self.txtvar_label_motsecret = StringVar()
		self.txtvar_label_essais = StringVar()
		self.txtvar_textfield = StringVar()
		self.txtvar_label_motsecret.set(self.modele_du_mot)
		self.txtvar_label_essais.set(f"{self.essais_restants} essais avant la pendaison")
		self.txtvar_textfield.set('')
		self.label_motsecret = Label(window, textvariable = self.txtvar_label_motsecret, font = ("Helvetica", 32))
		self.label_essais = Label(window, textvariable = self.txtvar_label_essais, fg = 'red', font = ("Helvetica", 16))
		self.textfield = Entry(window, textvariable = self.txtvar_textfield)
		self.button = Button(window, text = "Essayer")
		self.button.bind('<Button-1>', self.submit_hander)
		
		self.label_essais.place(x = 25, y = 25)
		self.label_motsecret.place(x = 25, y = 100)
		self.textfield.place(x = 25, y = 150)
		self.button.place(x = 25, y = 200)

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

	def submit_hander(self, event):
		lettre = self.textfield.get()[0].lower()
		self.txtvar_textfield.set('')
		isAlreadyTried = self.is_already_tried(lettre)

		if lettre in self.mot_secret:
			if not isAlreadyTried:	
				self.points += self.mot_secret.count(lettre)

				for x in [m.start() for m in re.finditer(lettre, self.mot_secret)]:
					modele = str_remove_spaces(self.modele_du_mot)
					nouveau_modele = self.replacer(modele, lettre, x)
					self.modele_du_mot = str_add_spaces_between_chars(nouveau_modele)

				self.txtvar_label_motsecret.set(self.modele_du_mot)

				if self.points == len(self.mot_secret):
					showinfo(title = "GG", message = "GG")
					exit(0)

			else:
				showinfo(title = "Attention", message = "Cette lettre a déjà été proposée...")

		else:
			if not isAlreadyTried:
				self.essais_restants -= 1
				self.txtvar_label_essais.set(f"{self.essais_restants} essais avant la pendaison")
				showinfo(title = "Ooops", message = "Raté")


				if self.essais_restants == 0:
					showinfo(title = "Bien essayé", message = "Tu as perdu. Le mot était '" + self.mot_secret + "'.")
					exit(0)
			else:
				showinfo(title = "Attention", message = "Cette lettre a déjà été proposée...")

		if not lettre in self.lettres_proposees: self.lettres_proposees.append(lettre)


if __name__ == "__main__":
	window = Tk()
	pendu = Pendu(window)
	window.title('Pendu')
	window.geometry('400x300')
	window.mainloop()