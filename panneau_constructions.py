# coding: utf-8

from panneau_clic import *


def vignette_batiment_panneau_construction(type_batiment, x: int, y: int, largeur: int, hauteur: int):
    illustration = illustration_batiment(type_batiment, (largeur, hauteur), PANNEAU_CONSTRUCTION_COTE_CASE_BATIMENT)

    return Vignette(type_batiment, x, y, largeur, hauteur, illustration,
                    Element.dic_elements[PARAM_F_NOM][type_batiment],
                    Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_batiment],
                    Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_batiment],
                    CONTOURS_PANNEAU_CONSTRUCTION, COULEUR_COMPTENU_PANNEAU_CONSTRUCTION,
                    TAILLE_TEXTE_PANNEAU_CONSTRUCTION, RAYON_RESSOURCE_PANNEAU_VIGNETTES)


class PanneauConstructions(PanneauClic):
    def __init__(self, monde):
        PanneauClic.__init__(self, monde, X_PANNEAU_CONSTRUCTION, Y_PANNEAU_CONSTRUCTION,
                             LARGEUR_PANNEAU_CONSTRUCTION, HAUTEUR_PANNEAU_CONSTRUCTION)
        self.vignettes_batiments = []
        self.dic_prix_affiches = {}
        self.init_vignettes_batiments()

    def update(self):
        for i, vignette in enumerate(self.vignettes_batiments):
            prix_actuel = \
                (Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][vignette.type_element],
                 Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][vignette.type_element])
            if not self.dic_prix_affiches[vignette.type_element] == prix_actuel:
                self.vignettes_batiments[i] = vignette_batiment_panneau_construction(vignette.type_element,
                                                                                     vignette.x, vignette.y,
                                                                                     vignette.largeur, vignette.hauteur)
                self.dic_prix_affiches[vignette.type_element] = prix_actuel
                self.new_affichage = True

    def init_vignettes_batiments(self):
        marge_vignettes_batiment = ESPACEMENT_VIGNETTES_BATIMENTS_PANNEAU_CONSTRUCTION
        distance_vignettes_batiment = (self.largeur_ecran -
                                       marge_vignettes_batiment) / NB_VIGNETTES_PANNEAU_CONSTRUCTION_LARGEUR
        largeur_vignettes_batiment = int(distance_vignettes_batiment - marge_vignettes_batiment)
        hauteur_vignettes_batiment = int((self.hauteur_ecran - marge_vignettes_batiment) /
                                         NB_VIGNETTES_PANNEAU_CONSTRUCTION_HAUTEUR) - marge_vignettes_batiment
        for i, type_batiment in enumerate(LISTE_TYPES_BATIMENTS_CONSTRUCTIBLE):
            y = int(marge_vignettes_batiment + (hauteur_vignettes_batiment + marge_vignettes_batiment)
                    * (i // NB_VIGNETTES_PANNEAU_CONSTRUCTION_LARGEUR))
            x = int((i % NB_VIGNETTES_PANNEAU_CONSTRUCTION_LARGEUR) * distance_vignettes_batiment
                    + marge_vignettes_batiment)
            self.vignettes_batiments.append(vignette_batiment_panneau_construction(type_batiment, x, y,
                                                                                   largeur_vignettes_batiment,
                                                                                   hauteur_vignettes_batiment))
            self.dic_prix_affiches[type_batiment] = \
                (Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_batiment],
                 Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_batiment])

    def gere_clic(self, x_souris: int, y_souris: int):
        for vignette_batiment in self.vignettes_batiments:
            if vignette_batiment.clic(x_souris - self.x_ecran, y_souris - self.y_ecran):
                self.monde.add_batiment_en_construction(vignette_batiment.type_element, x_souris, y_souris)
        return None

    def update_affichage(self):
        self.ecran.fill(COULEUR_FOND_PANNEAUX)
        for vignette_batiment in self.vignettes_batiments:
            vignette_batiment.affiche(self.ecran)
