# coding: utf-8

from element import *


class Constructeur:
    def __init__(self, liste_constructions_possibles: int):
        self.liste_constructions_possibles = liste_constructions_possibles
        self.liste_type_elements_en_attente = []
        self.type_element_en_construction = None
        self.avancement_construction = 0
        self.avancement_construction_max = 0
        self.new_affichage = True

    def update(self):
        if self.type_element_en_construction is not None:
            self.avancement_construction += 1
            if self.avancement_construction >= self.avancement_construction_max:
                return self.type_element_en_construction
            self.new_affichage = True
        if self.type_element_en_construction is None and len(self.liste_type_elements_en_attente) > 0:
            self.type_element_en_construction = self.liste_type_elements_en_attente[0]
            del self.liste_type_elements_en_attente[0]
            self.avancement_construction = 0
            self.avancement_construction_max = \
                DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION][self.type_element_en_construction]
            self.new_affichage = True
        return None

    def ajoute_construction(self, type_construction):
        if len(self.liste_type_elements_en_attente) < NB_CONSTRUCTION_EN_ATTENTE_MAX \
                and type_construction in self.liste_constructions_possibles:
            self.liste_type_elements_en_attente.append(type_construction)
            self.new_affichage = True
            return True
        return False

    def annuler_construction(self, n):
        if len(self.liste_type_elements_en_attente) > n:
            del self.liste_type_elements_en_attente[n]
            self.new_affichage = True
            return True
        return False


class Amelioreur:
    def __init__(self, liste_ameliorations_possibles):
        self.liste_ameliorations_possibles = liste_ameliorations_possibles
        self.type_ameliration_en_cours = None
        self.avancement_ameliration = 0
        self.avancement_ameliration_max = 0
        self.new_affichage = True

    def update(self):
        if self.type_ameliration_en_cours is not None:
            self.avancement_ameliration += 1
            self.new_affichage = True
            if self.avancement_ameliration >= self.avancement_ameliration_max:
                type_ameliration = self.type_ameliration_en_cours
                self.type_ameliration_en_cours = None
                return type_ameliration
        return None

    def ajoute_amelioration(self, type_amelioration):
        # if self.type_ameliration_en_cours is None and \
        #         self.type_ameliration_en_cours in self.liste_ameliorations_possibles:
        #     self.type_ameliration_en_cours = type_amelioration
        #     self.avancement_ameliration = 0
        #     self.avancement_ameliration_max = DIC_AMELIORATION_DUREE[type_amelioration]
        #     return True
        # return False
        pass  # TODO


class Batiment(Element):
    argent_comptenu_relay_general = NB_ARGENT_INIT
    liquide_comptenu_general = NB_LIQUIDE_INIT
    nb_personne_max = 0

    def __init__(self, type_batiment, i_centre: int, j_centre: int, carte: Carte, contruit=False):
        Element.__init__(self, type_batiment)
        self.i = i_centre
        self.j = j_centre
        self.liste_cases_pleines_relatives = DIC_ELEMENTS[PARAM_F_BATIMENT_LISTE_CASES][self.type][TYPE_CASE_PLEINE]
        self.liste_cases_relais_relatives = \
            DIC_ELEMENTS[PARAM_F_BATIMENT_LISTE_CASES][self.type][TYPE_CASE_S_RELAIS]
        self.liste_cases_depos_relatives = \
            DIC_ELEMENTS[PARAM_F_BATIMENT_LISTE_CASES][self.type][TYPE_CASE_S_DEPOS]
        self.liste_couleur_cases_pleines = DIC_ELEMENTS[PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES][self.type]
        self.nb_cases = len(self.liste_cases_pleines_relatives + self.liste_cases_relais_relatives
                            + self.liste_cases_depos_relatives)
        self.liste_cases_pleines = []
        self.liste_cases_relais = []
        self.liste_cases_depos = []
        self.liste_cases_interdites_constuction = []
        self.update_position(i_centre, j_centre, carte)

        self.fixe = contruit
        self.prix_liquide = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][self.type]
        self.prix_construction = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][self.type]
        self.argent_comptenu = 0
        self.etape_construction_max = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION][self.type]
        self.etape_construction = self.etape_construction_max if contruit else 0
        self.nb_places = DIC_ELEMENTS[PARAM_A_BATIMENT_NB_PLACES][self.type]

        self.argent_comptenu_max = DIC_ELEMENTS[PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX][self.type]

        self.constructeur = None
        self.point_sortie_constructions = None
        if len(DIC_ELEMENTS[PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES][self.type]) > 0:
            self.constructeur = \
                Constructeur(DIC_ELEMENTS[PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES][self.type])

        self.amelioreur = None
        if len(DIC_ELEMENTS[PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES][self.type]) > 0:
            self.amelioreur = \
                Amelioreur(DIC_ELEMENTS[PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES][self.type])

    def get_value_param(self, param):
        if param == PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION:
            return self.prix_liquide
        elif param == PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION:
            return self.prix_construction
        elif param == PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION:
            return self.etape_construction_max
        elif param == PARAM_A_BATIMENT_NB_PLACES:
            return self.nb_places
        elif param == PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX:
            if self.type == TYPE_BATIMENT_BASE or self.argent_comptenu_max == 0:
                return None
            return self.argent_comptenu_max
        elif param == PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES:
            if self.constructeur is None:
                return None
            return self.constructeur.liste_constructions_possibles
        elif param == PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES:
            if self.amelioreur is None:
                return None
            return self.amelioreur.liste_ameliorations_possibles
        return Element.get_value_param(self, param)

    def set_value_a_param(self, param, val):
        if param == PARAM_A_BATIMENT_NB_PLACES:
            self.nb_places = val
            return True
        elif param == PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX:
            self.argent_comptenu_max = val
            return True
        return Element.set_value_a_param(self, param, val)

    def case_dans_source(self, i, j):
        if (i, j) in self.liste_cases_pleines + self.liste_cases_relais + self.liste_cases_depos:
            return True
        return False

    def add_argent(self, nb, type_ressource):
        if self.etape_construction >= self.etape_construction_max:
            if type_ressource == TYPE_RESSOURCE_LIQUIDE:
                if self.liste_cases_relais:
                    Batiment.liquide_comptenu_general += nb
                    return True
            elif type_ressource == TYPE_RESSOURCE_MINERAI:
                if self.liste_cases_relais:
                    Batiment.argent_comptenu_relay_general += nb
                    return True
            elif type_ressource == TYPE_RESSOURCE_ARGENT:
                if self.argent_comptenu_max >= self.argent_comptenu + nb:
                    if self.liste_cases_relais:
                        Batiment.argent_comptenu_relay_general += nb
                        return True
                    if self.liste_cases_depos:
                        self.argent_comptenu += nb
                        return True
        else:
            if type_ressource == TYPE_RESSOURCE_ARGENT:
                self.argent_comptenu += nb
                return True
        return False

    def remove_argent(self, nb):
        if self.liste_cases_relais and Batiment.argent_comptenu_relay_general >= nb \
                and self.etape_construction >= self.etape_construction_max:
            Batiment.argent_comptenu_relay_general -= nb
            return True
        return False

    def fixer(self, liste_cases_impossibles):
        if not self.fixe:
            if not self.liste_cases_interdites_constuction:
                for case in self.liste_cases_pleines:
                    if case in liste_cases_impossibles:
                        return False
                self.fixe = True
                self.argent_comptenu = - self.prix_construction
                return True
            return False

    def update_position(self, i_centre: int, j_centre: int, carte: Carte):
        if not self.i == i_centre or not self.j == j_centre or (not self.liste_cases_pleines and
                                                                not self.liste_cases_depos and
                                                                not self.liste_cases_relais):
            self.i = i_centre
            self.j = j_centre
            self.liste_cases_pleines = [(i + self.i, j + self.j) for i, j in self.liste_cases_pleines_relatives]
            self.liste_cases_relais = [(i + self.i, j + self.j) for i, j in self.liste_cases_relais_relatives]
            self.liste_cases_depos = [(i + self.i, j + self.j) for i, j in self.liste_cases_depos_relatives]

            self.liste_cases_interdites_constuction = []
            for i, j in self.liste_cases_pleines + self.liste_cases_relais + self.liste_cases_depos:
                if not carte.get_cases_grille(i, j) == TYPE_CASE_VIDE:
                    self.liste_cases_interdites_constuction.append((i, j))

    def update_construction(self):
        if self.argent_comptenu < 0:
            return True
        if self.etape_construction < self.etape_construction_max:
            self.etape_construction += 1
            return True
        if self.liste_cases_relais:
            Batiment.argent_comptenu_relay_general += self.argent_comptenu
            self.argent_comptenu = 0
        Batiment.nb_personne_max += self.nb_places
        return False

    def update_constructeur(self):
        if self.constructeur is not None:
            return self.constructeur.update()
        return None

    def ajoute_construction_constructeur(self, type_personnage):
        prix_argent = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_personnage]
        prix_liquide = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_personnage]
        if self.argent_comptenu >= prix_argent and Batiment.liquide_comptenu_general >= prix_liquide:
            if self.constructeur.ajoute_construction(type_personnage):
                self.argent_comptenu -= prix_argent
                Batiment.liquide_comptenu_general -= prix_liquide
                return True
        return False

    def annule_construction_constructeur(self, n):
        if len(self.constructeur.liste_type_elements_en_attente) > n:
            type_personnage = self.constructeur.liste_type_elements_en_attente[n]
            prix_argent = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_personnage]
            prix_liquide = DIC_ELEMENTS[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_personnage]
            if self.constructeur.annuler_construction(n):
                self.argent_comptenu += prix_argent
                if self.argent_comptenu > self.argent_comptenu_max:
                    self.argent_comptenu = self.argent_comptenu_max
                Batiment.liquide_comptenu_general += prix_liquide
                return True
        return False

    def clic(self, i_clic: int, j_clic: int):
        if (i_clic, j_clic) in self.liste_cases_depos + self.liste_cases_relais + self.liste_cases_pleines:
            return True
        return False

    def set_point_sortie_constructions(self, carte: Carte, x_carte: int, y_carte: int):
        i, j = carte.xy_carte_to_ij_case(x_carte, y_carte)
        if not carte.get_cases_grille(i, j) == TYPE_CASE_PLEINE:
            self.point_sortie_constructions = x_carte, y_carte

    def affiche(self, screen, carte: Carte):
        if self.fixe:
            if self.argent_comptenu >= 0:
                for i, j in self.liste_cases_depos:
                    x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                    draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                     DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_DEPOS])
                for i, j in self.liste_cases_relais:
                    x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                    draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                     DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_RELAIS])

                if self.etape_construction < self.etape_construction_max:
                    alpha = int(self.etape_construction / self.etape_construction_max * 180)
                    for n, (i, j) in enumerate(self.liste_cases_pleines):
                        x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                        draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                         DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_NON_CONSTRUITE])
                        couleur = self.liste_couleur_cases_pleines[n]
                        if not couleur == DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_NON_CONSTRUITE]:
                            draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                             (couleur, alpha))
                else:
                    for n, (i, j) in enumerate(self.liste_cases_pleines):
                        x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                        draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                         self.liste_couleur_cases_pleines[n])
            else:
                for i, j in self.liste_cases_depos:
                    x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                    draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                     DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_DEPOS])
                for i, j in self.liste_cases_relais:
                    x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                    draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                     DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_RELAIS])

                alpha = int((1 + self.argent_comptenu / self.prix_construction) * 255)
                for i, j in self.liste_cases_pleines:
                    x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                    draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                                     (DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_NON_CONSTRUITE], alpha))

        else:
            for i, j in self.liste_cases_depos + self.liste_cases_pleines + self.liste_cases_relais:
                x, y = carte.ij_case_to_coin_xy_relatif(i, j)
                couleur_alpha = DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_POSSIBLE]
                if (i, j) in self.liste_cases_interdites_constuction:
                    couleur_alpha = DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_IMPOSSIBLE]
                draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom), couleur_alpha)

    def affiche_selectionne(self, screen, carte: Carte):
        for i, j in self.liste_cases_depos + self.liste_cases_relais + self.liste_cases_pleines:
            x, y = carte.ij_case_to_coin_xy_relatif(i, j)
            draw_filled_rect(screen, (x, y, carte.cote_case_zoom, carte.cote_case_zoom),
                             DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_SELECTIONNEE])
        if self.point_sortie_constructions is not None:
            x, y = self.point_sortie_constructions
            x, y = carte.xy_carte_to_xy_relatif(x, y)
            draw_filled_circle(screen, (x, y), 3, COULEUR_ELEMENT_SELECTION)
