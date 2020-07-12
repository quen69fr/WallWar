# coding: utf-8

from element import *


class ElementMobile(Element):
    def __init__(self, type_element_mobil, carte: Carte, x_sur_carte: int, y_sur_carte: int,
                 choix_mouvement: bool, objectif: (int, int) = None, orientation=0):
        Element.__init__(self, type_element_mobil)
        self.carte = carte

        # Attention : On ne peut pas changer l'image d'un élément mobile en cours de route (on peut par contre changer
        # sa taille)
        self.ecran_original = loaded_images(Element.dic_elements[PARAM_F_ELEMENT_MOBILE_CHEMIN_IMAGE][self.type])
        self.ecran_original_size = (self.ecran_original.get_width(), self.ecran_original.get_height())
        self._scale_ecran_original_zoom = 0
        self.ecran = pygame.transform.rotozoom(self.ecran_original, 0, self.scale_ecran_original_zoom)
        self.ecran_size = (self.ecran.get_width(), self.ecran.get_height())

        self.x_sur_carte = x_sur_carte
        self.y_sur_carte = y_sur_carte
        self.x_float = x_sur_carte
        self.y_float = y_sur_carte
        self._orientation = orientation

        self.chemin_liste_objectifs = []
        self.objectif: (int, int) = None
        if objectif:
            self.new_objectif(objectif[0], objectif[1])
        self.choix_mouvement = choix_mouvement

        self.new_affichage = True

    # -------------------------------------------------
    #             Gestion objectifs/chemins
    # -------------------------------------------------
    def update_chemin_et_position(self):
        i_pos, j_pos = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)
        if self.objectif is None:
            x, y = self.ajuste_xy_objectif(self.x_sur_carte, self.y_sur_carte, i_pos, j_pos)
            if not x == self.x_sur_carte or not y == self.y_sur_carte:
                self.chemin_liste_objectifs = [(x, y)]
                self.objectif_suivant()
        else:
            if len(self.chemin_liste_objectifs) > 0:
                x, y = self.chemin_liste_objectifs[-1]
            else:
                x, y = self.objectif
            i, j = self.carte.xy_carte_to_ij_case(x, y)
            if self.carte.get_cases_grille(i, j) == TYPE_CASE_PLEINE:
                self.objectif = None
                self.chemin_liste_objectifs = []
            else:
                self.new_objectif(x, y, modification_chemin_seulement=True)

    def new_objectif(self, x_carte, y_carte, i_pos: int = None, j_pos: int = None, i_objectif: int = None,
                     j_objectif: int = None, modification_chemin_seulement=False):
        if i_pos is None or j_pos is None:
            i_pos, j_pos = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)
        if i_objectif is None or j_objectif is None:
            i_objectif, j_objectif = self.carte.xy_carte_to_ij_case(x_carte, y_carte)
        case_obj = self.carte.get_cases_grille(i_objectif, j_objectif)
        if not case_obj == TYPE_CASE_INEXISTANTE:
            x_obj, y_obj = self.ajuste_xy_objectif(x_carte, y_carte, i_objectif, j_objectif)
            if i_pos == i_objectif and j_pos == j_objectif:
                self.chemin_liste_objectifs = [(x_obj, y_obj)]
            else:
                if case_obj == TYPE_CASE_PLEINE:
                    pass  # TODO
                else:
                    self.chemin_liste_objectifs = self.calcul_new_chemin_grille_objectif_xy(x_obj, y_obj, i_pos, j_pos,
                                                                                            i_objectif, j_objectif)
            if len(self.chemin_liste_objectifs) > 0:
                self.objectif_suivant()

    def new_objectif_point_relay(self):
        i_pos, j_pos = self.carte.xy_carte_to_ij_case(self.x_sur_carte, self.y_sur_carte)

        self.chemin_liste_objectifs = self.calcul_new_chemin_grille_liste_objectifs(i_pos, j_pos,
                                                                                    self.carte.get_all_ij_cases_relay())
        if len(self.chemin_liste_objectifs) > 0:
            self.objectif_suivant()

    def oriente_vers_point(self, x_obj, y_obj):
        dx = x_obj - self.x_sur_carte
        dy = y_obj - self.y_sur_carte
        if dx == 0:
            if dy > 0:
                self._orientation = - math.pi / 2
            else:
                self._orientation = math.pi / 2
        else:
            if dx > 0:
                self._orientation = math.atan(- dy / dx)
            else:
                self._orientation = math.pi - math.atan(dy / dx)
        self.new_affichage = True

    def objectif_suivant(self):
        if len(self.chemin_liste_objectifs) == 0:
            self.objectif = None
            return
        self.objectif = self.chemin_liste_objectifs[0]
        if self.test_ojectif_atteind():
            del self.chemin_liste_objectifs[0]
            self.objectif = None
            return
        self.oriente_vers_point(self.objectif[0], self.objectif[1])
        del self.chemin_liste_objectifs[0]

    def ajuste_xy_objectif(self, x_carte: int, y_carte: int, i_objectif: int, j_objectif: int):
        x_centre_case_obj, y_centre_case_obj = self.carte.ij_case_to_centre_xy_carte(i_objectif, j_objectif)

        if not x_centre_case_obj == x_carte:
            if x_carte > x_centre_case_obj:
                case = self.carte.get_cases_grille(i_objectif + 1, j_objectif)
                if case == TYPE_CASE_PLEINE or case == TYPE_CASE_INEXISTANTE:
                    x_carte = x_centre_case_obj
            elif x_carte < x_centre_case_obj:
                case = self.carte.get_cases_grille(i_objectif - 1, j_objectif)
                if case == TYPE_CASE_PLEINE or case == TYPE_CASE_INEXISTANTE:
                    x_carte = x_centre_case_obj

        if not y_centre_case_obj == y_carte:
            if y_carte > y_centre_case_obj:
                case = self.carte.get_cases_grille(i_objectif, j_objectif + 1)
                if case == TYPE_CASE_PLEINE or case == TYPE_CASE_INEXISTANTE:
                    y_carte = y_centre_case_obj
            else:
                case = self.carte.get_cases_grille(i_objectif, j_objectif - 1)
                if case == TYPE_CASE_PLEINE or case == TYPE_CASE_INEXISTANTE:
                    y_carte = y_centre_case_obj

        if not y_centre_case_obj == y_carte and not x_centre_case_obj == x_carte:
            recadrage = False
            if x_carte > x_centre_case_obj:
                if y_carte > y_centre_case_obj:
                    if self.carte.get_cases_grille(i_objectif + 1, j_objectif + 1) == TYPE_CASE_PLEINE:
                        recadrage = True
                else:
                    if self.carte.get_cases_grille(i_objectif + 1, j_objectif - 1) == TYPE_CASE_PLEINE:
                        recadrage = True
            else:
                if y_carte > y_centre_case_obj:
                    if self.carte.get_cases_grille(i_objectif - 1, j_objectif + 1) == TYPE_CASE_PLEINE:
                        recadrage = True
                else:
                    if self.carte.get_cases_grille(i_objectif - 1, j_objectif - 1) == TYPE_CASE_PLEINE:
                        recadrage = True

            if recadrage:
                if abs(x_carte - x_centre_case_obj) > abs(y_carte - y_centre_case_obj):
                    y_carte = y_centre_case_obj
                else:
                    x_carte = x_centre_case_obj

        return x_carte, y_carte

    def test_ojectif_atteind(self):
        cran_min = math.ceil(self.vitesse_deplacement / 2) + MARGE_OBJECTIF_ATTEIND + 1
        if self.objectif is not None and abs(self.x_sur_carte - self.objectif[0]) < cran_min \
                and abs(self.y_sur_carte - self.objectif[1]) < cran_min:
            return True
        return False

    def calcul_new_chemin_grille_objectif_xy(self, x_carte: int, y_carte: int, i_pos: int, j_pos: int,
                                             i_objectif: int, j_objectif: int):
        chemin_ij = self.carte.graph.trouve_trajectoire_ij(i_pos, j_pos, [(i_objectif, j_objectif)])

        chemin_xy = [self.carte.ij_case_to_centre_xy_carte(i, j) for i, j in chemin_ij]
        del chemin_xy[0]
        chemin_xy[-1] = (x_carte, y_carte)

        return chemin_xy

    def calcul_new_chemin_grille_liste_objectifs(self, i_pos: int, j_pos: int, liste_ij_objectif: list):
        chemin_ij = self.carte.graph.trouve_trajectoire_ij(i_pos, j_pos, liste_ij_objectif)

        chemin_xy = [self.carte.ij_case_to_centre_xy_carte(i, j) for i, j in chemin_ij]
        del chemin_xy[0]

        return chemin_xy

    # -------------------------------------------------
    #                     Evenements
    # -------------------------------------------------
    def deplace(self):
        self.deplace_dx_dy(self.vitesse_deplacement * math.cos(self._orientation),
                           - self.vitesse_deplacement * math.sin(self._orientation))

    def deplace_dx_dy(self, dx: int, dy: int):
        self.x_float += dx
        self.y_float += dy

        self.x_sur_carte = int(self.x_float)
        self.y_sur_carte = int(self.y_float)

    def stop(self):
        self.chemin_liste_objectifs = []
        self.objectif = None

    def update(self):
        if self.objectif is not None:
            self.deplace()
            if self.test_ojectif_atteind():
                self.objectif_suivant()

    def clic(self, x_carte_clic: int, y_carte_clic: int):
        if abs(x_carte_clic - self.x_sur_carte) <= self.rayon and \
                abs(y_carte_clic - self.y_sur_carte) <= self.rayon:
            return True
        return False

    # -------------------------------------------------
    #                     Affichage
    # -------------------------------------------------
    def update_affichage(self):
        self.ecran = pygame.transform.rotozoom(self.ecran_original, self._orientation * 180 / math.pi,
                                               self.scale_ecran_original_zoom * self.carte.coef_zoom)
        self.ecran_size = (self.ecran.get_width(), self.ecran.get_height())
        self.new_affichage = False

    def affiche(self, screen: pygame.Surface):
        if self.new_affichage:
            self.update_affichage()
        x_relatif, y_relatif = self.carte.xy_carte_to_xy_relatif(self.x_sur_carte, self.y_sur_carte)
        screen.blit(self.ecran, (x_relatif - int(self.ecran_size[0] / 2), y_relatif - int(self.ecran_size[1] / 2)))

    def affiche_selectionne(self, screen: pygame.Surface):
        x_relatif, y_relatif = self.carte.xy_carte_to_xy_relatif(self.x_sur_carte, self.y_sur_carte)
        rayon = int((self.rayon + ANNEAU_SELECTION_DISTANCE) * self.carte.coef_zoom)
        pygame.gfxdraw.aacircle(screen, x_relatif, y_relatif, rayon, COULEUR_ELEMENT_SELECTION)
        pygame.gfxdraw.aacircle(screen, x_relatif, y_relatif, rayon, COULEUR_ELEMENT_SELECTION)

    def affiche_objectif(self, screen: pygame.Surface):
        if self.objectif is not None:
            a_x_r, a_y_r = None, None
            for x, y in [(self.x_sur_carte, self.y_sur_carte), self.objectif] + self.chemin_liste_objectifs:
                x_r, y_r = self.carte.xy_carte_to_xy_relatif(x, y)
                if a_x_r is not None and a_y_r is not None:
                    pygame.gfxdraw.line(screen, x_r, y_r, a_x_r, a_y_r, COULEUR_ELEMENT_SELECTION)
                a_x_r, a_y_r = x_r, y_r
            pygame.draw.circle(screen, COULEUR_ELEMENT_SELECTION, (a_x_r, a_y_r), 2)

    @property
    def orientation(self):
        return self._orientation

    @property
    def scale_ecran_original_zoom(self):
        scale = Element.dic_elements[PARAM_F_ELEMENT_MOBILE_SCALE_IMAGE_ZOOM][self.type]
        if not self._scale_ecran_original_zoom == scale:
            self._scale_ecran_original_zoom = scale
            self.new_affichage = True
        return self._scale_ecran_original_zoom

    @property
    def vitesse_deplacement(self):
        return Element.dic_elements[PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT][self.type]

    @property
    def rayon(self):
        return Element.dic_elements[PARAM_F_ELEMENT_MOBILE_RAYON][self.type]

    @property
    def masse_relative(self):
        return Element.dic_elements[PARAM_F_ELEMENT_MOBILE_MASSE_RELATIVE][self.type]
