# coding: utf-8

from source import *
from batiment import *
from element_mobile import *


class Personne(ElementMobile):
    def __init__(self, type_personne, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0):
        ElementMobile.__init__(self, type_personne, carte, x_sur_carte, y_sur_carte, True, objectif, orientation)

    @property
    def nb_places(self):
        return Element.dic_elements[PARAM_A_PERSONNE_NB_PLACES][self.type]
