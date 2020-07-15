# coding: utf-8

from carte import *
import copy


class Element:
    dic_elements = copy.deepcopy(DIC_ELEMENTS)

    def __init__(self, type_element):
        self.type = type_element
        self.nb_vies_malus = 0

    def get_value_param(self, param):
        return Element.dic_elements[param][self.type]

    def recoit_tir(self, force_tir):
        self.nb_vies_malus += force_tir

    def add_vies(self, nb_vies):
        self.nb_vies_malus -= nb_vies
        if self.nb_vies_malus < 0:
            self.nb_vies_malus = 0

    @property
    def nom(self):
        return Element.dic_elements[PARAM_F_NOM][self.type]

    @property
    def description(self):
        return Element.dic_elements[PARAM_F_DESCRIPTION][self.type]

    @property
    def nb_vies_max(self):
        return Element.dic_elements[PARAM_A_VIES][self.type]

    @property
    def nb_vies(self):
        return self.nb_vies_max - self.nb_vies_malus

    @property
    def type_explosion(self):
        return Element.dic_elements[PARAM_F_TYPE_EXPLOSION][self.type]
