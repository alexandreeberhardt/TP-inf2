import sqlite3
import pandas as pd

def main():
    try:
        # Connexion à la BDD (création si elle n'existe pas)
        connexion = sqlite3.connect("alesc.sqlite")
        curseur = connexion.cursor()

        requete_type_logement = '''CREATE TABLE IF NOT EXISTS type_logement
                                   (
                                       id_type_logement INTEGER PRIMARY KEY,
                                       type VARCHAR(100)
                                   );'''

        curseur.execute(requete_type_logement)

        # Script de création de la table logeur
        requete_logeur = '''CREATE TABLE IF NOT EXISTS logeur (
                                id_logeur INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                nom TEXT NULL,
                                prenom TEXT NULL,
                                numero_rue INTEGER NULL,
                                nom_rue TEXT NULL,
                                code_postal INTEGER NULL,
                                ville TEXT NULL
                               );'''

        curseur.execute(requete_logeur)  # Exécution de la requête

        # Script de création de la table logement
        requete_logement = '''CREATE TABLE IF NOT EXISTS logement (
                                id_logement INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                type INTEGER REFERENCES type_logement(type),
                                numero_rue TEXT NULL,
                                label INTEGER NULL,
                                nom_rue TEXT NULL,
                                code_postal TEXT NULL,
                                ville TEXT NULL,
                                id_logeur INTEGER NULL,
                                CONSTRAINT fk_logement_type_logement
                                    FOREIGN KEY (type) REFERENCES type_logement(type)
                                    ON DELETE NO ACTION
                                    ON UPDATE NO ACTION,
                                CONSTRAINT fk_logement_logeur
                                    FOREIGN KEY (id_logeur) REFERENCES logeur(id_logeur)
                                    ON DELETE NO ACTION
                                    ON UPDATE NO ACTION
                            );'''

        curseur.execute(requete_logement)  # Exécution de la requête

        # Script de création de la table etudiant
        requete_etudiant = '''CREATE TABLE IF NOT EXISTS etudiant (
                                id_etudiant INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                nom TEXT NULL,
                                prenom TEXT NULL,
                                semestre INTEGER NULL,
                                id_logement INTEGER NULL,
                                CONSTRAINT fk_etudiant_logement
                                    FOREIGN KEY (id_logement) REFERENCES logement(id_logement)
                                    ON DELETE NO ACTION
                                    ON UPDATE NO ACTION
                            );'''

        curseur.execute(requete_etudiant)  # Exécution de la requête

        connexion.commit()

    except FileNotFoundError:
        print("Fichier inexistant")
    finally:
        if connexion:
            curseur.close()
            connexion.close()

if __name__ == '__main__':
    main()
