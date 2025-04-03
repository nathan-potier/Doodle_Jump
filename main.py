from A_constantes_et_variables_globales import *



# II. FONCTIONS

# Affichage score
def creation_fichier_score():
  #sinon on le met à 9 par défaut
  with open("score.txt", "w") as file:
    file.write("0")


def charger_fichier_score():
  global best
  #on charge le meilleur score depuis un fichier texte:
  if os.path.exists("score.txt"):
    #si le fichier existe on recup le meilleur score
    with open("score.txt", "r") as file:
      best = int(file.read())

  else:
    creation_fichier_score()


def affiche_score_menu():
  canevas.create_text(10, 400, fill = "darkblue", font = "Times 16", text = "Votre Score: "+ str(current_score),  anchor = "w")
  canevas.create_text(10, 450, fill = "darkblue", font = "Times 16", text = "Votre Meilleur Score: "+ str(best),  anchor = "w")


def appelle_change_difi():
  # appelle la fonction change_difi et change les valeur passer en paramètre grace aux tableau creer dans le fichier constantes et variable globales
  for i in range(0, 12) :
    change_difi(scores_limite[i],  k_vitesse[i] ,  hauteur_sauts[i] , l_vide_cotes[i])


def multiplier_valeur_niv_1(vitesse_augment):
  global platforms_Vitesse, gravity, playerVel

  platforms_Vitesse = platforms_Vitesse * vitesse_augment 
  gravity           = gravity * vitesse_augment
  playerVel         = playerVel * vitesse_augment

 
def valeurs_niv_1():
  global jumpVector, vitesse_multiplicateur, platforms_Vitesse, gravity, playerVel
  jumpVector    = -170
  vitesse_multiplicateur = 1
  platforms_Vitesse = 20
  gravity = 100
  playerVel = [0, 0]
  multiplier_valeur_niv_1(vitesse_multiplicateur)


def change_difi_plat(palier_niv, L_v_c):
  global platformsL
  if nombre_sauts == palier_niv:
    platformsL = L_v_c


def change_difi_vitesse(vm, jV):
  global vitesse_multiplicateur, jumpVector
  valeurs_niv_1()
  vitesse_multiplicateur = vm
  jumpVector = jV
  multiplier_valeur_niv_1(vitesse_multiplicateur)


def change_difi(palier_niv, vm, jV, L_v_c):

  if  verifier_mode == 0:
    change_difi_plat(palier_niv, L_v_c)

  if nombre_sauts == palier_niv :
    change_difi_vitesse(vm, jV)


def acceleration_jeu():

  appelle_change_difi()
  print(vitesse_multiplicateur, jumpVector, platformsL)


def spawn_platform(_x=None, _y=None):
  # Fonction pour faire apparaitre une plateforme

  px = random.randint(platformsL, canevasL - platformsL)
  # on remplace px par _x si il est fourni
    
  px = _x if _x else px
  altitude_lst = [p[1] for p in platforms_pos]
  altitude_lst.append(canevasH)
  alt_min = min(altitude_lst)
  py = alt_min - canevasH / 5

  # ici on remplace py par _y si il est fourni
  py = _y if _y else py

  #on crée l'image de la plateforme sur le canevas
  p_img = canevas.create_image(px, py, image=platform_img)
  p = [px, py, p_img]
  platforms_pos.append(p)


def update_platforms():
  global playerX
  # Fonction qui s'occupe de faire bouger les plateformes à l'écran et en faire apparaitre d'autres quand il n'y en a plus assez.
  
  #on bouge les plateformes et on les suppprime si elles sortent en bas
  for i in platforms_pos:
    p_img = i[2]
    if i[1] > canevasH + 10:
      canevas.delete(i[2])
      platforms_pos.remove(i)
    else:
      canevas.coords(p_img, i[0], i[1])

  #on rajoute des plateformes si il en manque
  for j in range(platformNum - len(platforms_pos)):
    spawn_platform()
  playerX = playerX % canevasL


def move_platforms(n):
  """
  Fonction qui s'occupe de bouger chaque plateforme vers le bas d'une distance n
  """
  for i in platforms_pos:
    i[1] += n


def collidesWith(platform, player_deltaY):  
  """
  permet de verif les collisions que pendant la descente 
  """
  pT = platform[1]   # altitude de la plateforme
  dB = playerY + 52  # bas du joueur

  """
  soit la valeur absolue de la distance joueur-plateforme > 0
  si le joueur monte, delta y est négatif et la 1re condition ne peut pas étre verifiée 
  si le joueur descend, delta y est positif et si il est supérieur à la distance entre joueur et palteforme il y a collision
  il suffit ensuite de vérifier que le joueur n'est pas passé à coté de la plateforme en tombant, avec la 2nde condition
  """
  if abs(pT - dB) < player_deltaY and (pT > dB):
    verif_colision(platform)
     
    if (pRX >= dLX >= pLX ) or (pRX >= dRX >= pLX ): # si les deux delta x sont confondus il y a bien collision
      return True
  return False


def verif_colision(platform):
  global pLX, pRX, dLX, dRX
  pLX = platform[0] # position du coin gauche de la plateforme
  pRX = (pLX + 80)  # position du coin droit de la plateforme 
                    # (positionx plateforme + largeur)
  dLX = playerX  # position du joueur a partir du coin gauche
  dRX = dLX + 70  # position du coin droit dy joueur (pos x du  joueur + largeur)


def clamp(v, mx, mn):
  return max(mn, min(mx, v))


def callback(event):
  print(platforms_pos)
  print("clicked at", event.x, event.y)
  clicks.append([event.x, event.y])
  return clicks


def onpress(event):
  global pressed
  key = event.keysym
  # print('PRESSED:', key)
  pressed[key] = 1
  quitte(key)


def onrelease(event):
  key = event.keysym
  # print('RELEASED:', key)
  pressed[key] = 0


def quitte(key):
  if key == "Escape":
    fen.destroy()


fen.bind("<Button-1>", callback)
fen.bind("<KeyPress>", onpress)
fen.bind("<KeyRelease>", onrelease)


def jump():
  global playerVel, nombre_sauts
  acceleration_jeu()

  playerVel[1] = jumpVector
  nombre_sauts = nombre_sauts + 1


def init_game():
  global playerX, playerY, playerVel, img, platforms_pos
  playerX, playerY = 150, 200
  playerVel = [0, 0]
  
  jump()
  
  img = canevas.create_image(playerX, playerY, image = player)  # On importe l'image dans le canevas

  platforms_pos = []

  spawn_platform(canevasL, canevasH)


def deplace_X(dx : int, direction : str, imag) :
  if pressed.get(direction, 0):
    playerVel[0] += dx
    canevas.itemconfig(img, image = imag)


def mouvement_X():
  deplace_X( 200, "Right", player_right) 
  deplace_X(-200, "Left",  player_left )


def calcul_deplacement_joueur(deltatime):
  global platform_shift, compensate_shift, _playerY, _playerY_maxed, player_deltaY

  
  
  player_deltaY  = playerVel[1] * deltatime
  _playerY       = playerY + player_deltaY   # position du joueur + déplacement du joueur (sur l'axe Y)
  _playerY_maxed = max(canevasH/2, _playerY) # hauteur maximal du joueur 

  platform_shift = platforms_Vitesse * deltatime # permet que les déplacement des platforms soient en 
  compensate_shift = _playerY-_playerY_maxed     # relations avec la vitesse du joueur 
  
  move_platforms(platform_shift-compensate_shift)


def prevoir_pos_joueur():
  global playerY 
  
  # collideswith doit prévoir la pos du joueur, donc on le fait avant de changer sa position
  for p in platforms_pos:
    c = collidesWith(p, player_deltaY-compensate_shift)
    if c:
      jump()
      break
  playerY = _playerY_maxed # permet que le joueur ne s'envole pas et reste sous la haut maximale 


def depassement_joueur_bas(playerY,canevasH):
  return playerY > canevasH


def changer_valeur_best_score():
  global best

  if current_score>best:
    best = current_score
    with open("score.txt", "w") as file:
      file.write(str(best))


def changer_valeur_score(score_text, best):
  global nombre_sauts, current_score

  current_score = nombre_sauts
  canevas.itemconfig(score_text, text = ("Score: " + str(current_score)))
  canevas.itemconfig(best_score_text, text = ("Meilleur score:" + str(best)))
  
  int(best)
  if verifier_mode == 0:
    changer_valeur_best_score()


def affichage_joueur():
  canevas.coords(img, playerX, playerY)
  canevas.tag_raise(img)
  fen.update()


def debut_mvt() :
  global playerVel, playerX

  playerVel[0] /= 2
  mouvement_X()
  playerX += playerVel[0] * deltatime


def nouvelle_vit_joueur():
  global playerVel
  
  # calcule la nouvelle vitesse du joueur
  playerVel[1] += gravity * deltatime
  playerVel[1] = min(2000, playerVel[1])


def game_run(last, score_text, best):
  global now, run, deltatime
  now = time.time()
  deltatime = now - last
  debut_mvt()
  run = not depassement_joueur_bas(playerY, canevasH) #on arrete la partie si on depasse
  nouvelle_vit_joueur()
  calcul_deplacement_joueur(deltatime)
  prevoir_pos_joueur()       
  changer_valeur_score(score_text, best)
  update_platforms()
  affichage_joueur()


def verif_start(score_text):
  global last
  while run : 
    game_run(last, score_text, best) 
    last = now


def game():
  global  run, best_score_text, last
  init_game()
  
  run = True
  last = time.time()
  affichage_background__jeu()
  best_score_text = canevas.create_text(10, 20, fill = "darkblue", font = "Times 16", text = "Meilleur score: " + str(best),  anchor = "w")
  score_text = canevas.create_text(10, 40, fill = "darkblue", font = "Times 16", text = "Score: 0",  anchor = "w")
  verif_start(score_text)


def affichage_background__jeu():
  canevas.create_image(0, 0,   image = bg, anchor = "nw")
  canevas.create_image(0, 800, image = bg, anchor = "sw")


def creation_fond_menu():
  global fond
  fond = PhotoImage(file = "assets/background.png")
  canevas.create_image(-225, 0, image = fond, anchor = "nw")
  can.create_image(0, 0, image = fond, anchor = "nw")


def boutons(btnX,btnY, txt, col):
  canevas.create_rectangle(btnX, btnY, btnX + BoutonsL, btnY + BoutonsH,  fill = col, width=2)
  canevas.create_text(btnX + BoutonsL/2, btnY + BoutonsH/2, text = txt, fill = "white")


def affichage_menu():
  global buttonX, buttonY, nombre_sauts
  
  creation_fond_menu()
  buttonX, buttonY = 50, 50
  
  affiche_score_menu()
  valeurs_niv_1()
  
  boutons(buttonX, 50 , "Jouer"            , "red"  )
  boutons(buttonX, 150, "Mode entrainement", "green")

  
  nombre_sauts = 0
  fen.update()


def verif_clic(c, btnX, btnY, plL, bin):
  global platformsL, verifier_mode
  if (btnX <= c[0] <= btnX + BoutonsL) and (btnY <= c[1] <= btnY + BoutonsH):
    canevas.delete("all")
    clicks.remove(c)
    platformsL = plL
    verifier_mode = bin
    game()


def main():
  charger_fichier_score()
  acceleration_jeu()
  gameRunning = True
  
  while gameRunning :
    affichage_menu()

    for c in clicks:
      verif_clic(c, buttonX, buttonY, 180, 0)
      verif_clic(c, buttonX, 150, 250, 1)


main()
fen.destroy