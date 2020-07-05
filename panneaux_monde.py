# coding: utf-8

from panneau_infos import *
from panneau_selection import *
from panneau_constructions import *


class PanneauxMonde:
    def __init__(self, monde):
        self.panneau_infos = PanneauInfos(monde)
        self.panneau_selection = PanneauSelection(monde)
        self.panneau_constructions = PanneauConstructions(monde)

        self.panneau_souris: PanneauClic or None = None

    def souris_sur_panneau(self, x_souris: int, y_souris: int):
        self.panneau_souris = None
        if self.panneau_selection.souris_sur_ecran(x_souris, y_souris):
            self.panneau_souris = self.panneau_selection
            return True
        if self.panneau_constructions.souris_sur_ecran(x_souris, y_souris):
            self.panneau_souris = self.panneau_constructions
            return True
        return False

    def gere_ctrl_clic(self, x_souris: int, y_souris: int):
        if self.panneau_souris == self.panneau_selection:
            self.panneau_souris.gere_ctrl_clic(x_souris, y_souris)
        return None

    def gere_clic(self, x_souris: int, y_souris: int):
        if self.panneau_souris is not None:
            self.panneau_souris.gere_clic(x_souris, y_souris)
        return None

    def update(self):
        self.panneau_infos.update()
        self.panneau_selection.update()
        self.panneau_constructions.update()

    def affiche(self, screen: pygame.Surface):
        self.panneau_infos.affiche(screen)
        self.panneau_selection.affiche(screen)
        self.panneau_constructions.affiche(screen)
