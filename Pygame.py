import pygame
pygame.init()

dimensione_finestra = width,height = 800,600  # creo variabile di dimensione finestra
black= 0,0,0
RED  = 255, 0, 0 
WHITE = 255,255,255
finestra = pygame.display.set_mode(dimensione_finestra) # creo la finestra inserendo la variabile creata
# carichiamo il font e lo assegniamo alla variabile fnt
fnt = pygame.font.SysFont("Times New Roman", 24)


surf_text1 = fnt.render("!! GAME OVER !!", True, "yellow")
surf_text2 = fnt.render("Willst du noch spielen ?", True, "yellow")
surf_text3 = fnt.render(" Ja = Strg + j \ Nein = Strg + n", True, "yellow")


################################## TESTA UNO ####################################################################

testa = pygame.image.load('testa.png') # carico la foto
testa = pygame.transform.scale(testa, (50, 50))  # ridimensiona la testa nota che ho chiamato con lo stesso nome della foto 
speed_testa = [6,-3]   # parametro per lo spostamento indica i pixel che vanno a cambiare in x e y
testarect = testa.get_rect()  #Serve per inscrivere l´immagine in un rettangolo vengono applicati wuesti valori (asse x, asse y, w,h)
testarect[0] = 0
testarect[1] = 200
game_over = False


################################### SPIELER #################################################################################

giocatore= pygame.Rect(230,590,120,10)
speed_giocatore = [10]               # solo sull´asse x
#rettangolo_rect = rettangolo.get_rec() non serve perche é gia un rettangolo a quanto pare serve per le foto o altri elementi
 
############################################## VIERECK-KONTRUKTION #################################################################
# X-ACHSE CALKULATION
erste_stock=  []
zweite_stock= []
dritte_stock= []

def x_position_Viereck (n,name_liste):
    Abstand = 3
    width_Viereck = 28
    x_position = (dimensione_finestra[0]/2) - ((n//2)*(Abstand + width_Viereck))   # Wo die erste viereck im x Achse fengt
    if name_liste == erste_stock:
        for i in range (0,n):
            position = x_position + ((Abstand + width_Viereck) * i)
            name_liste.append(position)
    elif name_liste == zweite_stock:
        position = erste_stock[1]         # Ertse Vierck fängt , nach die zweite Viereck von erste-stock
        for i in range (0,n):
            position = x_position + ((Abstand + width_Viereck) * i)
            name_liste.append(position)
    else:
        position = zweite_stock[1]
        for i in range (0,n):
            position = x_position + ((Abstand + width_Viereck) * i)
            name_liste.append(position)


x_position_Viereck(16,erste_stock)       
x_position_Viereck(16,zweite_stock)
x_position_Viereck(16,dritte_stock)

########################################### VIERECK - KLASSE #################################################################
class Viereck:
    def __init__(self, x, y, width = 28, height = 28, lebe=20):
        self.rect = pygame.Rect(x, y, width, height)  # Oggetto pygame.Rect
        self.lebe = lebe  # Vita del rettangolo
        self.in_game = True  # Stato attivo nel gioco
        self.width = width  # Definizione esplicita
        self.height = height


  # erste-Stock
erste_stock_viereck=[]                          # liste für um die Viereck einzutragen    da rivedere perche non funziona 
y_Achse_Vierecke1 = 231
for _ in range(0,15):
    erste_stock_viereck.append(Viereck(erste_stock[_],y_Achse_Vierecke1))                         # OCCHIO CHE I QUADRATI NELLA LISTA NON HANNO NOME QUINDI SI DEVE UTILIZZARE L´INDEX 


  # zweite-Stock
zweite_stock_viereck=[] 
y_Achse_Vierecke2 = 201
for _ in range(0,15) :
    zweite_stock_viereck.append(Viereck(zweite_stock[_],y_Achse_Vierecke2))


      # dritte-Stock
dritte_stock_viereck =[]
y_Achse_Vierecke3 = 171
for _ in range(0,15) :
    dritte_stock_viereck.append(Viereck(dritte_stock[_],y_Achse_Vierecke3))


########################################################### MAIN LOOP ###############################################
# configuro il gioco per chiudere la finestra 
running = True    #  variabile per far partire il loop
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT : 
            running = False

       
######################################### INSERIMENTO DEI TASTI PER MUOVERE IL RETTANGOLO######################################################
            #   KEY ANWENDUNG
    tasti_premuti = pygame.key.get_pressed()

    if  tasti_premuti[pygame.K_LEFT]:  # Freccia sinistra
        giocatore.x -= speed_giocatore [0]
    if tasti_premuti[pygame.K_RIGHT]:  # Freccia destra
        giocatore.x +=  speed_giocatore [0]
        
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running= False
 #       if event.key == pygame.K_n:
  #          running= False
        if event.key == pygame.K_j:
            running= True
##################################################################################################################
######### !!!! È IMPORTANTE CHE DALLA CHIAMATA DEL PROGRAMMA TUTTO RIENTRI NEL WHILE 
   

    testarect= testarect.move(speed_testa)   # .move dichiara lo spostamennto della testa
    
    
                # KOPF
    if testarect.left < 0 or testarect.right > width :     # determino una if per non superare i
        speed_testa[0] = - speed_testa [0]                             #  bordi e falla ritornare in dietro convertendo il umero in negativo
    if testarect.top < 0 or testarect.bottom > height:    
        speed_testa[1] = - speed_testa [1]                              # é 1 perche si parla dell´index della tupla nella speed
    if testarect.bottom > height:
        game_over == True
        finestra.blit(surf_text1, (300, 300))
        finestra.blit(surf_text2, (275, 330))
        finestra.blit(surf_text3, (240, 370))
        pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running= False





         # SPIELER
    if giocatore.left < 0:
        giocatore.left = 0                       # limito il rettangolo nello screen 
    if giocatore.right > width:
        giocatore.right = width

#######################################################  COLLISIONI TESTA ####################################################################################################
    # calcolo tutte le probabili collisioni 
    def Collision_testarect(name):                            
       if testarect.colliderect(name):
            if  name != giocatore and name.in_game == True:
                if testarect.right >= name.rect.left and testarect.left < name.rect.left:
                    speed_testa[0] = - speed_testa[0]
                    name.lebe -= 5
                    print(f"vita {name} = {name.lebe}")
                elif testarect.left <= name.rect.right and testarect.right > name.rect.right:
                    speed_testa[0] = - speed_testa[0]
                    name.lebe -= 5                                                                                                                 # ANCORA DA AGGIUSTARE  
                    print(f"vita {name} = {name.lebe}")
                elif testarect.top <= name.rect.bottom and testarect.bottom > name.rect.bottom:
                    speed_testa[1] = - speed_testa[1]
                    name.lebe -= 5
                    print(f"vita {name} = {name.lebe}")
                if testarect.bottom >= name.rect.top and testarect.top < name.rect.top:
                    speed_testa[0] = - speed_testa[0]
                    speed_testa[1] = - speed_testa[1]
                    name.lebe -= 5
                    print("Collisione")
                    print(f"vita {name} = {name.lebe}")
                    
                    
                    #      elif Ecken
                    # angolo in alto a sinistra  per dichiararli scrivo in parentesi prima i lati che si toccano con i quadrati e poi determino la posizione degli opposti (cioe di quelli che non si toccano )
                elif  (testarect.right >= name.rect.left and testarect.bottom >= name.rect.top) and (testarect.left < name.rect.left and testarect.top < name.rect.top):
                    speed_testa[0] = - speed_testa[0]
                    speed_testa[1] = - speed_testa[1]
                    name.lebe -= 5
                    print(f"vita {name} = {name.lebe}")
                elif (testarect.left <= name.rect.right and testarect.bottom >= name.rect.top) and (testarect.right > name.rect.right and testarect.top < name.rect.top):
                    speed_testa[0] = - speed_testa[0]
                    speed_testa[1] = - speed_testa[1]
                    name.lebe -= 5
                    print(f"vita {name} = {name.lebe}")
                elif (testarect.right >= name.rect.left and testarect.top <= name.rect.bottom) and (testarect.left < name.rect.left and testarect.bottom > name.rect.bottom):
                    speed_testa[0] = - speed_testa[0]
                    speed_testa[1] = - speed_testa[1]
                    name.lebe -= 5
                    print(f"vita {name} = {name.lebe}")

                elif (testarect.left <= name.rect.right and testarect.top <= name.rect.bottom) and (testarect.right > name.rect.right and testarect.bottom > name.rect.bottom):
                    speed_testa[0] = - speed_testa[0]
                    speed_testa[1] = - speed_testa[1]
                    name.lebe -= 5
                    print(f"vita {name} = {name.lebe}")
            elif name== giocatore:
                speed_testa[1] = - speed_testa[1]          # Kollision Testa - Spieler
       

    Collision_testarect(giocatore)

         # erste Stock
    for _ in range(0,15):
        Collision_testarect(erste_stock_viereck[_])

           # zweite Stock
    for _ in range(0,15):
        Collision_testarect(zweite_stock_viereck[_])
           
            # dritte Stock
    for _ in range(0,15):
        Collision_testarect(dritte_stock_viereck[_])

################################################ IF DEI RETTANGOLO #####################################################################################
    def lebeViereck(name):
        if name.lebe <=0:
            name.in_game = False
            name.width = 0
            name.height = 0

        # erste Stock 
    for _ in range (0,15):
        lebeViereck(erste_stock_viereck[_])
                                                        # VOGLIO ELIMINARE QUESTA PARTE   
       
        # zweite Stock
    for _ in range (0,15):
        lebeViereck(zweite_stock_viereck[_])    
    
        # dritte Stock 
    for _ in range (0,15):
        lebeViereck(dritte_stock_viereck[_])   
   
 
###################################################### SCREEN COLOR AND SURFACES #####################################################################################
    finestra.fill(black)      # do un colore alla finestra inserendo la variabile dichiarata sopra
    if game_over == False:
        finestra.blit(testa,testarect)   # serve per disegnare la testa nella finestra
    
    pygame.draw.rect(finestra, RED, giocatore)

################################################### DRAW RETTANGOLI ################################################################################################
    def draw_in_screen (name):
        if name.in_game == True:
            pygame.draw.rect(finestra, WHITE , name)
        
       
         # erste Stock
    for _ in range(0,15):
        draw_in_screen(erste_stock_viereck[_])  

        # zweite Stock
    for _ in range(0,15):
        draw_in_screen(zweite_stock_viereck[_])  

        # dritte Stock
    for _ in range(0,15):
        draw_in_screen(dritte_stock_viereck[_])   

    
##################################################################################################################################################################################   
   #Imposta il frame rate cioé la quantitá di frame al secondo, quindi ogni volta che riparte il ciclo 
    pygame.time.Clock().tick(60)
    pygame.display.flip()   # aggiorno sempre la finestra e inserisco gli aggiornamenti , importante
pygame.quit()

