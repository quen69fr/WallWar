# coding: utf-8

from panneau import *


class PanneauInfos(Panneau):
    def __init__(self, monde):
        Panneau.__init__(self, monde, X_PANNEAU_INFOS, Y_PANNEAU_INFOS, LARGEUR_PANNEAU_INFOS, HAUTEUR_PANNEAU_INFOS)
        self.monde = monde
        self.x, self.y = X_PANNEAU_INFOS, Y_PANNEAU_INFOS
        self.largeur, self.hauteur = LARGEUR_PANNEAU_INFOS, HAUTEUR_PANNEAU_INFOS

        self.ecran_base = pygame.Surface((self.largeur, self.hauteur))
        if CONTOURS_PANNEAU_INFOS == 0:
            self.ecran_base.fill(COULEUR_FOND_PANNEAUX)
        else:
            self.ecran_base.fill(COULEUR_COMPTENU_PANNEAU_INFOS)
            pygame.draw.rect(self.ecran_base, COULEUR_FOND_PANNEAUX,
                             (CONTOURS_PANNEAU_INFOS, CONTOURS_PANNEAU_INFOS,
                              self.largeur - 2 * CONTOURS_PANNEAU_INFOS, self.hauteur - 2 * CONTOURS_PANNEAU_INFOS))

        self.y_texte = int(self.hauteur / 2)

        larg = int((LARGEUR_PANNEAU_INFOS - 3 * ESPACEMENT_INFOS_PANNEAU_INFOS) / 3 - 5)
        draw_filled_circle(self.ecran_base, (ESPACEMENT_INFOS_PANNEAU_INFOS + RAYON_RESSOURCE_PANNEAU_INFOS,
                                             self.y_texte), RAYON_RESSOURCE_PANNEAU_INFOS - 1,
                           DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_ARGENT])
        draw_filled_circle(self.ecran_base, (ESPACEMENT_INFOS_PANNEAU_INFOS * 2 + larg + RAYON_RESSOURCE_PANNEAU_INFOS,
                                             self.y_texte), RAYON_RESSOURCE_PANNEAU_INFOS - 1,
                           DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_LIQUIDE])
        self.ecran_base.blit(loaded_images(PANNEAU_INFOS_CHEMIN_IMAGE_NB_PERSONNES),
                             (2 * larg + 3 * ESPACEMENT_INFOS_PANNEAU_INFOS,
                              self.y_texte - RAYON_RESSOURCE_PANNEAU_INFOS))

        self.x_val_argent = 2 * RAYON_RESSOURCE_PANNEAU_INFOS + 8
        self.x_val_liquide = self.x_val_argent + ESPACEMENT_INFOS_PANNEAU_INFOS + larg
        self.x_val_personnes = self.x_val_liquide + int(ESPACEMENT_INFOS_PANNEAU_INFOS / 2) + larg
        self.taille_texte = TAILLE_TEXTE_PANNEAU_INFOS

        self.ecran = self.ecran_base.copy()
        self.y_texte += 2
        self.val_argent_liquide_personnes_actuelles = 0, 0, 0, 0

    def update(self):
        argent = Batiment.argent_comptenu_relay_general
        liquide = Batiment.liquide_comptenu_general
        personnes = len(self.monde.liste_personnes)
        personnes_max = Batiment.nb_personne_max
        if not (argent, liquide, personnes) == self.val_argent_liquide_personnes_actuelles:
            self.new_affichage = True
            self.val_argent_liquide_personnes_actuelles = argent, liquide, personnes, personnes_max

    def update_affichage(self):
        self.ecran = self.ecran_base.copy()
        argent, liquide, personnes, personnes_max = self.val_argent_liquide_personnes_actuelles
        affiche_texte(str(argent), self.x_val_argent, self.y_texte, self.ecran, y_0haut_1centre_2bas=1,
                      taille=self.taille_texte if argent < 1000 else int(self.taille_texte * 0.75),
                      couleur=COULEUR_COMPTENU_PANNEAU_INFOS)
        affiche_texte(str(liquide), self.x_val_liquide, self.y_texte, self.ecran, y_0haut_1centre_2bas=1,
                      taille=self.taille_texte if liquide < 1000 else int(self.taille_texte * 0.75),
                      couleur=COULEUR_COMPTENU_PANNEAU_INFOS)
        affiche_texte(f'{personnes}/{personnes_max}', self.x_val_personnes, self.y_texte, self.ecran,
                      y_0haut_1centre_2bas=1, taille=self.taille_texte if personnes < 100 and personnes_max < 100 else
                      int(self.taille_texte * 0.75), couleur=COULEUR_COMPTENU_PANNEAU_INFOS if personnes < personnes_max
                      else COULEUR_COMPTENU_MAUVAIS_PANNEAU_INFOS)
