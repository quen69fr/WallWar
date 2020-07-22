# coding: utf-8

from batiment import *


class BaseEnnemi(Batiment):
    def __init__(self, i_centre: int, j_centre: int, carte: Carte):
        Batiment.__init__(self, TYPE_BATIMENT_ENNEMI, i_centre, j_centre, carte, True)
        self.x_min, self.y_min = carte.ij_case_to_centre_xy_carte(
            min(self.liste_cases_pleines, key=lambda point: point[0])[0] - 1,
            min(self.liste_cases_pleines, key=lambda point: point[1])[1] - 1)
        self.x_max, self.y_max = carte.ij_case_to_centre_xy_carte(
            max(self.liste_cases_pleines, key=lambda point: point[0])[0] + 1,
            max(self.liste_cases_pleines, key=lambda point: point[1])[1] + 1)

    def get_value_param(self, param):
        if param == PARAM_A_VIES or param == PARAM_F_NOM or param == PARAM_F_DESCRIPTION or \
                param == PARAM_F_BATIMENT_LISTE_CASES or param == PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES or \
                param == PARAM_F_TYPE_EXPLOSION:
            return Batiment.get_value_param(self, param)
        return 0

    def get_pos_autour(self):
        n1 = random.randint(0, 1)
        n2 = random.randint(0, 1)
        if n1 == 0:
            x = self.x_min if n2 == 0 else self.x_max
            y = random.randint(self.y_min, self.y_max)
        else:
            x = random.randint(self.x_min, self.x_max)
            y = self.y_min if n2 == 0 else self.y_max
        return x, y

    @property
    def nb_places(self):
        return 0

    @property
    def prix_liquide(self):
        return 0

    @property
    def prix_construction(self):
        return 0

    @property
    def etape_construction_max(self):
        return 0

    @property
    def argent_comptenu_max(self):
        return 0

    @property
    def constructeur(self):
        return None

    @property
    def amelioreur(self):
        return None

    @property
    def peut_tirer(self):
        return False

    @property
    def tireur(self):
        return None

    @property
    def nb_vies_regen(self):
        return 0
