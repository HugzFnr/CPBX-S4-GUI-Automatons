#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module Modele: contains all the elements that acts \
on the cellular Automaton.
"""

import random
import copy

class Automaton:
    """All data about the board and its evolution.

    This is the main class of this file.
    """
    def __init__(self,dimensions=(40,30),ruleset="LifeGame"
                 ):
        """Initializes the automaton.

        :param dimensions: the dimensions of the automaton, as a pair
        (width, height)
        :param ruleset: a ruleset, as a string. 
        If the string is not acceptable or implemented, makes an automaton with the ruleset "Fire".
        """
        (self.largeur,self.hauteur) = dimensions
        self.dimensions=dimensions
        
        self.ruleset=ruleset
        self.dico=self.get_states()

        self.M=[]
        self.R=[]
        for y in range (self.hauteur):
            self.M.append([])
            for x in range (self.largeur):
                self.R.append("Vide")
                self.M[y].append(self.R[x])
                
        

    def empty_board(self):
        """Empty the current board.

        Acts by side-effect on the automaton.
        """
        for y in range (self.hauteur):
            for x in range (self.largeur):
                self.M[y][x]="Vide"
        

        

    def random_board(self):
        """Fills the current board with random states appropriate for the rules.

        Acts by side-effect on the automaton.
        """

        numeriser=[]
        for k in self.dico.keys():
            if (self.ruleset=="Fire") and (k=="Arbres"): #on ne génère pas de feu ni de cendres pour une map aléatoire
                numeriser.append(k)
                numeriser.append(k)
            if(self.ruleset=="Fire") and (k=="Vide") : #pour le feu de forêt, on génère 2/3 d'arbres
                numeriser.append(k)

            if (self.ruleset=="LifeGame"):
                if (k=="Vivante"):
                    numeriser.append(k)
                elif (k=="Vide"): #pour le jeu de la vie, on génère 1/4 de cellules vivantes
                    numeriser.append(k)
                    numeriser.append(k)
                    numeriser.append(k)
            
        for y in range (self.hauteur):
            for x in range (self.largeur):
                t=int(random.uniform(0,len(numeriser)))
                self.set_cell(y,x,numeriser[t])
        
        if self.ruleset=="Fire": #on rajoute un seul feu sur une cellule aléatoire pour le feu de forêt
            li=int(random.uniform(0,self.hauteur))
            co=int(random.uniform(0,self.largeur))
            self.set_cell(li,co,"Feu")
            
        
    def get_cell_color(self, l, c):
        """Returns the cell color of the cell at position (l,c).

        :params l,c: line and column for the edition of the board. They range from 0 to height-1 or width-1
        :returns: a color as a string from the python standard colors.
        """ 
        return self.dico[self.M[l][c]]
        

    def set_cell(self, l, c, state):
        """Updates the cell l,c to state corresponding to the key "state".

        Is used in particular for editing the board from the controller.
        :param l,c: line and column for the edition of the board. They range from 0 to height-1 or width-1
        :param state: a state as the key in the association form get_states.
        """
        self.M[l][c]=state
        
        
    def compute_step(self, feedback=(lambda l, c, color: None)):
        """ Applies one step to every square on the board.

        :param feedback: a function on three arguments, l, c, color, 
        that is used to notify the controller that a change of color 
        is needed on the cell at position l,c (into the given color).
        :returns: a boolean,  True if at least one cell changed of state.
        """
        retour=bool()
        retour=False
        
        if self.ruleset=="Fire":
            Mcopie =copy.deepcopy(self.M) #il faut faire une deepcopy qui crée bien deux instances différentes de la liste
            for y in range (0,self.hauteur):
                for x in range (0,self.largeur):
                    if Mcopie[y][x]=="Feu":
                        self.set_cell(y,x,"Cendres")
                        feedback(y,x,"grey")
                        if (y-1>=0) and (Mcopie[y-1][x]=="Arbres"): #propagation du feu dans les 4 directions
                            self.set_cell(y-1,x,"Feu")
                            feedback(y-1,x,"red")
                        if (y+1<self.hauteur) and (Mcopie[y+1][x]=="Arbres"):
                            self.set_cell(y+1,x,"Feu")
                            feedback(y+1,x,"red")
                        if (x-1>=0) and (Mcopie[y][x-1]=="Arbres"):
                            self.set_cell(y,x-1,"Feu")
                            feedback(y,x-1,"red")
                        if (x+1<self.largeur) and (Mcopie[y][x+1]=="Arbres"):
                            self.set_cell(y,x+1,"Feu")
                            feedback(y,x+1,"red")   #pourquoi ça explose des fois vers le bas et à droite? c'était le soucis deepcopy/shallow copy
                        retour=True
                        
        elif self.ruleset=="LifeGame":
            Mcopie=copy.deepcopy(self.M)
            for y in range (0,self.hauteur):
                for x in range (0,self.largeur):
                    if Mcopie[y][x]=="Vivante":
                        voisinsviv=0
                        
                        for xv in range (x-1,x+2):
                            for yv in range (y-1,y+2):
                                if (((xv,yv)!=(x,y))==True) and (xv<self.largeur) and (yv<self.hauteur) and (yv>=0) and (xv>=0) and (Mcopie[yv][xv]=="Vivante"):
                                    voisinsviv=voisinsviv+1
                
                        if (voisinsviv!=3) and (voisinsviv!=2):
                            feedback(y,x,"white")
                            self.set_cell(y,x,"Vide")
                            
                            retour=True
                        
                                    
                    elif Mcopie[y][x]=="Vide":
                        voisinsviv=0
                        for xv in range (x-1,x+2):
                            for yv in range (y-1,y+2):
                                if (((xv,yv)!=(x,y))==True) and (xv<self.largeur) and (yv<self.hauteur) and (yv>=0) and (xv>=0) and (Mcopie[yv][xv]=="Vivante"):
                                    voisinsviv=voisinsviv+1
                        if (voisinsviv==3):
                            feedback(y,x,"orange")
                            self.set_cell(y,x,"Vivante")
                            
                            retour=True
        return retour
                        

    def get_states(self):
        """ Returns the states of the current ruleset.
        
        :returns: a dictionary of {state :color} for the current ruleset.
        """
        if self.ruleset=="Fire":
            return ({"Feu":"red","Arbres":"green","Vide":"white","Cendres":"grey"})
            
        elif self.ruleset=="LifeGame":
            return ({"Vivante":"orange","Vide":"white"})
        
