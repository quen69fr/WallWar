# coding: utf-8

from element import *


class Tireur:
    def __init__(self, type_element):
        self.type_element = type_element
        self.delay_dernier_tir = 0
        self.peut_tirer = False
        self.nb_destructions = 0

    def update(self):
        if self.delay_dernier_tir < self.delay_tir:
            self.delay_dernier_tir += 1
            if self.delay_dernier_tir >= self.delay_tir:
                self.peut_tirer = True

    def point_a_porter_de_tir(self, x_sur_carte, y_sur_carte, x_cible_sur_carte, y_cible_sur_carte):
        return (x_cible_sur_carte - x_sur_carte) ** 2 + (y_cible_sur_carte - y_sur_carte) ** 2 <= self.portee_tir ** 2

    def tir(self):
        self.delay_dernier_tir = 0
        self.peut_tirer = False

    def affiche(self, screen: pygame.Surface, carte: Carte, x_centre_sur_carte, y_centre_sur_carte):
        x_relatif, y_relatif = carte.xy_carte_to_xy_relatif(x_centre_sur_carte, y_centre_sur_carte)
        rayon = int(self.portee_tir * carte.coef_zoom)
        couleur = COULEUR_PORTER_TIR_TIREUR_SELECTION
        draw_filled_circle(screen, (x_relatif, y_relatif), rayon, couleur)
        if len(couleur) == 2:
            couleur = COULEUR_PORTER_TIR_TIREUR_SELECTION[0]
        pygame.gfxdraw.aacircle(screen, x_relatif, y_relatif, rayon, couleur)

    @property
    def force_tir(self):
        return Element.dic_elements[PARAM_A_TIREUR_FORCE_TIR][self.type_element]

    @property
    def portee_tir(self):
        return Element.dic_elements[PARAM_A_TIREUR_PORTEE_TIR][self.type_element]

    @property
    def delay_tir(self):
        return Element.dic_elements[PARAM_A_TIREUR_DELAY_TIR][self.type_element]

    @property
    def type_explosion_tir(self):
        return Element.dic_elements[PARAM_F_TIREUR_TYPE_EXPLOSION_TIR][self.type_element]

    @property
    def distance_explosion_centre(self):
        return Element.dic_elements[PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE][self.type_element]
