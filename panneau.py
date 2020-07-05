# coding: utf-8

from monde import *


class Panneau:
    def __init__(self, monde: Monde, x_ecran: int, y_ecran: int, largeur_ecran: int, hauteur_ecran: int):
        self.monde = monde

        self.x_ecran, self.y_ecran = x_ecran, y_ecran
        self.largeur_ecran, self.hauteur_ecran = largeur_ecran, hauteur_ecran
        self.ecran = pygame.Surface((self.largeur_ecran, self.hauteur_ecran))

        self.new_affichage = True

    def update(self):
        pass

    def update_affichage(self):
        pass

    def affiche(self, screen: pygame.Surface):
        if self.new_affichage:
            self.update_affichage()
            self.new_affichage = False
        screen.blit(self.ecran, (self.x_ecran, self.y_ecran))
