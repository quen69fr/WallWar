# coding: utf-8

from constantes import *
import pygame.gfxdraw

dict_fonts = {}


def calcul_couleur(couleur_alpha: (tuple, int), couleur_fond: tuple):
    couleur, alpha = couleur_alpha
    coef = alpha / 255
    coef_fond = 1 - coef
    return [int(couleur[i] * coef + couleur_fond[i] * coef_fond) for i in range(3)]


liste_chemin_images = []
liste_images = []


def loaded_images(chemin):
    if chemin in liste_chemin_images:
        return liste_images[liste_chemin_images.index(chemin)]
    else:
        liste_chemin_images.append(chemin)
        liste_images.append(pygame.image.load(chemin))
        return liste_images[-1]


def affiche_texte(texte: str, x: int, y: int, screen: pygame.Surface, police=DEFAULT_POLICE, taille=30, couleur=NOIR,
                  x_0gauche_1centre_2droite=0, y_0haut_1centre_2bas=0):
    if police not in dict_fonts:
        dict_fonts[police] = {}
    if taille not in dict_fonts[police]:
        dict_fonts[police][taille] = pygame.font.Font(police, int(taille))
    font = dict_fonts[police][taille]

    surface = font.render(texte, True, couleur)
    if x_0gauche_1centre_2droite == 0 and y_0haut_1centre_2bas == 0:
        screen.blit(surface, (x, y))
    else:
        largeur, hauteur = surface.get_size()
        screen.blit(surface, (int(x - largeur * x_0gauche_1centre_2droite / 2),
                              int(y - hauteur * y_0haut_1centre_2bas / 2)))


def draw_filled_rect(screen: pygame.Surface, rect: (int, int, int, int), couleur: tuple or (tuple, int)):
    if len(couleur) == 2:
        rectangle = pygame.Surface((rect[2], rect[3]))
        rectangle.fill(couleur[0])
        rectangle.set_alpha(couleur[1])
        screen.blit(rectangle, (rect[0], rect[1]))
    else:
        pygame.draw.rect(screen, couleur, rect)


def draw_filled_circle(screen: pygame.Surface, pos: (int, int), rayon: int, couleur: tuple or (tuple, int)):
    if len(couleur) == 2:
        surface = pygame.Surface((rayon * 2, rayon * 2), pygame.SRCALPHA)
        couleur_4 = (couleur[0][0], couleur[0][1], couleur[0][2], couleur[1])
        pygame.draw.circle(surface, couleur_4, (rayon, rayon), rayon)
        screen.blit(surface, (pos[0] - rayon, pos[1] - rayon))
    else:
        rayon -= 1
        pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], rayon, couleur)
        pygame.gfxdraw.aacircle(screen, pos[0], pos[1], rayon, couleur)
