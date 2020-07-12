# coding: utf-8

from porteur import *
from soldat import *
from ennemi import *
from source import *
from batiment import *
from explosion import *


class Monde:
    def __init__(self, nb_cases_x, nb_cases_y, cote_case):
        self.carte = Carte(nb_cases_x, nb_cases_y, cote_case)
        # Batiments
        self.liste_batiments_constuits = []
        self.liste_batiments_en_cours_de_construction = []
        self.batiment_en_construction = None

        self.liste_sources = []
        self.liste_personnes = []
        self.liste_ennemis = []
        self.liste_explosions = []
        self.nb_places_personnes = 0

        self.element_selectionne = None
        self.rect_clic_down_sur_carte = None

        self.init_carte()

        # Affichage
        self.ecran_static = pygame.Surface((self.carte.largeur_ecran, self.carte.hauteur_ecran))
        self.ecran_complet = pygame.Surface((self.carte.largeur_ecran, self.carte.hauteur_ecran))
        self.new_affichage_static = True

    def init_carte(self):
        for pos_batiment, type_batiment in LISTE_BATIMENTS_INIT:
            self.add_batiment_fixe(Batiment(type_batiment, pos_batiment[0], pos_batiment[1], self.carte, contruit=True))

        for pos_source, type_source, nb_ressources in LISTE_SOURCES_INIT:
            self.add_source(Source(type_source, pos_source, nb_ressources))

        for type_personne, x_carte, y_carte in LISTE_PERSONNE_INIT:
            self.cree_personne(type_personne, x_carte, y_carte)

    def get_element_fixe(self, i, j):
        for source in self.liste_sources:
            if source.case_dans_source(i, j):
                return source
        for batiment in self.liste_batiments_constuits + self.liste_batiments_en_cours_de_construction:
            if batiment.case_dans_source(i, j):
                return batiment
        return None

    # -------------------------------------------------
    #                     Personnes
    # -------------------------------------------------
    def cree_personne(self, type_personne, x_carte, y_carte, objectif=None):
        if Element.dic_elements[PARAM_F_PERSONNE_TYPE_CLASS][type_personne] == TYPE_PERSONNE_CLASS_PERSONNE:
            self.add_personne(Personne(type_personne, self.carte, x_carte, y_carte))
            return True
        elif Element.dic_elements[PARAM_F_PERSONNE_TYPE_CLASS][type_personne] == TYPE_PERSONNE_CLASS_PORTEUR:
            self.add_personne(Porteur(type_personne, self.carte, x_carte, y_carte, objectif=objectif))
            return True
        elif Element.dic_elements[PARAM_F_PERSONNE_TYPE_CLASS][type_personne] == TYPE_PERSONNE_CLASS_SOLDAT:
            self.add_personne(Soldat(type_personne, self.carte, x_carte, y_carte, objectif=objectif))
            return True
        return False

    def add_personne(self, personne: Personne):
        self.liste_personnes.append(personne)
        self.nb_places_personnes += personne.nb_places

    def remove_personne(self, personne: Personne):
        self.liste_personnes.remove(personne)
        self.nb_places_personnes -= personne.nb_places
        if type(self.element_selectionne) == list:
            if personne in self.element_selectionne:
                self.element_selectionne.remove(personne)
                if len(self.element_selectionne) == 1:
                    self.element_selectionne = self.element_selectionne[0]
        else:
            if self.element_selectionne == personne:
                self.element_selectionne = None
        if personne.type_explosion is not None:
            self.liste_explosions.append(Explosion(personne.type_explosion, personne.x_float, personne.y_float))
        for pers in self.liste_personnes:
            if isinstance(pers, Soldat):
                if pers.cible == personne:
                    pers.cible = None

    def gere_transaction_a_effectuer(self, porteur: Porteur):
        if len(porteur.liste_transaction_a_effectuer) > 0:
            for i, j, type_transaction in porteur.liste_transaction_a_effectuer:
                element = self.get_element_fixe(i, j)
                if element is not None:
                    porteur.gere_transaction(element, type_transaction)
                porteur.liste_transaction_a_effectuer.remove((i, j, type_transaction))

    def cherche_cible_ennemi_soldat(self, soldat: Soldat):
        for ennemi in self.liste_ennemis:
            if soldat.point_a_porter_de_tir(ennemi.x_float, ennemi.y_float):
                soldat.new_cible(ennemi, True)

    def update_personnes(self):
        for personne in self.liste_personnes:
            personne.update()
        for personne in self.liste_personnes:
            if isinstance(personne, Porteur):
                self.gere_transaction_a_effectuer(personne)
            elif isinstance(personne, Soldat):
                if personne.cible is None and personne.objectif is None:
                    self.cherche_cible_ennemi_soldat(personne)
                else:
                    if personne.tir_si_possible():
                        self.cree_explosion_tir(personne)
                        if personne.cible.nb_vies <= 0:
                            if isinstance(personne.cible, Personne):
                                self.remove_personne(personne.cible)
                            elif isinstance(personne.cible, Ennemi):
                                pass  # TODO
                            elif isinstance(personne.cible, Batiment):
                                self.remove_batiement_constuit(personne.cible)
                            personne.tireur.nb_destructions += 1
        self.gere_chevauchements_personnes()

    def update_chemin_personnes(self):
        for personne in self.liste_personnes:
            personne.update_chemin_et_position()

    def get_all_cases_elements_mobiles(self):
        return [self.carte.xy_carte_to_ij_case(element_mobile.x_sur_carte, element_mobile.y_sur_carte)
                for element_mobile in self.liste_personnes + self.liste_ennemis]

    def gere_new_objectif_cible_soldat(self, soldat: Soldat, x_carte_clic: int, y_carte_clic: int):
        for ennemi in self.liste_ennemis:
            if ennemi.clic(x_carte_clic, y_carte_clic):
                soldat.new_cible(ennemi)
                return
        for batiment in self.liste_batiments_constuits:
            i_clic, j_clic = self.carte.xy_carte_to_ij_case(x_carte_clic, y_carte_clic)
            if batiment.clic(i_clic, j_clic):
                soldat.new_cible(batiment, pos_cible_fixe=(x_carte_clic, y_carte_clic))
                return
        for personne in self.liste_personnes:
            if not personne == soldat and personne.clic(x_carte_clic, y_carte_clic):
                soldat.new_cible(personne)
                return
        soldat.new_objectif(x_carte_clic, y_carte_clic)

    def gere_chevauchements_personnes(self):
        for i, personne1 in enumerate(self.liste_personnes):
            for personne2 in self.liste_personnes[i + 1:]:
                # if personne1.objectif is None or personne2.objectif is None:
                d_max = (personne1.rayon + personne2.rayon) * COEF_RAYONS_PERSONNES_CHEVAUCHEMENT
                dx = personne2.x_float - personne1.x_float
                if abs(dx) < d_max:
                    dy = personne2.y_float - personne1.y_float
                    if abs(dy) < d_max:
                        d2 = dx ** 2 + dy ** 2
                        if d2 < d_max ** 2:
                            d = math.sqrt(d2)
                            somme_masses = personne1.masse_relative + personne2.masse_relative
                            coef = 2 * VITESSE_REPOUSSEMENT_CHEVAUCHEMENTS / d
                            for personne in [personne2, personne1]:
                                # if personne.objectif is None:
                                coef_relatif = coef * (1 - personne.masse_relative / somme_masses)
                                if personne == personne1:
                                    coef_relatif *= -1
                                personne.deplace_dx_dy(dx * coef_relatif, dy * coef_relatif)
                                i, j = self.carte.xy_carte_to_ij_case(personne.x_sur_carte, personne.y_sur_carte)
                                new_x, new_y = personne.ajuste_xy_objectif(personne.x_sur_carte, personne.y_sur_carte,
                                                                           i, j)
                                if not new_x == personne.x_sur_carte or not new_y == personne.y_sur_carte:
                                    personne.deplace_dx_dy(new_x - personne.x_float, new_y - personne.y_float)
                                if personne.objectif is not None:
                                    x, y = personne.objectif
                                    personne.oriente_vers_point(x, y)

    # -------------------------------------------------
    #                      Sources
    # -------------------------------------------------
    def add_source(self, source: Source):
        self.liste_sources.append(source)
        self.carte.add_source(source.liste_cases_sources)

    def update_sources(self):
        self.gere_deleted_cases_source()

    def gere_deleted_cases_source(self):
        for source in self.liste_sources:
            if len(source.resent_deleted_cases) > 0:
                self.carte.clear_case(source.resent_deleted_cases)
                source.resent_deleted_cases = []
                self.new_affichage_static = True
                if len(source.liste_cases_sources) == 0:
                    self.liste_sources.remove(source)
                    if self.element_selectionne == source:
                        self.element_selectionne = None

    # -------------------------------------------------
    #                     Batiments
    # -------------------------------------------------
    def add_batiment_en_construction(self, type_batiment, x_souris: int, y_souris: int):
        i_souris, j_souris = self.carte.xy_absolu_to_ij_case(x_souris, y_souris)
        self.batiment_en_construction = Batiment(type_batiment, i_souris, j_souris, self.carte)
        self.element_selectionne = None

    def update_position_batiment_en_construction(self, x_souris: int, y_souris: int):
        if self.batiment_en_construction is not None:
            i_souris, j_souris = self.carte.xy_absolu_to_ij_case(x_souris, y_souris)
            self.batiment_en_construction.update_position(i_souris, j_souris, self.carte)

    def update_batiments_en_cours_de_construction(self):
        for batiment in self.liste_batiments_en_cours_de_construction:
            if not batiment.update_construction():
                self.liste_batiments_en_cours_de_construction.remove(batiment)
                self.liste_batiments_constuits.append(batiment)
                self.carte.add_cases_relais_batiment(batiment.liste_cases_relais)
                self.new_affichage_static = True

    def remove_batiement_constuit(self, batiment: Batiment):
        self.liste_batiments_constuits.remove(batiment)
        if self.element_selectionne == batiment:
            self.element_selectionne = None
        x, y = self.carte.ij_case_to_centre_xy_carte(batiment.i, batiment.j)
        if batiment.type_explosion is not None:
            self.liste_explosions.append(Explosion(batiment.type_explosion, x, y))
        self.carte.clear_case(batiment.liste_cases_depos + batiment.liste_cases_relais + batiment.liste_cases_pleines)
        for personne in self.liste_personnes:
            if isinstance(personne, Soldat):
                if personne.cible == batiment:
                    personne.cible = None
        Batiment.nb_personne_max -= batiment.nb_places

    def update_batiemnt_amelioration(self):
        for batiment in self.liste_batiments_constuits:
            type_amelioration_prete = batiment.update_amelioreur()
            if type_amelioration_prete is not None:
                for type_element, param, value in \
                        (Amelioreur.dic_ameliorations[PARAM_AMELIORATION_LISTE__TYPE_PARAM_VALUE]
                         [type_amelioration_prete]):
                    Element.dic_elements[param][type_element] = value

    def update_batiments_constuits(self):
        for batiment in self.liste_batiments_constuits:
            type_construction_prete = batiment.update_constructeur()
            if type_construction_prete is not None and Batiment.nb_personne_max >= self.nb_places_personnes + \
                    Element.dic_elements[PARAM_A_PERSONNE_NB_PLACES][type_construction_prete]:
                i, j = random.choice(batiment.liste_cases_depos + batiment.liste_cases_relais)
                x, y = self.carte.ij_case_to_centre_xy_carte(i, j)
                self.cree_personne(type_construction_prete, x, y, batiment.point_sortie_constructions)
                batiment.constructeur.type_element_en_construction = None
                batiment.constructeur.new_affichage = True

    def add_batiment_fixe(self, batiment: Batiment):
        self.liste_batiments_en_cours_de_construction.append(batiment)
        self.carte.add_batiment(batiment.liste_cases_pleines, batiment.liste_cases_relais, batiment.liste_cases_depos,
                                batiment_construit=batiment.etape_construction >= batiment.etape_construction_max)
        self.update_chemin_personnes()

    def fixe_batiement_en_construction(self):
        if self.batiment_en_construction is not None:
            if Batiment.liquide_comptenu_general >= self.batiment_en_construction.prix_liquide and \
                    self.batiment_en_construction.fixer(self.get_all_cases_elements_mobiles()):
                Batiment.liquide_comptenu_general -= self.batiment_en_construction.prix_liquide
                self.add_batiment_fixe(self.batiment_en_construction)
                self.batiment_en_construction = None
                self.update_affichage_static()

    def annule_batiment_en_construction(self):
        if self.batiment_en_construction is not None:
            self.batiment_en_construction = None

    def annule_batiment_en_cours_de_construction_selectionne(self):
        if isinstance(self.element_selectionne, Batiment) and \
                self.element_selectionne in self.liste_batiments_en_cours_de_construction:
            self.carte.clear_case(self.element_selectionne.liste_cases_depos +
                                  self.element_selectionne.liste_cases_relais +
                                  self.element_selectionne.liste_cases_pleines)
            self.liste_batiments_en_cours_de_construction.remove(self.element_selectionne)
            self.element_selectionne = None

    # -------------------------------------------------
    #                     Explosions
    # -------------------------------------------------
    def cree_explosion_tir(self, element):
        x_centre, y_centre, orientation = None, None, None
        if isinstance(element, ElementMobile):
            x_centre, y_centre, orientation = element.x_float, element.y_float, element.orientation

        if x_centre is not None:
            self.liste_explosions.append(explosion_tireur(element.tireur.type_explosion_tir,
                                                          element.tireur.distance_explosion_centre,
                                                          x_centre, y_centre, orientation))

    def update_explosions(self):
        for explosion in self.liste_explosions:
            explosion.update()
            if explosion.fin:
                self.liste_explosions.remove(explosion)

    # -------------------------------------------------
    #                     Evenements
    # -------------------------------------------------
    def souris_sur_ecran(self, x_souris: int, y_souris: int):
        return self.carte.xy_absolu_dans_ecran(x_souris, y_souris)

    def gere_deplacement_souris(self, x_souris: int, y_souris: int):
        self.carte.update_deplacement(x_souris, y_souris)
        if self.batiment_en_construction is not None:
            self.update_position_batiment_en_construction(x_souris, y_souris)
        if self.rect_clic_down_sur_carte is not None:
            x, y, _, _ = self.rect_clic_down_sur_carte
            x2, y2 = self.carte.xy_absolu_to_xy_carte(x_souris, y_souris)
            self.rect_clic_down_sur_carte = x, y, x2, y2

    def gere_zoom(self, n: int, x_souris: int, y_souris: int):
        if self.carte.zoom_dezoom(n, x_souris, y_souris):
            for element_mobile in self.liste_personnes + self.liste_ennemis:
                element_mobile.new_affichage = True
            for explosion in self.liste_explosions:
                explosion.new_affichage = True
            self.new_affichage_static = True

    def gere_clic_down(self, x_souris: int, y_souris: int):
        if self.batiment_en_construction is None:
            x_carte_souris, y_carte_souris = self.carte.xy_absolu_to_xy_carte(x_souris, y_souris)
            self.rect_clic_down_sur_carte = x_carte_souris, y_carte_souris, x_carte_souris, y_carte_souris

    def gere_ctrl_clic(self, x_souris: int, y_souris: int):
        ancien_element_selectionne = self.element_selectionne
        self.element_selectionne = []
        self.gere_clic(x_souris, y_souris)
        if ancien_element_selectionne is not None:
            if self.element_selectionne is None or not (type(self.element_selectionne) == list or
                                                        self.element_selectionne in self.liste_personnes) \
                    or not (type(ancien_element_selectionne) == list or
                            ancien_element_selectionne in self.liste_personnes):
                self.element_selectionne = ancien_element_selectionne
            elif type(self.element_selectionne) == list:
                if type(ancien_element_selectionne) == list:
                    for element_mobile in ancien_element_selectionne:
                        if element_mobile not in self.element_selectionne:
                            self.element_selectionne.append(element_mobile)
                else:
                    self.element_selectionne.append(ancien_element_selectionne)
            else:
                if type(ancien_element_selectionne) == list:
                    if self.element_selectionne in ancien_element_selectionne:
                        ancien_element_selectionne.remove(self.element_selectionne)
                        if len(ancien_element_selectionne) == 1:
                            ancien_element_selectionne = ancien_element_selectionne[0]
                    else:
                        ancien_element_selectionne.append(self.element_selectionne)
                    self.element_selectionne = ancien_element_selectionne
                else:
                    if not ancien_element_selectionne == self.element_selectionne:
                        self.element_selectionne = [self.element_selectionne, ancien_element_selectionne]

    def gere_clic(self, x_souris: int, y_souris: int):
        if self.batiment_en_construction is not None:
            self.fixe_batiement_en_construction()
        elif self.rect_clic_down_sur_carte is not None and \
                (abs(self.rect_clic_down_sur_carte[0] - self.rect_clic_down_sur_carte[2]) > MARGE_CLIC_MOTION or
                 abs(self.rect_clic_down_sur_carte[1] - self.rect_clic_down_sur_carte[3]) > MARGE_CLIC_MOTION):
            self.element_selectionne = []
            x_min, x_max = sorted([self.rect_clic_down_sur_carte[0], self.rect_clic_down_sur_carte[2]])
            y_min, y_max = sorted([self.rect_clic_down_sur_carte[1], self.rect_clic_down_sur_carte[3]])
            for personne in self.liste_personnes:
                if x_min <= personne.x_sur_carte <= x_max and y_min <= personne.y_sur_carte <= y_max:
                    self.element_selectionne.append(personne)
            if len(self.element_selectionne) == 0:
                self.element_selectionne = None
            elif len(self.element_selectionne) == 1:
                self.element_selectionne = self.element_selectionne[0]
        else:
            self.element_selectionne = None
            x_carte_clic, y_carte_clic = self.carte.xy_absolu_to_xy_carte(x_souris, y_souris)
            for personne in self.liste_personnes:
                if personne.clic(x_carte_clic, y_carte_clic):
                    self.element_selectionne = personne
                    break
            if self.element_selectionne is None:
                i_clic_abs, j_clic_abs = self.carte.xy_absolu_to_ij_case(x_souris, y_souris)
                for source in self.liste_sources:
                    if source.clic(i_clic_abs, j_clic_abs):
                        self.element_selectionne = source
                        break
                if self.element_selectionne is None:
                    for batiment in self.liste_batiments_en_cours_de_construction + self.liste_batiments_constuits:
                        if batiment.clic(i_clic_abs, j_clic_abs):
                            self.element_selectionne = batiment
                            break
        self.rect_clic_down_sur_carte = None

    def gere_clic_droit(self, x_souris: int, y_souris: int):
        self.annule_batiment_en_construction()
        if self.element_selectionne is not None:
            liste = self.element_selectionne if type(self.element_selectionne) == list else [self.element_selectionne]
            for element in liste:
                if isinstance(element, ElementMobile) and element.choix_mouvement:
                    x_carte_clic, y_carte_clic = self.carte.xy_absolu_to_xy_carte(x_souris, y_souris)
                    if isinstance(element, Soldat):
                        self.gere_new_objectif_cible_soldat(element, x_carte_clic, y_carte_clic)
                    else:
                        element.new_objectif(x_carte_clic, y_carte_clic)

            if isinstance(self.element_selectionne, Batiment) and self.element_selectionne.constructeur is not None:
                x_carte_clic, y_carte_clic = self.carte.xy_absolu_to_xy_carte(x_souris, y_souris)
                self.element_selectionne.set_point_sortie_constructions(self.carte, x_carte_clic, y_carte_clic)

    def update(self):
        if self.carte.deplace():
            self.new_affichage_static = True
        self.update_batiments_en_cours_de_construction()
        self.update_batiments_constuits()
        self.update_batiemnt_amelioration()
        self.update_sources()
        self.update_personnes()
        self.update_explosions()

    # -------------------------------------------------
    #                     Affichage
    # -------------------------------------------------
    def update_affichage_static(self):
        self.carte.affiche(self.ecran_static)
        for batiment in self.liste_batiments_constuits:
            batiment.affiche(self.ecran_static, self.carte)
        for source in self.liste_sources:
            source.affiche(self.ecran_static, self.carte)

    def affiche_element_selectionne(self, screen: pygame.Surface):
        if type(self.element_selectionne) == list:
            for element_selectionne in self.element_selectionne:
                element_selectionne.affiche_selectionne(screen)
        else:
            if isinstance(self.element_selectionne, Batiment):
                self.element_selectionne.affiche_selectionne(screen, self.carte)
            if isinstance(self.element_selectionne, Source):
                self.element_selectionne.affiche_selectionne(screen, self.carte)
            if isinstance(self.element_selectionne, ElementMobile):
                self.element_selectionne.affiche_selectionne(screen)
                if isinstance(self.element_selectionne, Soldat):
                    self.element_selectionne.affiche_tireur(screen)

    def update_affichage_complet(self):
        self.ecran_complet.blit(self.ecran_static, (0, 0))

        for batiment in self.liste_batiments_en_cours_de_construction:
            batiment.affiche(self.ecran_complet, self.carte)

        if self.batiment_en_construction is not None:
            self.batiment_en_construction.affiche(self.ecran_complet, self.carte)

        for personne in self.liste_personnes:
            personne.affiche(self.ecran_complet)

        for explosion in self.liste_explosions:
            explosion.affiche(self.ecran_complet, self.carte)

        if self.element_selectionne is not None:
            self.affiche_element_selectionne(self.ecran_complet)
        if self.rect_clic_down_sur_carte is not None:
            x, y, x2, y2 = self.rect_clic_down_sur_carte
            x, y = self.carte.xy_carte_to_xy_relatif(x, y)
            x2, y2 = self.carte.xy_carte_to_xy_relatif(x2, y2)
            pygame.draw.rect(self.ecran_complet, COULEUR_ELEMENT_SELECTION, (x, y, x2 - x, y2 - y), 1)

    def affiche(self, screen: pygame.Surface):
        if self.new_affichage_static:
            self.update_affichage_static()
        self.update_affichage_complet()
        screen.blit(self.ecran_complet, (self.carte.x_ecran, self.carte.y_ecran))
