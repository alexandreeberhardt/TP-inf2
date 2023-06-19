import sqlite3

def get_logements(connexion, curseur):
    nom1 = input("Entrez le nom du logeur: ")
    nom = nom1.lower()
    prenom1 = input("Entrez le prénom du logeur: ")
    prenom = prenom1.lower()

    # on recherche l'id_logeur en considerant qu'il n'y a pas d'homonymes
    curseur.execute('SELECT id_logeur FROM logeur WHERE nom = ? AND prenom = ?', (nom, prenom))
    result = curseur.fetchone()

    # Si on a un logeur, on peut continuer
    if result is not None:
        id_logeur = result[0]

        # on recherche les logements de ce logeur
        curseur.execute('SELECT id_logement, numero_rue, nom_rue, code_postal, ville, type FROM logement WHERE id_logeur = ?', (id_logeur,))
        logements = curseur.fetchall()

        # S'il existe des logements pour ce logeur, on affiche tout
        if logements:
            print(f"Nom du logeur : {prenom} {nom}")
            num_logement=1
            # on affiche les logements
            for logement in logements:
                print(f"Logement {num_logement} : \n{logement[1]} {logement[2]} {logement[3]} {logement[4]} {logement[5]}")
                num_logement+=1
                # on recherche les étudiants dans ce logement
                curseur.execute('SELECT nom, prenom FROM etudiant WHERE id_logement = ?', (logement[0],))
                etudiants = curseur.fetchall()

                # Si il y a des étudiants dans ce logement, alors on peut les afficher comme selon le modele
                if etudiants:
                    for etudiant in etudiants:
                        print(f"Nom de l'étudiant : {etudiant[0]} {etudiant[1]}")
                #sinon on affiche qu'il n'y en a pas
                else:
                    print("Il n'y a pas d'étudiants dans ce logement")

        else:
            print("Le logeur existe mais n'a pas de logements")
    else:
        print(f"le logeur nommé {prenom} {nom} n'est pas dans la table")
        #on peut imaginer une fonction qui demanderait a l'utilisateur si iel veut ajouter le logeur dans la base de donnée
        #il faudrait demander les informations et l'ajouter avec la methode du fichier "remplissage.py"
    curseur.close()

def main():
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()
    get_logements(connexion, curseur)

if __name__ == '__main__':
    main()
