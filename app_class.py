import pygame
import random
from pygame import mixer

class Bird:

    def __init__(self):
        pygame.init()  # Initialisation de tous les modules de Pygame
        self.gamerunning = True # Intitialisation de l'attribut à True
        self.xScreen, self.yScreen = 900, 900  # Création de la fenêtre
        linkBackGround = './data/background.jpg'  # permet d'utiliser une image comme fond
        self.linkImgBird = "./data/bird.png"  # lien pour l'image de l'oiseau
        self.screen = pygame.display.set_mode(
            (self.xScreen, self.yScreen))  # Créer les dimensions de l'écran
        pygame.display.set_caption("Projet Python - Flappybird")
        self.background = pygame.image.load(linkBackGround)
        icon = pygame.image.load(self.linkImgBird)
        pygame.display.set_icon(icon)
        self.playingButtons = []
        # --------------------------------------------------------
        self.xSizeBird = 60  # la taille du oiseau
        self.ySizeBird = 50  # largeur du oiseau
        self.xBird = self.xScreen / 3  # position initiale x du oiseau
        self.yBird = self.yScreen / 2  # position initiale y du oiseau
        self.VBirdUp = 70  # la vitesse à laquelle saute l'oiseau
        self.VBirdDown = 7  # la vitesse à laquelle tombe l'oiseau
        # ------------------------------
        self.xColunm = self.yScreen + 100  # création de la première colonne
        self.yColunm = 0
        self.xSizeColunm = 100  # largeur de la colonne
        self.ySizeColunm = self.yScreen
        self.Vcolunm = 10  
        self.colunmChange = 0

        self.scores = 0
        self.checkLost = False
    def music(self, url):  # permet d'ajouter une musique pendant la partie
        bulletSound = mixer.Sound(url)
        bulletSound.play()

    def StartText(self):# pour créer la mise en forme et position du bouton START
         font = pygame.font.SysFont("arial", 20, bold=1)
         StartText = font.render("START", True, (242, 242, 242))
         self.screen.blit(StartText, (420,415))


    def image_draw(self, url, xLocal, yLocal, xImg, yImg):  # impression l'image
        PlanesImg = pygame.image.load(url)
        PlanesImg = pygame.transform.scale(
            PlanesImg, (xImg, yImg))  # pour changer la taille de l'image
        self.screen.blit(PlanesImg, (xLocal, yLocal))

    def show_score(self, x, y, scores, size):  # l'affichage de point de joueur
        font = pygame.font.SysFont("comicsansms", size)
        score = font.render(str(scores), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def colunm(self): 
        maginColunm = 80
        yColunmChangeTop = -self.ySizeColunm / 2 - maginColunm + \
                           self.colunmChange  # distance entre la colonne en bas et la colonne en haute est 80*2
        yColunmChangeBotton = self.ySizeColunm / 2 + maginColunm + self.colunmChange
        self.image_draw("./colunm.png", self.xColunm,
                        yColunmChangeTop, self.xSizeColunm, self.ySizeColunm) # pour créer la forme de la colonne en haut
        self.image_draw("./colunm.png", self.xColunm,
                        yColunmChangeBotton, self.xSizeColunm, self.ySizeColunm)  # pour créer la forme de la colonne en bas
        self.xColunm = self.xColunm - self.Vcolunm
        if self.xColunm < -100:
            self.xColunm = self.xScreen  # créer une nouvelle colonne
            # Random distance entre les colonne
            self.colunmChange = random.randint(-150, 150)
            self.scores += 1
        return yColunmChangeTop + self.ySizeColunm, yColunmChangeBotton  # rendre la position de la colonne


    def starting_page(self):# pour démarrer le jeu lorsque le joueur clique sur le bouton START
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            x,y = pygame.mouse.get_pos()
            button1 = pygame.Rect(350,400,200,50)
            self.StartText()
            pygame.draw.rect(self.screen, (242,242,242),button1,6)
            if button1.collidepoint(x,y):
                if click:
                    self.run()
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()


    def run(self):
        while self.gamerunning:
            self.screen.blit(self.background, (0, 0))
            self.music("./moonlight.wav")
            for event in pygame.event.get():  # capter des évenements
                # print(event)
                if event.type == pygame.QUIT:  # pour quitter
                    self.gamerunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.yBird -= self.VBirdUp  # l'oiseau s'en vole

                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_SPACE:
                        self.yBird -= self.VBirdUp  
            self.yBird += self.VBirdDown  # L'oiseau tombe
            yColunmChangeTop, yColunmChangeBotton = self.colunm()
            # print(self.yBird,yColunmChangeTop,self.yBird+self.ySizeBird, yColunmChangeBotton)
            # ---------Vérifier si l'oiseau touche la colonne----------------------------------
            if self.yBird < yColunmChangeTop and (
                    self.xColunm + self.xSizeColunm - 5 > self.xBird + self.xSizeBird > self.xColunm + 5 or self.xColunm + self.xSizeColunm > self.xBird > self.xColunm):
                self.checkLost = True
            if self.yBird + self.ySizeBird > yColunmChangeBotton and (
                    self.xColunm + self.xSizeColunm - 5 > self.xBird + self.xSizeBird > self.xColunm + 5 or self.xColunm + self.xSizeColunm > self.xBird > self.xColunm):
                self.checkLost = True
            # ---------Vérifier si l'oiseau touche le mur-----------------------------
            if (self.yBird + self.ySizeBird > self.yScreen) or self.yBird < 0:
                self.yBird = self.yScreen / 2
                self.checkLost = True
            self.Vcolunm = 10 if self.scores < 1 else 10 + self.scores / 5  # Le score augmente de 1 ) chaque fois que l'oiseau dépasse une colonne sans la toucher
            self.VBirdDown = 7 if self.scores < 1 else 7 + \
                                                       self.scores / 10  
            while (self.checkLost):  # Si l'oiseau touche des objets => le jouer perd
                self.xColunm = self.xScreen + 100
                for event in pygame.event.get():  
                    if event.type == pygame.QUIT:  # quitter
                        self.gamerunning = False
                        self.checkLost = False
                        break
                    if event.type == pygame.KEYDOWN:  # quitter
                        self.checkLost = False
                        self.scores = 0
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.checkLost = False
                        self.scores = 0
                self.show_score(100, 100, "Scores:{}".format(
                    self.scores), 40)  #  Pour afficher le score
                self.show_score(self.xScreen / 2 - 100, self.yScreen /
                                2 - 100, "PERDUUUUU", 50)  # Pour annoncer au joueur qu'il a perdu
                self.Vcolunm = 6
                self.VBirdDown = 7
                pygame.display.update()
            self.image_draw(self.linkImgBird, self.xBird,
                            self.yBird, self.xSizeBird, self.ySizeBird)
            self.show_score(self.xScreen - 200, 20, "Master 2 MIMO", 25)
            self.show_score(10, 10, "Scores:{}".format(self.scores), 35)
            pygame.display.update()  # pour mettre à jour le jeu
            clock = pygame.time.Clock()
            clock.tick(80)
