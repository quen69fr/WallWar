# coding: utf-8

from personne import *
from tireur import *


class Soldat(Personne):
    def __init__(self, type_pers, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0, alea=0):
        self.cible: ElementMobile or Batiment or None = None
        self.tireur = Tireur(type_pers)
        self.ij_cible = 0, 0
        self.immobile = False
        Personne.__init__(self, type_pers, carte, x_sur_carte, y_sur_carte, objectif, orientation, alea)

    def update_chemin_et_position(self):
        if self.cible is not None:
            self.new_objectif_cible()
        else:
            Personne.update_chemin_et_position(self)

    def new_cible(self, cible: Element, cible_auto_portee_tir=False):
        self.cible = cible
        if not cible_auto_portee_tir:
            self.new_objectif_cible()

    def annule_cible(self):
        self.cible = None
        self.objectif = None
        self.chemin_liste_objectifs = []

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False, alea=0):
        self.cible = None
        self.immobile = False
        Personne.new_objectif(self, x_carte, y_carte, i_pos, j_pos, i_objectif, j_objectif,
                              modification_chemin_seulement, alea=alea)

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
        if isinstance(self.cible, Batiment):
            self.ij_cible = self.cible.i, self.cible.j
        elif isinstance(self.cible, ElementMobile):
            self.ij_cible = self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte, self.cible.y_sur_carte)

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

    def new_choc(self, nb_chocs_max=NB_CHOC_AVANT_ABANDON_OBJECTIF):
        if self.cible is not None:
            nb_chocs_max = int(nb_chocs_max * COEF_NB_CHOC_AVANT_ABANDON_OBJECTIF_CIBLE_SOLDAT)
        if Personne.new_choc(self, nb_chocs_max):
            self.cible = None
            return True
        return False

    def update(self):
        Personne.update(self)
        self.tireur.update()
        if self.cible is not None:
            if self.cible_a_porter_de_tir():
                if self.objectif is not None and isinstance(self.cible, Batiment):
                    x_batiment, y_batiment = self.carte.ij_case_to_centre_xy_carte(self.cible.i, self.cible.j)
                    ancienne_orientation = self._orientation
                    ancien_affichage = self.new_affichage
                    self.oriente_vers_point(x_batiment, y_batiment)
                    if not ancien_affichage and abs(ancienne_orientation - self._orientation) < 0.001:
                        self.new_affichage = False
                self.objectif = None
                self.chemin_liste_objectifs = []
                if isinstance(self.cible, ElementMobile):
                    if self.new_affichage:
                        self.oriente_vers_point(self.cible.x_sur_carte, self.cible.y_sur_carte)
                    else:
                        ancienne_orientation = self._orientation
                        ancien_affichage = self.new_affichage
                        self.oriente_vers_point(self.cible.x_sur_carte, self.cible.y_sur_carte)
                        if not ancien_affichage and abs(ancienne_orientation - self._orientation) < 0.0001:
                            self.new_affichage = False
            else:
                if isinstance(self.cible, ElementMobile):
                    if self.immobile:
                        self.cible = None
                    else:
                        if self.objectif is not None:
                            i_cible, j_cible = self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte,
                                                                              self.cible.y_sur_carte)
                            if not (i_cible == self.ij_cible[0] and j_cible == self.ij_cible[1]):
                                self.new_objectif_cible()
                        else:
                            self.new_objectif_cible()
                elif isinstance(self.cible, Batiment):
                    if self.objectif is None:
                        self.new_objectif_cible()

    def affiche_tireur(self, screen: pygame.Surface):
        self.tireur.affiche(screen, self.carte, self.x_sur_carte, self.y_sur_carte)

    def affiche_objectif(self, screen: pygame.Surface):
        if self.cible is not None:
            x_cible, y_cible = 0, 0
            if isinstance(self.cible, Batiment):
                x_cible, y_cible = self.carte.ij_case_to_centre_xy_relatif(self.cible.i, self.cible.j)
            elif isinstance(self.cible, ElementMobile):
                x_cible, y_cible = self.carte.xy_carte_to_xy_relatif(self.cible.x_sur_carte, self.cible.y_sur_carte)

            x_pos, y_pos = self.carte.xy_carte_to_xy_relatif(self.x_sur_carte, self.y_sur_carte)
            pygame.gfxdraw.line(screen, x_pos, y_pos, x_cible, y_cible, COULEUR_ELEMENT_SELECTION)
            pygame.draw.circle(screen, COULEUR_ELEMENT_SELECTION, (x_cible, y_cible), 2)
        else:
            Personne.affiche_objectif(self, screen)
