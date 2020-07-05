# coding: utf-8

from carte import *


def explosion_tireur(type_explosion, distance_centre, x_tireur, y_tireur, orientation_tireur):
    return Explosion(type_explosion, x_tireur + math.cos(orientation_tireur) * distance_centre,
                     y_tireur - math.sin(orientation_tireur) * distance_centre)


class Explosion:
    def __init__(self, type_explosion, x_centre, y_centre, direction=None):
        if direction is None:
            self.direction = random.randint(0, 360)
        else:
            self.direction = direction
        self.scale = DIC_EXPLOSIONS[PARAM_EXPLOSION_SCALE][type_explosion]
        self.images = [loaded_images(chemin) for chemin in DIC_EXPLOSIONS[PARAM_EXPLOSION_LISTE_IMAGES][type_explosion]]
        self.nb_tours_par_image = DIC_EXPLOSIONS[PARAM_EXPLOSION_NB_TOURS_PAR_IMAGE][type_explosion]
        self.nb_tours = 0
        self.num_image = 0
        self.ecran = pygame.transform.rotozoom(self.images[self.num_image], self.direction, self.scale)
        self.x = int(x_centre - self.ecran.get_width() / 2)
        self.y = int(y_centre - self.ecran.get_height() / 2)
        self.new_affichage = True
        self.fin = False

    def update(self):
        self.nb_tours += 1
        num_image = int(self.nb_tours / self.nb_tours_par_image)
        if not self.num_image == num_image:
            self.num_image = num_image
            if self.num_image >= len(self.images):
                self.fin = True
            else:
                self.new_affichage = True

    def update_affichage(self, carte: Carte):
        self.ecran = pygame.transform.rotozoom(self.images[self.num_image],
                                               self.direction, self.scale * carte.coef_zoom)

    def affiche(self, screen: pygame.Surface, carte: Carte):
        if self.new_affichage:
            self.update_affichage(carte)
        x, y = carte.xy_carte_to_xy_relatif(self.x, self.y)
        screen.blit(self.ecran, (x, y))
