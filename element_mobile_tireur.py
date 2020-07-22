# coding: utf-8

from batiment import *
from element_mobile import *
from tireur import *


class ElementMobileTireur(ElementMobile):
    def __init__(self, type_pers, carte: Carte, x_sur_carte: int, y_sur_carte: int, tireur: Tireur,
                 objectif: (int, int) = None, orientation=0, alea=0):
        self.cible: ElementMobile or Batiment or None = None
        self.tireur = tireur
        self.ij_cible = 0, 0
        self.immobile = False
        ElementMobile.__init__(self, type_pers, carte, x_sur_carte, y_sur_carte, objectif, orientation, alea)
        self.niveau_d_intelligence_actuel = self.niveau_d_intelligence

    def update_chemin_et_position(self):
        if self.cible is not None:
            self.new_objectif_cible()
        else:
            ElementMobile.update_chemin_et_position(self)

    def annule_cible(self):
        self.cible = None
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
        
    def find_tireur_sur_self(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        liste_tireur_sur_self = []
        for element_mobile in liste_adversaires_mobiles:
            if isinstance(element_mobile, ElementMobileTireur) and element_mobile.cible == self:
                liste_tireur_sur_self.append(element_mobile)
        for batiment in liste_adversaires_statiques:
            if batiment.peut_tirer and batiment.tireur.cible == self:
                liste_tireur_sur_self.append(batiment)
        return liste_tireur_sur_self

    def update_cible_niv_1(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.cible is not None and (not self.cible_a_porter_de_distance_max(self.cible) or
                                       (self.immobile and (self.cible is None or
                                                           not self.cible_a_porter_de_tir(self.cible)))):
            self.cible = None
        if self.cible is None:
            liste_cibles_potentielles = liste_adversaires_mobiles + liste_adversaires_statiques
            random.shuffle(liste_cibles_potentielles)
            for cible in liste_cibles_potentielles:
                if self.cible_a_porter_de_tir(cible):
                    self.cible = cible
                    break

    def update_cible_niv_2(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.immobile:
            self.update_cible_niv_1(liste_adversaires_mobiles, liste_adversaires_statiques)
        else:
            if self.cible is None:
                liste_cibles_potentielles = liste_adversaires_mobiles + liste_adversaires_statiques
                random.shuffle(liste_cibles_potentielles)
                for cible in liste_cibles_potentielles:
                    if self.cible_visible(cible):
                        self.cible = cible
                        break

    def update_cible_niv_3(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.cible is not None and (not self.cible_a_porter_de_distance_max(self.cible) or
                                       (self.immobile and (self.cible is None or
                                                           not self.cible_a_porter_de_tir(self.cible)))):
            self.cible = None
        if self.cible is None:
            liste_tireur_sur_self = self.find_tireur_sur_self(liste_adversaires_mobiles, liste_adversaires_statiques)
            if self.immobile:
                liste = liste_tireur_sur_self[:]
                for adv in liste:
                    if not self.cible_a_porter_de_tir(adv):
                        liste_tireur_sur_self.remove(adv)
            if len(liste_tireur_sur_self) == 0:
                self.update_cible_niv_2(liste_adversaires_mobiles, liste_adversaires_statiques)
            elif len(liste_tireur_sur_self) == 1:
                self.cible = liste_tireur_sur_self[0]
            else:
                self.cible = random.choice(liste_tireur_sur_self)
        else:
            if not (isinstance(self.cible, ElementMobileTireur) and self.cible.cible == self) and not \
                    (isinstance(self.cible, Batiment) and self.cible.peut_tirer and self.cible.tireur.cible == self):
                liste_tireur_sur_self = self.find_tireur_sur_self(liste_adversaires_mobiles,
                                                                  liste_adversaires_statiques)
                if self.immobile:
                    liste = liste_tireur_sur_self[:]
                    for adv in liste:
                        if not self.cible_a_porter_de_tir(adv):
                            liste_tireur_sur_self.remove(adv)
                if len(liste_tireur_sur_self) > 0:
                    if len(liste_tireur_sur_self) == 1:
                        self.cible = liste_tireur_sur_self[0]
                    else:
                        self.cible = random.choice(liste_tireur_sur_self)

    def update_cible_niv_4(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.immobile and (self.cible is None or not self.cible_a_porter_de_tir(self.cible)):
            self.cible = None
        if not (isinstance(self.cible, ElementMobileTireur) and self.cible.cible == self) and not \
                (isinstance(self.cible, Batiment) and self.cible.peut_tirer and self.cible.tireur.cible == self):
            liste_tireur_sur_self = self.find_tireur_sur_self(liste_adversaires_mobiles, liste_adversaires_statiques)
            if self.immobile:
                liste = liste_tireur_sur_self[:]
                for adv in liste:
                    if not self.cible_a_porter_de_tir(adv):
                        liste_tireur_sur_self.remove(adv)
            if len(liste_tireur_sur_self) > 0:
                if len(liste_tireur_sur_self) > 1:
                    random.shuffle(liste_tireur_sur_self)
                    if self.cible is not None and self.cible in liste_tireur_sur_self:
                        liste_tireur_sur_self.remove(self.cible)
                        liste_tireur_sur_self.insert(0, self.cible)
                    liste_tireur_sur_self.sort(key=lambda element: (isinstance(element, ElementMobileTireur)
                                                                    if isinstance(element, ElementMobile)
                                                                    else element.peut_tirer), reverse=True)
                self.cible = liste_tireur_sur_self[0]
            else:
                if not isinstance(self.cible, ElementMobileTireur) and not (isinstance(self.cible, Batiment)
                                                                            and self.cible.peut_tirer):
                    liste_cibles_potentielles = liste_adversaires_mobiles + liste_adversaires_statiques
                    random.shuffle(liste_cibles_potentielles)
                    liste_cibles_potentielles.sort(key=lambda element: (isinstance(element, ElementMobileTireur)
                                                                        if isinstance(element, ElementMobile)
                                                                        else element.peut_tirer), reverse=True)
                    if self.immobile:
                        self.cible = None
                        for cible in liste_cibles_potentielles:
                            if self.cible_a_porter_de_tir(cible):
                                self.cible = cible
                                break
                    else:
                        changement = False
                        for cible in liste_cibles_potentielles:
                            if self.cible_visible(cible):
                                self.cible = cible
                                changement = True
                                break
                        if not changement and not self.cible_a_porter_de_distance_max(self.cible):
                            self.cible = None

    def update_cible_niv_5(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        liste_tireur_sur_self = self.find_tireur_sur_self(liste_adversaires_mobiles, liste_adversaires_statiques)
        if len(liste_tireur_sur_self) > 0:
            if len(liste_tireur_sur_self) > 1:
                liste_tireur_sur_self.sort(key=lambda element: element.nb_vies)
                liste_tireur_sur_self.sort(key=lambda element: (isinstance(element, ElementMobileTireur)
                                                                if isinstance(element, ElementMobile)
                                                                else element.peut_tirer), reverse=True)
            self.cible = liste_tireur_sur_self[0]
        else:
            liste_cibles_potentielles = liste_adversaires_mobiles + liste_adversaires_statiques
            liste_cibles_potentielles.sort(key=lambda element: element.nb_vies)
            liste_cibles_potentielles.sort(key=lambda element: (isinstance(element, ElementMobileTireur)
                                                                if isinstance(element, ElementMobile)
                                                                else element.peut_tirer), reverse=True)
            if self.immobile:
                self.cible = None
                for cible in liste_cibles_potentielles:
                    if self.cible_a_porter_de_tir(cible):
                        self.cible = cible
                        break
            else:
                changement = False
                for cible in liste_cibles_potentielles:
                    if self.cible_visible(cible):
                        self.cible = cible
                        changement = True
                        break
                if not changement and not self.cible_a_porter_de_distance_max(self.cible):
                    self.cible = None

    def update_cible_niv_6(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        liste_adversaires_potentiels = []
        for adversaire in liste_adversaires_mobiles + liste_adversaires_statiques:
            if self.immobile:
                dist = self.cible_a_porter_de_tir(adversaire)
                if dist:
                    dist = 0
            else:
                dist = self.cible_a_porter_de_distance_max(adversaire)
            if dist:
                rate = 0
                dist_relative = max(0, dist - self.tireur.portee_tir)
                if isinstance(adversaire, ElementMobile):
                    if isinstance(adversaire, ElementMobileTireur):
                        rate = rate_adversaire_niv_intelligence_max(dist_relative, adversaire.nb_vies,
                                                                    (adversaire.tireur.force_tir /
                                                                     adversaire.tireur.delay_tir),
                                                                    True, adversaire.cible == self)
                    else:
                        rate = rate_adversaire_niv_intelligence_max(dist_relative, adversaire.nb_vies, 0, False, False)
                if isinstance(adversaire, Batiment):
                    if adversaire.peut_tirer:
                        rate = rate_adversaire_niv_intelligence_max(dist_relative, adversaire.nb_vies,
                                                                    (adversaire.tireur.force_tir /
                                                                     adversaire.tireur.delay_tir),
                                                                    True, adversaire.tireur.cible == self)
                    else:
                        rate = rate_adversaire_niv_intelligence_max(dist_relative, adversaire.nb_vies, 0, False, False)
                liste_adversaires_potentiels.append((adversaire, rate))
        if len(liste_adversaires_potentiels) > 0:
            self.cible = min(liste_adversaires_potentiels, key=lambda adv: adv[1])[0]
        else:
            self.cible = None

    def update_cible(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        if self.niveau_d_intelligence_actuel == 0:
            pass
        elif self.niveau_d_intelligence_actuel == 1:
            self.update_cible_niv_1(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 2:
            self.update_cible_niv_2(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 3:
            self.update_cible_niv_3(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 4:
            self.update_cible_niv_4(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 5:
            self.update_cible_niv_5(liste_adversaires_mobiles, liste_adversaires_statiques)
        elif self.niveau_d_intelligence_actuel == 6:
            self.update_cible_niv_6(liste_adversaires_mobiles, liste_adversaires_statiques)

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

    def update_tireur(self, liste_adversaires_mobiles: list, liste_adversaires_statiques: list):
        self.tireur.update()
        self.update_cible(liste_adversaires_mobiles, liste_adversaires_statiques)
        if self.cible is not None:
            self.gere_cible()
        ElementMobile.update(self)

    @property
    def niveau_d_intelligence(self):
        return Element.dic_elements[PARAM_A_TIREUR_INTELLIGENCE][self.type]
