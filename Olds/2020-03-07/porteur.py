# coding: utf-8

from personne import *


class Porteur(Personne):
    def __init__(self, type_personne, carte: Carte, x_sur_carte: int, y_sur_carte: int, objectif: (int, int) = None,
                 orientation=0):
        self.ressource_comptenu_max = DIC_ELEMENTS[PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX][type_personne]
        self.ressource_comptenu = 0
        self.type_ressource_comptenu = None
        self.objectif_global = None
        self.liste_transaction_a_effectuer = []
        self.peut_recolter = DIC_ELEMENTS[PARAM_A_PORTEUR_PEUT_RECOLTER][type_personne]
        Personne.__init__(self, type_personne, carte, x_sur_carte, y_sur_carte, objectif, orientation)
        self.reel_ecran_original = self.ecran_original.copy()
        self.new_ecran_original = True
        self.dic_nb_ressources_transportees_en_tout = {TYPE_RESSOURCE_ARGENT: 0,
                                                       TYPE_RESSOURCE_MINERAI: 0,
                                                       TYPE_RESSOURCE_LIQUIDE: 0}

    def get_value_param(self, param):
        if param == PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX:
            return self.ressource_comptenu_max
        elif param == PARAM_A_PORTEUR_PEUT_RECOLTER:
            return self.peut_recolter
        return Personne.get_value_param(self, param)

    def set_value_a_param(self, param, val):
        if param == PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX:
            self.ressource_comptenu_max = val
            return True
        elif param == PARAM_A_PORTEUR_PEUT_RECOLTER:
            self.peut_recolter = val
            return True
        return Personne.set_value_a_param(self, param, val)

    def stop(self):
        Personne.stop(self)
        self.objectif_global = None

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False):
        if not modification_chemin_seulement:
            self.objectif_global = None
            i_objectif, j_objectif = self.carte.xy_carte_to_ij_case(x_carte, y_carte)
            case = self.carte.get_cases_grille(i_objectif, j_objectif)
            if case == TYPE_CASE_S_DEPOS:
                self.objectif_global = self.carte.ij_case_to_centre_xy_carte(i_objectif, j_objectif)
            elif case == TYPE_CASE_SOURCE and self.peut_recolter:
                self.objectif_global = self.carte.ij_case_to_centre_xy_carte(i_objectif, j_objectif)
        ElementMobile.new_objectif(self, x_carte, y_carte, i_pos, j_pos, i_objectif, j_objectif)

    def objectif_suivant(self):
        ElementMobile.objectif_suivant(self)
        if self.objectif is None:
            if self.transaction_possible() or self.ressource_comptenu == 0:
                if self.objectif_global is not None:
                    i_pos, j_pos = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)
                    case_pos = self.carte.get_cases_grille(i_pos, j_pos)
                    if case_pos == TYPE_CASE_S_RELAIS or case_pos == TYPE_CASE_VIDE:
                        i_obj, j_obj = self.carte.xy_carte_to_ij_case(self.objectif_global[0], self.objectif_global[1])
                        case_obj = self.carte.get_cases_grille(i_obj, j_obj)
                        if case_obj == TYPE_CASE_S_RELAIS:
                            self.objectif_global = None
                            return
                        if not case_obj == TYPE_CASE_SOURCE and not case_obj == TYPE_CASE_S_DEPOS and \
                                self.peut_recolter:
                            liste_i = [i_obj - 1, i_obj, i_obj + 1]
                            liste_j = [j_obj - 1, j_obj, j_obj + 1]
                            random.shuffle(liste_i)
                            random.shuffle(liste_j)
                            for i in liste_i:
                                for j in liste_j:
                                    case = self.carte.get_cases_grille(i, j)
                                    if case == TYPE_CASE_SOURCE:
                                        self.objectif_global = self.carte.ij_case_to_centre_xy_carte(i, j)
                                        break
                        self.new_objectif(self.objectif_global[0], self.objectif_global[1], i_pos, j_pos, i_obj, j_obj)
                    else:
                        self.new_objectif_point_relay()

    def transaction_possible(self):
        if self.objectif is None:
            i, j = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)
            case = self.carte.get_cases_grille(i, j)
            if case == TYPE_CASE_S_RELAIS:
                if self.ressource_comptenu == 0:
                    self.liste_transaction_a_effectuer.append((i, j, TYPE_TRANSACTION_GET))
                else:
                    self.liste_transaction_a_effectuer.append((i, j, TYPE_TRANSACTION_GIVE))
                return True
            if case == TYPE_CASE_SOURCE:
                if self.peut_recolter and self.ressource_comptenu_max > self.ressource_comptenu:
                    self.liste_transaction_a_effectuer.append((i, j, TYPE_TRANSACTION_GET))
                    return True
                return False
            if case == TYPE_CASE_S_DEPOS:
                if self.ressource_comptenu > 0 and self.type_ressource_comptenu == TYPE_RESSOURCE_ARGENT:
                    self.liste_transaction_a_effectuer.append((i, j, TYPE_TRANSACTION_GIVE))
                    return True
                return False
        return False

    def gere_transaction(self, element: Element, type_transaction):
        if type_transaction == TYPE_TRANSACTION_GET:
            if self.get_argent(element):
                self.new_ecran_original = True
                return True
            return False
        if type_transaction == TYPE_TRANSACTION_GIVE and isinstance(element, Batiment):
            if self.give_argent(element):
                self.new_ecran_original = True
                return True
            return False
        return False

    def give_argent(self, batiment: Batiment):
        if batiment.argent_comptenu >= 0 and (batiment.etape_construction < batiment.etape_construction_max
                                              or batiment.argent_comptenu >= batiment.argent_comptenu_max):
            self.objectif_global = None
            return False
        nb_argent = self.ressource_comptenu
        if batiment.etape_construction < batiment.etape_construction_max and batiment.argent_comptenu < 0 \
                and - batiment.argent_comptenu <= nb_argent:
            nb_argent = - batiment.argent_comptenu
            self.objectif_global = None
        elif batiment.etape_construction >= batiment.etape_construction_max:
            nb_argent_test = batiment.argent_comptenu_max - batiment.argent_comptenu
            if nb_argent_test <= nb_argent:
                nb_argent = nb_argent_test
                self.objectif_global = None
        if batiment.add_argent(nb_argent, self.type_ressource_comptenu):
            self.ressource_comptenu -= nb_argent
            if self.ressource_comptenu == 0:
                self.type_ressource_comptenu = None
            return True
        return False

    def get_argent(self, source_or_batiment: Batiment or Source):
        if isinstance(source_or_batiment, Source):
            if source_or_batiment and (self.ressource_comptenu == 0 or
                                       self.type_ressource_comptenu == source_or_batiment.type_ressource):
                i, j = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)
                ressource_comptenu_case = source_or_batiment.get_ressource_case(i, j)
                n = min(self.ressource_comptenu_max - self.ressource_comptenu, ressource_comptenu_case)
                if source_or_batiment.remove_ressource(n, i, j):
                    self.ressource_comptenu += n
                    self.type_ressource_comptenu = source_or_batiment.type_ressource
                    self.dic_nb_ressources_transportees_en_tout[self.type_ressource_comptenu] += n
                    return True
            return False

        if isinstance(source_or_batiment, Batiment):
            n = min(self.ressource_comptenu_max - self.ressource_comptenu, Batiment.argent_comptenu_relay_general)
            if source_or_batiment.remove_argent(n):
                self.ressource_comptenu += n
                self.type_ressource_comptenu = TYPE_RESSOURCE_ARGENT
                self.dic_nb_ressources_transportees_en_tout[self.type_ressource_comptenu] += n
                return True
            return False

    def update_ecran_original(self):
        self.ecran_original = self.reel_ecran_original.copy()
        if not self.ressource_comptenu == 0:
            x, y = self.ecran_original_size
            x = int(x / 2 + DIC_ELEMENTS[PARAM_F_PORTEUR_DISTANCE_RESSOURCE][self.type])
            y = int(y / 2)
            draw_filled_circle(self.ecran_original, (x, y),
                               DIC_ELEMENTS[PARAM_F_PORTEUR_RAYON_RESSOURCE][self.type],
                               DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][self.type_ressource_comptenu])

    def affiche(self, screen: pygame.Surface):
        if self.new_ecran_original:
            self.update_ecran_original()
            self.new_affichage = True
            self.new_ecran_original = False
        ElementMobile.affiche(self, screen)
