import pygame
import random
from pygame import mixer

class Bird:
    def __init__(self):
        pygame.init()  # Init pygame
        self.gamerunning = True
        self.xScreen, self.yScreen = 900, 900  # Screen create
        linkBackGround = './data/background.jpg'  # lien pour l'image de background
        self.linkImgBird = "./data/bird.png"  # lien pour l'image de l'oiseau
        self.screen = pygame.display.set_mode(
            (self.xScreen, self.yScreen))  # Créer dimension d'écran
        pygame.display.set_caption("Projet Python - Flappybird")
        self.background = pygame.image.load(linkBackGround)
        icon = pygame.image.load(self.linkImgBird)
        pygame.display.set_icon(icon)
        self.playingButtons = []
        # --------------------------------------------------------
        self.xSizeBird = 60  # la taille de l'oiseau
        self.ySizeBird = 50  # largeur de l'oiseau
        self.xBird = self.xScreen / 3  # position initial de l'oiseau
        self.yBird = self.yScreen / 2
        self.VBirdUp = 70  # la vitess sauter de l'oiseau
        self.VBirdDown = 7  # la vitess tomber de l'oiseau
        # ------------------------------
        self.xColunm = self.yScreen + 200  # créer premier colonne
        self.yColunm = 0
        self.xSizeColunm = 150  # largeur de la colonne
        self.ySizeColunm = self.yScreen
        self.Vcolunm = 10  # la vitesse déplacer de la colonne
        self.colunmChange = 0

        self.scores = 0
        self.checkLost = False

    def music(self, url):  # pour la musique
        bulletSound = mixer.Sound(url)
        bulletSound.play()

    def image_draw(self, url, xLocal, yLocal, xImg, yImg):  # impression l'image
        PlanesImg = pygame.image.load(url)
        PlanesImg = pygame.transform.scale(
            PlanesImg, (xImg, yImg))  # change size image
        self.screen.blit(PlanesImg, (xLocal, yLocal))

    def show_score(self, x, y, scores, size):  # motrer position
        font = pygame.font.SysFont("comicsansms", size)
        score = font.render(str(scores), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def colunm(self):
        maginColunm = 80
        yColunmChangeTop = -self.ySizeColunm / 2 - maginColunm + \
                           self.colunmChange  # distance entre la colonne en bas et la colonne en haute est 80*2
        yColunmChangeBotton = self.ySizeColunm / 2 + maginColunm + self.colunmChange
        self.image_draw("./data/colunm.png", self.xColunm,
                        yColunmChangeTop, self.xSizeColunm, self.ySizeColunm)
        self.image_draw("./data/colunm.png", self.xColunm,
                        yColunmChangeBotton, self.xSizeColunm, self.ySizeColunm)
        self.xColunm = self.xColunm - self.Vcolunm
        if self.xColunm < -100:
            self.xColunm = self.xScreen  # créer nouvelle colonne
            # Random distance entre les colonne
            self.colunmChange = random.randint(-150, 150)
            self.scores += 1
        return yColunmChangeTop + self.ySizeColunm, yColunmChangeBotton  # rentre la position des colonne

    def run(self): 
        while self.gamerunning:
            self.screen.blit(self.background, (0, 0))
            self.music("./data/moonlight.wav")
            for event in pygame.event.get():  # capter des évenement
                # print(event)
                if event.type == pygame.QUIT:  # pour quitter
                    self.gamerunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.yBird -= self.VBirdUp  # l'oiseau monte
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_SPACE:
                        self.yBird -= self.VBirdUp  # L'oiseau monte
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
            self.Vcolunm = 10 if self.scores < 1 else 10 + self.scores / 5  # la vitesse d'apparaître de colonne augrementé au fur à mesure
            self.VBirdDown = 7 if self.scores < 1 else 7 + \
                                                       self.scores / 10  # la vitesse de tomber de l'oiseau augrementé au fur à mesure
            print(self.Vcolunm)
            while (self.checkLost):  # Si l'oiseau touche des objets
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
                    self.scores), 40)  # Annoncer point gagné
                self.show_score(self.xScreen / 2 - 100, self.yScreen /
                                2 - 100, "GAME OVER", 50)  # Pour annoncer la perde de joueur
                self.Vcolunm = 6
                self.VBirdDown = 7
                pygame.display.update()
            self.image_draw(self.linkImgBird, self.xBird,
                            self.yBird, self.xSizeBird, self.ySizeBird)
            self.show_score(self.xScreen - 200, 20, "Master 2 MIMO", 25)
            self.show_score(10, 10, "Scores:{}".format(self.scores), 35)
            pygame.display.update()  # Update
            clock = pygame.time.Clock()
            clock.tick(80)



  
