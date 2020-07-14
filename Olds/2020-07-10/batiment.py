# coding: utf-8

from element import *


class Constructeur:
    def __init__(self, liste_constructions_possibles: int):
        self.liste_constructions_possibles = liste_constructions_possibles
        self.liste_type_elements_en_attente = []
        self.type_element_en_construction = None
        self.avancement_construction = 0
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

    @property
    def avancement_construction_max(self):
        if self.type_element_en_construction is not None:
            return Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION][self.type_element_en_construction]
        return None


class Amelioreur:
    dic_ameliorations = copy.deepcopy(DIC_AMELIORATIONS)

    def __init__(self, liste_ameliorations_possibles):
        self.liste_ameliorations_possibles = liste_ameliorations_possibles
        self.type_amelioration_en_cours = None
        self.avancement_amelioration = 0
        self.new_affichage = True

    def update(self):
        if self.type_amelioration_en_cours is not None:
            self.avancement_amelioration += 1
            self.new_affichage = True
            if self.avancement_amelioration >= self.avancement_ameliration_max:
                type_ameliration = self.type_amelioration_en_cours
                self.type_amelioration_en_cours = None
                self.liste_ameliorations_possibles.remove(type_ameliration)
                return type_ameliration
        return None

    def lance_amelioration(self, type_amelioration):
        if self.type_amelioration_en_cours is None and type_amelioration in self.liste_ameliorations_possibles:
            self.type_amelioration_en_cours = type_amelioration
            self.avancement_amelioration = 0
            return True
        return False

    def annule_construction(self):
        self.type_amelioration_en_cours = None
        self.avancement_amelioration = 0
        self.new_affichage = True

    @property
    def avancement_ameliration_max(self):
        if self.type_amelioration_en_cours is not None:
            return Amelioreur.dic_ameliorations[PARAM_AMELIORATION_DUREE][self.type_amelioration_en_cours]
        return None


class Batiment(Element):
    argent_comptenu_relay_general = NB_ARGENT_INIT
    liquide_comptenu_general = NB_LIQUIDE_INIT
    nb_personne_max = 0

    def __init__(self, type_batiment, i_centre: int, j_centre: int, carte: Carte, contruit=False):
        Element.__init__(self, type_batiment)
        self.i = i_centre
        self.j = j_centre
        # Attention : On ne peut pas changer la liste des cases d'un batiment en cours de route (cela évite d'appeler
        # tout le temps la fonction update_position(), on peut sinon créer une mémoire qui détecte le changement...).
        self.liste_cases_pleines = []
        self.liste_cases_relais = []
        self.liste_cases_depos = []
        self.liste_cases_interdites_constuction = []
        self.update_position(i_centre, j_centre, carte)

        self.fixe = contruit
        self.argent_comptenu = 0
        self.etape_construction = math.inf if contruit else 0

        self._constructeur = None
        self.point_sortie_constructions = None
        self._amelioreur = None

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
            if self.etape_construction >= self.etape_construction_max:
                self.etape_construction = math.inf
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

    def update_amelioreur(self):
        if self.amelioreur is not None:
            return self.amelioreur.update()
        return None

    def ajoute_construction_constructeur(self, type_personnage):
        prix_argent = Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_personnage]
        prix_liquide = Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_personnage]
        if self.argent_comptenu >= prix_argent and Batiment.liquide_comptenu_general >= prix_liquide:
            if self.constructeur.ajoute_construction(type_personnage):
                self.argent_comptenu -= prix_argent
                Batiment.liquide_comptenu_general -= prix_liquide
                return True
        return False

    def annule_construction_constructeur(self, n):
        if len(self.constructeur.liste_type_elements_en_attente) > n:
            type_personnage = self.constructeur.liste_type_elements_en_attente[n]
            prix_argent = Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_personnage]
            prix_liquide = Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_personnage]
            if self.constructeur.annuler_construction(n):
                self.argent_comptenu += prix_argent
                if self.argent_comptenu > self.argent_comptenu_max:
                    self.argent_comptenu = self.argent_comptenu_max
                Batiment.liquide_comptenu_general += prix_liquide
                return True
        return False

    def lance_amelioration_amelioreur(self, type_amelioration):
        prix_argent = Amelioreur.dic_ameliorations[PARAM_AMELIORATION_PRIX_ARGENT][type_amelioration]
        prix_liquide = Amelioreur.dic_ameliorations[PARAM_AMELIORATION_PRIX_LIQUIDE][type_amelioration]
        if self.argent_comptenu >= prix_argent and Batiment.liquide_comptenu_general >= prix_liquide:
            if self.amelioreur.lance_amelioration(type_amelioration):
                self.argent_comptenu -= prix_argent
                Batiment.liquide_comptenu_general -= prix_liquide
                return True
        return False

    def annule_amelioration_en_cours(self):
        if self.amelioreur is not None:
            type_amelioration = self._amelioreur.type_amelioration_en_cours
            if type_amelioration is not None:
                coef = 1 - (self._amelioreur.avancement_amelioration / self._amelioreur.avancement_ameliration_max)
                self.argent_comptenu += \
                    int(coef * Amelioreur.dic_ameliorations[PARAM_AMELIORATION_PRIX_ARGENT][type_amelioration])
                if self.argent_comptenu > self.argent_comptenu_max:
                    self.argent_comptenu = self.argent_comptenu_max
                Batiment.liquide_comptenu_general += \
                    int(coef * Amelioreur.dic_ameliorations[PARAM_AMELIORATION_PRIX_LIQUIDE][type_amelioration])
                self._amelioreur.annule_amelioration()
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

    @property
    def liste_cases_pleines_relatives(self):
        return Element.dic_elements[PARAM_F_BATIMENT_LISTE_CASES][self.type][TYPE_CASE_PLEINE]

    @property
    def liste_cases_relais_relatives(self):
        return Element.dic_elements[PARAM_F_BATIMENT_LISTE_CASES][self.type][TYPE_CASE_S_RELAIS]

    @property
    def liste_cases_depos_relatives(self):
        return Element.dic_elements[PARAM_F_BATIMENT_LISTE_CASES][self.type][TYPE_CASE_S_DEPOS]

    @property
    def liste_couleur_cases_pleines(self):
        return Element.dic_elements[PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES][self.type]

    @property
    def nb_cases(self):
        return len(self.liste_cases_pleines_relatives + self.liste_cases_relais_relatives +
                   self.liste_cases_depos_relatives)

    @property
    def nb_places(self):
        return Element.dic_elements[PARAM_A_BATIMENT_NB_PLACES][self.type]

    @property
    def prix_liquide(self):
        return Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][self.type]

    @property
    def prix_construction(self):
        return Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][self.type]

    @property
    def etape_construction_max(self):
        return Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION][self.type]

    @property
    def argent_comptenu_max(self):
        return Element.dic_elements[PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX][self.type]

    @property
    def constructeur(self):
        liste_constructions = Element.dic_elements[PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES][self.type]
        if len(liste_constructions) == 0:
            if self._constructeur is not None:
                self._constructeur = None
        else:
            if self._constructeur is None:
                self._constructeur = Constructeur(liste_constructions)
            else:
                self._constructeur.liste_constructions_possibles = liste_constructions

        return self._constructeur

    @property
    def amelioreur(self):
        liste_ameliorations = Element.dic_elements[PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES][self.type]
        if len(liste_ameliorations) == 0:
            if self._amelioreur is not None:
                self._amelioreur = None
        else:
            if self._amelioreur is None:
                self._amelioreur = Amelioreur(liste_ameliorations)
            else:
                self._amelioreur.liste_ameliorations_possibles = liste_ameliorations

        return self._amelioreur
