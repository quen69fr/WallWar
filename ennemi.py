# coding: utf-8

from element_mobile import *
from tireur_ennemi import *


class Ennemi(ElementMobile):
    def __init__(self, carte: Carte, x_sur_carte: int, y_sur_carte: int, nb_vies, vitesse, force_tir, portee_tir,
                 delay_tir):
        ElementMobile.__init__(self, TYPE_ENNEMI, carte, x_sur_carte, y_sur_carte, False)
        self.cible = None
        self._nb_vies_max = nb_vies
        self._vitesse_deplacement = vitesse
        self.tireur = TireurEnnemi(force_tir, portee_tir, delay_tir)

    def affiche_tireur(self, screen: pygame.Surface):
        self.tireur.affiche(screen, self.carte, self.x_sur_carte, self.y_sur_carte)

    def mort_cible(self):
        self.cible = None

    def get_value_param(self, param):
        if param == PARAM_A_VIES:
            return self._nb_vies_max
        elif param == PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT:
            return self._vitesse_deplacement
        elif param == PARAM_A_TIREUR_FORCE_TIR:
            return self.tireur.force_tir
        elif param == PARAM_A_TIREUR_DELAY_TIR:
            return self.tireur.delay_tir
        elif param == PARAM_A_TIREUR_PORTEE_TIR:
            return self.tireur.portee_tir

    @property
    def nb_vies_max(self):
        return self._nb_vies_max

    @property
    def vitesse_deplacement(self):
        return self._vitesse_deplacement
