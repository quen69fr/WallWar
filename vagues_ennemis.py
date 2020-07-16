# coding: utf-8

from element import *


def get_valeur_param_ennemi(param, nb_entree):
    if param == PARAM_A_TIREUR_DELAY_TIR:
        return round(DIC_ENNEMIS[param][VALEUR_MIN] * DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN] /
                     (DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MAX] -
                     DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN]) /
                     DIC_ENNEMIS[param][ENTREE_MAX] * nb_entree + DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN], 1)
    else:
        return round((DIC_ENNEMIS[param][VALEUR_MAX] - DIC_ENNEMIS[param][VALEUR_MIN]) / DIC_ENNEMIS[param][ENTREE_MAX]
                     * nb_entree + DIC_ENNEMIS[param][VALEUR_MIN], 1)


class VaguesEnnemis:
    def __init__(self):
        self.num_vague = 0
        self.delay_vague_suivante = DELAY_ENTRE_VAGUES
        self.delay_actuelle = 0
