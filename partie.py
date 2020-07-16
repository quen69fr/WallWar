# coding: utf-8

from panneaux_monde import *


class Partie:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        if FULL_SCREEN:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        self.running = True
        self.monde = Monde(NB_CASE_X_GRILLE, NB_CASE_Y_GRILLE, COTE_CASES_GRILLE)
        self.panneaux_monde = PanneauxMonde(self.monde)
        self.x_souris, self.y_souris = pygame.mouse.get_pos()
        self.controle_presse = False

    def gere_eventements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.controle_presse = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.controle_presse = False
                elif event.key == KEY_TOUCHE_PAUSE:
                    self.monde.gere_touche_pause_enfoncee()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.monde.souris_sur_ecran(self.x_souris, self.y_souris):
                        self.monde.gere_clic_down(self.x_souris, self.y_souris)
                elif event.button == 4:
                    self.monde.gere_zoom(1, self.x_souris, self.y_souris)
                elif event.button == 5:
                    self.monde.gere_zoom(-1, self.x_souris, self.y_souris)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if self.monde.souris_sur_ecran(self.x_souris, self.y_souris):
                        if self.controle_presse:
                            self.monde.gere_ctrl_clic(self.x_souris, self.y_souris)
                        else:
                            self.monde.gere_clic(self.x_souris, self.y_souris)
                    elif self.panneaux_monde.souris_sur_panneau(self.x_souris, self.y_souris):
                        if self.controle_presse:
                            self.panneaux_monde.gere_ctrl_clic(self.x_souris, self.y_souris)
                        else:
                            self.panneaux_monde.gere_clic(self.x_souris, self.y_souris)
                elif event.button == pygame.BUTTON_RIGHT:
                    if self.monde.souris_sur_ecran(self.x_souris, self.y_souris):
                        self.monde.gere_clic_droit(self.x_souris, self.y_souris)

            elif event.type == pygame.MOUSEMOTION:
                self.x_souris, self.y_souris = pygame.mouse.get_pos()
                self.monde.gere_deplacement_souris(self.x_souris, self.y_souris)

    def update(self):
        self.gere_eventements()
        self.monde.update()
        self.panneaux_monde.update()

    def affiche(self):
        self.screen.fill(0)
        self.monde.affiche(self.screen)
        self.panneaux_monde.affiche(self.screen)
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
