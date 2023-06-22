import pandas as pd
import sqlite3


connexion = sqlite3.connect("alesc.sqlite")
curseur = connexion.cursor()


def creation_bdd(connexion, curseur):
    # On recupere les donnees avec le module pandas

    datalogeurs = pd.read_excel("logeurs.xlsx")

    # POur chaque logeur, on associe a une variable ses donnees

    for i in range(len(datalogeurs)):
        compo = (datalogeurs.nom[i],datalogeurs.prenom[i],int(datalogeurs.numero_rue[i]),datalogeurs.nom_rue[i],int(datalogeurs.code_postal[i]),datalogeurs.ville[i])

        # On verifie si il existe deja une adresse identique dans la table adresse

        curseur.execute(
            f'SELECT * FROM logeur WHERE nom = ? AND prenom = ? AND numero_rue=? AND  nom_rue=? AND code_postal =? AND ville=?',
            (compo))

        # si il n'y en a pas, on l'insere dans la table logeur avec comme valeurs les donnees du fichier excel

        if curseur.fetchone() is None:
            curseur.execute(f'INSERT INTO logeur (nom, prenom, numero_rue, nom_rue, code_postal, ville) VALUES (?,?,?,?,?,?)',
                            (compo))

    # On insere ensuite tous les typs de logement possibles dans la table type de logement

    types_logement = ['f1', 'f2', 'f3', 'f4', 'f5', 'maison', 'studio', 'chambre']

    for type_logement in types_logement:
        curseur.execute(f'SELECT id_type_logement FROM type_logement WHERE type=?', (type_logement,))
        result = curseur.fetchone()

        if result is None:
            curseur.execute(f'INSERT INTO type_logement (Type) VALUES (?)', (type_logement,))
            connexion.commit()

    # On lit les donnees du fichier excel

    data = pd.read_excel("logements.xlsx")
    for i in range(len(data)):
            #création d'une variable qui stocke le type de logement
            nom_logement = (data.type_logement[i],)
            # On sélectionne la donnée du type_logement, ce à quoi sert la table type_logement.
            curseur.execute(f'SELECT type FROM type_logement WHERE (?) = type_logement.type', nom_logement)
            result = curseur.fetchone()
            # S'il y en a pas déjà, on sélectionne les autres données pour remplir la table
            if result is not None:
                id_type = result[0]
                # On sélectionne les données du logeur
                prenom_nom = (data.prenom_logeur[i], data.nom_logeur[i])
                curseur.execute('SELECT id_logeur FROM logeur WHERE prenom = ? AND nom = ?', prenom_nom)
                result = curseur.fetchone()
                # S'il n'est pas déjà présnet on remplit la table
                if result is not None:
                    id_logeur = result[0]

            # remplissage de la table"
            compo = (
            int(data.numero_rue[i]), data.nom_rue[i], int(data.code_postal[i]), data.ville[i], int(data.label[i]),
            id_type, id_logeur)
            curseur.execute(
                f'INSERT INTO logement (numero_rue,nom_rue,code_postal,ville,label,type,id_logeur) VALUES (?,?,?,?,?,?,?)',
                compo)
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
                f'SELECT id_logement FROM logement WHERE numero_rue=? AND nom_rue=? AND ville=? AND code_postal=?',
                (numero_rue, nom_rue, ville, code_postal))
            result = curseur.fetchall()
            if result:
                id_adr = int(result[0][0])
            else:
                id_adr = None  # Si aucun résultat n'est trouvé, définir id_adr à None puisqu'il n'y a aucune donnée trouvée.

            # Puis on les insere dans la table etudiant

            curseur.execute(f'INSERT INTO etudiant (nom,prenom,semestre,id_logement) VALUES (?,?,?,?)',
                            (nom, prenom, semestre, id_adr))
            connexion.commit()
def main():
    connexion = sqlite3.connect("alesc.sqlite")
    curseur = connexion.cursor()
    creation_bdd(connexion, curseur)
 

if __name__ == '__main__':
    main()

