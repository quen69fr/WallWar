# coding: utf-8

from panneau_clic import *


class ZoneClicable:
    def __init__(self, x: int, y: int, largeur: int, hauteur: int):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def clic(self, x_souris: int, y_souris: int):
        return self.x <= x_souris <= self.x + self.largeur and self.y <= y_souris <= self.y + self.hauteur

    def affiche(self, screen: pygame.Surface):
        pass


class VignetteElementVie(ZoneClicable):
    def __init__(self, element: ElementMobile or Batiment, x: int, y: int, largeur: int, hauteur: int):
        self.element = element
        ZoneClicable.__init__(self, x, y, largeur, hauteur)
        self.infos_vies = element.nb_vies, element.nb_vies_max

        self.hauteur_barre_texte = int(TAILLE_TEXTE_PANNEAU_SELECTION * self.hauteur / 100)

        if isinstance(element, ElementMobile):
            self.illustration = illustration_element_mobile(self.element.type, (largeur, hauteur),
                                                            int(self.hauteur_barre_texte * 1.1 +
                                                                MARGE_PANNEAU_SELECTION / 2))
        else:
            self.illustration = illustration_batiment(self.element.type, (largeur, hauteur),
                                                      int(hauteur / 9))

        self.ecran = pygame.Surface((largeur, hauteur))
        self.new_affichage = True

        contours = CONTOURS_BULLE_PANNEAU_SELECTION
        if contours > 0:
            couleur = COULEUR_COMPTENU_PANNEAU_SELECTION
            draw_filled_rect(self.illustration, (0, 0, self.largeur, contours), couleur)
            draw_filled_rect(self.illustration, (0, 0, contours, self.hauteur), couleur)
            draw_filled_rect(self.illustration, (0, self.hauteur - contours, self.largeur, self.hauteur), couleur)
            draw_filled_rect(self.illustration, (self.largeur - contours, 0, self.largeur, self.hauteur), couleur)

        x_centre = int(self.largeur / 2)
        affiche_texte(self.element.nom, x_centre, 4, self.illustration, x_0gauche_1centre_2droite=1,
                      taille=self.hauteur_barre_texte, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)

        self.ecran.blit(self.illustration, (0, 0))

    def update(self):
        new_infos_vies = self.element.nb_vies, self.element.nb_vies_max
        if not new_infos_vies == self.infos_vies:
            self.new_affichage = True
            self.infos_vies = new_infos_vies

    def update_affichage(self):
        # self.ecran.blit(self.illustration, (0, 0))
        hauteur = int(self.hauteur_barre_texte * 0.8)
        barre_vie = barre_avancement((self.largeur - 2 * MARGE_PANNEAU_SELECTION, hauteur),
                                     COULEUR_BARRES_VIE_PANNEAU_SELECTION,
                                     max(0, self.infos_vies[0]) / self.infos_vies[1],
                                     width=CONTOURS_BULLE_PANNEAU_SELECTION,
                                     couleur_bord=COULEUR_COMPTENU_PANNEAU_SELECTION)
        self.ecran.blit(barre_vie, (MARGE_PANNEAU_SELECTION, self.hauteur - MARGE_PANNEAU_SELECTION - hauteur))

    def affiche(self, screen: pygame.Surface):
        if self.new_affichage:
            self.update_affichage()
            self.new_affichage = False
        screen.blit(self.ecran, (self.x, self.y))


def barre_etapes_generale(screen: pygame.Surface, x: int, y: int, dimention: (int, int), couleur,
                          proportion_etape: float, numero_etape: int, width: int, couleur_bord_et_etiquette,
                          rayon_etiquette):
    largeur, hauteur = dimention
    proportion_etiquette = (4 * numero_etape - 3) / 17
    proportion_coloree = proportion_etiquette + 4 * proportion_etape / 17
    barre = barre_avancement(dimention, couleur, proportion_coloree, width, couleur_bord_et_etiquette)

    dx = 2 / 17 * largeur
    for i in range(4):
        x_i = (1 + i * 4) / 17 * largeur
        pygame.draw.line(barre, couleur_bord_et_etiquette, (x_i, 0), (x_i, hauteur), width)
        if i < numero_etape - 1 or (i == numero_etape - 1 and proportion_etape == 1):
            etiquette(barre, (i + 1), int(x_i + dx), int(hauteur / 2), int(rayon_etiquette * 0.7),
                      couleur_bord_et_etiquette)

    screen.blit(barre, (x, y))
    if not proportion_etape == 1:
        etiquette(screen, numero_etape, int(x + proportion_coloree * largeur), y + hauteur,
                  rayon_etiquette, couleur_bord_et_etiquette)


def barre_avancement(dimention: (int, int), couleur, proportion_coloree: float, width=0, couleur_bord=NOIR,
                     avancement_vertical=False, etiquette_simple: (str, tuple, int) = None):
    largeur, hauteur = dimention
    barre = pygame.Surface((largeur, hauteur))
    barre.blit(loaded_images(CARTE_CHEMIN_IMAGE_FOND_PAVAGE_SABLE), (0, 0))
    if proportion_coloree < 0:
        proportion_coloree = 0
    if avancement_vertical:
        dy = int(proportion_coloree * hauteur)
        draw_filled_rect(barre, (0, hauteur - dy, largeur, dy), couleur)
        if etiquette_simple is not None:
            texte, couleur, taille = etiquette_simple
            affiche_texte(texte, int(largeur / 2), hauteur - dy + (0 if taille + 8 > dy else 4),
                          barre, couleur=couleur, taille=taille, x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=2 if taille + 8 > dy else 0)
    else:
        dx = int(proportion_coloree * largeur)
        draw_filled_rect(barre, (0, 0, dx, hauteur), couleur)
        if etiquette_simple is not None:
            texte, couleur, taille = etiquette_simple
            affiche_texte(texte, dx, int(hauteur / 2), barre, couleur=couleur, taille=taille, y_0haut_1centre_2bas=1,
                          x_0gauche_1centre_2droite=2 if proportion_coloree > 0.5 else 0)
    if not width == 0:
        draw_filled_rect(barre, (0, 0, largeur, width), couleur_bord)
        draw_filled_rect(barre, (0, 0, width, hauteur), couleur_bord)
        draw_filled_rect(barre, (0, hauteur - width, largeur, hauteur), couleur_bord)
        draw_filled_rect(barre, (largeur - width, 0, largeur, hauteur), couleur_bord)
    return barre


def etiquette(screen: pygame.Surface, nb: int, x: int, y: int, rayon: int, couleur):
    draw_filled_circle(screen, (x, y), rayon + 1, couleur)
    draw_filled_circle(screen, (x, y), rayon - 1, COULEUR_FOND_PANNEAUX)
    affiche_texte(str(nb), x, y + 1, screen, taille=int(rayon * 1.5), couleur=couleur,
                  x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)


def vignette_construction_panneau_selection(type_element_mobile, x: int, y: int, largeur: int, hauteur: int):
    illustration = illustration_element_mobile(type_element_mobile, (largeur, hauteur), MARGE_PANNEAU_SELECTION * 2)

    return Vignette(type_element_mobile, x, y, largeur, hauteur, illustration,
                    Element.dic_elements[PARAM_F_NOM][type_element_mobile],
                    Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION][type_element_mobile],
                    Element.dic_elements[PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION][type_element_mobile],
                    CONTOURS_PANNEAU_INFOS, COULEUR_COMPTENU_PANNEAU_INFOS, int(TAILLE_TEXTE_PANNEAU_INFOS * 0.7),
                    RAYON_RESSOURCE_PANNEAU_VIGNETTES)


class BoutonImage(ZoneClicable):
    dic_ecrans = {}

    def __init__(self, x: int, y: int, largeur: int, hauteur: int, type_bouton, contours=0):
        ZoneClicable.__init__(self, x, y, largeur, hauteur)
        self.type = type_bouton
        chemin = DIC_CHEMIN_IMAGE_TYPE_BOUTON_IMAGE[type_bouton]
        if not (chemin, largeur, hauteur, contours) in BoutonImage.dic_ecrans:
            img = loaded_images(chemin)
            img_size = img.get_size()
            ecran = pygame.transform.rotozoom(img, 0, min((largeur + 1) / img_size[0], (hauteur + 1) / img_size[1]))
            contours = CONTOURS_BULLE_PANNEAU_SELECTION
            if contours > 0:
                couleur = COULEUR_COMPTENU_PANNEAU_SELECTION
                draw_filled_rect(ecran, (0, 0, self.largeur, contours), couleur)
                draw_filled_rect(ecran, (0, 0, contours, self.hauteur), couleur)
                draw_filled_rect(ecran, (0, self.hauteur - contours, self.largeur, self.hauteur), couleur)
                draw_filled_rect(ecran, (self.largeur - contours, 0, self.largeur, self.hauteur), couleur)
            BoutonImage.dic_ecrans[chemin, largeur, hauteur, contours] = ecran

        self.ecran = BoutonImage.dic_ecrans[chemin, largeur, hauteur, contours]

    def affiche(self, screen: pygame.Surface):
        screen.blit(self.ecran, (self.x, self.y))


class BoutonTexte(ZoneClicable):
    def __init__(self, x: int, y: int, largeur: int, hauteur: int, couleur, texte: str, taille_texte: int,
                 couleur_texte: tuple, param=''):
        ZoneClicable.__init__(self, x, y, largeur, hauteur)
        self.couleur = couleur
        self.texte = texte
        self.taille_texte = taille_texte
        self.couleur_texte = couleur_texte
        self.x_texte = int(x + largeur / 2)
        self.y_texte = int(y + hauteur / 2)
        self.param = param

    def affiche(self, screen: pygame.Surface):
        draw_filled_rect(screen, (self.x, self.y, self.largeur, self.hauteur), self.couleur)
        affiche_texte(self.texte, self.x_texte, self.y_texte, screen, taille=self.taille_texte,
                      couleur=self.couleur_texte, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)


def ecran_amelioration(largeur, hauteur, type_amelioration_presentee, grisee=False):
    ecran = pygame.Surface((largeur, hauteur))
    ecran.fill(COULEUR_FOND_PANNEAUX)
    contours = CONTOURS_BULLE_PANNEAU_SELECTION
    couleur = COULEUR_PANNEAU_SELECTION_FENETRE_GRISEE if grisee else COULEUR_COMPTENU_PANNEAU_SELECTION
    if contours > 0:
        draw_filled_rect(ecran, (0, 0, largeur, contours), couleur)
        draw_filled_rect(ecran, (0, 0, contours, hauteur), couleur)
        draw_filled_rect(ecran, (0, hauteur - contours, largeur, hauteur), couleur)
        draw_filled_rect(ecran, (largeur - contours, 0, largeur, hauteur), couleur)
    affiche_texte(Amelioreur.dic_ameliorations[PARAM_AMELIORATION_NOM][type_amelioration_presentee],
                  int(largeur * COEF_PROPORTION_TITRE_ARGENT_PANNEAU_AMELIORATION / 2 + MARGE_PANNEAU_SELECTION),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.95),
                  couleur=couleur, x_0gauche_1centre_2droite=1)

    prix_argent = Amelioreur.dic_ameliorations[PARAM_AMELIORATION_PRIX_ARGENT][type_amelioration_presentee]
    prix_liquide = Amelioreur.dic_ameliorations[PARAM_AMELIORATION_PRIX_LIQUIDE][type_amelioration_presentee]

    marge = int(MARGE_PANNEAU_SELECTION / 2)
    rayon = RAYON_RESSOURCE_PANNEAU_VIGNETTES
    x_min = int(COEF_PROPORTION_TITRE_ARGENT_PANNEAU_AMELIORATION * largeur)
    y_centre = int((MARGE_PANNEAU_SELECTION + TAILLE_TEXTE_PANNEAU_SELECTION) / 2)
    x_centre = int(x_min + (largeur - x_min) / 2)
    draw_filled_circle(ecran, (x_min + rayon + marge, y_centre), rayon,
                       couleur=(couleur if grisee else DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_ARGENT]))
    affiche_texte(str(prix_argent), x_min + 2 * rayon + marge + 2, y_centre + 2,
                  ecran, taille=int(rayon * 2 + 2), couleur=couleur,
                  y_0haut_1centre_2bas=1)
    draw_filled_circle(ecran, (x_centre + rayon + marge, y_centre), rayon,
                       couleur=(couleur if grisee else DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_LIQUIDE]))
    affiche_texte(str(prix_liquide), x_centre + 2 * rayon + marge + 2, y_centre + 2, ecran,
                  taille=int(rayon * 2 + 2), couleur=couleur, y_0haut_1centre_2bas=1)

    liste_textes_ameliorations = []
    for i, affichage in enumerate(
            Amelioreur.dic_ameliorations[PARAM_AMELIORATION_LISTE_TPV_AFFICHAGE][type_amelioration_presentee]):
        if affichage:
            type_e, param_a, new_value = \
                Amelioreur.dic_ameliorations[PARAM_AMELIORATION_LISTE__TYPE_PARAM_VALUE][type_amelioration_presentee][i]
            nom_element = Element.dic_elements[PARAM_F_NOM][type_e]

            ancienne_valeur = Element.dic_elements[param_a][type_e]
            if (type(ancienne_valeur) == int or type(ancienne_valeur) == float) and \
                    (type(new_value) == int or type(new_value) == float):
                if new_value >= ancienne_valeur:
                    valeur = f'{round(ancienne_valeur, 1)} + {round(new_value - ancienne_valeur, 1)}'
                else:
                    valeur = f'{round(ancienne_valeur, 1)} - {round(ancienne_valeur - new_value, 1)}'
            else:
                valeur = new_value
            texte = DIC_TEXTE_PARAM_PANNEAU_INFOS_ELEMENT_SELECT[param_a](valeur)
            texte = texte[0].lower() + texte[1:]
            liste_textes_ameliorations.append(f'{nom_element}, {texte}')
    hauteur_titre = int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.5)
    y = hauteur_titre + (hauteur - hauteur_titre) / 2
    dy = int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.2)
    if len(liste_textes_ameliorations) > 3:
        dy = int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.94)
    y = int(y - dy * (len(liste_textes_ameliorations) - 1) / 2)
    for texte in liste_textes_ameliorations:
        affiche_texte(texte, marge, y, ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.8),
                      couleur=couleur, y_0haut_1centre_2bas=1)
        y += dy

    return ecran


class PanneauConstructionAmeliorationBatiment(PanneauClic):
    ecran_informations = None
    ecran_construction = None
    ecran_amelioration = None
    hauteur_bandeau = None
    rect = None
    rect_centre = None
    liste_positions_vignettes = None
    dimention_vignettes = None
    liste_position_illustrations_en_attente = None
    dimention_illustrations_en_attente = None
    rect_barre_construction = None
    position_illustration_construction = None
    rect_barre_amelioration = None
    rect_presentation_amelioration = None
    bouton_amelioration = None
    bouton_amelioration_stop = None
    largeur_vignette_cible = None

    def __init__(self, monde: Monde, batiment_selectionne, centre=False):
        if centre:
            x, y, largeur, hauteur = PanneauConstructionAmeliorationBatiment.rect_centre
        else:
            x, y, largeur, hauteur = PanneauConstructionAmeliorationBatiment.rect
        PanneauClic.__init__(self, monde, x, y, largeur, hauteur)

        self.batiment = batiment_selectionne

        self.mon_ecran_construction = pygame.Surface((largeur, hauteur))
        self.mon_ecran_amelioration = pygame.Surface((largeur, hauteur))
        self.mon_ecran_information = pygame.Surface((largeur, hauteur))
        self.ecran_base = self.mon_ecran_information
        self.vignettes = []
        self.construction_actif = (self.batiment.constructeur is not None)
        self.amelioreur_actif = (self.batiment.amelioreur is not None)
        self.type_amelioration_presentee = None
        self.ecran_amelioration_presentee = None
        self.etat_batiment_infos = None
        self.etat_et_vignette_info_cible_ecran_information = None, None
        self.init_mon_ecran_construction()
        self.init_mon_ecran_amelioration()
        self.mon_ecran_information.blit(self.ecran_informations, (0, 0))

    def init_mon_ecran_construction(self):
        self.mon_ecran_construction.blit(self.ecran_construction, (0, 0))
        if self.construction_actif:
            largeur, hauteur = self.dimention_vignettes
            liste_vigentte_type_construction = self.batiment.constructeur.liste_constructions_possibles[:]
            self.vignettes = [vignette_construction_panneau_selection(type_construction,
                                                                      self.liste_positions_vignettes[i][0],
                                                                      self.liste_positions_vignettes[i][1],
                                                                      largeur, hauteur)
                              for i, type_construction in enumerate(liste_vigentte_type_construction)]
            for vignette in self.vignettes:
                vignette.affiche(self.mon_ecran_construction)
        else:
            x_centre = int(self.rect[2] / 2)
            dy = TAILLE_TEXTE_PANNEAU_SELECTION + MARGE_PANNEAU_SELECTION
            y = int(self.hauteur_bandeau + (self.rect[3] - self.hauteur_bandeau) / 2 -
                    dy * (len(TEXTE_AUCUNE_CONSTRUCTION_POSSIBLE) - 1) / 2)
            for texte in TEXTE_AUCUNE_CONSTRUCTION_POSSIBLE:
                affiche_texte(texte, x_centre, y, self.mon_ecran_construction,
                              taille=TAILLE_TEXTE_PANNEAU_SELECTION,
                              couleur=COULEUR_SECONDAIRE_COMPTENU_PANNEAU_SELECTION,
                              x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
                y += dy

    def init_mon_ecran_amelioration(self):
        self.mon_ecran_amelioration.blit(self.ecran_amelioration, (0, 0))
        if self.amelioreur_actif:
            x_rect, y_rect, largeur_rect, hauteur_rect = self.rect_presentation_amelioration
            dx = int(self.largeur_ecran / 2 + largeur_rect / 2) / 2
            x_centre = int(x_rect + largeur_rect / 2)
            y_centre = int(y_rect + hauteur_rect / 2)
            for sens in [-1, 1]:
                x = int(x_centre - sens * (dx + TAILLE_FLECHES_AMELIORATIONS / 3))
                p1 = x + sens * TAILLE_FLECHES_AMELIORATIONS, y_centre - sens * TAILLE_FLECHES_AMELIORATIONS
                p2 = x, y_centre
                p3 = p1[0], y_centre + sens * TAILLE_FLECHES_AMELIORATIONS
                pygame.draw.line(self.mon_ecran_amelioration, NOIR, p1, p2, 3)
                pygame.draw.line(self.mon_ecran_amelioration, NOIR, p2, p3, 3)
        else:
            x_centre = int(self.rect[2] / 2)
            dy = TAILLE_TEXTE_PANNEAU_SELECTION + MARGE_PANNEAU_SELECTION
            y = int(self.hauteur_bandeau + (self.rect[3] - self.hauteur_bandeau) / 2 -
                    dy * (len(TEXTE_AUCUNE_AMELIORATION_POSSIBLE) - 1) / 2)
            for texte in TEXTE_AUCUNE_AMELIORATION_POSSIBLE:
                affiche_texte(texte, x_centre, y, self.mon_ecran_amelioration,
                              taille=TAILLE_TEXTE_PANNEAU_SELECTION,
                              couleur=COULEUR_SECONDAIRE_COMPTENU_PANNEAU_SELECTION,
                              x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
                y += dy

    def gere_clic(self, x_souris: int, y_souris: int):
        # if self.souris_sur_ecran(x_souris, y_souris):
        y_relatif = y_souris - self.y_ecran
        x_relatif = x_souris - self.x_ecran
        if 0 <= y_relatif <= self.hauteur_bandeau:
            if x_relatif > self.largeur_ecran * 2 / 3:
                if not self.ecran_base == self.mon_ecran_amelioration:
                    self.ecran_base = self.mon_ecran_amelioration
                    if self.batiment.amelioreur is not None:
                        if self.batiment.amelioreur.type_amelioration_en_cours is None:
                            self.type_amelioration_presentee = self.batiment.amelioreur.liste_ameliorations_possibles[0]
                        else:
                            self.type_amelioration_presentee = self.batiment.amelioreur.type_amelioration_en_cours
                        self.ecran_amelioration_presentee = None
                    self.new_affichage = True
            elif x_relatif < self.largeur_ecran / 3:
                if not self.ecran_base == self.mon_ecran_construction:
                    self.ecran_base = self.mon_ecran_construction
                    self.new_affichage = True
            else:
                if not self.ecran_base == self.mon_ecran_information:
                    self.ecran_base = self.mon_ecran_information
                    self.new_affichage = True
        else:
            if self.construction_actif and self.ecran_base == self.mon_ecran_construction:
                for vignette in self.vignettes:
                    if vignette.clic(x_relatif, y_relatif):
                        self.batiment.ajoute_construction_constructeur(vignette.type_element)
                        return
                largeur, hauteur = self.dimention_illustrations_en_attente
                for i, (x, y) in enumerate(self.liste_position_illustrations_en_attente):
                    if i >= len(self.batiment.constructeur.liste_type_elements_en_attente):
                        break
                    if x <= x_relatif <= x + largeur and y <= y_relatif <= y + hauteur:
                        self.batiment.annule_construction_constructeur(i)
                        return
            elif self.amelioreur_actif and self.ecran_base == self.mon_ecran_amelioration:
                if self.batiment.amelioreur.type_amelioration_en_cours is None:
                    if self.bouton_amelioration.clic(x_relatif, y_relatif):
                        self.batiment.lance_amelioration_amelioreur(self.type_amelioration_presentee)
                    else:
                        x, y, largeur, hauteur = self.rect_presentation_amelioration
                        if y < y_relatif < y + hauteur and \
                                len(self.batiment.amelioreur.liste_ameliorations_possibles) > 1:
                            if x_relatif < x:
                                i = self.batiment.amelioreur.liste_ameliorations_possibles.index(
                                    self.type_amelioration_presentee)
                                if i > 0:
                                    self.type_amelioration_presentee = \
                                        self.batiment.amelioreur.liste_ameliorations_possibles[i - 1]
                                    self.ecran_amelioration_presentee = None
                                    self.new_affichage = True
                            elif x_relatif > x + largeur:
                                i = self.batiment.amelioreur.liste_ameliorations_possibles.index(
                                    self.type_amelioration_presentee)
                                if i < len(self.batiment.amelioreur.liste_ameliorations_possibles) - 1:
                                    self.type_amelioration_presentee = \
                                        self.batiment.amelioreur.liste_ameliorations_possibles[i + 1]
                                    self.ecran_amelioration_presentee = None
                                    self.new_affichage = True
                else:
                    if self.bouton_amelioration.clic(x_relatif, y_relatif):
                        self.batiment.annule_amelioration_en_cours()
            elif self.ecran_base == self.mon_ecran_information:
                vignette = self.etat_et_vignette_info_cible_ecran_information[1]
                # if vignette is not None:
                if vignette is not None and isinstance(vignette, VignetteElementVie) \
                        and vignette.clic(x_relatif, y_relatif):
                    self.monde.element_selectionne = vignette.element

    def update(self):
        if self.ecran_base == self.mon_ecran_information:
            liste_params_infos_batiment = LISTE_PARAM_PANNEAU_INFOS_BATIMENT_PEUT_TIRER if self.batiment.peut_tirer \
                else (LISTE_PARAM_PANNEAU_INFOS_BATIMENT if not self.batiment.liste_cases_regen_relatives
                      else LISTE_PARAM_PANNEAU_INFOS_BATIMENT_REGEN)
            etat_batiment_infos = [self.batiment.get_value_param(param) for param in liste_params_infos_batiment]
            if self.batiment.peut_tirer:
                etat_batiment_infos += [self.batiment.tireur.nb_destructions]
                if not self.etat_et_vignette_info_cible_ecran_information == self.batiment.tireur.cible:
                    if self.batiment.tireur.cible is None:
                        self.etat_et_vignette_info_cible_ecran_information = \
                            self.batiment.tireur.cible, self.etat_et_vignette_info_cible_ecran_information[1]
                    else:
                        self.etat_et_vignette_info_cible_ecran_information = self.batiment.tireur.cible, None
            if not etat_batiment_infos == self.etat_batiment_infos:
                self.etat_batiment_infos = etat_batiment_infos
                self.new_affichage = True
        elif self.ecran_base == self.mon_ecran_construction:
            if self.construction_actif:
                if self.batiment.constructeur.new_type_element_en_construction:
                    self.init_mon_ecran_construction()
                    self.batiment.constructeur.new_type_element_en_construction = False
                    self.new_affichage = True
                    self.batiment.constructeur.new_affichage = False
                elif self.batiment.constructeur.new_affichage:
                    self.new_affichage = True
                    self.batiment.constructeur.new_affichage = False
        else:
            if not self.amelioreur_actif:
                if self.batiment.amelioreur is not None:
                    self.init_mon_ecran_amelioration()
                    self.amelioreur_actif = True
                    if self.batiment.amelioreur.type_amelioration_en_cours is None:
                        self.type_amelioration_presentee = self.batiment.amelioreur.liste_ameliorations_possibles[0]
                    else:
                        self.type_amelioration_presentee = self.batiment.amelioreur.type_amelioration_en_cours
                    self.ecran_amelioration_presentee = None
                    self.new_affichage = True
            if self.amelioreur_actif:
                if self.batiment.amelioreur is None:
                    self.amelioreur_actif = False
                    self.init_mon_ecran_amelioration()
                    self.new_affichage = True
                else:
                    if self.batiment.amelioreur.new_affichage:
                        if self.batiment.amelioreur.type_amelioration_en_cours is None:
                            self.type_amelioration_presentee = self.batiment.amelioreur.liste_ameliorations_possibles[0]
                            self.ecran_amelioration_presentee = None
                        self.batiment.amelioreur.new_affichage = False
                        self.new_affichage = True

    def update_affichage(self):
        self.ecran.blit(self.ecran_base, (0, 0))
        if self.ecran_base == self.mon_ecran_information:
            self.update_affichage_informations()
        elif self.ecran_base == self.mon_ecran_construction:
            if self.construction_actif:
                self.update_affichage_construction_active()
        else:
            if self.amelioreur_actif:
                self.update_affichage_amelioreur_actif()

    def update_affichage_informations(self):
        self.mon_ecran_information.blit(self.ecran_informations, (0, 0))
        x_centre = int(self.largeur_ecran / 2)
        if self.batiment.peut_tirer:
            x_centre_texte_cible = int(MARGE_PANNEAU_SELECTION + self.largeur_vignette_cible / 2)
            y_texte_cible = int(self.hauteur_bandeau + MARGE_PANNEAU_SELECTION * 0.8)
            affiche_texte(TEXTE_PANNEAU_SELECTION_CIBLE, x_centre_texte_cible, y_texte_cible, self.ecran,
                          taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.1),
                          couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1)
            x_centre = int((self.largeur_ecran - MARGE_PANNEAU_SELECTION - self.largeur_vignette_cible) / 2
                           + MARGE_PANNEAU_SELECTION + self.largeur_vignette_cible)

            y_texte_en_tout = y_texte_cible + self.largeur_vignette_cible + MARGE_PANNEAU_SELECTION * 0.6
            # affiche_texte(TEXTE_PANNEAU_SELECTION_EN_TOUT, x_centre_texte_cible, y_texte_en_tout,
            #               self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.9), x_0gauche_1centre_2droite=1,
            #               couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)
            affiche_texte(str(self.batiment.tireur.nb_destructions) + ' ' +
                          TEXTE_PANNEAU_SELECTION_NB_VICTIMES_SOLDAT, x_centre_texte_cible,
                          int(y_texte_en_tout + MARGE_PANNEAU_SELECTION * 0.2 + TAILLE_TEXTE_PANNEAU_SELECTION * 0.9),
                          self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.9), x_0gauche_1centre_2droite=1,
                          couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)
            self.ecran.blit(ecran_illustration_vierge((self.largeur_vignette_cible, self.largeur_vignette_cible)),
                            (MARGE_PANNEAU_SELECTION, int(self.hauteur_bandeau + TAILLE_TEXTE_PANNEAU_SELECTION +
                                                          MARGE_PANNEAU_SELECTION)))
            self.etat_et_vignette_info_cible_ecran_information = (self.etat_et_vignette_info_cible_ecran_information[0],
                                                                  None)

        dy = int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.3)
        liste_params_infos_batiment = LISTE_PARAM_PANNEAU_INFOS_BATIMENT_PEUT_TIRER if self.batiment.peut_tirer \
            else (LISTE_PARAM_PANNEAU_INFOS_BATIMENT if not self.batiment.liste_cases_regen_relatives
                  else LISTE_PARAM_PANNEAU_INFOS_BATIMENT_REGEN)
        y = self.hauteur_bandeau + (self.hauteur_ecran - self.hauteur_bandeau) / 2
        y = int(y - dy * (len(liste_params_infos_batiment) - 1) / 2)
        for param in liste_params_infos_batiment:
            val = self.batiment.get_value_param(param)
            if val is None:
                val = '/'
            texte = DIC_TEXTE_PARAM_PANNEAU_INFOS_ELEMENT_SELECT[param](val)
            affiche_texte(texte, x_centre, y,
                          self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.9),
                          couleur=COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=1)
            y += dy

    def update_affichage_amelioreur_actif(self):
        if self.ecran_amelioration_presentee is None:
            self.update_affichage_amelioreur_presentation_amelioration()
        self.ecran.blit(self.ecran_amelioration_presentee, (0, 0))
        self.update_affichage_amelioreur_barre_avancement()
        if self.batiment.amelioreur.type_amelioration_en_cours is None:
            self.bouton_amelioration.affiche(self.ecran)
        else:
            self.bouton_amelioration_stop.affiche(self.ecran)

    def update_affichage_amelioreur_presentation_amelioration(self):
        self.ecran_amelioration_presentee = pygame.Surface((self.largeur_ecran, self.hauteur_ecran))
        self.ecran_amelioration_presentee.blit(self.mon_ecran_amelioration, (0, 0))
        x, y, largeur, hauteur = self.rect_presentation_amelioration
        grisee = (self.type_amelioration_presentee in Amelioreur.liste_types_ameliorations_en_cours and
                  not self.batiment.amelioreur.type_amelioration_en_cours == self.type_amelioration_presentee)
        presentation = ecran_amelioration(largeur, hauteur, self.type_amelioration_presentee, grisee)
        self.ecran_amelioration_presentee.blit(presentation, (x, y))

    def update_affichage_amelioreur_barre_avancement(self):
        type_amelioration_en_cours = self.batiment.amelioreur.type_amelioration_en_cours
        x_barre, y_barre, largeur_barre, hauteur_barre = self.rect_barre_amelioration
        if type_amelioration_en_cours is not None:
            rapport = (self.batiment.amelioreur.avancement_amelioration /
                       self.batiment.amelioreur.avancement_ameliration_max)
            pourcentage = int(rapport * 100)
            barre_amelioration = barre_avancement((largeur_barre, hauteur_barre),
                                                  COULEUR_BARRE_ETAPE_NEUTRE_PANNEAU_CONSTRUCTION,
                                                  rapport, width=CONTOURS_BULLE_PANNEAU_SELECTION,
                                                  couleur_bord=COULEUR_COMPTENU_PANNEAU_SELECTION)
            self.ecran.blit(barre_amelioration, (x_barre, y_barre))

            affiche_texte(f'{pourcentage}%', int(x_barre + largeur_barre / 2), int(y_barre + hauteur_barre / 2 + 2),
                          self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4), x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=1, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)
        else:
            barre_amelioration = barre_avancement((largeur_barre, hauteur_barre),
                                                  COULEUR_BARRE_ETAPE_NEUTRE_PANNEAU_CONSTRUCTION,
                                                  0, width=CONTOURS_BULLE_PANNEAU_SELECTION,
                                                  couleur_bord=COULEUR_COMPTENU_PANNEAU_SELECTION)
            self.ecran.blit(barre_amelioration, (x_barre, y_barre))

    def update_affichage_construction_active(self):
        x_carre_illustration, y_carre_illustration = self.position_illustration_construction
        x_barre, y_barre, largeur_barre, hauteur_barre = self.rect_barre_construction

        type_construction_en_cours = self.batiment.constructeur.type_element_en_construction
        if type_construction_en_cours is not None:
            rapport = min((self.batiment.constructeur.avancement_construction /
                           self.batiment.constructeur.avancement_construction_max, 0.99))
            illustration = illustration_element_mobile(type_construction_en_cours, (COTE_CARRE_ILLUSTRATION,
                                                                                    COTE_CARRE_ILLUSTRATION),
                                                       int(MARGE_PANNEAU_SELECTION * 0.5))
            pourcentage = int(rapport * 100)
        else:
            rapport = 0
            illustration = ecran_illustration_vierge((COTE_CARRE_ILLUSTRATION, COTE_CARRE_ILLUSTRATION))
            pourcentage = None

        barre_construction = barre_avancement((largeur_barre, hauteur_barre),
                                              COULEUR_BARRE_ETAPE_NEUTRE_PANNEAU_CONSTRUCTION,
                                              rapport, width=CONTOURS_BULLE_PANNEAU_SELECTION,
                                              couleur_bord=COULEUR_COMPTENU_PANNEAU_SELECTION)

        nb = COTE_CARRE_ILLUSTRATION - CONTOURS_BULLE_PANNEAU_SELECTION
        pygame.draw.polygon(illustration, COULEUR_COMPTENU_PANNEAU_SELECTION, [(0, 0), (0, nb), (nb, nb), (nb, 0)],
                            CONTOURS_BULLE_PANNEAU_SELECTION)

        self.ecran.blit(barre_construction, (x_barre, y_barre))
        self.ecran.blit(illustration, (x_carre_illustration, y_carre_illustration))
        if pourcentage is not None:
            affiche_texte(f'{pourcentage}%', int(x_barre + largeur_barre / 2),
                          int(y_barre + hauteur_barre / 2 + 2), self.ecran,
                          taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4), x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=1, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)

        largeur_illustr, hauteur_illustr = self.dimention_illustrations_en_attente
        for i, (x, y) in enumerate(self.liste_position_illustrations_en_attente):
            if len(self.batiment.constructeur.liste_type_elements_en_attente) > i:
                illustr = illustration_element_mobile(self.batiment.constructeur.liste_type_elements_en_attente[i],
                                                      (largeur_illustr, hauteur_illustr), 2)
            else:
                illustr = ecran_illustration_vierge((largeur_illustr, hauteur_illustr))
                affiche_texte(str(i + 1), int(largeur_illustr / 2), int(hauteur_illustr / 2 + 2), illustr,
                              taille=largeur_illustr * 0.9, couleur=COULEUR_TEXTE_SUR_SABLE,
                              x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
            self.ecran.blit(illustr, (x, y))

    def update_et_affiche_vignette_cible(self):
        if self.batiment.tireur.cible is None:
            if self.etat_et_vignette_info_cible_ecran_information[1] is not None:
                self.etat_et_vignette_info_cible_ecran_information = None, None
                self.ecran.blit(ecran_illustration_vierge((self.largeur_vignette_cible, self.largeur_vignette_cible)),
                                (MARGE_PANNEAU_SELECTION, int(self.hauteur_bandeau + TAILLE_TEXTE_PANNEAU_SELECTION
                                                              + MARGE_PANNEAU_SELECTION)))
        else:
            if self.etat_et_vignette_info_cible_ecran_information[1] is None:
                vignette = VignetteElementVie(self.batiment.tireur.cible, MARGE_PANNEAU_SELECTION,
                                              int(self.hauteur_bandeau + TAILLE_TEXTE_PANNEAU_SELECTION +
                                                  MARGE_PANNEAU_SELECTION), self.largeur_vignette_cible,
                                              self.largeur_vignette_cible)
                self.etat_et_vignette_info_cible_ecran_information = (self.batiment.tireur.cible, vignette)

        vignette = self.etat_et_vignette_info_cible_ecran_information[1]
        # if vignette is not None:
        if vignette is not None and isinstance(vignette, VignetteElementVie):
            vignette.update()
            if vignette.new_affichage:
                vignette.affiche(self.ecran)

    def affiche(self, screen: pygame.Surface):
        if self.new_affichage:
            self.update_affichage()
            self.new_affichage = False
        if self.batiment.tireur is not None and self.ecran_base == self.mon_ecran_information:
            self.update_et_affiche_vignette_cible()
        screen.blit(self.ecran, (self.x_ecran, self.y_ecran))


def init_panneau_construction_amelioration(rect_bulle: (int, int, int, int), pos_bulle: (int, int)):
    x_rect, y_rect, largeur_rect, hauteur_rect = rect_bulle
    x_rect += pos_bulle[0]
    y_rect += pos_bulle[1]

    x = MARGE_PANNEAU_SELECTION * 3 + DIMENTION_BARRES_PANNEAU_SELECTION[1]
    y = int(TAILLE_TEXTE_PANNEAU_SELECTION * 2.2 + MARGE_PANNEAU_SELECTION * 3.5 +
            DIMENTION_BARRES_VIE_PANNEAU_SELECTION[1])
    largeur = int(largeur_rect - x - 1.5 * MARGE_PANNEAU_SELECTION)
    hauteur = hauteur_rect - y - MARGE_PANNEAU_SELECTION
    x += x_rect
    y += y_rect

    PanneauConstructionAmeliorationBatiment.rect = (x, y, largeur, hauteur)
    PanneauConstructionAmeliorationBatiment.rect_centre = (x_rect + int(largeur_rect - largeur) / 2,
                                                           y, largeur, hauteur)

    largeur_sur_trois = int(largeur / 3)
    hauteur_bandeau = int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.2)
    taille_texte = int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.95)
    PanneauConstructionAmeliorationBatiment.hauteur_bandeau = hauteur_bandeau

    largeur_diminuee = largeur - CONTOURS_BULLE_PANNEAU_SELECTION
    hauteur_diminuee = hauteur - CONTOURS_BULLE_PANNEAU_SELECTION
    largeur_sur_trois_diminuee = int(largeur_sur_trois - CONTOURS_BULLE_PANNEAU_SELECTION / 2)

    PanneauConstructionAmeliorationBatiment.largeur_vignette_cible = int(hauteur - hauteur_bandeau -
                                                                         MARGE_PANNEAU_SELECTION -
                                                                         TAILLE_TEXTE_PANNEAU_SELECTION * 2.3)

    # L'ecran construction
    PanneauConstructionAmeliorationBatiment.ecran_construction = pygame.Surface((largeur, hauteur))
    PanneauConstructionAmeliorationBatiment.ecran_construction.fill(COULEUR_FOND_PANNEAUX)
    draw_filled_rect(PanneauConstructionAmeliorationBatiment.ecran_construction,
                     (largeur_sur_trois, 0, largeur - largeur_sur_trois, hauteur_bandeau),
                     COULEUR_PANNEAU_SELECTION_FENETRE_GRISEE)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_CONSTRUCTION, int(largeur / 6),
                  int(MARGE_PANNEAU_SELECTION / 2), PanneauConstructionAmeliorationBatiment.ecran_construction,
                  taille=taille_texte, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_AMELIORATION, int(largeur * 5 / 6),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, PanneauConstructionAmeliorationBatiment.ecran_construction,
                  taille=int(taille_texte * 0.95), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_INFORMATIONS, int(largeur / 2),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, PanneauConstructionAmeliorationBatiment.ecran_construction,
                  taille=int(taille_texte * 0.95), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    pygame.draw.polygon(PanneauConstructionAmeliorationBatiment.ecran_construction,
                        COULEUR_COMPTENU_PANNEAU_SELECTION, [(0, 0),
                                                             (largeur_sur_trois_diminuee, 0),
                                                             (largeur_sur_trois_diminuee, hauteur_bandeau),
                                                             (largeur_diminuee, hauteur_bandeau),
                                                             (largeur_diminuee, hauteur_diminuee),
                                                             (0, hauteur_diminuee)],
                        CONTOURS_BULLE_PANNEAU_SELECTION)

    # Illustrations vignette
    marge_l = MARGE_PANNEAU_SELECTION - 2
    marge_h = MARGE_PANNEAU_SELECTION
    largeur_vignette = int((largeur - DIMENTION_CONSTRUCTION_EN_ATTENTE[0] - 5 * marge_l - 3) / 3)
    hauteur_vignette = hauteur - hauteur_bandeau - 2 * marge_h - DIMENTION_BARRES_PANNEAU_SELECTION[1]
    pos_vignettes = [(largeur - (marge_l + largeur_vignette) * (i + 1) - 2, hauteur - hauteur_vignette - marge_h)
                     for i in range(NB_CONSTRUCTION_POSSIBLE_MAX)]
    PanneauConstructionAmeliorationBatiment.dimention_vignettes = (largeur_vignette, hauteur_vignette)
    PanneauConstructionAmeliorationBatiment.liste_positions_vignettes = pos_vignettes

    # Barre construction et illustration construction
    largeur_en_attente, hauteur_en_attente = DIMENTION_CONSTRUCTION_EN_ATTENTE
    y_en_attente = hauteur - MARGE_PANNEAU_SELECTION - hauteur_en_attente
    x_carre_illustration = int(largeur_en_attente / 2 - COTE_CARRE_ILLUSTRATION / 2
                               + MARGE_PANNEAU_SELECTION)
    y_carre_illustration = y_en_attente - MARGE_PANNEAU_SELECTION - COTE_CARRE_ILLUSTRATION + 2
    x_barre = x_carre_illustration + COTE_CARRE_ILLUSTRATION - 2
    y_barre = hauteur_bandeau + MARGE_PANNEAU_SELECTION
    hauteur_barre = DIMENTION_BARRES_VIE_PANNEAU_SELECTION[1]
    largeur_barre = largeur - x_barre - MARGE_PANNEAU_SELECTION

    PanneauConstructionAmeliorationBatiment.rect_barre_construction = (x_barre, y_barre, largeur_barre, hauteur_barre)
    PanneauConstructionAmeliorationBatiment.position_illustration_construction = (x_carre_illustration,
                                                                                  y_carre_illustration)

    # Illustrations en attente
    marge = int(MARGE_PANNEAU_SELECTION * 0.75)
    largeur_illustrations = int((DIMENTION_CONSTRUCTION_EN_ATTENTE[0] - marge *
                                 (NB_CONSTRUCTION_EN_ATTENTE_PAR_LIGNE - 1)) / NB_CONSTRUCTION_EN_ATTENTE_PAR_LIGNE)
    nb_construction_colone = math.ceil(NB_CONSTRUCTION_EN_ATTENTE_MAX / NB_CONSTRUCTION_EN_ATTENTE_PAR_LIGNE)
    hauteur_illustrations = int((DIMENTION_CONSTRUCTION_EN_ATTENTE[1] - marge * (nb_construction_colone - 1)) /
                                nb_construction_colone)
    x_0 = MARGE_PANNEAU_SELECTION
    y_0 = hauteur - DIMENTION_CONSTRUCTION_EN_ATTENTE[1] - MARGE_PANNEAU_SELECTION + 1
    liste = []
    for y in range(nb_construction_colone):
        for x in range(NB_CONSTRUCTION_EN_ATTENTE_PAR_LIGNE):
            liste.append((x_0 + x * (largeur_illustrations + marge), y_0 + y * (hauteur_illustrations + marge)))
    PanneauConstructionAmeliorationBatiment.liste_position_illustrations_en_attente = liste
    PanneauConstructionAmeliorationBatiment.dimention_illustrations_en_attente = (largeur_illustrations,
                                                                                  hauteur_illustrations)

    # L'ecran amelioration
    PanneauConstructionAmeliorationBatiment.ecran_amelioration = pygame.Surface((largeur, hauteur))
    PanneauConstructionAmeliorationBatiment.ecran_amelioration.fill(COULEUR_FOND_PANNEAUX)
    draw_filled_rect(PanneauConstructionAmeliorationBatiment.ecran_amelioration,
                     (0, 0, largeur - largeur_sur_trois, hauteur_bandeau), COULEUR_PANNEAU_SELECTION_FENETRE_GRISEE)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_CONSTRUCTION, int(largeur / 6),
                  int(MARGE_PANNEAU_SELECTION / 2), PanneauConstructionAmeliorationBatiment.ecran_amelioration,
                  taille=int(taille_texte * 0.95), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_AMELIORATION, int(largeur * 5 / 6),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, PanneauConstructionAmeliorationBatiment.ecran_amelioration,
                  taille=taille_texte, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_INFORMATIONS, int(largeur / 2),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, PanneauConstructionAmeliorationBatiment.ecran_amelioration,
                  taille=int(taille_texte * 0.95), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    pygame.draw.polygon(PanneauConstructionAmeliorationBatiment.ecran_amelioration,
                        COULEUR_COMPTENU_PANNEAU_SELECTION, [(0, hauteur_bandeau),
                                                             (largeur_diminuee - largeur_sur_trois_diminuee,
                                                              hauteur_bandeau),
                                                             (largeur_diminuee - largeur_sur_trois_diminuee, 0),
                                                             (largeur_diminuee, 0),
                                                             (largeur_diminuee, hauteur_diminuee),
                                                             (0, hauteur_diminuee)],
                        CONTOURS_BULLE_PANNEAU_SELECTION)

    # largeur_bouton, hauteur_bouton = DIMENTION_BOUTON_AMELIORATION
    PanneauConstructionAmeliorationBatiment.rect_barre_amelioration = (MARGE_PANNEAU_SELECTION, y_barre,
                                                                       largeur - hauteur_barre + 1 -
                                                                       3 * MARGE_PANNEAU_SELECTION, hauteur_barre)
    x_presentation_amelioration = int(largeur / 2 - LARGEUR_PANNEAU_INFOS_AMELIORATION / 2)
    y_presentation_amelioration = y_barre + hauteur_barre + MARGE_PANNEAU_SELECTION - 1
    hauteur_presentation_amelioration = hauteur - y_presentation_amelioration - MARGE_PANNEAU_SELECTION
    PanneauConstructionAmeliorationBatiment.rect_presentation_amelioration = \
        (x_presentation_amelioration, y_presentation_amelioration,
         LARGEUR_PANNEAU_INFOS_AMELIORATION, hauteur_presentation_amelioration)
    PanneauConstructionAmeliorationBatiment.bouton_amelioration = \
        BoutonTexte(largeur - hauteur_barre - MARGE_PANNEAU_SELECTION, y_barre, hauteur_barre, hauteur_barre,
                    COULEUR_BOUTONS_PANNEAU_SELECTION, TEXTE_BOUTON_AMELIORATION,
                    TAILLE_TEXTE_PANNEAU_SELECTION, COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION)
    PanneauConstructionAmeliorationBatiment.bouton_amelioration_stop = \
        BoutonTexte(PanneauConstructionAmeliorationBatiment.bouton_amelioration.x,
                    PanneauConstructionAmeliorationBatiment.bouton_amelioration.y, hauteur_barre, hauteur_barre,
                    COULEUR_BOUTONS_PANNEAU_SELECTION, TEXTE_BOUTON_AMELIORATION_STOP,
                    TAILLE_TEXTE_PANNEAU_SELECTION, COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION)

    # L'ecran informations
    PanneauConstructionAmeliorationBatiment.ecran_informations = pygame.Surface((largeur, hauteur))
    PanneauConstructionAmeliorationBatiment.ecran_informations.fill(COULEUR_FOND_PANNEAUX)
    draw_filled_rect(PanneauConstructionAmeliorationBatiment.ecran_informations,
                     (0, 0, largeur_sur_trois, hauteur_bandeau),
                     COULEUR_PANNEAU_SELECTION_FENETRE_GRISEE)
    draw_filled_rect(PanneauConstructionAmeliorationBatiment.ecran_informations,
                     (largeur - largeur_sur_trois, 0, largeur_sur_trois, hauteur_bandeau),
                     COULEUR_PANNEAU_SELECTION_FENETRE_GRISEE)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_CONSTRUCTION, int(largeur / 6),
                  int(MARGE_PANNEAU_SELECTION / 2), PanneauConstructionAmeliorationBatiment.ecran_informations,
                  taille=int(taille_texte * 0.95), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_AMELIORATION, int(largeur * 5 / 6),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, PanneauConstructionAmeliorationBatiment.ecran_informations,
                  taille=int(taille_texte * 0.95), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    affiche_texte(TEXTE_PANNEAU_SELECTION_FENETRE_INFORMATIONS, int(largeur / 2),
                  int(MARGE_PANNEAU_SELECTION / 2) - 1, PanneauConstructionAmeliorationBatiment.ecran_informations,
                  taille=taille_texte, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                  x_0gauche_1centre_2droite=1)
    pygame.draw.polygon(PanneauConstructionAmeliorationBatiment.ecran_informations,
                        COULEUR_COMPTENU_PANNEAU_SELECTION, [(0, hauteur_bandeau),
                                                             (largeur_sur_trois_diminuee, hauteur_bandeau),
                                                             (largeur_sur_trois_diminuee, 0),
                                                             (largeur_diminuee - largeur_sur_trois_diminuee, 0),
                                                             (largeur_diminuee - largeur_sur_trois_diminuee,
                                                              hauteur_bandeau),
                                                             (largeur_diminuee, hauteur_bandeau),
                                                             (largeur_diminuee, hauteur_diminuee),
                                                             (0, hauteur_diminuee)],
                        CONTOURS_BULLE_PANNEAU_SELECTION)


class PanneauInfosSelectionElementMobile(PanneauClic):
    def __init__(self, monde, x, y: int, hauteur: int):
        PanneauClic.__init__(self, monde, x + X_PANNEAU_INFOS_ELEMENT_MOBILE, y,
                             LARGEUR_PANNEAU_INFOS_ELEMENT_MOBILE, hauteur)
        self.ecran_base = pygame.Surface((LARGEUR_PANNEAU_INFOS_ELEMENT_MOBILE, hauteur))
        self.init_ecran_base()
        self.element_selectionne = None
        self.etat_element_selectionne = None
        self.doit_s_afficher = False
        self.update()

    def init_ecran_base(self):
        self.ecran_base.fill(COULEUR_FOND_PANNEAUX)
        contours = CONTOURS_BULLE_PANNEAU_SELECTION
        if contours > 0:
            couleur = COULEUR_COMPTENU_PANNEAU_SELECTION
            draw_filled_rect(self.ecran_base, (0, 0, self.largeur_ecran, contours), couleur)
            draw_filled_rect(self.ecran_base, (0, 0, contours, self.hauteur_ecran), couleur)
            draw_filled_rect(self.ecran_base, (0, self.hauteur_ecran - contours,
                                               self.largeur_ecran, self.hauteur_ecran), couleur)
            draw_filled_rect(self.ecran_base, (self.largeur_ecran - contours, 0,
                                               self.largeur_ecran, self.hauteur_ecran), couleur)
        affiche_texte(TEXTE_TITRE_PANNEAU_INFOS_ELEMENT_MOBILE, int(self.largeur_ecran / 2),
                      TAILLE_TEXTE_PANNEAU_SELECTION, self.ecran_base, taille=TAILLE_TEXTE_PANNEAU_SELECTION,
                      couleur=COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1,
                      y_0haut_1centre_2bas=1)

    def update(self):
        if not self.element_selectionne == self.monde.element_selectionne:
            self.element_selectionne = self.monde.element_selectionne
            if isinstance(self.element_selectionne, Porteur) or isinstance(self.element_selectionne, Soldat) or \
                    isinstance(self.element_selectionne, Ennemi):
                self.doit_s_afficher = True
            else:
                self.doit_s_afficher = False
        if self.doit_s_afficher:
            etat_element_selectionne = None
            if isinstance(self.element_selectionne, ElementMobile):
                if isinstance(self.element_selectionne, Ennemi):
                    liste_params = LISTE_PARAM_PANNEAU_INFOS_ENNEMIS
                else:
                    type_class_element_selec = \
                        Element.dic_elements[PARAM_F_PERSONNE_TYPE_CLASS][self.element_selectionne.type]
                    liste_params = DIC_LISTE_PARAM_PANNEAU_INFOS_PERSONNES[type_class_element_selec]
                etat_element_selectionne = [self.element_selectionne.get_value_param(param) for param in
                                            liste_params]

            if not etat_element_selectionne == self.etat_element_selectionne:
                self.etat_element_selectionne = etat_element_selectionne
                self.new_affichage = True

    def update_affichage(self):
        self.ecran.blit(self.ecran_base, (0, 0))
        y = TAILLE_TEXTE_PANNEAU_SELECTION + MARGE_PANNEAU_SELECTION * 0.5
        y = y + (self.hauteur_ecran - y) / 2
        if isinstance(self.element_selectionne, Ennemi):
            liste_params = LISTE_PARAM_PANNEAU_INFOS_ENNEMIS
        else:
            type_class_element_selec = \
                Element.dic_elements[PARAM_F_PERSONNE_TYPE_CLASS][self.element_selectionne.type]
            liste_params = DIC_LISTE_PARAM_PANNEAU_INFOS_PERSONNES[type_class_element_selec]
        dy = int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.15) if len(liste_params) > 6 else \
            int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.3)
        y = int(y - dy * (len(liste_params) - 1) / 2)
        for param in liste_params:
            val = self.element_selectionne.get_value_param(param)
            if val is None:
                val = '/'
            texte = DIC_TEXTE_PARAM_PANNEAU_INFOS_ELEMENT_SELECT[param](val)
            affiche_texte(texte, int(self.largeur_ecran / 2), y,
                          self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 0.9),
                          couleur=COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=1)
            y += dy


class PanneauSelection(PanneauClic):
    def __init__(self, monde):
        PanneauClic.__init__(self, monde, X_PANNEAU_ACTIONS, Y_PANNEAU_ACTIONS,
                             LARGEUR_PANNEAU_ACTIONS, HAUTEUR_PANNEAU_ACTIONS)

        self.ecran_base = pygame.Surface((self.largeur_ecran, self.hauteur_ecran))
        self.new_affichage_base = True
        self.rect_bulle = (0, 0, 0, 0)

        self.element_selectionne = None
        self.etat_element_selectionne = None
        self.liste_boutons_ecran = []
        self.liste_vigettes_ecran_base = []
        self.panneau_construction_amelioration_batiments: PanneauConstructionAmeliorationBatiment or None = None
        self.panneau_infos_selection_element_mobile: PanneauInfosSelectionElementMobile or None = None
        self.liste_boutons_menu = []
        self.init_liste_boutons_menu()

        self.action_menu_a_exec = None

    def init_liste_boutons_menu(self):
        marge = MARGE_GENERALE
        largeur = self.largeur_ecran - 4 * marge
        hauteur = (self.hauteur_ecran - 2 * marge) // (len(LISTE_ACTIONS_MENU) + 1) - marge
        x = marge * 2
        y = marge
        for action in LISTE_ACTIONS_MENU:
            y += hauteur + marge
            self.liste_boutons_menu.append((action, BoutonTexte(x, y, largeur, hauteur, COULEUR_BOUTONS_ACTIONS_MENU,
                                                                DIC_ACTION_MENU[PARAM_ACTION_MENU_TEXTE][action],
                                                                int(TAILLE_TEXTE_PANNEAU_SELECTION * 2.5),
                                                                COULEUR_COMPTENU_PANNEAU_SELECTION)))

    def gere_clic(self, x_souris: int, y_souris: int):
        if self.panneau_construction_amelioration_batiments is not None and \
                self.panneau_construction_amelioration_batiments.souris_sur_ecran(x_souris, y_souris):
            self.panneau_construction_amelioration_batiments.gere_clic(x_souris, y_souris)
        else:
            x_souris_relatif, y_souris_relatif = x_souris - self.x_ecran, y_souris - self.y_ecran
            if self.element_selectionne is None:
                for action, bouton in self.liste_boutons_menu:
                    if bouton.clic(x_souris_relatif, y_souris_relatif):
                        self.action_menu_a_exec = action
                        break
            else:
                for bouton in self.liste_boutons_ecran:
                    if bouton.clic(x_souris_relatif, y_souris_relatif):
                        if isinstance(self.element_selectionne, Batiment):
                            if self.element_selectionne.etape_construction < \
                                    self.element_selectionne.etape_construction_max:
                                self.monde.annule_batiment_en_cours_de_construction_selectionne()
                        elif isinstance(self.element_selectionne, ElementMobile):
                            if isinstance(bouton, VignetteElementVie):
                                self.monde.element_selectionne = bouton.element
                            elif isinstance(bouton, BoutonImage):
                                if bouton.type == TYPE_BOUTON_IMAGE_STOP:
                                    self.element_selectionne.stop()
                                elif bouton.type == TYPE_BOUTON_IMAGE_IMMOBILE and \
                                        isinstance(self.element_selectionne, Soldat):
                                    self.element_selectionne.immobilise()
                        elif type(self.element_selectionne) == list:
                            if bouton.type == TYPE_BOUTON_IMAGE_STOP:
                                self.monde.stop_selection()
                            elif bouton.type == TYPE_BOUTON_IMAGE_IMMOBILE:
                                self.monde.immobilise_selection()
                        return
                for vignette in self.liste_vigettes_ecran_base:
                    if vignette.clic(x_souris_relatif, y_souris_relatif):
                        self.monde.element_selectionne = vignette.element
                        return

    def gere_ctrl_clic(self, x_souris: int, y_souris: int):
        x_souris_relatif, y_souris_relatif = x_souris - self.x_ecran, y_souris - self.y_ecran
        for vignette in self.liste_vigettes_ecran_base:
            if vignette.clic(x_souris_relatif, y_souris_relatif):
                self.monde.element_selectionne.remove(vignette.element)
                if len(self.monde.element_selectionne) == 1:
                    self.monde.element_selectionne = self.monde.element_selectionne[0]
                break

    def update(self):
        if self.panneau_construction_amelioration_batiments is not None:
            self.panneau_construction_amelioration_batiments.update()
        if self.panneau_infos_selection_element_mobile is not None:
            self.panneau_infos_selection_element_mobile.update()
        if not self.new_affichage_base:
            if type(self.monde.element_selectionne) == list:
                element_selectionne = self.monde.element_selectionne[:]
            else:
                element_selectionne = self.monde.element_selectionne
            if element_selectionne is None:
                element_selectionne = self.monde.batiment_en_construction

            if not self.element_selectionne == element_selectionne:
                self.element_selectionne = element_selectionne
                self.new_affichage_base = True

        if self.new_affichage_base or not self.new_affichage:
            if isinstance(self.element_selectionne, Batiment):
                if self.element_selectionne.etape_construction < self.element_selectionne.etape_construction_max:
                    liquide = None
                    if not self.element_selectionne.fixe and \
                            Batiment.liquide_comptenu_general < self.element_selectionne.prix_liquide:
                        liquide = Batiment.liquide_comptenu_general
                    etat_batiment = (self.element_selectionne.argent_comptenu,
                                     self.element_selectionne.etape_construction,
                                     self.element_selectionne.fixe, liquide,
                                     self.element_selectionne.liste_cases_interdites_constuction)
                else:
                    etat_batiment = (self.element_selectionne.nb_vies_max,
                                     self.element_selectionne.argent_comptenu_max,
                                     self.element_selectionne.argent_comptenu,
                                     self.element_selectionne.nb_vies)

                if not self.etat_element_selectionne == etat_batiment:
                    self.new_affichage = True
                    self.etat_element_selectionne = etat_batiment

            elif isinstance(self.element_selectionne, Porteur):
                etat_porteur = (self.element_selectionne.ressource_comptenu,
                                self.element_selectionne.type_ressource_comptenu,
                                self.element_selectionne.objectif is None,
                                self.element_selectionne.nb_vies_max,
                                self.element_selectionne.ressource_comptenu_max,
                                self.element_selectionne.nb_vies,
                                self.element_selectionne.dic_nb_ressources_transportees_en_tout)
                if not self.etat_element_selectionne == etat_porteur:
                    self.new_affichage = True
                    self.etat_element_selectionne = etat_porteur

            elif isinstance(self.element_selectionne, Soldat):
                etat_soldat = (self.element_selectionne.nb_vies,
                               self.element_selectionne.nb_vies_max,
                               self.element_selectionne.objectif is None and self.element_selectionne.cible is None,
                               self.element_selectionne.cible,
                               self.element_selectionne.tireur.nb_destructions)
                if not self.etat_element_selectionne == etat_soldat:
                    self.new_affichage = True
                    self.etat_element_selectionne = etat_soldat

            elif isinstance(self.element_selectionne, Ennemi):
                etat_ennemi = (self.element_selectionne.nb_vies,
                               self.element_selectionne.nb_vies_max,
                               self.element_selectionne.objectif is None and self.element_selectionne.cible is None,
                               self.element_selectionne.cible,
                               self.element_selectionne.tireur.nb_destructions)
                if not self.etat_element_selectionne == etat_ennemi:
                    self.new_affichage = True
                    self.etat_element_selectionne = etat_ennemi

            elif isinstance(self.element_selectionne, Source):
                etat_source = self.element_selectionne.ressource_comptenu
                if not self.etat_element_selectionne == etat_source:
                    self.new_affichage = True
                    self.etat_element_selectionne = etat_source

    def update_affichage(self):
        self.ecran.blit(self.ecran_base, (0, 0))
        self.liste_boutons_ecran = []
        if type(self.element_selectionne) == list:
            marge = MARGE_PANNEAU_SELECTION
            taille = int(TAILLE_TEXTE_PANNEAU_SELECTION * 2.5 * 1.5 - marge)
            self.liste_boutons_ecran.append(BoutonImage(marge, marge, taille, taille, TYPE_BOUTON_IMAGE_STOP))
            affiche_bouton_immobile = False
            for element in self.element_selectionne:
                if isinstance(element, Soldat):
                    affiche_bouton_immobile = True
                    break
            if affiche_bouton_immobile:
                self.liste_boutons_ecran.append(BoutonImage(marge * 2 + taille, marge, taille, taille,
                                                            TYPE_BOUTON_IMAGE_IMMOBILE))
        elif self.element_selectionne is not None:
            x, y, largeur, hauteur = self.rect_bulle
            x_centre = int(x + largeur / 2)

            titre = ''
            if isinstance(self.element_selectionne, Element):
                largeur_barre_vie, hauteur_barre_vie = DIMENTION_BARRES_VIE_PANNEAU_SELECTION
                y_barre_vie = int(y + TAILLE_TEXTE_PANNEAU_SELECTION * 2.2 + MARGE_PANNEAU_SELECTION * 2)

                affiche_vie = True
                infos_barre_ressource = None
                if isinstance(self.element_selectionne, Batiment):
                    if self.element_selectionne.etape_construction < self.element_selectionne.etape_construction_max:
                        titre = TEXTE_PANNEAU_SELECTION_BATIMENT_EN_CONSTRUCTION
                        affiche_vie = False
                        texte_precision = ''
                        if self.element_selectionne.fixe:
                            if self.element_selectionne.argent_comptenu >= 0:
                                numero_etape = 4
                                texte_etape = TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_4
                                proportion_etape = (self.element_selectionne.etape_construction /
                                                    self.element_selectionne.etape_construction_max)
                                couleur_barre = COULEUR_BARRE_ETAPE_NEUTRE_PANNEAU_CONSTRUCTION
                            else:
                                numero_etape = 3
                                texte_etape = TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_3
                                proportion_etape = 1 + (self.element_selectionne.argent_comptenu /
                                                        self.element_selectionne.prix_construction)
                                couleur_barre = DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_ARGENT]
                                texte_precision = str(self.element_selectionne.argent_comptenu)

                            largeur_bouton, hauteur_bouton = DIMENTION_BOUTON_ANNULER_CONSTRUCTION_PANNEAU_SELECTION
                            self.liste_boutons_ecran.append(
                                BoutonTexte(x + largeur - MARGE_PANNEAU_SELECTION - largeur_bouton,
                                            y + hauteur - MARGE_PANNEAU_SELECTION - hauteur_bouton,
                                            largeur_bouton, hauteur_bouton, COULEUR_BOUTONS_PANNEAU_SELECTION,
                                            TEXTE_BOUTON_ANNULER_CONSTRUCTION_PANNEAU_SELECTION,
                                            int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.5),
                                            COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION))
                        else:
                            if Batiment.liquide_comptenu_general >= self.element_selectionne.prix_liquide:
                                numero_etape = 2
                                texte_etape = TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_2
                                proportion_etape = (1 - (len(self.element_selectionne.liste_cases_interdites_constuction
                                                             ) / self.element_selectionne.nb_cases)) * 0.99
                                couleur_barre = DIC_CASES_SPECIALES[PARAM_CASE_S_COULEUR][TYPE_CASE_S_POSSIBLE]
                            else:
                                numero_etape = 1
                                texte_etape = TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_1
                                proportion_etape = (Batiment.liquide_comptenu_general /
                                                    self.element_selectionne.prix_liquide)
                                couleur_barre = DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][TYPE_RESSOURCE_LIQUIDE]
                                texte_precision = str(Batiment.liquide_comptenu_general -
                                                      self.element_selectionne.prix_liquide)

                        rayon_etiquette = RAYON_ETIQUETTE_ETAPES_CONSTRUCTION_PANNEAU_SELECTION
                        n_barre_generale = MARGE_ET_HAUTEUR_BARRE_CONSTRUCTION_GENERALE_PANNEAU_SELECTION
                        y_barre = int(y + TAILLE_TEXTE_PANNEAU_SELECTION * 2.2 + MARGE_PANNEAU_SELECTION * 2.5)
                        barre_etapes_generale(self.ecran, n_barre_generale + x, y_barre,
                                              (int(largeur - 2 * n_barre_generale), n_barre_generale),
                                              COULEUR_BARRE_ETAPE_NEUTRE_PANNEAU_CONSTRUCTION, proportion_etape,
                                              numero_etape, CONTOURS_BULLE_PANNEAU_SELECTION,
                                              COULEUR_COMPTENU_PANNEAU_SELECTION, rayon_etiquette)

                        y_centre_texte_etape = int(y_barre + n_barre_generale + MARGE_PANNEAU_SELECTION * 2 +
                                                   TAILLE_TEXTE_PANNEAU_SELECTION * 1.4)
                        affiche_texte(f'      {texte_etape}', x + MARGE_PANNEAU_SELECTION, y_centre_texte_etape,
                                      self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4),
                                      couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, y_0haut_1centre_2bas=1)
                        etiquette(self.ecran, numero_etape, int(x + 2 * MARGE_PANNEAU_SELECTION + rayon_etiquette / 2),
                                  y_centre_texte_etape, rayon_etiquette, COULEUR_COMPTENU_PANNEAU_SELECTION)

                        barre_etape = barre_avancement(DIMENTION_BARRES_PANNEAU_SELECTION, couleur_barre,
                                                       proportion_etape, CONTOURS_BULLE_PANNEAU_SELECTION)

                        y_barre_etape = int(y_centre_texte_etape + TAILLE_TEXTE_PANNEAU_SELECTION * 1.4)
                        x_barres = int(x_centre - DIMENTION_BARRES_PANNEAU_SELECTION[0] / 2)
                        self.ecran.blit(barre_etape, (x_barres - MARGE_PANNEAU_SELECTION, y_barre_etape))

                        y_pourcentage = int(y_barre_etape + DIMENTION_BARRES_PANNEAU_SELECTION[1] / 2)
                        affiche_texte(f'{int(proportion_etape * 100)}%', x_centre, y_pourcentage, self.ecran,
                                      taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4), x_0gauche_1centre_2droite=1,
                                      y_0haut_1centre_2bas=1, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)

                        if not texte_precision == '':
                            couleur_sans_alpha = couleur_barre
                            if len(couleur_sans_alpha) == 2:
                                couleur_sans_alpha = calcul_couleur(couleur_barre, COULEUR_FOND_BULLE_PANNEAU_SELECTION)
                            x_precision = x_barres + DIMENTION_BARRES_PANNEAU_SELECTION[0]
                            affiche_texte(texte_precision, x_precision, y_pourcentage, self.ecran,
                                          taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4), y_0haut_1centre_2bas=1,
                                          couleur=couleur_sans_alpha)

                    else:
                        titre = TEXTE_PANNEAU_SELECTION_BATIMENT_CONSTRUIT
                        if not self.element_selectionne.type == TYPE_BATIMENT_BASE and \
                                not self.element_selectionne.argent_comptenu_max == 0:
                            infos_barre_ressource = (self.element_selectionne.argent_comptenu,
                                                     self.element_selectionne.argent_comptenu_max,
                                                     TYPE_RESSOURCE_ARGENT)
                            if self.panneau_construction_amelioration_batiments is None:
                                self.panneau_construction_amelioration_batiments = \
                                    PanneauConstructionAmeliorationBatiment(self.monde, self.element_selectionne)
                        else:
                            if self.element_selectionne.type == TYPE_BATIMENT_ENNEMI:
                                self.panneau_construction_amelioration_batiments = None
                                # TODO : afficher les infos de la base ennemi !
                            else:
                                if self.panneau_construction_amelioration_batiments is None:
                                    self.panneau_construction_amelioration_batiments = \
                                        PanneauConstructionAmeliorationBatiment(self.monde, self.element_selectionne,
                                                                                True)

                elif isinstance(self.element_selectionne, ElementMobile):
                    if self.panneau_infos_selection_element_mobile is None:
                        y_panneau_selection_element_mobile = (y_barre_vie + hauteur_barre_vie
                                                              + MARGE_PANNEAU_SELECTION)
                        self.panneau_infos_selection_element_mobile = \
                            PanneauInfosSelectionElementMobile(self.monde, self.x_ecran + x,
                                                               self.y_ecran + y_panneau_selection_element_mobile,
                                                               int(y + hauteur - y_panneau_selection_element_mobile
                                                                   - MARGE_PANNEAU_SELECTION))

                    if self.element_selectionne.objectif is None:
                        if isinstance(self.element_selectionne, Soldat) and self.element_selectionne.cible is not None:
                            titre = TEXTE_PANNEAU_SELECTION_PERSONNE_ACTIVE
                        else:
                            if isinstance(self.element_selectionne, Ennemi):
                                if self.element_selectionne.cible is None:
                                    titre = TEXTE_PANNEAU_SELECTION_ENNEMI_INACTIF
                                else:
                                    titre = TEXTE_PANNEAU_SELECTION_ENNEMI_ACTIF
                            else:
                                titre = TEXTE_PANNEAU_SELECTION_PERSONNE_INACTIVE
                    else:
                        if isinstance(self.element_selectionne, Ennemi):
                            titre = TEXTE_PANNEAU_SELECTION_ENNEMI_ACTIF
                        else:
                            titre = TEXTE_PANNEAU_SELECTION_PERSONNE_ACTIVE

                    x_bouton_stop = (x + X_PANNEAU_INFOS_ELEMENT_MOBILE + LARGEUR_PANNEAU_INFOS_ELEMENT_MOBILE
                                     + int(MARGE_PANNEAU_SELECTION * 0.9))
                    cote_bouton_stop = x + largeur - x_bouton_stop - MARGE_PANNEAU_SELECTION
                    if isinstance(self.element_selectionne, Personne):
                        self.liste_boutons_ecran.append(BoutonImage(x_bouton_stop, (y + hauteur - cote_bouton_stop
                                                                                    - MARGE_PANNEAU_SELECTION),
                                                                    cote_bouton_stop, cote_bouton_stop,
                                                                    TYPE_BOUTON_IMAGE_STOP))

                        if isinstance(self.element_selectionne, Porteur):
                            infos_barre_ressource = (self.element_selectionne.ressource_comptenu,
                                                     self.element_selectionne.ressource_comptenu_max,
                                                     self.element_selectionne.type_ressource_comptenu)
                            x_textes_ressource_en_tout = (DIMENTION_BARRES_PANNEAU_SELECTION[1] +
                                                          MARGE_PANNEAU_SELECTION * 1.5)
                            x_textes_ressource_en_tout = int(x + x_textes_ressource_en_tout +
                                                             (X_PANNEAU_INFOS_ELEMENT_MOBILE -
                                                              x_textes_ressource_en_tout) / 2)
                            y_textes_ressource_en_tout_centre = (y_barre_vie + hauteur_barre_vie +
                                                                 MARGE_PANNEAU_SELECTION)
                            y_textes_ressource_en_tout_centre = int(y_textes_ressource_en_tout_centre +
                                                                    (y + hauteur - MARGE_PANNEAU_SELECTION -
                                                                     y_textes_ressource_en_tout_centre) / 2)

                            affiche_texte(TEXTE_PANNEAU_SELECTION_EN_TOUT, x_textes_ressource_en_tout,
                                          int(y_textes_ressource_en_tout_centre -
                                              1.5 * ECART_TEXTE_PANNEAU_SELECTION_RESSOURCE_EN_TOUT),
                                          self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION),
                                          couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1,
                                          y_0haut_1centre_2bas=1)
                            x_textes_ressource = x_textes_ressource_en_tout - MARGE_PANNEAU_SELECTION
                            for i, type_ressource in enumerate([TYPE_RESSOURCE_ARGENT, TYPE_RESSOURCE_MINERAI,
                                                                TYPE_RESSOURCE_LIQUIDE]):
                                y_i = int(y_textes_ressource_en_tout_centre +
                                          (i - 0.5) * ECART_TEXTE_PANNEAU_SELECTION_RESSOURCE_EN_TOUT)
                                nb = self.element_selectionne.dic_nb_ressources_transportees_en_tout[type_ressource]
                                affiche_texte(str(nb), x_textes_ressource, y_i, self.ecran,
                                              taille=int(TAILLE_TEXTE_PANNEAU_SELECTION),
                                              couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, y_0haut_1centre_2bas=1)
                                rayon = RAYON_RESSOURCE_PANNEAU_VIGNETTES
                                draw_filled_circle(self.ecran, (x_textes_ressource - 2 * rayon, y_i - 1),
                                                   rayon, DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][type_ressource])

                        if isinstance(self.element_selectionne, Soldat):
                            self.liste_boutons_ecran.append(BoutonImage(x_bouton_stop,
                                                                        y + hauteur - 2 * (cote_bouton_stop +
                                                                                           MARGE_PANNEAU_SELECTION),
                                                                        cote_bouton_stop, cote_bouton_stop,
                                                                        TYPE_BOUTON_IMAGE_IMMOBILE))

                    if isinstance(self.element_selectionne, ElementMobileTireur):
                        largeur_vignette_cible = int(self.panneau_infos_selection_element_mobile.x_ecran -
                                                     self.x_ecran - x - 2 * MARGE_PANNEAU_SELECTION)
                        x_centre_cible = int(largeur_vignette_cible / 2 + x + MARGE_PANNEAU_SELECTION)
                        y_texte_cible = int(y_barre_vie + hauteur_barre_vie + MARGE_PANNEAU_SELECTION)
                        affiche_texte(TEXTE_PANNEAU_SELECTION_CIBLE, x_centre_cible, y_texte_cible, self.ecran,
                                      taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.2),
                                      couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1)
                        y_vignette_cible = int(y_texte_cible + TAILLE_TEXTE_PANNEAU_SELECTION * 1.15 +
                                               MARGE_PANNEAU_SELECTION * 0.4)
                        if self.element_selectionne.cible is not None:
                            vignette_cible = VignetteElementVie(self.element_selectionne.cible,
                                                                x + MARGE_PANNEAU_SELECTION, y_vignette_cible,
                                                                largeur_vignette_cible, largeur_vignette_cible)
                            self.liste_boutons_ecran.append(vignette_cible)
                        else:
                            self.ecran.blit(ecran_illustration_vierge((largeur_vignette_cible,
                                                                       largeur_vignette_cible)),
                                            (x + MARGE_PANNEAU_SELECTION, y_vignette_cible))
                        y_texte_en_tout = y_vignette_cible + largeur_vignette_cible + MARGE_PANNEAU_SELECTION * 0.5
                        affiche_texte(TEXTE_PANNEAU_SELECTION_EN_TOUT, x_centre_cible, y_texte_en_tout,
                                      self.ecran, taille=TAILLE_TEXTE_PANNEAU_SELECTION,
                                      x_0gauche_1centre_2droite=1, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)
                        affiche_texte(str(self.element_selectionne.tireur.nb_destructions) + ' ' +
                                      TEXTE_PANNEAU_SELECTION_NB_VICTIMES_SOLDAT, x_centre_cible,
                                      (y_texte_en_tout + MARGE_PANNEAU_SELECTION * 0.2 +
                                       TAILLE_TEXTE_PANNEAU_SELECTION), self.ecran,
                                      taille=TAILLE_TEXTE_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1,
                                      couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)

                if affiche_vie:
                    barre_vies = barre_avancement(DIMENTION_BARRES_VIE_PANNEAU_SELECTION,
                                                  COULEUR_BARRES_VIE_PANNEAU_SELECTION,
                                                  (self.element_selectionne.nb_vies /
                                                   self.element_selectionne.nb_vies_max),
                                                  CONTOURS_BULLE_PANNEAU_SELECTION, COULEUR_COMPTENU_PANNEAU_SELECTION)
                    # etiquette_simple = (str(int(self.element_selectionne.nb_vies)),
                    #                     COULEUR_COMPTENU_PANNEAU_SELECTION,
                    #                     int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4))
                    if infos_barre_ressource is None:
                        x_barre_vie = int(x_centre - largeur_barre_vie / 2)
                    else:
                        x_barre_vie = int(x + largeur - largeur_barre_vie - MARGE_PANNEAU_SELECTION * 1.5)
                    self.ecran.blit(barre_vies, (x_barre_vie, y_barre_vie))
                    affiche_texte(str(int(self.element_selectionne.nb_vies)),
                                  int(x_barre_vie + DIMENTION_BARRES_VIE_PANNEAU_SELECTION[0] / 2),
                                  int(y_barre_vie + DIMENTION_BARRES_VIE_PANNEAU_SELECTION[1] / 2 + 2),
                                  self.ecran, taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4),
                                  x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1,
                                  couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)
                    image = loaded_images(CHEMIN_IMAGE_VIES_PANNEAU_SELECTION)
                    larg, haut = image.get_size()
                    self.ecran.blit(image, (x_barre_vie - larg / 2, int(y_barre_vie - haut / 2 +
                                                                        hauteur_barre_vie / 2)))
                    if infos_barre_ressource is not None:
                        nb, nb_max, type_ressource = infos_barre_ressource
                        hauteur_barre_ressource = y + hauteur - y_barre_vie - MARGE_PANNEAU_SELECTION
                        barre_ressource = barre_avancement((DIMENTION_BARRES_PANNEAU_SELECTION[1],
                                                            hauteur_barre_ressource),
                                                           ((NOIR, 0) if nb <= 0 else
                                                            DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][type_ressource]),
                                                           nb / nb_max, CONTOURS_BULLE_PANNEAU_SELECTION,
                                                           COULEUR_COMPTENU_PANNEAU_SELECTION, avancement_vertical=True,
                                                           etiquette_simple=(str(nb),
                                                                             COULEUR_COMPTENU_PANNEAU_SELECTION,
                                                                             TAILLE_TEXTE_PANNEAU_SELECTION))
                        self.ecran.blit(barre_ressource, (int(x + MARGE_PANNEAU_SELECTION * 1.5), y_barre_vie))

            elif isinstance(self.element_selectionne, Source):
                titre = TEXTE_PANNEAU_SELECTION_SOURCE_NON_EPUISEE

                liste_texte = DIC_TEXTE_PANNEAU_SELECTION_RESSOURCES_RESTANTES[self.element_selectionne.type]
                couleur = DIC_RESSOURCE[PARAM_RESSOURCE_COULEUR][self.element_selectionne.type_ressource]
                if len(couleur) == 2:
                    couleur = couleur[0]

                dy = int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.5 + MARGE_PANNEAU_SELECTION)
                y_temp = int(y + MARGE_PANNEAU_SELECTION +
                             (hauteur - dy * (len(liste_texte) - 2)) / 2)
                for i, (texte) in enumerate(liste_texte):
                    if not i == 0:
                        if i == 1:
                            texte = liste_texte[0] + str(self.element_selectionne.ressource_comptenu) + texte
                        affiche_texte(texte, x_centre, y_temp, self.ecran,
                                      taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.5), couleur=couleur,
                                      x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
                        y_temp += dy

            affiche_texte(titre, x_centre, int(y + MARGE_PANNEAU_SELECTION * 1.5), self.ecran,
                          taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 1.4), couleur=COULEUR_COMPTENU_PANNEAU_SELECTION,
                          x_0gauche_1centre_2droite=1)

        for bouton in self.liste_boutons_ecran:
            bouton.affiche(self.ecran)

    def update_affichage_base(self):
        self.ecran_base.fill(-1)
        self.panneau_construction_amelioration_batiments = None
        self.liste_vigettes_ecran_base = []
        centre_x = self.largeur_ecran // 2
        if self.element_selectionne is None:
            affiche_texte(TEXTE_PANNEAU_SELECTION_WALL_WAR, centre_x, MARGE_GENERALE, self.ecran_base,
                          taille=int(TAILLE_TEXTE_PANNEAU_SELECTION * 4.5),
                          x_0gauche_1centre_2droite=1, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)
            for _, bouton in self.liste_boutons_menu:
                bouton.affiche(self.ecran_base)
        else:
            if type(self.element_selectionne) == list:
                taille = int(TAILLE_TEXTE_PANNEAU_SELECTION * 2.5)
                affiche_texte(TEXTE_PANNEAU_SELECTION_GROUPE, centre_x, TAILLE_TEXTE_PANNEAU_SELECTION, self.ecran_base,
                              taille=taille, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1)
                nb_cases = len(self.element_selectionne)
                if nb_cases > NB_PANNEAU_SELECTION_PERSONNES_AFFICHAGE_MAX:
                    nb_cases = NB_PANNEAU_SELECTION_PERSONNES_AFFICHAGE_MAX
                marge = MARGE_PANNEAU_SELECTION
                y = int(taille * 1.5)
                largeur = self.largeur_ecran
                hauteur = self.hauteur_ecran - y
                nx = math.ceil(math.sqrt(nb_cases))
                # ny = math.ceil(nb_cases / nx)
                dx = int((largeur - marge * (nx + 1)) / nx)
                # dy = int((hauteur - marge * (ny + 1)) / ny)
                dy = int(dx * hauteur / largeur)
                x = marge
                y += marge
                i = 0
                # for yi in range(ny):
                for yi in range(nx):
                    for xi in range(nx):
                        if i >= nb_cases:
                            break
                        self.liste_vigettes_ecran_base.append(VignetteElementVie(self.element_selectionne[i],
                                                                                 x, y, dx, dy))
                        i += 1
                        x += marge + dx
                    y += marge + dy
                    x = marge

            else:
                # Le titre
                titre = 'Rien'
                if isinstance(self.element_selectionne, Element):
                    titre = self.element_selectionne.nom
                elif isinstance(self.element_selectionne, Source):
                    titre = self.element_selectionne.nom

                taille = int(TAILLE_TEXTE_PANNEAU_SELECTION * 2.5)
                affiche_texte(titre, centre_x, TAILLE_TEXTE_PANNEAU_SELECTION, self.ecran_base,
                              taille=taille, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION, x_0gauche_1centre_2droite=1)

                # L'illustration
                y_information = taille * 1.8
                if isinstance(self.element_selectionne, Batiment):
                    ecran_illustration = illustration_batiment(self.element_selectionne.type,
                                                               DIMENTION_ILLUSTRATION_PANNEAU_SELECTION,
                                                               PANNEAU_SELECTION_COTE_CASE_BATIMENT)
                elif isinstance(self.element_selectionne, ElementMobile):
                    ecran_illustration = illustration_element_mobile(self.element_selectionne.type,
                                                                     DIMENTION_ILLUSTRATION_PANNEAU_SELECTION,
                                                                     MARGE_PANNEAU_SELECTION)
                elif isinstance(self.element_selectionne, Source):
                    ecran_illustration = illustration_source(self.element_selectionne.type,
                                                             DIMENTION_ILLUSTRATION_PANNEAU_SELECTION,
                                                             PANNEAU_SELECTION_COTE_CASE_BATIMENT)
                else:
                    ecran_illustration = ecran_illustration_vierge(DIMENTION_ILLUSTRATION_PANNEAU_SELECTION)

                self.ecran_base.blit(ecran_illustration, (MARGE_PANNEAU_SELECTION, y_information))

                # La description
                description = []
                if isinstance(self.element_selectionne, Element):
                    description = self.element_selectionne.description
                elif isinstance(self.element_selectionne, Source):
                    description = self.element_selectionne.description

                x_desctiption = MARGE_PANNEAU_SELECTION * 2 + DIMENTION_ILLUSTRATION_PANNEAU_SELECTION[0]
                ecart_lignes = TAILLE_TEXTE_PANNEAU_SELECTION * 1.5
                y_description = y_information + int((6 - len(description)) * ecart_lignes / 2)
                for i, ligne in enumerate(description):
                    affiche_texte(ligne, x_desctiption, y_description + i * ecart_lignes, self.ecran_base,
                                  taille=TAILLE_TEXTE_PANNEAU_SELECTION, couleur=COULEUR_COMPTENU_PANNEAU_SELECTION)

                # La bulle
                if self.rect_bulle == (0, 0, 0, 0):
                    y = y_information + DIMENTION_ILLUSTRATION_PANNEAU_SELECTION[1] + MARGE_PANNEAU_SELECTION
                    self.rect_bulle = (MARGE_PANNEAU_SELECTION, y, self.largeur_ecran - 2 * MARGE_PANNEAU_SELECTION,
                                       self.hauteur_ecran - y - MARGE_PANNEAU_SELECTION)

                    init_panneau_construction_amelioration(self.rect_bulle, (self.x_ecran, self.y_ecran))

                x_centre_fleche = MARGE_PANNEAU_SELECTION + DIMENTION_ILLUSTRATION_PANNEAU_SELECTION[0] / 2
                y_fleche = self.rect_bulle[1]
                draw_filled_rect(self.ecran_base, self.rect_bulle, COULEUR_FOND_BULLE_PANNEAU_SELECTION)
                pygame.draw.rect(self.ecran_base, COULEUR_COMPTENU_PANNEAU_SELECTION, self.rect_bulle,
                                 CONTOURS_BULLE_PANNEAU_SELECTION)
                pygame.draw.polygon(self.ecran_base, COULEUR_COMPTENU_PANNEAU_SELECTION,
                                    [(x_centre_fleche, y_fleche - MARGE_PANNEAU_SELECTION),
                                     (x_centre_fleche + 5, y_fleche),
                                     (x_centre_fleche - 5, y_fleche)])
                y_fleche += CONTOURS_BULLE_PANNEAU_SELECTION * 2
                pygame.draw.polygon(self.ecran_base, COULEUR_FOND_BULLE_PANNEAU_SELECTION,
                                    [(x_centre_fleche, y_fleche - MARGE_PANNEAU_SELECTION),
                                     (x_centre_fleche + 5, y_fleche),
                                     (x_centre_fleche - 5, y_fleche)])

        self.new_affichage = True

    def update_affichage_vignettes(self):
        for vignette in self.liste_vigettes_ecran_base:
            vignette.update()
            if vignette.new_affichage:
                vignette.affiche(self.ecran_base)
                self.new_affichage = True

    def update_affichage_boutons_vignettes(self):
        for bouton in self.liste_boutons_ecran:
            if isinstance(bouton, VignetteElementVie):
                bouton.update()
                if bouton.new_affichage:
                    bouton.affiche(self.ecran)

    def affiche(self, screen: pygame.Surface):
        if self.new_affichage_base:
            self.update_affichage_base()
            self.new_affichage_base = False
            self.new_affichage = True
        if self.element_selectionne is not None and len(self.liste_vigettes_ecran_base) > 0:
            self.update_affichage_vignettes()
        if self.element_selectionne is not None and len(self.liste_boutons_ecran) > 0:
            self.update_affichage_boutons_vignettes()
        PanneauClic.affiche(self, screen)
        if self.panneau_construction_amelioration_batiments is not None:
            self.panneau_construction_amelioration_batiments.affiche(screen)
        if self.panneau_infos_selection_element_mobile is not None and \
                self.panneau_infos_selection_element_mobile.doit_s_afficher:
            self.panneau_infos_selection_element_mobile.affiche(screen)
