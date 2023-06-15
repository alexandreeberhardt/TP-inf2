import pandas as pd
import sqlite3


connexion = sqlite3.connect("alesc.sqlite")
curseur = connexion.cursor()


def creation_bdd(connexion, curseur):
    # On recupere les donnees avec le module pandas

    datalogeurs = pd.read_excel("logeurs.xlsx")

    # POur chaque logeur, on associe a une variable ses donnees

    for i in range(len(datalogeurs)):
        nom = datalogeurs.nom[i]
        prenom = datalogeurs.prenom[i]
        numero_rue = int(datalogeurs.numero_rue[i])
        nom_rue = datalogeurs.nom_rue[i]
        code_postal = int(datalogeurs.code_postal[i])
        ville = datalogeurs.ville[i]

        # On verifie si il existe deja une adresse identique dans la table adresse

        curseur.execute(
            f'SELECT id_adresse FROM Adresses WHERE numero_rue=? AND  nom_rue=? AND code_postal =? AND ville=?',
            (numero_rue, nom_rue, code_postal, ville))

        # si il n'y en a pas, on l'insere dans la table Adresses avec comme valeurs les donnees du fichier excel

        if curseur.fetchone() is None:
            curseur.execute(f'INSERT INTO Adresses (numero_rue, nom_rue, code_postal, ville) VALUES (?,?,?,?)',
                            (numero_rue, nom_rue, code_postal, ville))

        # Et on recupere son id pour le mettre dans la table logeur

        curseur.execute(
            f'SELECT id_adresse FROM Adresses WHERE numero_rue=? AND  nom_rue=? AND code_postal =? AND ville=?',
            (numero_rue, nom_rue, code_postal, ville))
        id_adresse = curseur.fetchone()[0]

        # On verifie ensuite si il existe deja un logeur ayant meme prenom et nom

        curseur.execute(f'SELECT id_logeur FROM logeur WHERE nom=? AND prenom=?', (nom, prenom))

        # si il n'y en a pas, on l'insere dans la table logeur

        if curseur.fetchone() is None:
            curseur.execute(f'INSERT INTO logeur (nom,prenom, id_adresse) VALUES (?,?,?)', (nom, prenom, id_adresse))

    # On insere ensuite tous les typs de logement possibles dans la table type de logement

    for i in ['f1', 'f2', 'f3', 'f4', 'f5', 'maison', 'studio']:

        # On creer une verification pour ne pas creer de doublons lorsque re execute le programme pour rajouter des logeurs etc...

        curseur.execute(f'SELECT id_type_logement FROM type_logement WHERE type=?', (i,))
        if curseur.fetchone() is None:
            curseur.execute(f'INSERT INTO type_logement (Type) VALUES (?)', (i,))
            connexion.commit()

    # On lit les donnees du fichier excel

    datalogements = pd.read_excel("logements.xlsx")

    # pour chaque logement on associe des variable

    for i in range(len(datalogements)):
        numero_rue = int(datalogements.numero_rue[i])
        nom_rue = datalogements.nom_rue[i]
        code_postal = int(datalogements.code_postal[i])
        ville = datalogements.ville[i]

        # On verifie que l'adresse n'existe pas deja

        curseur.execute(
            f'SELECT id_adresse FROM Adresses WHERE numero_rue=? AND  nom_rue=? AND code_postal =? AND ville=?',
            (numero_rue, nom_rue, code_postal, ville))
        id_adr = curseur.fetchone()
        if id_adr is None:
            # Si elle n'existe pas on l'insere dans la table et on recupere son id

            curseur.execute(f'INSERT INTO Adresses (numero_rue, nom_rue, code_postal, ville) VALUES (?,?,?,?)',
                            (numero_rue, nom_rue, code_postal, ville))
            curseur.execute(
                f'SELECT id_adresse FROM Adresses WHERE numero_rue=? AND  nom_rue=? AND code_postal =? AND ville=?',
                (numero_rue, nom_rue, code_postal, ville))
            id_adr = curseur.fetchone()

        # On verifie si il existe deja un logement a la meme adresse

        curseur.execute(f'SELECT id_logement FROM Logement WHERE id_adresse=?', (id_adr[0],))

        # Si il n'y en a pas on recupere le reste des donnees du logement

        if curseur.fetchone() is None:
            label = int(datalogements.label[i])
            nom_logeur = datalogements.nom_logeur[i]
            prenom_logeur = datalogements.prenom_logeur[i]

            # On selectionne l'id du logeur de l'appartement pour le rentrer dans la table logement egalemet

            curseur.execute(f'SELECT id_logeur FROM logeur WHERE nom=? AND prenom=?',
                            (nom_logeur, prenom_logeur))
            id = curseur.fetchone()[0]
            type_logement1 = datalogements.type_logement[i]

            # Meme chose avec l'id du type de logement

            curseur.execute(f'SELECT id_type_logement FROM type_logement WHERE type=?', (type_logement1,))
            type = curseur.fetchall()[0][0]

            # Puis on insere toutes les donnees dans la table logement

            curseur.execute(
                f'INSERT INTO Logement (id_adresse,label,id_logeur,id_type_logement) VALUES (?,?,?,?)',
                (id_adr[0], label, id, type))
            connexion.commit()

    # Meme principe avec les etudiants

    dataetudiants = pd.read_excel("etudiants.xlsx")

    for i in range(len(dataetudiants)):
        semestre = dataetudiants.semestre[i]
        nom = dataetudiants.nom[i]
        prenom = dataetudiants.prenom[i]
        numero_rue = int(dataetudiants.numero_rue[i])
        nom_rue = dataetudiants.nom_rue[i]
        code_postal = int(dataetudiants.code_postal[i])
        ville = dataetudiants.ville[i]

        # On verifie qu'il n'existe aucun etudiant identique

        curseur.execute(f'SELECT id_etudiant FROM etudiant WHERE nom=? AND prenom=? AND semestre=?',
                        (nom, prenom, semestre))

        # Si il n'y en a pas on selectionne les id adresse, logement qui corresponde a son adresse

        if curseur.fetchone() is None:
            curseur.execute(
                f'SELECT id_adresse FROM Adresses WHERE numero_rue=? AND nom_rue=? AND ville=? AND code_postal=?',
                (numero_rue, nom_rue, ville, code_postal))
            id_adr = int(curseur.fetchall()[0][0])
            curseur.execute(f'SELECT id_logement FROM Logement WHERE id_adresse=?', (id_adr,))
            id = curseur.fetchall()[0][0]

            # Puis on les insere dans la table etudiants

            curseur.execute(f'INSERT INTO etudiant (nom,prenom,semestre,id_logement) VALUES (?,?,?,?)',
                            (nom, prenom, semestre, id))
            connexion.commit()
def main():
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()
    #delete_all(connexion, curseur)
    creation_bdd(connexion, curseur)
    #fenetre = Interface()
    #fenetre.mainloop()

if __name__ == '__main__':
    main()

