# coding: utf-8

from element_mobile_tireur import *


class Ennemi(ElementMobileTireur):
    def __init__(self, carte: Carte, x_sur_carte: int, y_sur_carte: int, nb_vies, vitesse, force_tir, portee_tir,
                 delay_tir, portee_vision, num_base_ennemi, niveau_d_intelligence, alea=0):
        ElementMobileTireur.__init__(self, TYPE_ENNEMI, carte, x_sur_carte, y_sur_carte,
                                     TireurEnnemi(force_tir, portee_tir, delay_tir, portee_vision), False, alea=alea)
        self.num_base_ennemi = num_base_ennemi
        self._nb_vies_max = nb_vies
        self._vitesse_deplacement = vitesse
        self._niveau_d_intelligence = niveau_d_intelligence
        self.offencif = False
        self.num_vague = 0
        self.type_vague = LISTE_VAGUES_ENNEMIS[self.num_vague]
        self.niveau_d_intelligence_actuel = niveau_d_intelligence
        self.update_new_type_vague()

    def tir_si_possible(self):
        if ElementMobileTireur.tir_si_possible(self):
            if isinstance(self.cible, Batiment):
                self.tireur.nb_degas_batiment += self.tireur.force_tir
            else:
                self.tireur.nb_degas_element_mobile += self.tireur.force_tir
            return True
        return False

    def vague_suivante(self):
        self.num_vague += 1
        if self.num_vague < len(LISTE_VAGUES_ENNEMIS):
            type_vague = LISTE_VAGUES_ENNEMIS[self.num_vague]
            if not type_vague == self.type_vague:
                self.type_vague = type_vague
                self.update_new_type_vague()

    def update_new_type_vague(self):
        if self.type_vague == TYPE_VAGUE_ENNEMI_DEFFENCEIVE_IMMOBILE:
            self.immobile = True
            self.offencif = False
        elif self.type_vague == TYPE_VAGUE_ENNEMI_DEFFENCEIVE_LIBRE:
            self.immobile = False
            self.offencif = False
        elif self.type_vague == TYPE_VAGUE_ENNEMI_OFFENCIVE:
            self.immobile = False
            self.offencif = True

    def mort_cible(self):
        self.cible = None

    def find_cible_base(self, liste_batiments):
        liste_bases = []
        for batiment in liste_batiments:
            if batiment.type == TYPE_BATIMENT_BASE:
                liste_bases.append(batiment)
        if len(liste_bases) > 0:
            if len(liste_bases) == 1:
                return liste_bases[0]
            else:
                i, j = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)
                return min(liste_bases, key=lambda bat: (bat.i - i) ** 2 + (bat.j - j) ** 2)
        return None

    def update_cible(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        ElementMobileTireur.update_cible(self, liste_adversaires_mobiles, liste_adversaires_statiques)
        if self.cible is None and self.offencif:
            self.cible = self.find_cible_base(liste_adversaires_statiques)

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
        elif param == PARAM_A_TIREUR_INTELLIGENCE:
            return self._niveau_d_intelligence
        return 0

    @property
    def nb_vies_max(self):
        return self._nb_vies_max

    @property
    def vitesse_deplacement(self):
        return self._vitesse_deplacement

    def niveau_d_intelligence(self):
        return self._niveau_d_intelligence
