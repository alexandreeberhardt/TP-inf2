'''Choix d'implémentation
En ce qui est de l'interface graphique, nous avons opté pour des couleurs pastelles (simple choix personnel n'aimant pas les couleurs de "base")
Ensuite, nous avons implémenté les boutons demandés par l'énoncé puis nous avons décidé d'ajouter 2 nouvelles
fonctionnalités : les parenthèses de calcul ainsi qu'un bouton "supprimer le dernier élément". Les boutons sont placés pour permettre une plus grande ergonomie et compréhension
Nous avons aussi ajouté des parenthèses car cela permet d'éviter les erreurs de
calcul mais aussi d'utiliser des outils plus complexes comme le calcul d'une racine par exemple
De plus lors de l'activation d'un bouton de calcul nous avons fait le choix d'ajouter directement une parenthèse ouvrante. Si on appuie sur cos on aura "cos(" pour éviter tout soucis d'ambigüité et l'utilisateur saura qu'il faut qu'il rajoute une parenthèse fermante en fin d'expression sinon il aura une erreur.
En ce qui est du bouton supprimer le dernier élément, ce bouton est intéressant pour rendre ergonomique la calculatrice si jamais l'utilisateur se trompe dans le calcul qu'il souhaite effectuer.

Nous avons aussi choisi d'utiliser la fonction eval de python pour faire les calculs car elle prend en compte les priorités de calcul.

L'historique effectue un cycle pour éviter de se bloquer, ceci est un choix personnel pour revenir plus simplement sur tous les calculs effectués mais il est tout a fait possible de l'implémenter de sorte à ce qu'il s'arrête au premier calcul (dans l'ordre chrnologique).
'''

from tkinter import Button, Entry, Label, Tk, END, Frame #On importe le module tkinter avec chaque fonctionnalité utilisée pour éviter de faire un import* (éviter les confusions)
from math import sin, tan, cos, sqrt, pi # Pareil que le tkinter


class Fenetre(Tk):
    '''La classe fenêtre contient le nom de la calculatrice l'écran les boutons et tout les méthodes pour son
    fonctionnement'''
    historique = []
    nb = 0

    def __init__(self): #Constructeur qui répertorie toutes les méthodes
        Tk.__init__(self)
        '''self.ecran = None
        self.label = None'''
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        l = 340
        h = 280
        pos_x = ecran_x // 2 - l // 2
        pos_y = ecran_y // 2 - h // 2
        geometrie = f"{l}x{h}+{pos_x}+{pos_y}"
        self.geometry(geometrie)
        self.title("TP Calculatrice")
        self.config(bg='black')
        self.eval('tk::PlaceWindow . center')
        self.str_operation = ""  # str qui permet de stocker les opérations
        '''self.operation = StringVar()
        self.operation.set('')'''
        self.create_ecran()
        self.create_label()
        self.build()

    def build(self): # Construction de la calculatrice
        parametre_bouton_nombre = {'bd': '4', 'bg': '#778da9', 'fg': 'white'} # Dictionnaire de paramètres pour enregistrer les caractèristiques de chaque bouton pour économiser les lignes de code
        parametre_bouton_calcul = {'bd': '2', 'bg': '#9f86c0', 'fg': 'black'}
        parametre_bouton_clear = {'bd': '2', 'bg': '#4cc9f0', 'fg': 'black'}
        parametre_bouton_egal = {'bd': '2', 'bg': '#fbf8cc', 'fg': 'black'}

        frame = Frame(self)
        frame.grid()
        # boutons chiffre
        Button(frame, parametre_bouton_nombre, text='1', command=lambda: self.ajouter('1')).grid(row=3, column=0,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='2', command=lambda: self.ajouter('2')).grid(row=3, column=1,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='3', command=lambda: self.ajouter('3')).grid(row=3, column=2,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='4', command=lambda: self.ajouter('4')).grid(row=4, column=0,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='5', command=lambda: self.ajouter('5')).grid(row=4, column=1,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='6', command=lambda: self.ajouter('6')).grid(row=4, column=2,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='7', command=lambda: self.ajouter('7')).grid(row=5, column=0,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='8', command=lambda: self.ajouter('8')).grid(row=5, column=1,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='9', command=lambda: self.ajouter('9')).grid(row=5, column=2,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='0', command=lambda: self.ajouter('0')).grid(row=6, column=1,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='.', command=lambda: self.ajouter('.')).grid(row=6, column=2,
                                                                                                 padx=5, pady=10)

        # Boutons de calcul
        Button(frame, parametre_bouton_calcul, text='+', command=lambda: self.ajouter('+')).grid(row=2, column=4,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='-', command=lambda: self.ajouter('-')).grid(row=3, column=4,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='*', command=lambda: self.ajouter('*')).grid(row=4, column=4,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='/', command=lambda: self.ajouter('/')).grid(row=5, column=4,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='sin', command=lambda: self.ajouter('sin(')).grid(row=2, column=5,
                                                                                                     padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='tan', command=lambda: self.ajouter('tan(')).grid(row=3, column=5,
                                                                                                      padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='cos', command=lambda: self.ajouter('cos(')).grid(row=4, column=5,
                                                                                                      padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='x^2', command=lambda: self.ajouter('²')).grid(row=5, column=5,
                                                                                                   padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='√x', command=lambda: self.ajouter('√(')).grid(row=6, column=5,
                                                                                                   padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text='π', command=lambda: self.ajouter(str(round(pi, 6)))).grid(row=6,
                                                                                                               column=4,
                                                                                                               padx=5,
                                                                                                               pady=10)

        # Bouton clear et egal
        Button(frame, parametre_bouton_clear, text='C', command=lambda: self.clear()).grid(row=2, column=0, padx=5,
                                                                                           pady=10)
        Button(frame, parametre_bouton_egal, text='=', command=lambda: self.calculer()).grid(row=6, column=0, padx=5,
                                                                                             pady=10)

        # Parenthèses
        Button(frame, parametre_bouton_calcul, text='(', command=lambda: self.ajouter('(')).grid(row=2, column=1,
                                                                                                 padx=5, pady=10)
        Button(frame, parametre_bouton_calcul, text=')', command=lambda: self.ajouter(')')).grid(row=2, column=2,
                                                                                                 padx=5, pady=10)

        # Fleches
        Button(frame, parametre_bouton_egal, text='←', command=lambda: self.supp()).grid(row=3, column=6, padx=5,
                                                                                         pady=10)
        Button(frame, parametre_bouton_egal, text='↑', command=lambda: self.fleche('↑')).grid(row=4, column=6, padx=5,
                                                                                              pady=10)
        Button(frame, parametre_bouton_egal, text='↓', command=lambda: self.fleche('↓')).grid(row=5, column=6, padx=5,
                                                                                              pady=10)

    def create_ecran(self):
        '''Creation de l'écran de calcul'''
        self.ecran = Entry(text="", bg='white', fg='black')
        self.ecran.grid(row=1, column=0, columnspan=6, sticky='nsew')

    def create_label(self):
        '''Création du nom de la calculatrice'''
        self.label = Label(text='Calculator3000', fg='yellow', bg='black')
        self.label.grid(row=0, column=0, columnspan=6, sticky='nsew')

    def ajouter(self, car):
        '''Ajout de chaque caractère saisi par les boutons'''
        Fenetre.nb = 0
        self.str_operation += str(car)
        self.ecran.delete(0, END) # Supprimer ce qui est écrit à l'écran avant d'ajouter les nouvelles valeurs
        self.ecran.insert(END, self.str_operation)

    def calculer(self):
        '''Permet de calculer ce que l'utilisateur demande'''
        self.historique.append(self.str_operation) #On ajoute à l'historique le calcul
        self.str_operation = self.str_operation.replace('²', '**2').replace('√', 'sqrt')
        try:
            resultat = eval(self.str_operation) # Fonction eval de python pour calculer la demande de l'utilisateur
            resultat_a_afficher = " = " + str(resultat)
            '''Traitement des exceptions qui renvoient une erreur si jamais une exception est relevée'''
        except ZeroDivisionError:
            resultat_a_afficher = " = Erreur math"
        except ValueError:
            resultat_a_afficher = " = Erreur math"
        except SyntaxError:
            resultat_a_afficher = " = Erreur math"
        self.str_operation = ""
        self.ecran.insert(END, resultat_a_afficher)

    def clear(self):
        '''Remet l'écran vide si jamais le bouton C est pressé'''
        self.str_operation = ""
        self.ecran.delete(0, END)

    def fleche(self, sens):
        if sens == '↑': #Permet de revenir au calcul précédent (historique)
            Fenetre.nb += 1
            self.str_operation = Fenetre.historique[-Fenetre.nb % len(Fenetre.historique)]
            self.ecran.delete(0, END)
            self.ecran.insert(END, self.str_operation)
        elif sens == '↓': #Permet de passer au calcul suivant si une navigation dans l'historique a été faite
            Fenetre.nb -= 1
            self.str_operation = Fenetre.historique[-Fenetre.nb % len(Fenetre.historique)]
            self.ecran.delete(0, END)
            self.ecran.insert(END, self.str_operation)

    def supp(self):
        '''Permet de supprimer le dernier élément saisi'''
        self.str_operation = self.str_operation[:-1]
        self.ecran.delete(0, END)
        self.ecran.insert(END, self.str_operation)


    '''def calcul_et_fonction(self):
        self.str_operation = self.ecran.get()
        try:
            resultat = eval(self.str_operation)
            self.ajouter(resultat)
        except ValueError:
            self.set_screen("Error Math")
            
            Piste abandonnée, nous avons essayé de créer une fonction qui pouvait permettre d'activer une fonction
            au toucher d'un bouton. Cela signifie qu'il aura simplement fallu d'appuyer sur cos et le résultat serait 
            diretement apparu. Cependant nous n'avons pas réussi.
            '''


def main():
    ma_fenetre = Fenetre()
    ma_fenetre.mainloop()


if __name__ == '__main__':
    main()
