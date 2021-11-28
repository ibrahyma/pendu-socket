import re, random

mots = ["pizza", "salade", "donner", "bonjour", "calme", "paisible", "pluie", "mer", "eau", "tomate", "oignon"]
mot_secret = mots[random.randrange(0, len(mots))]
essais_restants = 20
points = 0
modele_du_mot = ("_" * len(mot_secret))
lettres_proposees = []


def replacer(s, newstring, index, nofail=False):
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    if index < 0:
        return newstring + s
    if index > len(s):
        return s + newstring

    return s[:index] + newstring + s[index + 1:]

while True:
	print("\n\nModèle du mot : " + modele_du_mot)
	print("Lettres utilisées : " + str(lettres_proposees))	

	lettre = input("Proposez une lettre: ")
	if len(lettre) > 1:
		if lettre == mot_secret:
			print("Tu as gagné, le mot était '" + mot_secret + "'.")
			break
		else:
			print("Erreur: le mot ne correspond pas.")
			continue

	if lettre in mot_secret:
		if not lettre in lettres_proposees:	
			points = points + mot_secret.count(lettre)
			print("Exact. Vous avez " + str(points) + " points.")

			for x in [m.start() for m in re.finditer(lettre, mot_secret)]:
				modele_du_mot = replacer(modele_du_mot, lettre, x)

			if points == len(mot_secret):
				print("Tu as gagné")
				break
		else:
			print("Cette lettre a déjà été proposée...")

	else:
		essais_restants = essais_restants - 1
		if essais_restants == 0:
			print ("Tu as perdu. Le mot était '" + mot_secret + "'.")
			break
		print("Faux. Il vous reste " + str(essais_restants) + " essais.")

	if not lettre in lettres_proposees: lettres_proposees.append(lettre)



