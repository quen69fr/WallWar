# coding: utf-8

from personne import *
from tireur import *


class Soldat(Personne):
    def __init__(self, type_personne, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0):
        self.cible: ElementMobile or Batiment or None = None
        self.tireur = Tireur(type_personne)
        self.immobile = False
        Personne.__init__(self, type_personne, carte, x_sur_carte, y_sur_carte, objectif, orientation)

    def affiche_tireur(self, screen: pygame.Surface):
        self.tireur.affiche(screen, self.carte, self.x_sur_carte, self.y_sur_carte)

    def new_cible(self, cible: Element, cible_auto_portee_tir=False):
        self.cible = cible
        if not cible_auto_portee_tir:
            self.new_objectif_cible()

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False):
        self.cible = None
        self.immobile = False
        Personne.new_objectif(self, x_carte, y_carte, i_pos, j_pos, i_objectif, j_objectif,
                              modification_chemin_seulement)

    def get_cases_porter_tir_autour_cible(self):
        liste_cases = []
        liste_ij = []
        if isinstance(self.cible, Batiment):
            liste_ij = self.cible.liste_cases_pleines
        elif isinstance(self.cible, ElementMobile):
            liste_ij = [self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte, self.cible.y_sur_carte)]

        for i_c, j_c in liste_ij:
            for di, dj in self.tireur.get_cases_relative_porter_tir(self.carte.cote_case):
                i, j = i_c + di, j_c + dj
                if not (i, j) in liste_cases:
                    case = self.carte.get_cases_grille(i, j)
                    if not case == TYPE_CASE_INEXISTANTE and not case == TYPE_CASE_PLEINE:
                        liste_cases.append((i, j))

        return liste_cases

    def new_objectif_cible(self):
        self.new_objectif_liste_cases(self.get_cases_porter_tir_autour_cible())

    def tir_si_possible(self):
        if self.cible is not None and \
                self.cible_a_porter_de_tir() \
                and self.tireur.peut_tirer:
            self.cible.recoit_tir(self.tireur.force_tir)
            self.tireur.tir()
            return True
        return False

    def point_a_porter_de_tir(self, x: int, y: int):
        return self.tireur.point_a_porter_de_tir(self.x_float, self.y_float, x, y)

    def cible_a_porter_de_tir(self):
        if isinstance(self.cible, Batiment):
            for i, j in self.cible.liste_cases_pleines:
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                if self.point_a_porter_de_tir(x, y):
                    return True
        elif isinstance(self.cible, ElementMobile):
            if self.point_a_porter_de_tir(self.cible.x_sur_carte, self.cible.y_sur_carte):
                return True
        return False

    def stop(self):
        Personne.stop(self)
        self.immobile = False
        self.cible = None

    def immobilise(self):
        self.stop()
        self.immobile = True

    def update(self):
        Personne.update(self)
        self.tireur.update()
        if self.cible is not None:
            if self.cible_a_porter_de_tir():
                if self.objectif is not None and isinstance(self.cible, Batiment):
                    x_batiment, y_batiment = self.carte.ij_case_to_centre_xy_carte(self.cible.i, self.cible.j)
                    ancienne_orientation = self._orientation
                    self.oriente_vers_point(x_batiment, y_batiment)
                    if abs(ancienne_orientation - self._orientation) < 0.1:
                        self.new_affichage = False
                self.objectif = None
                self.chemin_liste_objectifs = []
                if isinstance(self.cible, ElementMobile):
                    if self.new_affichage:
                        self.oriente_vers_point(self.cible.x_sur_carte, self.cible.y_sur_carte)
                    else:
                        ancienne_orientation = self._orientation
                        self.oriente_vers_point(self.cible.x_sur_carte, self.cible.y_sur_carte)
                        if abs(ancienne_orientation - self._orientation) < 0.0001:
                            self.new_affichage = False
            else:
                if isinstance(self.cible, ElementMobile):
                    if self.immobile:
                        self.cible = None
                    else:
                        if self.objectif is not None:
                            if not self.chemin_liste_objectifs:
                                self.new_objectif_cible()
                            else:
                                i_cible, j_cible = self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte,
                                                                                  self.cible.y_sur_carte)
                                x_obj, y_obj = self.chemin_liste_objectifs[-1]
                                i_obj, j_obj = self.carte.xy_carte_to_ij_case(x_obj, y_obj)
                                if i_cible == i_obj and j_cible == j_obj:
                                    self.chemin_liste_objectifs[-1] = self.cible.x_sur_carte, self.cible.y_sur_carte
                                else:
                                    self.new_objectif_cible()
                        else:
                            self.new_objectif_cible()
                elif isinstance(self.cible, Batiment):
                    self.new_objectif_cible()
