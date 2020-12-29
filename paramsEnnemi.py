# coding: utf-8

from carte import *


class ParamTireurEnnemi:
    def __init__(self, nb_points_tot: int = 0, nb_points_changes: int = 0, dic_distribution_params: dict = None):
        nb_points_del = 0
        if dic_distribution_params is None:
            self.dic_distribution_params = {}
            for param in LISTE_PARAMS_ENNEMIS:
                self.dic_distribution_params[param] = 0
            nb_points_sup = nb_points_tot
        else:
            self.dic_distribution_params = dic_distribution_params
            nb_points_sup = nb_points_tot - sum(self.dic_distribution_params.values())
            if nb_points_sup < 0:
                nb_points_del = - nb_points_sup
                nb_points_sup = 0

        self.vie = None
        self.vitesse_deplacement = None
        self.force_tir = None
        self.portee_tir = None
        self.delay_tir = None
        self.portee_vision = None
        self.intelligence = None

        self.enleve_points(nb_points_changes + nb_points_del)
        self.ajoute_points(nb_points_sup + nb_points_changes)
        self.calcul_valeurs_params()

    def enleve_points(self, nb_points_sup):
        for _ in range(nb_points_sup):
            # if sum(self.dic_distribution_params.values()) > 0:
            ok = False
            while not ok:
                key = LISTE_PARAMS_ENNEMIS[random.randint(0, len(LISTE_PARAMS_ENNEMIS) - 1)]
                if self.dic_distribution_params[key] > 0:
                    self.dic_distribution_params[key] -= 1
                    ok = True

    def ajoute_points(self, nb_points_sup):
        for _ in range(nb_points_sup):
            ok = False
            while not ok:
                key = LISTE_PARAMS_ENNEMIS[random.randint(0, len(LISTE_PARAMS_ENNEMIS) - 1)]
                if self.dic_distribution_params[key] < DIC_ENNEMIS[key][ENTREE_MAX]:
                    self.dic_distribution_params[key] += 1
                    ok = True

    def calcul_valeurs_params(self):
        for key, value in self.dic_distribution_params.items():
            self.calcul_and_set_valeur_param(key, value)
        self.portee_vision += self.portee_tir

    def calcul_and_set_valeur_param(self, param, nb_entree):
        if param == PARAM_A_TIREUR_DELAY_TIR:
            valeur = round(DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN] * DIC_ENNEMIS[param][VALEUR_MIN] /
                           ((DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MAX] -
                            DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN]) / DIC_ENNEMIS[param][ENTREE_MAX] *
                            nb_entree + DIC_ENNEMIS[PARAM_A_TIREUR_FORCE_TIR][VALEUR_MIN]), 1)
        else:
            valeur = round(
                (DIC_ENNEMIS[param][VALEUR_MAX] - DIC_ENNEMIS[param][VALEUR_MIN]) / DIC_ENNEMIS[param][ENTREE_MAX]
                * nb_entree + DIC_ENNEMIS[param][VALEUR_MIN], 1)
            if param == PARAM_A_TIREUR_INTELLIGENCE:
                valeur = int(valeur)
        self.set_valeur_param(param, valeur)

    def set_valeur_param(self, param, valeur):
        if param == PARAM_A_VIES:
            self.vie = valeur
        elif param == PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT:
            self.vitesse_deplacement = valeur
        elif param == PARAM_A_TIREUR_FORCE_TIR:
            self.force_tir = valeur
        elif param == PARAM_A_TIREUR_PORTEE_TIR:
            self.portee_tir = valeur
        elif param == PARAM_A_TIREUR_DELAY_TIR:
            self.delay_tir = valeur
        elif param == PARAM_A_TIREUR_PORTEE_VISION:
            self.portee_vision = valeur
        else:
            self.intelligence = valeur
