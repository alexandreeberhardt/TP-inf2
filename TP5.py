from tkinter import Button, Entry, Label, Tk, END, Frame
from math import sin, tan, cos, sqrt, pi


class Fenetre(Tk):
    historique = []

    def __init__(self):
        Tk.__init__(self)
        '''self.ecran = None
        self.label = None'''
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        l = 200
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

    def build(self):
        parametre_bouton_nombre = {'bd': '4', 'bg': '#778da9', 'fg': 'white'}
        parametre_bouton_calcul = {'bd': '2', 'bg': '#9f86c0', 'fg': 'black'}
        parametre_bouton_clear = {'bd': '2', 'bg': '#4cc9f0', 'fg': 'black'}
        parametre_bouton_egal = {'bd': '2', 'bg': '#fbf8cc', 'fg': 'black'}

        frame = Frame(self)
        frame.grid()
        # Nombre
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
        self.ecran = Entry(text="", bg='white', fg='black')
        self.ecran.grid(row=1, column=0, columnspan=6, sticky='nsew')

    def create_label(self):
        self.label = Label(text='Calculator3000', fg='yellow', bg='black')
        self.label.grid(row=0, column=0, columnspan=6, sticky='nsew')

    def ajouter(self, car):
        self.str_operation += str(car)
        self.ecran.delete(0, END)
        self.ecran.insert(END, self.str_operation)

    def calculer(self):

        self.historique.append(self.str_operation)
        self.str_operation = self.str_operation.replace('²', '**2').replace('√', 'sqrt')
        try:
            resultat = eval(self.str_operation)
            resultat_a_afficher = " = "+str(resultat)
            self.ecran.insert(END, resultat_a_afficher)
            self.str_operation=""
        except ZeroDivisionError:
            print("Error")
        except ValueError:
            print("Error")
        except SyntaxError:
            print("Error")

    def clear(self):
        self.str_operation = ""
        self.ecran.delete(0, END)

    def fleche(self, sens):
        pass

    def supp(self):
        self.str_operation = self.str_operation[:-1]
        self.ecran.delete(0, END)
        self.ecran.insert(END, self.str_operation)


def main():
    ma_fenetre = Fenetre()
    ma_fenetre.mainloop()


if __name__ == '__main__':
    main()

