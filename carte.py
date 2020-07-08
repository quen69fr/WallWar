# coding: utf-8

from drawing_box import *
import copy
import random
import math


class Carte:
    def __init__(self, nb_cases_i: int, nb_cases_j: int, cote_cases: int):
        self.x_ecran = X_CARTE
        self.y_ecran = Y_CARTE
        self.largeur_ecran = LARGEUR_CARTE
        self.hauteur_ecran = HAUTEUR_CARTE

        self.x_camera_sur_cadre = 0
        self.y_camera_sur_cadre = 0
        self.nb_cases_i = nb_cases_i
        self.nb_cases_j = nb_cases_j
        self._cote_case = cote_cases
        self.largeur_totale = 0
        self.hauteur_totale = 0

        self.deplacement_x = 0
        self.deplacement_y = 0

        self.image_fond = loaded_images(CARTE_CHEMIN_IMAGE_FOND_PAVAGE_SABLE)
        self.nb_cases_i_par_image_fond = 0
        self.nb_cases_j_par_image_fond = 0
        self.largeur_image_fond = 0
        self.hauteur_image_fond = 0
        self._coef_zoom = ZOOM_INIT
        self._cote_case_zoom: int = 0

        self.set_cote_case_zoom(int(cote_cases * ZOOM_INIT))

        self._cote_case_zoom_min = max(math.ceil(self.largeur_ecran / self.nb_cases_i),
                                       math.ceil(self.hauteur_ecran / self.nb_cases_j)) + 1
        self._cote_case_zoom_max = CARTE_COTE_CASE_ZOOM_MAX

        self._grille = [[TYPE_CASE_VIDE for _ in range(self.nb_cases_j)] for _ in range(self.nb_cases_i)]
        self._grille_vierge = [[CASE_VIDE_GRILLE_CHEMIN for _ in range(self.nb_cases_j)]
                               for _ in range(self.nb_cases_i)]
        self._grille_points_relay = copy.deepcopy(self._grille_vierge)
        self.new_grille_points_relay = True
        self._liste_coordonnees_objectifs_possibles = []
        self.new_liste_coordonnees_objectifs_possibles = True

    # -------------------------------------------------
    #                       Grille
    # -------------------------------------------------
    def set_cases_grille(self, type_cases, liste_cases):
        for i, j in liste_cases:
            self._grille[i][j] = type_cases
            if type_cases == TYPE_CASE_PLEINE:
                self._grille_vierge[i][j] = CASE_PLEINE_GRILLE_CHEMIN
                self.new_liste_coordonnees_objectifs_possibles = True
            else:
                self._grille_vierge[i][j] = CASE_VIDE_GRILLE_CHEMIN

    def get_cases_grille(self, i, j):
        if self.ij_case_existe(i, j):
            return self._grille[i][j]
        return TYPE_CASE_INEXISTANTE

    def get_all_cases_relay(self):
        liste_case_relay = []
        for i, colone in enumerate(self._grille):
            for j, case in enumerate(colone):
                if case == TYPE_CASE_S_RELAIS:
                    liste_case_relay.append((i, j))
        return liste_case_relay

    def get_all_cases_pleines(self):
        liste_case_pleines = []
        for i, colone in enumerate(self._grille):
            for j, case in enumerate(colone):
                if case == TYPE_CASE_PLEINE:
                    liste_case_pleines.append((i, j))
        return liste_case_pleines

    def add_source(self, liste_cases_sources: list):
        self.set_cases_grille(TYPE_CASE_SOURCE, liste_cases_sources)

    def add_batiment(self, liste_cases_pleines: list, liste_cases_relais: list, liste_cases_depos: list,
                     batiment_construit=False):
        self.set_cases_grille(TYPE_CASE_PLEINE, liste_cases_pleines)
        self.set_cases_grille(TYPE_CASE_S_RELAIS if batiment_construit else TYPE_CASE_S_DEPOS, liste_cases_relais)
        self.set_cases_grille(TYPE_CASE_S_DEPOS, liste_cases_depos)
        self.new_grille_points_relay = True

    def add_cases_relais_batiment(self, liste_cases_relais: list):
        self.set_cases_grille(TYPE_CASE_S_RELAIS, liste_cases_relais)
        self.new_grille_points_relay = True

    def clear_case(self, liste_cases_vides: list):
        for i, j in liste_cases_vides:
            if self.get_cases_grille(i, j) == TYPE_CASE_PLEINE:
                self.new_grille_points_relay = True
                self.new_liste_coordonnees_objectifs_possibles = True
        self.set_cases_grille(TYPE_CASE_VIDE, liste_cases_vides)

    def update_grille_points_relay(self):
        self._grille_points_relay = copy.deepcopy(self._grille_vierge)
        liste_cases_pos_bord = []
        for i, j in self.get_all_cases_relay():
            liste_cases_pos_bord.append((0, i, j))
            self._grille_points_relay[i][j] = 0
        racine_de_deux = math.sqrt(2)
        while not len(liste_cases_pos_bord) == 0:
            valeur_centre, i_centre, j_centre = min(liste_cases_pos_bord)
            for i in [i_centre - 1, i_centre, i_centre + 1]:
                for j in [j_centre - 1, j_centre, j_centre + 1]:
                    if self.ij_case_existe(i, j) and self._grille_points_relay[i][j] == -1:
                        if i_centre == i or j_centre == j:
                            valeur = valeur_centre + 1
                        else:
                            # On n'accepte pas les diagonales si il y a une case pleine à coté
                            if self._grille_points_relay[i_centre][j] == -99 or \
                                    self._grille_points_relay[i][j_centre] == -99:
                                continue
                            valeur = valeur_centre + racine_de_deux
                        self._grille_points_relay[i][j] = valeur
                        liste_cases_pos_bord.append((valeur, i, j))
            liste_cases_pos_bord.remove((valeur_centre, i_centre, j_centre))

    def update_liste_coordonnees_objectifs_possibles(self):
        self._liste_coordonnees_objectifs_possibles = []
        for i, j in self.get_all_cases_pleines():
            liste_coordonnees_sommets = [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]
            for i_s, j_s in liste_coordonnees_sommets[:]:
                if (not self.ij_case_existe(i_s, j_s)) or self.grille_vierge[i_s][j_s] == CASE_PLEINE_GRILLE_CHEMIN \
                        or (i_s, j_s) in self._liste_coordonnees_objectifs_possibles:
                    liste_coordonnees_sommets.remove((i_s, j_s))
            if len(liste_coordonnees_sommets) == 0:
                continue
            for i_a, j_a in [(i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)]:
                if self.grille_vierge[i_a][j_a] == CASE_PLEINE_GRILLE_CHEMIN:
                    if self.ij_case_existe(i_a, j_a):
                        for i_s, j_s in liste_coordonnees_sommets[:]:
                            if i_a == i_s or j_a == j_s:
                                liste_coordonnees_sommets.remove((i_s, j_s))
                                if len(liste_coordonnees_sommets) == 0:
                                    break
                        if len(liste_coordonnees_sommets) == 0:
                            break
            if len(liste_coordonnees_sommets) == 0:
                continue
            self._liste_coordonnees_objectifs_possibles += liste_coordonnees_sommets

    @property
    def grille(self):
        return self._grille

    @property
    def grille_vierge(self):
        return self._grille_vierge

    @property
    def grille_points_relay(self):
        if self.new_grille_points_relay:
            self.update_grille_points_relay()
            self.new_grille_points_relay = False
        return self._grille_points_relay

    @property
    def liste_coordonnees_objectifs_possibles(self):
        if self.new_liste_coordonnees_objectifs_possibles:
            self.update_liste_coordonnees_objectifs_possibles()
            self.new_liste_coordonnees_objectifs_possibles = False
        return self._liste_coordonnees_objectifs_possibles

    # -------------------------------------------------
    #                       Carte
    # -------------------------------------------------
    def set_cote_case_zoom(self, new_cote_case_zoom: int):
        if not new_cote_case_zoom == self._cote_case_zoom:
            self._cote_case_zoom = new_cote_case_zoom
            self.largeur_totale = self.nb_cases_i * self._cote_case_zoom
            self.hauteur_totale = self.nb_cases_j * self._cote_case_zoom

            self.nb_cases_i_par_image_fond = int(self.image_fond.get_width() / self._cote_case_zoom)
            self.nb_cases_j_par_image_fond = int(self.image_fond.get_height() / self._cote_case_zoom)
            self.largeur_image_fond = self.nb_cases_i_par_image_fond * self._cote_case_zoom
            self.hauteur_image_fond = self.nb_cases_j_par_image_fond * self._cote_case_zoom

            self._coef_zoom = self._cote_case_zoom / self._cote_case

            return True
        return False

    def zoom_dezoom(self, n, x_souris: int, y_souris: int):
        new_cote_case_zoom = self._cote_case_zoom + max(int(self._cote_case_zoom * CARTE_COEF_ZOOM), 1) * n
        if n > 0:
            if new_cote_case_zoom > self._cote_case_zoom_max:
                new_cote_case_zoom = self._cote_case_zoom_max
        else:
            if new_cote_case_zoom < self._cote_case_zoom_min:
                new_cote_case_zoom = self._cote_case_zoom_min

        old_cote_case_zoom = self._cote_case_zoom

        if self.set_cote_case_zoom(new_cote_case_zoom):
            coef = (1 - old_cote_case_zoom / self._cote_case_zoom) / self._coef_zoom
            self.x_camera_sur_cadre += coef * x_souris
            self.y_camera_sur_cadre += coef * y_souris
            self.recadre_si_necessaire()
            return True
        return False

    @property
    def cote_case_zoom(self):
        return self._cote_case_zoom

    @property
    def coef_zoom(self):
        return self._coef_zoom

    def recadre_si_necessaire(self):
        action = False
        if self.x_camera_sur_cadre < 0:
            self.x_camera_sur_cadre = 0
            self.deplacement_x = 0
            action = True
        else:
            x_camera_max = self.largeur_totale - self.largeur_ecran
            if self.x_camera_sur_cadre > x_camera_max:
                self.x_camera_sur_cadre = x_camera_max
                self.deplacement_x = 0
                action = True
        if self.y_camera_sur_cadre < 0:
            self.y_camera_sur_cadre = 0
            self.deplacement_y = 0
            action = True
        else:
            y_camera_max = self.hauteur_totale - self.hauteur_ecran
            if self.y_camera_sur_cadre > y_camera_max:
                self.y_camera_sur_cadre = y_camera_max
                self.deplacement_y = 0
                action = True
        return action

    def regadre_si_deplacement_inutil(self):
        if self.deplacement_x == 0 and self.deplacement_y == 0:
            return True

        inutil_x = False
        if not self.deplacement_x == 0:
            if self.deplacement_x < 0:
                if self.x_camera_sur_cadre == 0:
                    inutil_x = True
            else:
                if self.x_camera_sur_cadre == self.largeur_totale - self.largeur_ecran:
                    inutil_x = True
        if inutil_x:
            self.deplacement_x = 0

        inutil_y = False
        if not self.deplacement_y == 0:
            if self.deplacement_y < 0:
                if self.y_camera_sur_cadre == 0:
                    inutil_y = True
            else:
                if self.y_camera_sur_cadre == self.hauteur_totale - self.hauteur_ecran:
                    inutil_y = True
        if inutil_y:
            self.deplacement_y = 0

        if self.deplacement_x == 0 and self.deplacement_y == 0:
            return True
        return False

    def update_deplacement(self, x_souris: int, y_souris: int):
        # x_souris_relatif, y_souris_relatif = self.xy_absolu_to_xy_relatif(x_souris, y_souris)
        self.deplacement_x = 0
        dx = CARTE_MARGE_BORD_DEPLACEMENT - x_souris
        if dx > 0:
            self.deplacement_x = - dx / CARTE_MARGE_BORD_DEPLACEMENT * CARTE_VITESSE_DEPLACEMENT / self._coef_zoom
        else:
            dx = CARTE_MARGE_BORD_DEPLACEMENT - LARGEUR + x_souris
            if dx > 0:
                self.deplacement_x = dx / CARTE_MARGE_BORD_DEPLACEMENT * CARTE_VITESSE_DEPLACEMENT / self._coef_zoom

        self.deplacement_y = 0
        dy = CARTE_MARGE_BORD_DEPLACEMENT - y_souris
        if dy > 0:
            self.deplacement_y = - dy / CARTE_MARGE_BORD_DEPLACEMENT * CARTE_VITESSE_DEPLACEMENT / self._coef_zoom
        else:
            dy = CARTE_MARGE_BORD_DEPLACEMENT - HAUTEUR + y_souris
            if dy > 0:
                self.deplacement_y = dy / CARTE_MARGE_BORD_DEPLACEMENT * CARTE_VITESSE_DEPLACEMENT / self._coef_zoom

    def stop_deplacement(self):
        self.deplacement_x = 0
        self.deplacement_y = 0

    def deplace(self):
        if self.regadre_si_deplacement_inutil():
            return False
        if not self.deplacement_x == 0:
            self.x_camera_sur_cadre += int(self.deplacement_x)
        if not self.deplacement_y == 0:
            self.y_camera_sur_cadre += int(self.deplacement_y)
        self.recadre_si_necessaire()
        return True

    def affiche_liste_coordonnees_objectifs_possibles(self, ecran_monde: pygame.Surface):
        rayon = int(self.cote_case_zoom / 3)
        for i, j in self.liste_coordonnees_objectifs_possibles:
            x, y = self.ij_case_to_centre_xy_relatif(i, j)
            draw_filled_circle(ecran_monde, (x, y), rayon, ROUGE)

    def affiche_grille_points_relay(self, ecran_monde: pygame.Surface):
        couleur_max = 50
        for i, colone in enumerate(self._grille_points_relay):
            for j, case in enumerate(colone):
                if self.ij_case_dans_ecran(i, j):
                    if case == CASE_VIDE_GRILLE_CHEMIN or case == CASE_PLEINE_GRILLE_CHEMIN:
                        couleur = ROUGE
                    else:
                        c = min(int(case / couleur_max * 255), 255)
                        couleur = (c, c, c)
                    x, y = self.ij_case_to_coin_xy_relatif(i, j)
                    pygame.draw.rect(ecran_monde, couleur, (x, y, self._cote_case_zoom, self._cote_case_zoom))

    def affiche(self, ecran_monde: pygame.Surface):
        x_camera_zoom = self.x_camera_sur_cadre * self._coef_zoom
        y_camera_zoom = self.y_camera_sur_cadre * self._coef_zoom
        i_image = int(x_camera_zoom / self.largeur_image_fond)
        j_image = int(y_camera_zoom / self.hauteur_image_fond)
        x = i_image * self.largeur_image_fond - x_camera_zoom
        y = j_image * self.hauteur_image_fond - y_camera_zoom
        nb_image_x = math.ceil((self.largeur_ecran - x) / self.largeur_image_fond)
        nb_image_y = math.ceil((self.hauteur_ecran - y) / self.hauteur_image_fond)
        for xi in range(nb_image_x):
            for yi in range(nb_image_y):
                ecran_monde.blit(self.image_fond, (x + xi * self.largeur_image_fond, y + yi * self.hauteur_image_fond))

    # -------------------------------------------------
    #                    Conversions
    # -------------------------------------------------

    # ij to xy
    def ij_case_to_centre_xy_carte(self, i: int, j: int):
        return int(self._cote_case * (i + 0.5)), \
               int(self._cote_case * (j + 0.5))

    def ij_case_to_centre_xy_relatif(self, i: int, j: int):
        return int(self._cote_case_zoom * (i + 0.5) - self.x_camera_sur_cadre * self._coef_zoom), \
               int(self._cote_case_zoom * (j + 0.5) - self.y_camera_sur_cadre * self._coef_zoom)

    def ij_case_to_centre_xy_absolu(self, i: int, j: int):
        return int(self._cote_case_zoom * (i + 0.5) - self.x_camera_sur_cadre * self._coef_zoom + self.x_ecran), \
               int(self._cote_case_zoom * (j + 0.5) - self.y_camera_sur_cadre * self._coef_zoom + self.y_ecran)

    def ij_case_to_coin_xy_carte(self, i: int, j: int):
        return int(self._cote_case * i), \
               int(self._cote_case * j)

    def ij_case_to_coin_xy_relatif(self, i: int, j: int):
        return int(self._cote_case_zoom * i - self.x_camera_sur_cadre * self._coef_zoom), \
               int(self._cote_case_zoom * j - self.y_camera_sur_cadre * self._coef_zoom)

    def ij_case_to_coin_xy_absolu(self, i: int, j: int):
        return int(self._cote_case_zoom * i - self.x_camera_sur_cadre * self._coef_zoom + self.x_ecran), \
               int(self._cote_case_zoom * j - self.y_camera_sur_cadre * self._coef_zoom + self.y_ecran)

    # xy to ij
    def xy_carte_to_ij_case(self, x: int, y: int):
        return int(x / self._cote_case), \
               int(y / self._cote_case)

    def xy_relatif_to_ij_case(self, x: int, y: int):
        return int(x / self._cote_case_zoom + self.x_camera_sur_cadre / self._cote_case), \
               int(y / self._cote_case_zoom + self.y_camera_sur_cadre / self._cote_case)

    def xy_absolu_to_ij_case(self, x: int, y: int):
        return int((x - self.x_ecran) / self._cote_case_zoom + self.x_camera_sur_cadre / self._cote_case), \
               int((y - self.y_ecran) / self._cote_case_zoom + self.y_camera_sur_cadre / self._cote_case)

    # xy to xy
    def xy_carte_to_xy_relatif(self, x: int, y: int):
        return int((x - self.x_camera_sur_cadre) * self._coef_zoom), \
               int((y - self.y_camera_sur_cadre) * self._coef_zoom)

    def xy_carte_to_xy_absolu(self, x: int, y: int):
        return int((x - self.x_camera_sur_cadre) * self._coef_zoom + self.x_ecran), \
               int((y - self.y_camera_sur_cadre) * self._coef_zoom + self.y_ecran)

    def xy_relatif_to_xy_carte(self, x: int, y: int):
        return int(x / self._coef_zoom + self.x_camera_sur_cadre), \
               int(y / self._coef_zoom + self.y_camera_sur_cadre)

    def xy_relatif_to_xy_absolu(self, x: int, y: int):
        return x + self.x_ecran, \
               y + self.y_ecran

    def xy_absolu_to_xy_carte(self, x: int, y: int):
        return ((x - self.x_ecran) / self._coef_zoom + self.x_camera_sur_cadre), \
               ((y - self.y_ecran) / self._coef_zoom + self.y_camera_sur_cadre)

    def xy_absolu_to_xy_relatif(self, x: int, y: int):
        return x - self.x_ecran, \
               y - self.y_ecran

    # ij dans ecran
    def ij_case_dans_ecran(self, i: int, j: int):
        if (i + 1) * self._cote_case - self.x_camera_sur_cadre > 0 \
                and i * self._cote_case - self.x_camera_sur_cadre < self.largeur_ecran \
                and (j + 1) * self._cote_case - self.y_camera_sur_cadre > 0 \
                and j * self._cote_case - self.y_camera_sur_cadre < self.hauteur_ecran:
            return True
        return False

    # xy dans ecran
    def xy_carte_dans_ecran(self, x: int, y: int):
        if self.x_camera_sur_cadre < x / self._coef_zoom < self.x_camera_sur_cadre + self.largeur_ecran \
                and self.y_camera_sur_cadre < y / self._coef_zoom < self.y_camera_sur_cadre + self.hauteur_ecran:
            return True
        return False

    def xy_relatif_dans_ecran(self, x: int, y: int):
        if 0 < x < self.largeur_ecran and 0 < y < self.hauteur_ecran:
            return True
        return False

    def xy_absolu_dans_ecran(self, x: int, y: int):
        if 0 < x - self.x_ecran < self.largeur_ecran and 0 < y - self.y_ecran < self.hauteur_ecran:
            return True
        return False

    # ij existe
    def ij_case_existe(self, i: int, j: int):
        if 0 <= i < self.nb_cases_i and 0 <= j < self.nb_cases_j:
            return True
        return False

    # xy existe
    def xy_carte_existe(self, x: int, y: int):
        if 0 < x < self.largeur_totale and 0 <= y < self.hauteur_totale:
            return True
        return False

    def xy_relatif_existe(self, x: int, y: int):
        if 0 < x / self._coef_zoom + self.x_camera_sur_cadre < self.largeur_totale \
                and 0 <= y / self._coef_zoom + self.y_camera_sur_cadre < self.hauteur_totale:
            return True
        return False

    def xy_absolu_existe(self, x: int, y: int):
        if 0 < x / self._coef_zoom + self.x_camera_sur_cadre - self.x_ecran < self.largeur_totale \
                and 0 <= y / self._coef_zoom + self.y_camera_sur_cadre - self.y_ecran < self.hauteur_totale:
            return True
        return False

    # aleas
    def ajoute_alea_xy(self, x: int, y: int):
        return (x + random.randint(- ALEA_MAX_CENTRE_CASE_AUTO, ALEA_MAX_CENTRE_CASE_AUTO),
                y + random.randint(- ALEA_MAX_CENTRE_CASE_AUTO, ALEA_MAX_CENTRE_CASE_AUTO))
