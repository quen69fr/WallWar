# coding: utf-8

from batiment import *
from element_mobile import *
from tireur_ennemi import *
from tireur import *


def cible_peut_tirer(cible: Element):
    if isinstance(cible, Batiment) and cible.peut_tirer or isinstance(cible, ElementMobileTireur):
        return True
    return False


def find_adversaires_tireurs(liste_adversaires: list):
    liste_adversaires_tireurs = []
    for adversaire in liste_adversaires:
        if cible_peut_tirer(adversaire):
            liste_adversaires_tireurs.append(adversaire)
    return liste_adversaires_tireurs


class ElementMobileTireur(ElementMobile):
    def __init__(self, type_pers, carte: Carte, x_sur_carte: int, y_sur_carte: int, tireur: Tireur or TireurEnnemi,
                 choix_mouvement: bool, objectif: (int, int) = None, orientation=0, alea=0):
        self.cible: ElementMobile or Batiment or None = None
        self.tireur = tireur
        self.ij_cible = 0, 0
        self.immobile = False
        ElementMobile.__init__(self, type_pers, carte, x_sur_carte, y_sur_carte, choix_mouvement,
                               objectif, orientation, alea)
        self.niveau_d_intelligence_actuel = self.niveau_d_intelligence

    def update_chemin_et_position(self):
        if self.cible is not None:
            self.new_objectif_cible()
        else:
            ElementMobile.update_chemin_et_position(self)

    def annule_cible(self):
        self.cible = None
        self.ij_cible = 0, 0
        self.niveau_d_intelligence_actuel = self.niveau_d_intelligence
        self.objectif = None
        self.chemin_liste_objectifs = []

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
        if isinstance(self.cible, ElementMobile):
            self.new_objectif_liste_cases([self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte,
                                                                          self.cible.y_sur_carte)])
        else:
            self.new_objectif_liste_cases(self.get_cases_porter_tir_autour_cible())
        self.set_ij_cible()

    def set_ij_cible(self):
        if isinstance(self.cible, Batiment):
            self.ij_cible = self.cible.i, self.cible.j
        elif isinstance(self.cible, ElementMobile):
            self.ij_cible = self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte, self.cible.y_sur_carte)

    def tir_si_possible(self):
        if self.cible is not None and \
                self.cible_a_porter_de_tir(self.cible) \
                and self.tireur.peut_tirer:
            self.cible.recoit_tir(self.tireur.force_tir)
            self.tireur.tir()
            return True
        return False

    def point_a_porter_de_tir(self, x: int, y: int):
        return self.tireur.point_a_porter_de_tir(self.x_float, self.y_float, x, y)

    def cible_a_porter_de_tir(self, cible):
        if isinstance(cible, Batiment):
            for i, j in cible.liste_cases_pleines:
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                if self.point_a_porter_de_tir(x, y):
                    return True
        elif isinstance(cible, ElementMobile):
            if self.point_a_porter_de_tir(cible.x_sur_carte, cible.y_sur_carte):
                return True
        return False

    def cible_a_porter_de_tir_avec_distance(self, cible):
        if isinstance(cible, Batiment):
            for i, j in cible.liste_cases_pleines:
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                dist = self.tireur.point_a_porter_de_tir(self.x_float, self.y_float, x, y, True)
                if dist:
                    return dist
        elif isinstance(cible, ElementMobile):
            return self.tireur.point_a_porter_de_tir(self.x_float, self.y_float, cible.x_sur_carte, cible.y_sur_carte,
                                                     True)
        return False
    
    def point_visible(self, x: int, y: int):
        return self.tireur.point_visible(self.x_float, self.y_float, x, y)
    
    def cible_visible(self, cible):
        if isinstance(cible, Batiment):
            for i, j in cible.liste_cases_pleines:
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                if self.point_visible(x, y):
                    return True
        elif isinstance(cible, ElementMobile):
            if self.point_visible(cible.x_sur_carte, cible.y_sur_carte):
                return True
        return False

    def cible_visible_avec_distance(self, cible):
        if isinstance(cible, Batiment):
            for i, j in cible.liste_cases_pleines:
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                dist = self.tireur.point_visible(self.x_float, self.y_float, x, y, True)
                if dist:
                    return dist
        elif isinstance(cible, ElementMobile):
            return self.tireur.point_visible(self.x_float, self.y_float, cible.x_sur_carte, cible.y_sur_carte, True)
        return False

    def point_a_porter_de_distance(self, x: int, y: int, distance: int, return_distance=True):
        return point_a_porter_de_distance(self.x_float, self.y_float, x, y, distance, return_distance)

    def cible_a_porter_de_distance_max(self, cible):
        if isinstance(cible, Batiment):
            for i, j in cible.liste_cases_pleines:
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                dist = self.point_a_porter_de_distance(x, y,
                                                       self.tireur.portee_tir + DISTANCE_MAX_ADVERSAIRE_AU_DELA_VISION)
                if dist:
                    return dist
        elif isinstance(cible, ElementMobile):
            dist = self.point_a_porter_de_distance(cible.x_sur_carte, cible.y_sur_carte,
                                                   self.tireur.portee_tir + DISTANCE_MAX_ADVERSAIRE_AU_DELA_VISION)
            if dist:
                return dist
        return False

    def oriente_vers_cible_si_necessaire(self):
        if isinstance(self.cible, Batiment):
            x_batiment, y_batiment = self.carte.ij_case_to_centre_xy_carte(self.cible.i, self.cible.j)
            self.oriente_vers_point_si_necessaire(x_batiment, y_batiment)
        if isinstance(self.cible, ElementMobile):
            self.oriente_vers_point_si_necessaire(self.cible.x_sur_carte, self.cible.y_sur_carte)

    def affiche_tireur(self, screen: pygame.Surface):
        self.tireur.affiche(screen, self.carte, self.x_sur_carte, self.y_sur_carte)

    def cible_tir_sur_self(self, cible: Element):
        if isinstance(cible, ElementMobileTireur):
            if cible.cible_visible_ext and cible.cible == self and cible.cible_a_porter_de_tir(self) \
                    and self.cible_a_porter_de_distance_max(cible):
                return True
        elif isinstance(cible, Batiment) and cible.peut_tirer:
            if cible.tireur.cible_visible_ext and cible.tireur.cible == self and \
                    cible.tireur.point_a_porter_de_tir(cible.tireur.x, cible.tireur.y,
                                                       self.x_sur_carte, self.y_sur_carte) \
                    and self.cible_a_porter_de_distance_max(cible):
                return True
        return False
        
    def find_tireur_sur_self(self, liste_adversaires: list):
        liste_tireur_sur_self = []
        for adversaires in liste_adversaires:
            if self.cible_tir_sur_self(adversaires):
                liste_tireur_sur_self.append(adversaires)
        return liste_tireur_sur_self

    def find_adversaires_a_portee_de_tir(self, liste_adversaires: list, liste_adversaires_non: list = None):
        if liste_adversaires_non is None:
            liste_adversaires_non = []
        liste_adversaires_a_portee_de_tir = []
        for adversaire in liste_adversaires:
            if adversaire not in liste_adversaires_non and self.cible_a_porter_de_tir(adversaire):
                liste_adversaires_a_portee_de_tir.append(adversaire)
        return liste_adversaires_a_portee_de_tir

    def find_adversaires_visibles(self, liste_adversaires: list, liste_adversaires_non_visibles: list = None):
        if liste_adversaires_non_visibles is None:
            liste_adversaires_non_visibles = []
        liste_adversaires_visibles = []
        for adversaire in liste_adversaires:
            if adversaire not in liste_adversaires_non_visibles and self.cible_visible(adversaire):
                liste_adversaires_visibles.append(adversaire)
        return liste_adversaires_visibles

    def choix_liste_cibles(self, liste_cibles: list):
        if len(liste_cibles) > 0:
            if self.niveau_d_intelligence_actuel <= 3:
                return random.choice(liste_cibles)
            elif self.niveau_d_intelligence_actuel == 4:
                random.shuffle(liste_cibles)
                for cible in liste_cibles:
                    if cible_peut_tirer(cible):
                        return cible
                return liste_cibles[0]
            else:
                liste_cibles_tireuses = find_adversaires_tireurs(liste_cibles)
                if len(liste_cibles_tireuses) > 0:
                    return min(liste_cibles, key=lambda cib: cib.nb_vies)
                else:
                    return min(liste_cibles, key=lambda cib: cib.nb_vies)
        return None

    def choix_cible_a_portee_de_tir(self, liste_cibles, liste_cibles_non: list = None):
        if len(liste_cibles) > 0:
            if liste_cibles_non is None:
                liste_cibles_non = []
            if self.niveau_d_intelligence_actuel <= 3:
                random.shuffle(liste_cibles)
                for cible in liste_cibles:
                    if cible not in liste_cibles_non and self.cible_a_porter_de_tir(cible):
                        return cible
            else:
                return self.choix_liste_cibles(self.find_adversaires_a_portee_de_tir(liste_cibles, liste_cibles_non))
        return None

    def choix_cible_visibles(self, liste_cibles, liste_cibles_non: list = None):
        if len(liste_cibles) > 0:
            if liste_cibles_non is None:
                liste_cibles_non = []
            if self.niveau_d_intelligence_actuel <= 3:
                random.shuffle(liste_cibles)
                for cible in liste_cibles:
                    if cible not in liste_cibles_non and self.cible_visible(cible):
                        return cible
            else:
                return self.choix_liste_cibles(self.find_adversaires_visibles(liste_cibles, liste_cibles_non))
        return None

    def trouve_cible_niv_0(self):
        if self.immobile and self.cible is not None and not self.cible_a_porter_de_tir(self.cible):
            return None

        return self.cible

    def trouve_cible_niv_1(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.cible is not None and self.cible_a_porter_de_tir(self.cible):
            return self.cible

        cible = self.choix_cible_a_portee_de_tir(liste_adversaires_mobiles + liste_adversaires_statiques, [self.cible])
        if cible is not None:
            return cible

        return self.trouve_cible_niv_0()

    def trouve_cible_niv_2(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.immobile:
            return self.trouve_cible_niv_1(liste_adversaires_mobiles, liste_adversaires_statiques)

        if self.cible is not None and self.cible_a_porter_de_tir(self.cible):
            return self.cible

        cible = self.choix_cible_a_portee_de_tir(liste_adversaires_mobiles + liste_adversaires_statiques, [self.cible])
        if cible is not None:
            return cible

        if self.cible is not None and self.cible_visible(self.cible):
            return self.cible

        cible = self.choix_cible_visibles(liste_adversaires_mobiles + liste_adversaires_statiques, [self.cible])
        if cible is not None:
            return cible

        return self.cible

    def trouve_cible_niv_3_4_5(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.cible is not None and self.cible_tir_sur_self(self.cible) and self.cible_a_porter_de_tir(self.cible):
            return self.cible

        liste_tir_sur_self = self.find_tireur_sur_self(liste_adversaires_mobiles + liste_adversaires_statiques)

        cible = self.choix_cible_a_portee_de_tir(liste_tir_sur_self, [self.cible])
        if cible is not None:
            return cible

        if self.immobile:
            return self.trouve_cible_niv_1(liste_adversaires_mobiles, liste_adversaires_statiques)

        if self.cible is not None and self.cible_tir_sur_self(self.cible):
            return self.cible

        # Pas vraiment nécessaire :
        # cible = self.choix_cible_visibles(liste_tir_sur_self, [self.cible])
        # if cible is not None:
        #     return cible

        cible = self.choix_liste_cibles(liste_tir_sur_self)
        if cible is not None:
            return cible

        return self.trouve_cible_niv_2(liste_adversaires_mobiles, liste_adversaires_statiques)

    def rate_cible_niv_6(self, cible: Element, dist_2):
        if isinstance(cible, ElementMobile):
            if isinstance(cible, ElementMobileTireur):
                return rate_adversaire_niv_intelligence_max(dist_2, cible.nb_vies,
                                                            cible.tireur.force_tir / cible.tireur.delay_tir, True,
                                                            (cible.cible is not None and
                                                             cible.cible_a_porter_de_tir(cible.cible)),
                                                            self.tireur.force_tir)
            else:
                return rate_adversaire_niv_intelligence_max(dist_2, cible.nb_vies, 0, False, False,
                                                            self.tireur.force_tir)
        if isinstance(cible, Batiment):
            if cible.peut_tirer:
                return rate_adversaire_niv_intelligence_max(dist_2, cible.nb_vies,
                                                            (cible.tireur.force_tir / cible.tireur.delay_tir), True,
                                                            cible.tireur.cible is not None, self.tireur.force_tir)
            else:
                return rate_adversaire_niv_intelligence_max(dist_2, cible.nb_vies, 0, False, False,
                                                            self.tireur.force_tir)

        return RATE_MIN

    def liste_cibles_visibles_niv_6(self, liste_adversaires: list, liste_non: list):
        liste_cibles_visibles_dist_2 = []
        for cible in liste_adversaires:
            if cible not in liste_non:
                if self.cible_tir_sur_self(cible):
                    dist = self.cible_a_porter_de_distance_max(cible)
                    if dist:
                        liste_cibles_visibles_dist_2.append((cible, dist))
                    continue
                dist = self.cible_visible_avec_distance(cible)
                if dist:
                    liste_cibles_visibles_dist_2.append((cible, dist))
        return liste_cibles_visibles_dist_2

    def trouve_cible_niv_6(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        meilleur_note = RATE_MIN
        meilleur_cible = None
        liste_cibles_a_portee_de_tir = \
            self.find_adversaires_a_portee_de_tir(liste_adversaires_mobiles + liste_adversaires_statiques)
        liste_cibles_visibles_dist_2 = \
            self.liste_cibles_visibles_niv_6(liste_adversaires_mobiles + liste_adversaires_statiques,
                                             liste_cibles_a_portee_de_tir)
        for cible in liste_cibles_a_portee_de_tir:
            note = self.rate_cible_niv_6(cible, 0)
            if note > meilleur_note:
                meilleur_cible = cible
                meilleur_note = note
        for cible, ditance_2 in liste_cibles_visibles_dist_2:
            note = self.rate_cible_niv_6(cible, ditance_2)
            if note > meilleur_note:
                meilleur_cible = cible
                meilleur_note = note
        return meilleur_cible

    def update_cible(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.cible is not None and not isinstance(self.cible, Batiment) and \
                not self.cible_a_porter_de_distance_max(self.cible):
            self.cible = None
        if self.niveau_d_intelligence_actuel == 0:
            self.cible = self.trouve_cible_niv_0()
        elif self.niveau_d_intelligence_actuel == 1:
            self.cible = self.trouve_cible_niv_1(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 2:
            self.cible = self.trouve_cible_niv_2(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 6:
            self.cible = self.trouve_cible_niv_6(liste_adversaires_mobiles, liste_adversaires_statiques)
        else:
            self.cible = self.trouve_cible_niv_3_4_5(liste_adversaires_mobiles, liste_adversaires_statiques)

    def gere_cible(self):
        if self.cible_a_porter_de_tir(self.cible):
            self.oriente_vers_cible_si_necessaire()
            self.objectif = None
            self.chemin_liste_objectifs = []
        else:
            if not self.immobile:
                if self.objectif is None:
                    self.new_objectif_cible()
                else:
                    i_obj, j_obj = self.ij_cible
                    if isinstance(self.cible, Batiment):
                        if not i_obj == self.cible.i or not j_obj == self.cible.j:
                            self.new_objectif_cible()
                    elif isinstance(self.cible, ElementMobile):
                        i_cible, j_cible = self.carte.xy_carte_to_ij_case(self.cible.x_sur_carte,
                                                                          self.cible.y_sur_carte)
                        if i_obj == i_cible and j_obj == j_cible:
                            if len(self.chemin_liste_objectifs) == 0:
                                self.objectif = self.cible.x_sur_carte, self.cible.y_sur_carte
                                self.oriente_vers_point(self.cible.x_sur_carte, self.cible.y_sur_carte)
                            else:
                                self.chemin_liste_objectifs[-1] = self.cible.x_sur_carte, self.cible.y_sur_carte
                        else:
                            self.new_objectif_cible()

    def update_tireur(self):
        self.tireur.update()
        # self.update_cible(liste_adversaires_mobiles, liste_adversaires_statiques)
        if self.cible is None:
            if not self.ij_cible == (0, 0):
                self.annule_cible()
        else:
            self.gere_cible()
        ElementMobile.update(self)

    @property
    def niveau_d_intelligence(self):
        return Element.dic_elements[PARAM_A_TIREUR_INTELLIGENCE][self.type]

    @property
    def cible_visible_ext(self):
        return Element.dic_elements[PARAM_A_TIREUR_CIBLE_VISIBLE][self.type]
