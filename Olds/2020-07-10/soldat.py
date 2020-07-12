# coding: utf-8

from personne import *
from tireur import *


class Soldat(Personne):
    def __init__(self, type_personne, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0):
        self.cible: ElementMobile or Batiment or None = None
        self.x_cible, self.y_cible = 0, 0
        self.tireur = Tireur(type_personne)
        self.immobile = False
        Personne.__init__(self, type_personne, carte, x_sur_carte, y_sur_carte, objectif, orientation)

    def affiche_tireur(self, screen: pygame.Surface):
        self.tireur.affiche(screen, self.carte, self.x_sur_carte, self.y_sur_carte)

    def new_cible(self, cible: Element, cible_auto_portee_tir=False, pos_cible_fixe: (int, int) = None):
        if isinstance(cible, ElementMobile):
            self.x_cible, self.y_cible = cible.x_sur_carte, cible.y_sur_carte
        else:
            self.x_cible, self.y_cible = pos_cible_fixe
        if not cible_auto_portee_tir:
            self.new_objectif(self.x_cible, self.y_cible)
        self.cible = cible

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False):
        if not modification_chemin_seulement:
            self.cible = None
            self.immobile = False
        Personne.new_objectif(self, x_carte, y_carte, i_pos, j_pos, i_objectif, j_objectif,
                              modification_chemin_seulement)

    def tir_si_possible(self):
        if self.cible is not None and \
                self.point_a_porter_de_tir(self.x_cible, self.y_cible) \
                and self.tireur.peut_tirer:
            self.cible.recoit_tir(self.tireur.force_tir)
            self.tireur.tir()
            return True
        return False

    def point_a_porter_de_tir(self, x_cible, y_cible):
        return self.tireur.point_a_porter_de_tir(self.x_float, self.y_float, x_cible, y_cible)

    def stop(self):
        Personne.stop(self)
        self.immobile = False
        self.cible = None

    def immobilise(self):
        self.immobile = True
        self.stop()

    def update(self):
        Personne.update(self)
        self.tireur.update()
        if isinstance(self.cible, ElementMobile):
            self.x_cible, self.y_cible = self.cible.x_sur_carte, self.cible.y_sur_carte
        if self.cible is not None:
            if self.point_a_porter_de_tir(self.x_cible, self.y_cible):
                self.objectif = None
                self.chemin_liste_objectifs = []
                if self.new_affichage:
                    self.oriente_vers_point(self.x_cible, self.y_cible)
                else:
                    ancienne_orientation = self._orientation
                    self.oriente_vers_point(self.x_cible, self.y_cible)
                    if abs(ancienne_orientation - self._orientation) < 0.0001:
                        self.new_affichage = False
            else:
                if isinstance(self.cible, ElementMobile):
                    if self.immobile:
                        self.cible = None
                    else:
                        if self.objectif is not None:
                            if not self.chemin_liste_objectifs:
                                self.new_objectif(self.x_cible, self.y_cible,
                                                  modification_chemin_seulement=True)
                            else:
                                i_cible, j_cible = self.carte.xy_carte_to_ij_case(self.x_cible, self.y_cible)
                                x_obj, y_obj = self.chemin_liste_objectifs[-1]
                                i_obj, j_obj = self.carte.xy_carte_to_ij_case(x_obj, y_obj)
                                if i_cible == i_obj and j_cible == j_obj:
                                    self.chemin_liste_objectifs[-1] = self.x_cible, self.y_cible
                                else:
                                    self.new_objectif(self.x_cible, self.y_cible,
                                                      i_objectif=i_cible, j_objectif=j_cible,
                                                      modification_chemin_seulement=True)
                        else:
                            self.new_objectif(self.x_cible, self.y_cible,
                                              modification_chemin_seulement=True)
