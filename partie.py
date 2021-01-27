# coding: utf-8

from panneaux_monde import *


class Partie:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.fullscreen = FULL_SCREEN_INIT
        self.screen = None
        self.update_fullscreen()
        self.running = True
        self.monde = Monde(NB_CASE_X_GRILLE, NB_CASE_Y_GRILLE, COTE_CASES_GRILLE)
        self.panneaux_monde = PanneauxMonde(self.monde)
        self.x_souris, self.y_souris = pygame.mouse.get_pos()
        self.controle_presse = False
        self.compteur_couleur_fond = 0

    def quitter(self):
        self.running = False
        self.monde.thread_gere_cibles_actif = False
        pygame.quit()
        exit(0)

    def sauve(self):
        pass  # TODO

    def charge(self):
        pass  # TODO

    def update_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

    def change_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.update_fullscreen()

    def exec_action_menu(self, action):
        if action == ACTION_MENU_QUITTER:
            self.quitter()
        elif action == ACTION_MENU_FULLSCREEN:
            self.change_fullscreen()
        elif action == ACTION_MENU_PAUSE:
            self.monde.gere_touche_pause_enfoncee()
        elif action == ACTION_MENU_SAUVER:
            self.sauve()
        elif action == ACTION_MENU_CHARGER:
            self.charge()

    def gere_eventements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitter()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.controle_presse = True
                else:
                    for action in LISTE_ACTIONS_MENU:
                        if event.key == DIC_ACTION_MENU[PARAM_ACTION_MENU_KEY][action] \
                              and DIC_ACTION_MENU[PARAM_ACTION_MENU_CTRL][action] == self.controle_presse:
                            self.exec_action_menu(action)
                            break
                self.monde.gere_touche_enfoncee(event.key)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.controle_presse = False
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
                            action = self.panneaux_monde.pop_action_menu_a_exec()
                            if action is not None:
                                self.exec_action_menu(action)
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
        if self.monde.mode_pause:
            self.compteur_couleur_fond += 1
            if self.compteur_couleur_fond >= len(LISTE_COULEUR_FOND_ECRAN_PAUSE):
                self.compteur_couleur_fond = 0
            self.screen.fill(LISTE_COULEUR_FOND_ECRAN_PAUSE[self.compteur_couleur_fond])
        else:
            self.screen.fill(COULEUR_FOND_ECRAN)
        self.monde.affiche(self.screen)
        self.panneaux_monde.affiche(self.screen)
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
