from tkinter import *
import time, random, os


# I. Constantes
run = True
fen = Tk()
geo_larg = 950
geo_haut =  800
BoutonsL, BoutonsH = 400, 60


# Paramètre de la fenètre
fen.geometry('950x800')
fen.title("Doodle jump") 
fen.resizable(width=False, height=False)
#fen.iconbitmap('assets/icone.ico')      # incompatible avec IDE en ligne    


# Taille du canvas
canevasL = 500
canevasH = 800


# Valeur au début de la partie
nombre_sauts  = 0              # nombre de saut
current_score = nombre_sauts   # score défini grace aux nombre de sauts


# On charge les images depuis un fichier
player_left     = PhotoImage(file = "assets/perso.png"     )  
player_right    = PhotoImage(file = "assets/right.png"     )
platform_img    = PhotoImage(file = "assets/green.png"     )
bg              = PhotoImage(file = "assets/backg.png"     )
bg_stransparent = PhotoImage(file = "assets/bg_canevas.png")


# Creation du canvas
can = Canvas(fen, height = geo_haut, width = geo_larg, highlightthickness = 0)
can.pack(anchor = CENTER)
canevas = Canvas(fen, height = canevasH, width = canevasL, highlightthickness = 0)
canevas.place(relx = 0.5, rely = 0.5, anchor = CENTER)


# Paramètres de la plateforme
platformsL        = 180
platformNum       = 7
platforms_Vitesse = 20
platforms_pos     = []


# Valeurs au niveau 0
jumpVector             = 170                            
vitesse_multiplicateur = 1
player                 = player_left 
gravity                = 100
playerVel              = [0, 0]


# Paramètre d'une partie
verifier_mode          = 0
playerX                = canevasL/2
playerY                = 270


# Paramètres changements difficulté
scores_limite = [ 5 * k for k in range(1, 13)   ] # scores d'accéléraion de la vitesse
k_vitesse     = list(range(2, 11)) + [12, 15, 20] # multiplicateur des vitesses

increments    = [70, 110, 130, 160, 170, 190, 195, 205, 215, 223, 235, 250]
hauteur_sauts = [ - jumpVector - e for e in increments                    ] 

l_vide_cotes  = [ 170 - 10 * k for k in range(0, 6)] + [ 100 - 20 * k for k in range(0, 5)] + [1]   # Largeur sur les cotés où les plateformes ne peuvent apparaître
                # diminue la valeur de 10 en 10        diminue la valeur de 20 en 20       puis on finis avec une valeur égale à 1

# Contient les touche et les clics presser 
pressed = {}
clicks  = [] 