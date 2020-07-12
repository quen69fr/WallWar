# coding: utf-8

from element import *


class Source:
    def __init__(self, type_source, liste_cases_sources: list, nb_ressources: int):
        nb_cases = len(liste_cases_sources)
        if nb_cases > nb_ressources:
            return
        self.type = type_source
        self.nom = DIC_SOURCES[PARAM_SOURCE_NOM][self.type]
        self.description = DIC_SOURCES[PARAM_SOURCE_DESCRIPTION][self.type]
        self.liste_cases_sources = liste_cases_sources
        self.ressource_comptenu = nb_ressources
        self.ressource_comptenu_par_case = [1 for _ in range(nb_cases)]
        self.type_ressource = DIC_SOURCES[PARAM_SOURCE_TYPE_RESSOURCE][self.type]
        for _ in range(nb_ressources - nb_cases):
            self.ressource_comptenu_par_case[random.randint(0, nb_cases - 1)] += 1
        self.couleur_ressource = DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][self.type_ressource]

        self.resent_deleted_cases = []

    def case_dans_source(self, i, j):
        if (i, j) in self.liste_cases_sources:
            return True
        return False

    def get_ressource_case(self, i, j):
        return self.ressource_comptenu_par_case[self.liste_cases_sources.index((i, j))]

    def remove_ressource(self, nb, i, j):
        index = self.liste_cases_sources.index((i, j))
        self.ressource_comptenu_par_case[index] -= nb
        if self.ressource_comptenu_par_case[index] < 0:
            self.ressource_comptenu_par_case[index] += nb
            return False
        if self.ressource_comptenu_par_case[index] == 0:
            del self.ressource_comptenu_par_case[index]
            del self.liste_cases_sources[index]
            self.resent_deleted_cases.append((i, j))
        self.ressource_comptenu -= nb
        return True

    def clic(self, i_clic: int, j_clic: int):
        if (i_clic, j_clic) in self.liste_cases_sources:
            return True
        return False

    def affiche(self, screen: pygame.Surface, carte: Carte):
        for i, j in self.liste_cases_sources:
            x, y = carte.ij_case_to_coin_xy_relatif(i, j)
            draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom), self.couleur_ressource)

    def affiche_selectionne(self, screen: pygame.Surface, carte: Carte):
        for n, (i, j) in enumerate(self.liste_cases_sources):
            x, y = carte.ij_case_to_coin_xy_relatif(i, j)
            x_c, y_c = carte.ij_case_to_centre_xy_relatif(i, j)
            draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                             DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_SELECTIONNEE])
            affiche_texte(str(self.ressource_comptenu_par_case[n]), x_c, y_c, screen,
                          x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1,
                          taille=int(TAILLE_TEXTE_NB_RESSOURCES_RESTANTES * carte.coef_zoom),
                          couleur=COULEUR_TEXTE_NB_RESSOURCES_RESTANTES)
