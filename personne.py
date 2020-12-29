# coding: utf-8

from source import *
from batiment import *
from element_mobile import *


class Personne(ElementMobile):
    def __init__(self, type_personne, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0, alea=0):
        ElementMobile.__init__(self, type_personne, carte, x_sur_carte, y_sur_carte, True, objectif, orientation, alea)
        self.objectif_groupe = None

    def stop(self):
        ElementMobile.stop(self)
        self.objectif_groupe = None

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False, alea=0):
        if i_objectif is None or j_objectif is None:
            i_objectif, j_objectif = self.carte.xy_carte_to_ij_case(x_carte, y_carte)
        ElementMobile.new_objectif(self, x_carte, y_carte, i_pos, j_pos, i_objectif, j_objectif,
                                   modification_chemin_seulement, alea)
        self.objectif_groupe = (i_objectif, j_objectif)

    @property
    def nb_places(self):
        return Element.dic_elements[PARAM_A_PERSONNE_NB_PLACES][self.type]
