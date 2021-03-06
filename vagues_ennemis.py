# coding: utf-8

from paramsEnnemi import *


class VaguesEnnemis:
    def __init__(self, nb_bases_ennemis):
        self.num_vague = 0
        self.delay_vague_suivante = DELAY_ENTRE_VAGUES
        self.nb_bases_ennemis = nb_bases_ennemis
        self.liste_vagues_a_rajouter = []
        self.stats_ennemis_morts = []
        self.init_liste_ennemis_a_rajouter()

    def init_liste_ennemis_a_rajouter(self):
        for _ in range(NB_VAGUES_ENNEMIS_INIT):
            for i in range(self.nb_bases_ennemis):
                self.num_vague += 1
                nb_entrees = NB_ENTREES_PAR_VAGUES[self.num_vague]
                liste_pararms_ennemis = []
                for _ in range(random.choice(NB_ENNEMIS_PAR_VAGUE_LISTE)):
                    liste_pararms_ennemis.append(ParamTireurEnnemi(nb_entrees + random.randint(0, NB_ENTREES_SUP_MAX)))
                self.liste_vagues_a_rajouter.append((i, liste_pararms_ennemis))

    def new_vague(self):
        self.num_vague += 1
        if len(NB_ENTREES_PAR_VAGUES) > self.num_vague:
            nb_entrees = NB_ENTREES_PAR_VAGUES[self.num_vague]
        else:
            nb_entrees = NB_ENTREES_PAR_VAGUES[-1]
        liste_pararms_ennemis = []
        if len(self.stats_ennemis_morts) <= 1 or random.randint(1, PROBA_VAGUE_NOUVELLE) == 1:
            for _ in range(random.choice(NB_ENNEMIS_PAR_VAGUE_LISTE)):
                liste_pararms_ennemis.append(ParamTireurEnnemi(nb_entrees + random.randint(0, NB_ENTREES_SUP_MAX)))
        else:
            nb_ennemi_par_vague = random.choice(NB_ENNEMIS_PAR_VAGUE_LISTE)
            nb_deuxieme = nb_ennemi_par_vague // 2
            nb_premier = nb_ennemi_par_vague - nb_deuxieme
            nb_troisieme = 0
            if len(self.stats_ennemis_morts) > 2:
                nb_troisieme = nb_deuxieme // 3
                nb_deuxieme -= nb_troisieme

            self.stats_ennemis_morts.sort(key=lambda ennemi: ennemi[0])
            for i in [0] * nb_premier + [1] * nb_deuxieme + [2] * nb_troisieme:
                liste_pararms_ennemis.append(ParamTireurEnnemi(nb_entrees + random.randint(0, NB_ENTREES_SUP_MAX),
                                                               NB_ENTREES_CHANGEES_PAR_VAGUES,
                                                               self.stats_ennemis_morts[i][1].dic_distribution_params))

            del self.stats_ennemis_morts[0]
            del self.stats_ennemis_morts[0]

        self.liste_vagues_a_rajouter.append((random.randint(0, self.nb_bases_ennemis - 1), liste_pararms_ennemis))

    def new_ennemi_stat(self, note, params: ParamTireurEnnemi):
        if note > 0:
            self.stats_ennemis_morts.append((note / sum(params.dic_distribution_params.values()), params))
            if len(self.stats_ennemis_morts) > NB_ENNEMIS_MEMOIRE_STATS:
                self.stats_ennemis_morts.remove(min(self.stats_ennemis_morts, key=lambda ennemi: ennemi[0]))

    def update(self):
        if self.nb_bases_ennemis > 0:
            self.delay_vague_suivante -= 1
            if self.delay_vague_suivante <= 0:
                self.new_vague()
                self.delay_vague_suivante = DELAY_ENTRE_VAGUES + random.randint(- VARIATION_MAX_DELAY_ENTRE_VAGUES,
                                                                                VARIATION_MAX_DELAY_ENTRE_VAGUES)
