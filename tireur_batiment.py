# coding: utf-8

from tireur import *


class TireurBatiment(Tireur):
    def __init__(self, type_batiment, i, j):
        Tireur.__init__(self, type_batiment)
        self.i, self.j = i, j
        self.x, self.y = 0, 0
        self.cible = None
        self.orientation_canon = 0
        self.new_affichage_canon = True

        self.ecran_original = \
            loaded_images(Element.dic_elements[PARAM_F_BATIMENT_TIREUR_CHEMIN_IMAGE_CANON][self.type_element])
        self.ecran_original_size = (self.ecran_original.get_width(), self.ecran_original.get_height())
        self.ecran = pygame.transform.rotozoom(self.ecran_original, 0, self.scale_ecran_original_zoom)
        self.ecran_size = (self.ecran.get_width(), self.ecran.get_height())

    def tir_si_possible(self):
        if self.peut_tirer:
            self.cible.recoit_tir(self.force_tir)
            self.tir()
            return True
        return False

    def new_cible(self, cible: Element):
        if self.cible is None:
            self.cible = cible

    def annule_cible(self):
        self.cible = None

    def oriente_canon_vers_point(self, x_obj, y_obj):
        dx = x_obj - self.x
        dy = y_obj - self.y
        if dx == 0:
            if dy > 0:
                self.orientation_canon = - math.pi / 2
            else:
                self.orientation_canon = math.pi / 2
        else:
            if dx > 0:
                self.orientation_canon = math.atan(- dy / dx)
            else:
                self.orientation_canon = math.pi - math.atan(dy / dx)
        self.new_affichage_canon = True

    def update_general(self, carte: Carte):
        if self.x == 0 and self.y == 0:
            self.x, self.y = carte.ij_case_to_centre_xy_carte(self.i, self.j)
        self.update()
        if self.cible is not None:
            if self.point_a_porter_de_tir(self.x, self.y, self.cible.x_sur_carte, self.cible.y_sur_carte):
                ancienne_orientation = self.orientation_canon
                ancien_affichage = self.new_affichage_canon
                self.oriente_canon_vers_point(self.cible.x_sur_carte, self.cible.y_sur_carte)
                if not ancien_affichage and abs(ancienne_orientation - self.orientation_canon) < 0.001:
                    self.new_affichage_canon = False
                if self.tir_si_possible():
                    return True
            else:
                self.cible = None
        return False

    def update_ecran_canon(self, carte: Carte):
        self.ecran = pygame.transform.rotozoom(self.ecran_original, self.orientation_canon * 180 / math.pi,
                                               self.scale_ecran_original_zoom * carte.coef_zoom)
        self.ecran_size = (self.ecran.get_width(), self.ecran.get_height())
        self.new_affichage_canon = False

    def affiche_canon(self, screen: pygame.Surface, carte: Carte):
        if self.new_affichage_canon:
            self.update_ecran_canon(carte)
        x_relatif, y_relatif = carte.xy_carte_to_xy_relatif(self.x, self.y)
        screen.blit(self.ecran, (x_relatif - int(self.ecran_size[0] / 2), y_relatif - int(self.ecran_size[1] / 2)))

    def affiche_selectionne(self, screen: pygame.Surface, carte: Carte):
        Tireur.affiche(self, screen, carte, self.x, self.y)

    @property
    def scale_ecran_original_zoom(self):
        return Element.dic_elements[PARAM_F_BATIMENT_TIREUR_SCALE_IMAGE_CANON_ZOOM][self.type_element]

    @property
    def cible_visible_ext(self):
        return Element.dic_elements[PARAM_A_TIREUR_CIBLE_VISIBLE][self.type_element]
