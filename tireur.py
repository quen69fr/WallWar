# coding: utf-8

from element import *


def point_a_porter_de_distance(x_sur_carte, y_sur_carte, x_cible_sur_carte, y_cible_sur_carte, distance,
                               return_distance=False):
    dx = abs(x_cible_sur_carte - x_sur_carte)
    if dx > distance:
        return False
    dy = abs(y_cible_sur_carte - y_sur_carte)
    if dy > distance:
        return False
    d2 = dx ** 2 + dy ** 2
    if d2 > distance ** 2:
        return False
    if return_distance:
        return math.sqrt(distance)
    return True


class Tireur:
    dic_liste_cases_relatives_porter_tir = {}

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
        return point_a_porter_de_distance(x_sur_carte, y_sur_carte, x_cible_sur_carte, y_cible_sur_carte,
                                          self.portee_tir)

    def point_visible(self, x_sur_carte, y_sur_carte, x_cible_sur_carte, y_cible_sur_carte):
        return point_a_porter_de_distance(x_sur_carte, y_sur_carte, x_cible_sur_carte, y_cible_sur_carte,
                                          self.portee_vision)

    def tir(self):
        self.delay_dernier_tir = 0
        self.peut_tirer = False

    def affiche(self, screen: pygame.Surface, carte: Carte, x_centre_sur_carte, y_centre_sur_carte):
        x_relatif, y_relatif = carte.xy_carte_to_xy_relatif(x_centre_sur_carte, y_centre_sur_carte)
        rayon = int(self.portee_tir * carte.coef_zoom)
        couleur = COULEUR_PORTER_TIR_TIREUR_SELECTION
        draw_filled_circle(screen, (x_relatif, y_relatif), int(self.portee_vision * carte.coef_zoom), couleur)
        draw_filled_circle(screen, (x_relatif, y_relatif), rayon, couleur)
        if len(couleur) == 2:
            couleur = COULEUR_PORTER_TIR_TIREUR_SELECTION[0]
        pygame.gfxdraw.aacircle(screen, x_relatif, y_relatif, rayon, couleur)

    def get_cases_relative_porter_tir(self, cote_case):
        if self.force_tir not in Tireur.dic_liste_cases_relatives_porter_tir:
            liste_cases = []
            porter_tir_sur_cote_case = self.portee_tir / cote_case
            nb_cases_a_tester = int(porter_tir_sur_cote_case - 0.5)

            liste_cases.append((0, 0))
            for n in range(1, nb_cases_a_tester + 1):
                liste_cases += [(0, n), (0, - n), (n, 0), (- n, 0)]

            for i in range(1, nb_cases_a_tester + 1):
                for j in range(i, nb_cases_a_tester + 1):
                    if (i + 0.5) ** 2 + (j + 0.5) ** 2 <= porter_tir_sur_cote_case ** 2:
                        if i == j:
                            liste_cases += [(i, j), (- i, j), (i, - j), (- i, - j)]
                        else:
                            liste_cases += [(i, j), (- i, j), (i, - j), (- i, - j),
                                            (j, i), (- j, i), (j, - i), (- j, - i)]

            Tireur.dic_liste_cases_relatives_porter_tir[self.force_tir] = liste_cases

        return Tireur.dic_liste_cases_relatives_porter_tir[self.force_tir]

    @property
    def force_tir(self):
        return Element.dic_elements[PARAM_A_TIREUR_FORCE_TIR][self.type_element]

    @property
    def portee_tir(self):
        return Element.dic_elements[PARAM_A_TIREUR_PORTEE_TIR][self.type_element]

    @property
    def portee_vision(self):
        return Element.dic_elements[PARAM_A_TIREUR_PORTEE_VISION][self.type_element]

    @property
    def delay_tir(self):
        return Element.dic_elements[PARAM_A_TIREUR_DELAY_TIR][self.type_element]

    @property
    def type_explosion_tir(self):
        return Element.dic_elements[PARAM_F_TIREUR_TYPE_EXPLOSION_TIR][self.type_element]

    @property
    def distance_explosion_centre(self):
        return Element.dic_elements[PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE][self.type_element]
