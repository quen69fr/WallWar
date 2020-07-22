# coding: utf-8

from tireur import *


class TireurEnnemi(Tireur):
    dic_liste_cases_relatives_porter_tir = {}

    def __init__(self, force_tir, portee_tir, delay_tir, portee_vision):
        Tireur.__init__(self, TYPE_ENNEMI)
        self._force_tir = force_tir
        self._portee_tir = portee_tir
        self._delay_tir = delay_tir
        self._portee_vision = portee_vision
        self.nb_degas_batiment = 0
        self.nb_degas_element_mobile = 0

    def rate_degas_destructions(self):
        return self.nb_degas_batiment * COEF_NOTE_ENNEMI_DEGAS_BATIMENT + \
               self.nb_degas_element_mobile * COEF_NOTE_ENNEMI_DEGAS_ELEMENT_MOBILE + \
               self.nb_destructions * COEF_NOTE_ENNEMI_VICTIME

    @property
    def force_tir(self):
        return self._force_tir

    @property
    def portee_tir(self):
        return self._portee_tir

    @property
    def portee_vision(self):
        return self._portee_vision

    @property
    def delay_tir(self):
        return self._delay_tir
