from tkinter import *
from math import sin, tan, cos, sqrt, pi
class Fenetre(Tk):
    historique = []
    nb = 0

    def __init__(self):
        Tk.__init__(self)
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        l = 720
        h = 480
        pos_x = ecran_x // 2 - l // 2
        pos_y = ecran_y // 2 - h // 2
        geometrie = f"{l}x{h}+{pos_x}+{pos_y}"
        self.geometry(geometrie)
        self.title("TP Calculatrice")
        self.config(bg='black')
        self.eval('tk::PlaceWindow . center')
        self.str_operation = "" # str qui permet rStocker les opérations
        Label(self,text="Calculatrice d'Alexandre et Léo",fg='white',bg='black').pack()
        self.operation = StringVar()
        self.operation.set('')
        self.build()

    def build(self):
        parametre_bouton_nombre = {bd : '10', bg : 'white', fg : 'black'}
        parametre_bouton_calcul = {bd : '10', bg : 'yellow', fg : 'black'}
        parametre_bouton_clear = {bd : '10',bg: 'green',fg : 'black'}
        parametre_bouton_egal = {bd : '10',bg: 'red',fg : 'black'}

        frame = Frame(self)
        frame.grid()
        #Nombre
        Button(frame,parametre_bouton_nombre, text='1', command=lambda: self.ajouter('1')).grid(row=2, column=0, padx=5, pady=10)
        Button(frame, parametre_bouton_nombre, text='2', command=lambda: self.ajouter('2')).grid(row=2, column=1, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='3', command=lambda: self.ajouter('3')).grid(row=2, column=2, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='4', command=lambda: self.ajouter('4')).grid(row=3, column=0, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='5', command=lambda: self.ajouter('5')).grid(row=3, column=1, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='6', command=lambda: self.ajouter('6')).grid(row=3, column=2, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='7', command=lambda: self.ajouter('7')).grid(row=4, column=0, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='8', command=lambda: self.ajouter('8')).grid(row=4, column=1, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='9', command=lambda: self.ajouter('9')).grid(row=4, column=2, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='0', command=lambda: self.ajouter('0')).grid(row=5, column=1, padx=5,pady=10)
        Button(frame, parametre_bouton_nombre, text='.', command=lambda:self.ajouter('.')).grid(row=5, column=2 , padx=5,pady=10)


        #Boutons de calcul
        Button(frame,parametre_bouton_calcul, text='+', command=lambda: self.ajouter('+')).grid(row=2, column=4, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='-', command=lambda: self.ajouter('-')).grid(row=3, column=4, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='*', command=lambda: self.ajouter('*')).grid(row=4, column=4, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='/', command=lambda: self.ajouter('/')).grid(row=5, column=4, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='sin', command=lambda: self.ajouter('sin')).grid(row=2, column=5, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='tan', command=lambda: self.ajouter('tan')).grid(row=3, column=5, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='cos', command=lambda: self.ajouter('cos')).grid(row=4, column=5, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='x^2', command=lambda: self.ajouter('x²')).grid(row=5, column=5, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='√x', command=lambda: self.ajouter('√x')).grid(row=6, column=5, padx=5, pady=10)
        Button(frame,parametre_bouton_calcul, text='π', command=lambda: self.ajouter(str(round(pi,4)))).grid(row=6, column=4, padx=5, pady=10)

        #Bouton clear et egal
        Button(frame,parametre_bouton_clear, text='C', command=lambda: self.clear()).grid(row=2, column=4, padx=5, pady=10)
        Button(frame,parametre_bouton_egal,text = '=', command=lambda : self.calculer()).grid(row = 6, column = 0,padx=5, pady=10)

        #Parenthèses
        Button(frame,parametre_bouton_egal,text = '(', command=lambda : self.ajouter('(')).grid(row = 6, column = 1,padx=5, pady=10)
        Button(frame,parametre_bouton_egal,text = ')', command=lambda : self.ajouter(')')).grid(row = 6, column = 2,padx=5, pady=10)

        #Fleches
        Button(frame,parametre_bouton_egal,text = '←', command=lambda : self.supp()).grid(row = 2, column = 6,rowspan=3,padx=5, pady=10)
        Button(frame,parametre_bouton_egal,text = '↑', command=lambda : self.fleche('↑')).grid(row = 3, column = 6,rowspan=3,padx=5, pady=10)
        Button(frame,parametre_bouton_egal,text = '↓', command=lambda : self.fleche('↓')).grid(row = 4, column = 6,rowspan=3,padx=5, pady=10)
    def ajouter(self,car):
        Fenetre.nb = 0
        self.operation += str(car)
        self.operation.set(self.str_operation)

    def calculer(self):


    def clear(self):


    def fleche(self,sens):


    def supp(self):









def main():
    ma_fenetre=Fenetre()
    ma_fenetre.mainloop()

if __name__ == '__main__':
 main()
