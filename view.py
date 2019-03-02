#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" View
"""
largeur_canvas=400
hauteur_canvas=300

from math import *
from tkinter import *


class View():
    


    def __init__(self, dimensions, states, set_state, control_variables):
        """Initializes the view.

        :param dimensions: the dimensions of the automaton,
        as a pair (width, height)
        :param states: gives the available states.
        It is given as a dictionary whose keys are the names of the states
        and the corresponding entries are the colors.
        :param set_state: the function to call for updating a state
        in the automaton. It takes three arguments, the line, the column, and
        the state to apply (i.e. the key from the dictionary)
        :param control_variables: a dictionary of variables that are shared
        with the controller.
        """
        (w,h)=dimensions
        self.l_carre=int(largeur_canvas/w)
        self.h_carre=int(hauteur_canvas/h)
        self.states=states
        self.set_state=set_state
        self.control_variables=control_variables #on exporte les arguments donnés en init pour pouvoir les utiliser dans d'autres méthodes
        
        self.window = Tk()
        self.dessin=Canvas(self.window,height=hauteur_canvas,width=largeur_canvas,bg="grey")
        self.dessin.grid(row=1,column=0,columnspan=20,rowspan=10)

        self.L=[] #on génère le quadrillage de cellules qu'on associe à une matrice( liste de listes )
        self.C=[]
        for y in range (0,h):
            self.C.append([])
            for x in range (0,w):
                self.L.append(0)
                self.L[x]=self.dessin.create_rectangle(x*self.l_carre,y*self.h_carre,x*self.l_carre+self.l_carre,y*self.h_carre+self.h_carre,fill="white")
                self.C[y].append(self.L[x])     #(C[y])[x] pour accéder à la cellule (ligne y, colonne x)
        
        #on fait fonctionner le clic sur le canvas
        self.dessin.bind("<Button-1>",self.clic)
        self.dessin.bind("<B1-Motion>",self.clic)

        #Puces radio :
        self.radio=LabelFrame(self.window,bg="grey",text="Curseur",labelanchor="n")
        self.value=StringVar()
        for i in states :
            self.btnactionsouris = Radiobutton(self.radio,text=i,variable=self.value,value=i,bg=states[i],width=10)
            self.btnactionsouris.pack(side="bottom")

        self.radio.grid(row=0,column=21,rowspan=4)
        
        #fenêtre édition
        self.edition=LabelFrame(self.window,text="Edition",bg="grey",labelanchor = "n")

        #Boutons d'édition:
        self.btnreset=Button(self.edition,text="Réinitialiser")
        self.btnreset.pack(side="right")

        self.btnrandommap=Button(self.edition,text="Générer carte aléatoire")
        self.btnrandommap.pack(side="right")
        
        self.edition.grid(row=4,column=21,rowspan=2)

        #Fenêtre contrôle
        self.control=LabelFrame(self.window,text="Contrôle",bg="grey",labelanchor = "n")
        
        #Echelle de vitesse
        control_variables["speed"]=IntVar()
        self.btnscale=Scale(self.control,variable=control_variables["speed"],label="Vitesse de propagation",orient="horizontal", from_=0, to=500,resolution=1,tickinterval=50,length=300)
        self.btnscale.pack() 
        
        #Bouton(s) de contrôle
        self.btnpause=Button(self.control,text="Pause")
        self.btnpause.pack(side="top")
        
        self.control.grid(row=6,column=21,rowspan=4)
        
        #Menu changement d'automate
        self.menub = Menubutton(self.window, text="Automates")
        self.menub.grid(row=0,column=0)

        self.menub.menu = Menu(self.menub, tearoff=0)
        self.menub['menu'] = self.menub.menu

        self.menub.menu.insert_command(index=0,label="Petit feu de fôret")
        self.menub.menu.insert_command(index=1,label="Moyen feu de fôret")
        self.menub.menu.insert_command(index=2,label="Grand feu de fôret")
        self.menub.menu.insert_command(index=3,label="Petit jeu de la vie")
        self.menub.menu.insert_command(index=4,label="Moyen jeu de la vie")
        self.menub.menu.insert_command(index=5,label="Grand jeu de la vie")

        
    def set_cell_color(self, l, c, color):
        """Changes the color of cell to color.

        :param l: the line number of the cell to edit
        :param c: its column number
        :param color: the color of the cell to set
        """
        self.dessin.itemconfigure((self.C[l])[c],fill=color)

    def clic (self,event):
        if event.x<=largeur_canvas and event.y<=hauteur_canvas:#nouvelle méthode pour gérer le clic
            a=(event.x//self.l_carre)
            b=(event.y//self.h_carre)
            self.set_cell_color(b,a,self.states[self.value.get()])
            self.set_state(b,a,self.value.get())
        
    def loop(self):
        """Starts the mainloop of the GUI."""
        self.window.mainloop()

    def bind_action(self, name, action):
        """A function to set an action to a button.a

        :param name: a keyword for setting the action
        :param action: the function to call for that specific action

        :example: self.bind_action(pause,interrupt_execution) \
                  sets the action interrupt execution to the button Pause.
        :returns: False is the binding is not possible."""
        
        if name=="clearmap":
            self.btnreset.configure(command=action)
        elif name=="randmap":
            self.btnrandommap.configure(command=action)
        elif name=="pause":
            self.btnpause.configure(command=action)
        elif name=="small_fire":
            self.menub.menu.entryconfigure(index=0,command=action)
        elif name=="med_fire":
            self.menub.menu.entryconfigure(index=1,command=action)
        elif name=="large_fire":
            self.menub.menu.entryconfigure(index=2,command=action)
        elif name=="small_life":
            self.menub.menu.entryconfigure(index=3,command=action)
        elif name=="med_life":
            self.menub.menu.entryconfigure(index=4,command=action)
        elif name=="large_life":
            self.menub.menu.entryconfigure(index=5,command=action)
        
        

    def reset(self, dimensions, states, set_state):
        """Restart the view with new dimensions and states.

        The parameters coincide with the parameters of the initializer.
        :param dimensions: the dimensions of the automaton,
        as a pair (width, height)
        :param states: gives the available states.
        It is given as a dictionary whose keys are the names of the states
        and the corresponding entries are the colors.
        :param set_state: the function to call for updating a state
        in the automaton. It takes three arguments, the line, the column, and
        the state to apply (i.e. the key from the dictionary)
        """
        self.dessin.delete(ALL)
        self.radio.destroy()
        
        for i in self.states :
            self.btnactionsouris.destroy()
        
        self.radio=LabelFrame(self.window,bg="grey",text="Curseur",labelanchor="n")
        for i in states :
            
            self.btnactionsouris = Radiobutton(self.radio,text=i,variable=self.value,value=i,bg=states[i],width=10)
            self.btnactionsouris.pack(side="bottom")
        self.radio.grid(row=0,column=21,rowspan=4)
        
        (w,h)=dimensions
        self.l_carre=int(largeur_canvas/w)
        self.h_carre=int(hauteur_canvas/h)
        self.states=states
        self.set_state=set_state
        
        self.L=[] #on génère le quadrillage de cellules qu'on associe à une matrice( liste de listes )
        self.C=[]
        for y in range (0,h):
            self.C.append([])
            for x in range (0,w):
                self.L.append(0)
                self.L[x]=self.dessin.create_rectangle(x*self.l_carre,y*self.h_carre,x*self.l_carre+self.l_carre,y*self.h_carre+self.h_carre,fill="white")
                self.C[y].append(self.L[x])     #(C[y])[x] pour accéder à la cellule (ligne y, colonne x)
        
        
        
