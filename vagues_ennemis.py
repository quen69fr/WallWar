# coding: utf-8

from carte import *


def get_valeur_param_ennemi(param, nb_entree):
    if param == PARAM_A_TIREUR_DELAY_TIR:
        return round(DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN] * DIC_ENNEMIS[param][VALEUR_MIN] /
                     ((DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MAX] -
                       DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN]) / DIC_ENNEMIS[param][ENTREE_MAX] *
                      nb_entree + DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN]), 1)
    else:
        value = round((DIC_ENNEMIS[param][VALEUR_MAX] - DIC_ENNEMIS[param][VALEUR_MIN]) / DIC_ENNEMIS[param][ENTREE_MAX]
                      * nb_entree + DIC_ENNEMIS[param][VALEUR_MIN], 1)
        if param == PARAM_A_TIREUR_INTELLIGENCE:
            return int(value)
        return value


def get_listes_valeurs_params_ennemi_aleatoire(nb_entrees_max):
    dic_distribution_param = {}
    for param in LISTE_PARAMS_ENNEMIS:
        dic_distribution_param[param] = 0
    for _ in range(nb_entrees_max):
        ok = False
        while not ok:
            key = LISTE_PARAMS_ENNEMIS[random.randint(0, len(LISTE_PARAMS_ENNEMIS) - 1)]
            if dic_distribution_param[key] < DIC_ENNEMIS[key][ENTREE_MAX]:
                dic_distribution_param[key] += 1
                ok = True
    liste = [get_valeur_param_ennemi(key, dic_distribution_param[key]) for key in LISTE_PARAMS_ENNEMIS]
    liste[LISTE_PARAMS_ENNEMIS.index(PARAM_A_TIREUR_PORTEE_VISION)] += \
        liste[LISTE_PARAMS_ENNEMIS.index(PARAM_A_TIREUR_PORTEE_TIR)]
    return liste


class VaguesEnnemis:
    def __init__(self, nb_bases_ennemis):
        self.num_vague = 0
        self.delay_vague_suivante = DELAY_ENTRE_VAGUES
        self.delay_actuel = 0
        self.nb_ennemi_par_vague = NB_ENNEMIS_PAR_VAGUE
        self.nb_bases_ennemis = nb_bases_ennemis
        self.nb_entrees_max = NB_ENTREES_MAX
        self.liste_vagues_a_rajouter = []
        self.init_liste_ennemis_a_rajouter()

    def init_liste_ennemis_a_rajouter(self):
        for _ in range(NB_VAGUES_ENNEMIS_INIT):
            for i in range(self.nb_bases_ennemis):
                liste_pararms_ennemis = []
                for _ in range(self.nb_ennemi_par_vague):
                    liste_pararms_ennemis.append(get_listes_valeurs_params_ennemi_aleatoire(self.nb_entrees_max))
                self.liste_vagues_a_rajouter.append((i, liste_pararms_ennemis))

    def new_vague(self):
        liste_pararms_ennemis = []
        for _ in range(self.nb_ennemi_par_vague):
            liste_pararms_ennemis.append(get_listes_valeurs_params_ennemi_aleatoire(self.nb_entrees_max))
        self.liste_vagues_a_rajouter.append((random.randint(0, self.nb_bases_ennemis - 1), liste_pararms_ennemis))

    def update(self):
        self.delay_actuel += 1
        if self.delay_actuel >= self.delay_vague_suivante:
            self.new_vague()
            self.delay_actuel = 0
