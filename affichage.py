import sqlite3
def get_logements(connexion, curseur):
    nom = input("Entrez le nom du logeur: ")
    prenom = input("Entrez le prénom du logeur: ")

    # on recherche l'id_logeur en considerant qu'il n'y a pas d'homonymes, a
    curseur.execute('SELECT id_logeur FROM logeur WHERE nom = ? AND prenom = ?', (nom, prenom))
    result = curseur.fetchone()

    # Si on a un logeur, on peut continuer
    if result is not None:
        id_logeur = result[0]

        # Recherchons les logements de ce logeur
        curseur.execute('SELECT numero_rue, nom_rue, code_postal, ville, type FROM logement WHERE id_logeur = ?', (id_logeur,))
        logements = curseur.fetchall()

        # S'il existe des logements pour ce logeur, on affiche tout
        if logements:
            print(f"Nom du logeur : {prenom} {nom}")
            # Affichons les logements
            for i, logement in enumerate(logements, start=1):
                print(f"Logement {i} : {logement[0]} {logement[1]} {logement[2]} {logement[3]} *** {logement[4]}")

        else:
            print("Le logeur existe et n'a pas de logements")
    else:
        print(f"le logeur nommé {prenom} {nom} n'est pas dans la table")
        #on peut imaginer une fonction qui demanderai a l'utilisateur si iel veut ajouter le logeur dans la base de donnée
        #il faudrait demander les informations et l'ajouter avec la methode du fichier "remplissage.py"
    curseur.close()
def main():
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()
    get_logements(connexion, curseur)
if __name__ == '__main__':
    main()
