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

# TODO :
# def draw_line(screen: pygame.Surface, pt1: (int, int), pt2: (int, int), largeur: int, couleur: tuple or (tuple, int)):
#     largeur_sur_deux = int(largeur / 2)
#     largeur_sur_deux_reste = largeur - largeur_sur_deux
#     dx = pt2[0] - pt1[0]
#     dy = pt2[1] - pt1[1]
#
#     if pt1[0] == pt2[0]:
#         p1 = (pt1[0] + largeur_sur_deux, pt1[1])
#         p2 = (pt1[0] - largeur_sur_deux_reste, pt1[1])
#         p3 = (pt2[0] + largeur_sur_deux, pt2[1])
#         p4 = (pt2[0] - largeur_sur_deux_reste, pt2[1])
#     elif pt1[1] == pt2[1]:
#         p1 = (pt1[0], pt1[1] + largeur_sur_deux)
#         p2 = (pt1[0], pt1[1] - largeur_sur_deux)
#         p3 = (pt2[0], pt2[1] + largeur_sur_deux)
#         p4 = (pt2[0], pt2[1] - largeur_sur_deux)
#     else:
#         cx = (pt1[0] + pt2[0]) / 2
#         cy = (pt1[1] + pt2[1]) / 2
#         longueur = math.sqrt(dx ** 2 + dy ** 2)
#         angle = math.atan(dy / dx)
#         p1 = (cx + (longueur / 2) * math.cos(angle) - (largeur / 2) * math.sin(angle),
#               cy + (largeur / 2) * math.cos(angle) + (longueur / 2) * math.sin(angle))
#         p2 = (cx - (longueur / 2) * math.cos(angle) - (largeur / 2) * math.sin(angle),
#               cy + (largeur / 2) * math.cos(angle) - (longueur / 2) * math.sin(angle))
#         p3 = (cx + (longueur / 2) * math.cos(angle) + (largeur / 2) * math.sin(angle),
#               cy - (largeur / 2) * math.cos(angle) + (longueur / 2) * math.sin(angle))
#         p4 = (cx - (longueur / 2) * math.cos(angle) + (largeur / 2) * math.sin(angle),
#               cy - (largeur / 2) * math.cos(angle) - (longueur / 2) * math.sin(angle))
#
#     m = 1
#     x_min = min(pt1[0], pt2[0])
#     y_min = min(pt1[1], pt2[1])
#     decalage = largeur_sur_deux + m
#     surface = pygame.Surface((abs(dx) + largeur + 2 * m, abs(dy) + largeur + 2 * m), pygame.SRCALPHA)
#     if len(couleur) == 2:
#         couleur = (couleur[0][0], couleur[0][1], couleur[0][2], couleur[1])
#     pygame.draw.polygon(surface, couleur, [(p[0] - x_min + decalage, p[1] - y_min + decalage)
#                                            for p in [p1, p2, p4, p3]])
#     screen.blit(surface, (x_min - decalage, y_min - decalage))
