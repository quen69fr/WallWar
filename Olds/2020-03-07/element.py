# coding: utf-8

from carte import *


class Element:
    def __init__(self, type_element):
        self.type = type_element
        self.nom = DIC_ELEMENTS[PARAM_F_NOM][self.type]
        self.description = DIC_ELEMENTS[PARAM_F_DESCRIPTION][self.type]
        self.nb_vies_max = DIC_ELEMENTS[PARAM_A_VIES][self.type]
        self.nb_vies = self.nb_vies_max
        self.type_explosion = DIC_ELEMENTS[PARAM_F_TYPE_EXPLOSION][self.type]

    def recoit_tir(self, force_tir):
        self.nb_vies -= force_tir

    def get_value_param(self, param):
        if param == PARAM_F_NOM:
            return self.nom
        elif param == PARAM_F_DESCRIPTION:
            return self.description
        elif param == PARAM_A_VIES:
            return self.nb_vies_max
        elif param == PARAM_F_TYPE_EXPLOSION:
            return self.type_explosion
        return None

    def set_value_a_param(self, param, val):
        if param == PARAM_A_VIES:
            d_vie = val - self.nb_vies_max
            self.nb_vies_max += d_vie
            if d_vie > 0:
                self.nb_vies += d_vie
            elif self.nb_vies > self.nb_vies_max:
                self.nb_vies = self.nb_vies_max
            return True
        return False
