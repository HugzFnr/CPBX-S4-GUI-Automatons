from modele import *
from view import *


#il manque quelques ajouts ergonomiques et les changements d'automate (et le garde-fou à gauche wtf)

class Controler:

    def __init__(self,dimensions):

        (self.l,self.h)=dimensions

        self.vitesse=60
        self.control_variables={"speed": self.vitesse}
        self.actif=0 #0 : en pause; 1 : actif

        self.Automate=Automaton(dimensions,"LifeGame")
        self.Vue=View(dimensions,self.Automate.get_states(),self.Automate.set_cell,self.control_variables)

        self.Vue.bind_action("clearmap",self.reset)
        self.Vue.bind_action("randmap",self.randomiser)
        self.Vue.bind_action("pause",self.pose)
        self.Vue.bind_action("small_fire",self.petitfeu)
        self.Vue.bind_action("med_fire",self.moyenfeu)
        self.Vue.bind_action("large_fire",self.grandfeu)
        self.Vue.bind_action("small_life",self.petitvie)
        self.Vue.bind_action("med_life",self.moyenvie)
        self.Vue.bind_action("large_life",self.grandvie)
        

    def horloge(self):
        if (self.actif==1) and (self.Vue.control_variables["speed"].get()!=0):
            self.Vue.window.after(60000//self.Vue.control_variables["speed"].get(),self.control_step) #on va dire que la vitesse c'est en APM
        elif (self.actif==1) and (self.Vue.control_variables["speed"].get()==0):
            self.actif==0
            self.Vue.control_variables["speed"].set(60)
            
    def pose(self):
        if (self.actif==0):
            self.actif=1
            if (self.Vue.control_variables["speed"].get()==0):
                self.Vue.control_variables["speed"].set(60)
            self.horloge()
        elif (self.actif==1):
            self.actif=0
            self.horloge()
        
    def control_step(self):
        changement=self.Automate.compute_step(self.Vue.set_cell_color)
        if changement==False:
            self.actif=0
        else:
            self.horloge()
            
    def reset(self):
        self.Automate.empty_board()
        self.actu_vue()

    def randomiser(self):
        self.Automate.random_board()
        self.actu_vue()

    def actu_vue(self): #utile pour les empty_board et random_board pour actualiser la vue par rapport au modèle
        for x in range (self.l):
            for y in range (self.h):
                self.Vue.set_cell_color(y,x,self.Automate.get_cell_color(y,x))

    def petitfeu(self):
        (self.l,self.h)=(40,30)
        self.Automate=Automaton((self.l,self.h),"Fire")
        self.Vue.reset((self.l,self.h),self.Automate.get_states(),self.Automate.set_cell)

    def moyenfeu(self):
        (self.l,self.h)=(80,60)
        self.Automate=Automaton((self.l,self.h),"Fire")
        self.Vue.reset((self.l,self.h),self.Automate.get_states(),self.Automate.set_cell)

    def grandfeu(self):
        (self.l,self.h)=(100,75)
        self.Automate=Automaton((self.l,self.h),"Fire")
        self.Vue.reset((self.l,self.h),self.Automate.get_states(),self.Automate.set_cell)    

    def petitvie(self):
        (self.l,self.h)=(40,30)
        self.Automate=Automaton((self.l,self.h),"LifeGame")
        self.Vue.reset((self.l,self.h),self.Automate.get_states(),self.Automate.set_cell)

    def moyenvie(self):
        (self.l,self.h)=(80,60)
        self.Automate=Automaton((self.l,self.h),"LifeGame")
        self.Vue.reset((self.l,self.h),self.Automate.get_states(),self.Automate.set_cell)

    def grandvie(self):
        (self.l,self.h)=(100,75)
        self.Automate=Automaton((self.l,self.h),"LifeGame")
        self.Vue.reset((self.l,self.h),self.Automate.get_states(),self.Automate.set_cell)
                  
Controleur=Controler((40,30)) #largeur = 4*hauteur/3

Controleur.Vue.loop()
#print(test)
