# coding: utf-8

from panneau import *


def ecran_illustration_vierge(dimention_illustation):
    ecran_illustration = pygame.Surface(dimention_illustation)
    ecran_illustration.blit(loaded_images(CARTE_CHEMIN_IMAGE_FOND_PAVAGE_SABLE), (0, 0))
    return ecran_illustration


def illustration_batiment(type_batiment, dimention_illustation: (int, int), cote_case: int):
    largeur_ecran_illustration, hauteur_ecran_illustration = dimention_illustation
    ecran_illustration = ecran_illustration_vierge(dimention_illustation)

    x_centre_cases = int(largeur_ecran_illustration / 2 - cote_case / 2)
    y_centre_cases = int(hauteur_ecran_illustration / 2 - cote_case / 2)
    for i, j in Element.dic_elements[PARAM_F_BATIMENT_LISTE_CASES][type_batiment][TYPE_CASE_S_DEPOS]:
        draw_filled_rect(ecran_illustration, (x_centre_cases + i * cote_case,
                                              y_centre_cases + j * cote_case, cote_case, cote_case),
                         DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_DEPOS])
    for i, j in Element.dic_elements[PARAM_F_BATIMENT_LISTE_CASES][type_batiment][TYPE_CASE_S_RELAIS]:
        draw_filled_rect(ecran_illustration, (x_centre_cases + i * cote_case,
                                              y_centre_cases + j * cote_case, cote_case, cote_case),
                         DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_RELAIS])
    for n, (i, j) in enumerate(Element.dic_elements[PARAM_F_BATIMENT_LISTE_CASES][type_batiment][TYPE_CASE_PLEINE]):
        draw_filled_rect(ecran_illustration, (x_centre_cases + i * cote_case,
                                              y_centre_cases + j * cote_case, cote_case, cote_case),
                         Element.dic_elements[PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES][type_batiment][n])

    return ecran_illustration


def illustration_element_mobile(type_element_mobile, dimention_illustation: (int, int), marge: int):
    largeur_ecran_illustration, hauteur_ecran_illustration = dimention_illustation
    ecran_illustration = ecran_illustration_vierge(dimention_illustation)

    image_oribinale = loaded_images(Element.dic_elements[PARAM_F_ELEMENT_MOBILE_CHEMIN_IMAGE][type_element_mobile])
    largeur_image, hauteur_image = image_oribinale.get_size()
    scale = min((largeur_ecran_illustration - 2 * marge) / largeur_image,
                (hauteur_ecran_illustration - 2 * marge) / hauteur_image)

    image = pygame.transform.rotozoom(image_oribinale, 0, scale)
    x_image = int(largeur_ecran_illustration / 2 - image.get_width() / 2)
    y_image = int(hauteur_ecran_illustration / 2 - image.get_height() / 2)
    ecran_illustration.blit(image, (x_image, y_image))

    return ecran_illustration


def illustration_source(type_source, dimention_illustation: (int, int), marge):
    largeur_ecran_illustration, hauteur_ecran_illustration = dimention_illustation
    ecran_illustration = ecran_illustration_vierge(dimention_illustation)

    draw_filled_rect(ecran_illustration, (marge, marge, largeur_ecran_illustration - 2 * marge,
                                          hauteur_ecran_illustration - 2 * marge),
                     DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][DIC_SOURCES[PARAM_SOURCE_TYPE_RESSOURCE][type_source]])
    return ecran_illustration


class Vignette:
    def __init__(self, type_element, x: int, y: int, largeur: int, hauteur: int, illustration: pygame.Surface,
                 titre: str, prix_argent: int, prix_liquide: int, contours: int, couleur: tuple, taille_texte: int,
                 rayon: int):
        self.type_element = type_element
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

        self.ecran = illustration

        if not contours == 0:
            draw_filled_rect(self.ecran, (0, 0, self.largeur, contours), couleur)
            draw_filled_rect(self.ecran, (0, 0, contours, self.hauteur), couleur)
            draw_filled_rect(self.ecran, (0, self.hauteur - contours, self.largeur, self.hauteur), couleur)
            draw_filled_rect(self.ecran, (self.largeur - contours, 0, self.largeur, self.hauteur), couleur)

        x_centre = int(self.largeur / 2)
        affiche_texte(titre, x_centre, 4, self.ecran, x_0gauche_1centre_2droite=1, taille=taille_texte, couleur=couleur)

        marge = 4
        y = self.hauteur - rayon - marge
        draw_filled_circle(self.ecran, (rayon + marge, y), rayon,
                           DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_ARGENT])
        affiche_texte(str(prix_argent), 2 * rayon + marge + 2, y + 2,
                      self.ecran, taille=rayon * 2 + 2, couleur=COULEUR_COMPTENU_PANNEAU_CONSTRUCTION,
                      y_0haut_1centre_2bas=1)
        draw_filled_circle(self.ecran, (x_centre + rayon + marge, y), rayon,
                           DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_LIQUIDE])
        affiche_texte(str(prix_liquide), x_centre + 2 * rayon + marge + 2, y + 2, self.ecran, taille=rayon * 2 + 2,
                      couleur=COULEUR_COMPTENU_PANNEAU_CONSTRUCTION, y_0haut_1centre_2bas=1)

    def clic(self, x_souris: int, y_souris: int):
        return self.x <= x_souris <= self.x + self.largeur and self.y <= y_souris <= self.y + self.hauteur

    def affiche(self, screen: pygame.Surface):
        screen.blit(self.ecran, (self.x, self.y))


class PanneauClic(Panneau):
    def __init__(self, monde, x_ecran, y_ecran, largeur_ecran, hauteur_ecran):
        Panneau.__init__(self, monde, x_ecran, y_ecran, largeur_ecran, hauteur_ecran)

    def souris_sur_ecran(self, x_souris: int, y_souris: int):
        return self.x_ecran < x_souris < self.x_ecran + self.largeur_ecran \
               and self.y_ecran < y_souris < self.y_ecran + self.hauteur_ecran

    def gere_clic(self, x_souris: int, y_souris: int):
        pass
