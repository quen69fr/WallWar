# coding: utf-8

from element_mobile_tireur import *
from personne import *


class Soldat(Personne, ElementMobileTireur):
    def __init__(self, type_pers, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0, alea=0):
        ElementMobileTireur.__init__(self, type_pers, carte, x_sur_carte, y_sur_carte, Tireur(type_pers),
                                     True, objectif, orientation, alea)
        Personne.__init__(self, type_pers, carte, x_sur_carte, y_sur_carte, objectif, orientation, alea)

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False, alea=0):
        self.immobile = False
        self.annule_cible()
        self.niveau_d_intelligence_actuel = 0
        Personne.new_objectif(self, x_carte, y_carte, i_pos, j_pos, i_objectif, j_objectif,
                              modification_chemin_seulement, alea=alea)

    def new_cible_obligatoire(self, cible: Element):
        self.cible = cible
        self.niveau_d_intelligence_actuel = 0

    def stop(self):
        Personne.stop(self)
        self.immobile = False
        self.niveau_d_intelligence_actuel = self.niveau_d_intelligence
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

    def update_tireur(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.objectif is None and self.cible is None:
            self.niveau_d_intelligence_actuel = self.niveau_d_intelligence
        ElementMobileTireur.update_tireur(self, liste_adversaires_mobiles, liste_adversaires_statiques)

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
