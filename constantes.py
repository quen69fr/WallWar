import math

# Quelques couleurs :
NOIR = (0, 0, 0)
GRIS_FONCE = (50, 50, 50)
GRIS_MOYEN = (90, 90, 90)
GRIS_CLAIR = (130, 130, 130)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
VERT = (52, 175, 0)
ROUGE = (255, 0, 0)
ORANGE = (255, 127, 0)
JAUNE = (255, 230, 0)

DEFAULT_POLICE = 'Font/freesansbold.ttf'

#                  Sommaire
# ==========================================

# I. La fenêtre
# =============

# II. Tous les types d'objets
# ===========================

# III. La description du monde (init)
# ===================================

# IV. La carte et les cases
# =========================

# V. Les sources et ressources
# ============================

# VI. Les explosions
# ==================

# VII. Les éléments
# =================

# VIII. Les ennemis
# =================

# IX. Les améliorations
# =====================

# X. Les panneaux
# ===============
# A. Le panneau infos
# -------------------
# B. Le panneau constructions
# ---------------------------
# C. Le panneau selection
# -----------------------
# 1. Les batiments
# 2. Les sources
# 3. Les personnes

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# I. La fenêtre
# =============
FPS = 100
FPS_UPDATE_CIBLES_TIREUR = 2
CAPTION = 'WallWar'
FULL_SCREEN_INIT = False

LARGEUR = 1360
HAUTEUR = 700

COULEUR_FOND_ECRAN = 0
LISTE_COULEUR_FOND_ECRAN_PAUSE = [(abs(int(co - 200)) + 25, 0, 0) for co in range(0, 200 * 2, 10)]

MARGE_GENERALE = 10
X_CARTE = MARGE_GENERALE
Y_CARTE = MARGE_GENERALE
LARGEUR_CARTE = 930
HAUTEUR_CARTE = HAUTEUR - Y_CARTE - MARGE_GENERALE

X_PANNEAU_ACTIONS = X_CARTE + LARGEUR_CARTE + MARGE_GENERALE
Y_PANNEAU_ACTIONS = MARGE_GENERALE
LARGEUR_PANNEAU_ACTIONS = LARGEUR - X_PANNEAU_ACTIONS - MARGE_GENERALE
HAUTEUR_PANNEAU_ACTIONS = 450

X_PANNEAU_CONSTRUCTION = X_PANNEAU_ACTIONS
Y_PANNEAU_CONSTRUCTION = Y_PANNEAU_ACTIONS + HAUTEUR_PANNEAU_ACTIONS + MARGE_GENERALE
LARGEUR_PANNEAU_CONSTRUCTION = LARGEUR_PANNEAU_ACTIONS
HAUTEUR_PANNEAU_CONSTRUCTION = HAUTEUR - Y_PANNEAU_CONSTRUCTION - MARGE_GENERALE

MARGE_CLIC_MOTION = 30

ACTION_MENU_PAUSE = 0
ACTION_MENU_QUITTER = 1
ACTION_MENU_SAUVER = 2
ACTION_MENU_CHARGER = 3
ACTION_MENU_FULLSCREEN = 4

PARAM_ACTION_MENU_TEXTE = 0
PARAM_ACTION_MENU_KEY = 1
PARAM_ACTION_MENU_CTRL = 2

DIC_ACTION_MENU = {
    PARAM_ACTION_MENU_TEXTE: {
        ACTION_MENU_PAUSE: 'Pause (P)',
        ACTION_MENU_QUITTER: 'Quitter (Ctrl Q)',
        ACTION_MENU_SAUVER: 'Sauver (Ctrl S)',
        ACTION_MENU_CHARGER: 'Charger (Ctrl C)',
        ACTION_MENU_FULLSCREEN: 'Plein écran (Ctrl F)'},
    PARAM_ACTION_MENU_KEY: {
        ACTION_MENU_PAUSE: 112,
        ACTION_MENU_QUITTER: 97,
        ACTION_MENU_SAUVER: 115,
        ACTION_MENU_CHARGER: 99,
        ACTION_MENU_FULLSCREEN: 102},
    PARAM_ACTION_MENU_CTRL: {
        ACTION_MENU_PAUSE: False,
        ACTION_MENU_QUITTER: True,
        ACTION_MENU_SAUVER: True,
        ACTION_MENU_CHARGER: True,
        ACTION_MENU_FULLSCREEN: True}
}

LISTE_ACTIONS_MENU = [ACTION_MENU_PAUSE, ACTION_MENU_FULLSCREEN, ACTION_MENU_SAUVER,
                      ACTION_MENU_CHARGER, ACTION_MENU_QUITTER]

# II. Tous les types d'objets
# ===========================
TYPE_CASE_S_NON_CONSTRUITE = -5
TYPE_CASE_S_POSSIBLE = -4
TYPE_CASE_S_IMPOSSIBLE = -3
TYPE_CASE_S_SELECTIONNEE = -2
TYPE_CASE_INEXISTANTE = -1
TYPE_CASE_VIDE = 0
TYPE_CASE_PLEINE = 1
TYPE_CASE_S_RELAIS = 2
TYPE_CASE_SOURCE = 3
TYPE_CASE_S_DEPOS = 4
TYPE_CASE_S_REGEN = 5

TYPE_SOURCE_MINERAI = 10
TYPE_SOURCE_LIQUIDE = 11
TYPE_RESSOURCE_MINERAI = 'M'
TYPE_RESSOURCE_ARGENT = 'A'
TYPE_RESSOURCE_LIQUIDE = 'L'

TYPE_BATIMENT_BASE = 20
TYPE_BATIMENT_ENTREPOT = 21
TYPE_BATIMENT_GUILDE = 22
TYPE_BATIMENT_LABO = 23
TYPE_BATIMENT_CASERNE = 24
TYPE_BATIMENT_CENTRE = 25
TYPE_BATIMENT_TOURELLE = 26
TYPE_BATIMENT_STATION = 27
TYPE_BATIMENT_ENNEMI = 28

TYPE_PERSONNE_CLASS_PERSONNE = 300
TYPE_PERSONNE_CLASS_PORTEUR = 301
TYPE_PERSONNE_CLASS_SOLDAT = 302
TYPE_PERSONNE_PORTEUR = 30
TYPE_PERSONNE_COLTINEUR = 31
TYPE_PERSONNE_CHARGEUR = 32
TYPE_PERSONNE_SOLDAT = 33
TYPE_PERSONNE_TIRAILLEUR = 34
TYPE_PERSONNE_TANK = 35

TYPE_ENNEMI = 400

TYPE_EXPLOSION_PETITE = 50
TYPE_EXPLOSION_MOYENNE = 51
TYPE_EXPLOSION_GROSSE = 52

TYPE_AMELIORATION_PORTEURS_COMPTENU = 600
TYPE_AMELIORATION_COTINEURS_VITESSE = 601
TYPE_AMELIORATION_DEBLOQUE_PORTEURS = 602
TYPE_AMELIORATION_PORTEURS_VIES = 603
TYPE_AMELIORATION_PORTEURS_VIES_2 = 604
TYPE_AMELIORATION_CHARGEURS_COMPTENU = 605
TYPE_AMELIORATION_DEBLOQUE_CHARGEURS = 606
TYPE_AMELIORATION_CHARGEURS_VITESSE = 607
TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1 = 608
TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2 = 609
TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3 = 610
TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4 = 611
TYPE_AMELIORATION_SOLDATS_VIES_1 = 612
TYPE_AMELIORATION_SOLDATS_VIES_2 = 613
TYPE_AMELIORATION_SOLDATS_VIES_3 = 614
TYPE_AMELIORATION_SOLDATS_VIES_4 = 615
TYPE_AMELIORATION_SOLDATS_VITESSE_1 = 616
TYPE_AMELIORATION_SOLDATS_VITESSE_2 = 617
TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE = 618
TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS = 619
TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1 = 620
TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2 = 621
TYPE_AMELIORATION_DEBLOQUE_TANK = 622
TYPE_AMELIORATION_TANKS_PORTEE_TIR_1 = 623
TYPE_AMELIORATION_TANKS_PORTEE_TIR_2 = 624
TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE = 625
TYPE_AMELIORATION_BATIMENT_COMPTENU = 626
TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES = 627
TYPE_AMELIORATION_TOURELLE_VIES_1 = 628
TYPE_AMELIORATION_TOURELLE_VIES_2 = 629
TYPE_AMELIORATION_TOURELLE_TIR_1 = 630
TYPE_AMELIORATION_TOURELLE_TIR_2 = 631
TYPE_AMELIORATION_TOURELLE_TIR_3 = 632
TYPE_AMELIORATION_STATION_VIES = 633
TYPE_AMELIORATION_VITESSE_RECHARGE_1 = 634
TYPE_AMELIORATION_VITESSE_RECHARGE_2 = 635
TYPE_AMELIORATION_STATION_PRIX = 636
TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION = 637
TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1 = 638
TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2 = 639


# III. La description du monde (init)
# ===================================
NB_CASE_X_GRILLE = 100
NB_CASE_Y_GRILLE = 100
COTE_CASES_GRILLE = 60
ZOOM_INIT = 0.5

NB_ARGENT_INIT = 150
NB_LIQUIDE_INIT = 50
LISTE_BATIMENTS_INIT = [((7, 9), TYPE_BATIMENT_BASE),
                        ((3, 20), TYPE_BATIMENT_ENTREPOT),
                        ((22, 3), TYPE_BATIMENT_ENTREPOT),
                        ((11, 22), TYPE_BATIMENT_TOURELLE),
                        ((9, 23), TYPE_BATIMENT_TOURELLE),
                        ((40, 50), TYPE_BATIMENT_ENNEMI),
                        ((80, 12), TYPE_BATIMENT_ENNEMI),
                        ((12, 83), TYPE_BATIMENT_ENNEMI)]
LISTE_SOURCES_INIT = [
    ([(0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 5),
     (2, 2), (2, 3), (3, 3), (2, 4), (0, 2)], TYPE_SOURCE_MINERAI, 12873),
    ([(50, 50), (51, 51), (50, 51), (51, 50), (52, 51),
     (51, 52), (52, 52), (53, 51), (53, 50), (54, 50)], TYPE_SOURCE_MINERAI, 7475),
    ([(12, 1), (11, 1), (13, 1), (10, 1), (11, 2), (12, 2), (12, 3), (13, 2), (13, 3), (14, 2)],
     TYPE_SOURCE_LIQUIDE, 8162),
    ([(4, 91), (4, 92), (5, 92), (4, 93), (5, 93), (6, 93), (4, 94), (5, 94)],
     TYPE_SOURCE_LIQUIDE, 3821)]
LISTE_PERSONNE_INIT = [(TYPE_PERSONNE_COLTINEUR, 245, 490),
                       (TYPE_PERSONNE_COLTINEUR, 350, 370),
                       (TYPE_PERSONNE_PORTEUR, 530, 370),
                       (TYPE_PERSONNE_CHARGEUR, 650, 490),
                       (TYPE_PERSONNE_TIRAILLEUR, 1460, 710),
                       (TYPE_PERSONNE_TANK, 1380, 710),
                       (TYPE_PERSONNE_SOLDAT, 1380, 630),
                       (TYPE_PERSONNE_SOLDAT, 1460, 630)]

# IV. La carte et les cases
# =========================
CARTE_CHEMIN_IMAGE_FOND_PAVAGE_SABLE = 'Images/fondPavage.png'
COULEUR_TEXTE_SUR_SABLE = (127, 109, 82)
CARTE_MARGE_BORD_DEPLACEMENT = 28
CARTE_VITESSE_DEPLACEMENT = 20
CARTE_COEF_ZOOM = 0.1
CARTE_COTE_CASE_ZOOM_MAX = 200

CASE_VIDE_GRILLE_CHEMIN = 0
CASE_PLEINE_GRILLE_CHEMIN = 1

PARAM_CASE_S_COULEUR = 0

DIC_CASES_SPECIALES = {
    PARAM_CASE_S_COULEUR: {
        TYPE_CASE_S_DEPOS: (BLANC, 90),
        TYPE_CASE_S_RELAIS: (NOIR, 100),
        TYPE_CASE_S_POSSIBLE: (VERT, 180),
        TYPE_CASE_S_IMPOSSIBLE: (ROUGE, 120),
        TYPE_CASE_S_SELECTIONNEE: (BLANC, 70),
        TYPE_CASE_S_NON_CONSTRUITE: NOIR,
        TYPE_CASE_S_REGEN: (VERT, 150)
    }
}
ALPHA_MIN_COULEUR_CASE_NON_CONSTRUITES = 30

# V. Les sources et ressources
# ============================
PARAM_SOURCE_TYPE_RESSOURCE = 0
PARAM_SOURCE_NOM = 1
PARAM_SOURCE_DESCRIPTION = 2

DIC_SOURCES = {
    PARAM_SOURCE_TYPE_RESSOURCE: {
        TYPE_SOURCE_MINERAI: TYPE_RESSOURCE_MINERAI,
        TYPE_SOURCE_LIQUIDE: TYPE_RESSOURCE_LIQUIDE
    },
    PARAM_SOURCE_NOM: {
        TYPE_SOURCE_MINERAI: 'Source de minerai',
        TYPE_SOURCE_LIQUIDE: 'Source de liquide'
    },
    PARAM_SOURCE_DESCRIPTION: {
        TYPE_SOURCE_MINERAI: ["    Le minerai est essentiel à votre ",
                              "ville. Il constitue votre stock d’ar-",
                              "gent aussitôt qu’il est ramené à ",
                              "une base. Vous en dépenserez à ",
                              "chaque nouvelle construction. ",
                              "C’est la clé à tous vos projets !"],
        TYPE_SOURCE_LIQUIDE: ["    Le liquide est puisé par vos ",
                              "porteurs et ramené à la base. ",
                              "Tout comme le minerai il consti-",
                              "tuera une richesse nécessaire à ",
                              "chaque construction, création de ",
                              "personnage ou amélioration.  "]
    }
}

PARAM_RESSOURCE_COULEUR = 0

DIC_RESSOURCE = {
    PARAM_RESSOURCE_COULEUR: {
        TYPE_RESSOURCE_MINERAI: (ORANGE, 200),
        TYPE_RESSOURCE_ARGENT: ((255, 50, 0), 200),
        TYPE_RESSOURCE_LIQUIDE: (BLEU, 200)
    }
}

TAILLE_TEXTE_NB_RESSOURCES_RESTANTES = 28
COULEUR_TEXTE_NB_RESSOURCES_RESTANTES = GRIS_FONCE

# VI. Les explosions
# ==================
PARAM_EXPLOSION_LISTE_IMAGES = 0
PARAM_EXPLOSION_SCALE = 1
PARAM_EXPLOSION_NB_TOURS_PAR_IMAGE = 2

DIC_EXPLOSIONS = {
    PARAM_EXPLOSION_LISTE_IMAGES: {
        TYPE_EXPLOSION_PETITE: [f'Images/imagesExplosion/{i}.gif' for i in range(26)],
        TYPE_EXPLOSION_MOYENNE: [f'Images/imagesExplosion/{i}.gif' for i in range(26)],
        TYPE_EXPLOSION_GROSSE: [f'Images/imagesExplosion/{i}.gif' for i in range(26)]
    },
    PARAM_EXPLOSION_SCALE: {
        TYPE_EXPLOSION_PETITE: 0.1,
        TYPE_EXPLOSION_MOYENNE: 0.8,
        TYPE_EXPLOSION_GROSSE: 2.3
    },
    PARAM_EXPLOSION_NB_TOURS_PAR_IMAGE: {
        TYPE_EXPLOSION_PETITE: 0.2,
        TYPE_EXPLOSION_MOYENNE: 1,
        TYPE_EXPLOSION_GROSSE: 2
    }
}

# VII. Les éléments
# ================
PARAM_A_VIES = 0
PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT = 1
PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX = 2
PARAM_A_BATIMENT_NB_PLACES = 3
PARAM_A_PERSONNE_NB_PLACES = 4
PARAM_A_TIREUR_FORCE_TIR = 5
PARAM_A_TIREUR_PORTEE_TIR = 6
PARAM_A_TIREUR_DELAY_TIR = 7
PARAM_A_TIREUR_PORTEE_VISION = 8
PARAM_A_TIREUR_INTELLIGENCE = 9
PARAM_A_TIREUR_CIBLE_VISIBLE = 10
PARAM_A_PORTEUR_PEUT_RECOLTER = 11
PARAM_A_PORTEUR_PEUT_DONNER_VIES = 12
PARAM_A_BATIMENT_NB_VIES_REGEN = 13

PARAM_F_NOM = 20
PARAM_F_DESCRIPTION = 21
PARAM_F_TYPE_EXPLOSION = 22
PARAM_F_BATIMENT_LISTE_CASES = 23
PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES = 24
PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION = 25
PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION = 26
PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION = 27
PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES = 28
PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES = 29
PARAM_F_BATIMENT_PEUT_TIRER = 30
PARAM_F_ELEMENT_MOBILE_CHEMIN_IMAGE = 31
PARAM_F_ELEMENT_MOBILE_RAYON = 32
PARAM_F_ELEMENT_MOBILE_SCALE_IMAGE_ZOOM = 33
PARAM_F_PERSONNE_TYPE_CLASS = 34
PARAM_F_PORTEUR_DISTANCE_RESSOURCE = 35
PARAM_F_PORTEUR_RAYON_RESSOURCE = 36
PARAM_F_TIREUR_TYPE_EXPLOSION_TIR = 37
PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE = 38
PARAM_F_ELEMENT_MOBILE_MASSE_RELATIVE = 39
PARAM_F_BATIMENT_TIREUR_CHEMIN_IMAGE_CANON = 40
PARAM_F_BATIMENT_TIREUR_SCALE_IMAGE_CANON_ZOOM = 41

DIC_ELEMENTS = {
    # Tous les éléments :
    PARAM_A_VIES: {
        TYPE_BATIMENT_BASE: 9500,
        TYPE_BATIMENT_ENTREPOT: 5500,
        TYPE_BATIMENT_GUILDE: 8000,
        TYPE_BATIMENT_LABO: 7000,
        TYPE_BATIMENT_CASERNE: 9000,
        TYPE_BATIMENT_CENTRE: 7000,
        TYPE_BATIMENT_TOURELLE: 2000,
        TYPE_BATIMENT_STATION: 7000,
        TYPE_BATIMENT_ENNEMI: 30000,
        TYPE_PERSONNE_PORTEUR: 1200,
        TYPE_PERSONNE_COLTINEUR: 800,
        TYPE_PERSONNE_CHARGEUR: 2000,
        TYPE_PERSONNE_SOLDAT: 1600,
        TYPE_PERSONNE_TIRAILLEUR: 2000,
        TYPE_PERSONNE_TANK: 3200
    },
    PARAM_F_NOM: {
        TYPE_BATIMENT_BASE: 'Base',
        TYPE_BATIMENT_ENTREPOT: 'Entrepot',
        TYPE_BATIMENT_GUILDE: 'Guilde',
        TYPE_BATIMENT_LABO: 'Labo',
        TYPE_BATIMENT_CENTRE: 'Centre',
        TYPE_BATIMENT_TOURELLE: 'Tourelle',
        TYPE_BATIMENT_CASERNE: 'Caserne',
        TYPE_BATIMENT_STATION: 'Station',
        TYPE_BATIMENT_ENNEMI: 'Base ennemi',
        TYPE_PERSONNE_PORTEUR: 'Soigneur',
        TYPE_PERSONNE_COLTINEUR: 'Coltineur',
        TYPE_PERSONNE_CHARGEUR: 'Chargeur',
        TYPE_PERSONNE_SOLDAT: 'Unité',
        TYPE_PERSONNE_TIRAILLEUR: 'Tirailleur',
        TYPE_PERSONNE_TANK: 'Tank'
    },
    PARAM_F_DESCRIPTION: {
        TYPE_BATIMENT_BASE: ["    Ce bâtiment est le bâtiment ",
                             "phare de votre ville. C’est le seul ",
                             "qui vous permettra de convertir le ",
                             "minerai en argent. Il joue de plus ",
                             "le rôle d’entrepôt et contient tout ",
                             "votre stock d’argent. "],
        TYPE_BATIMENT_ENTREPOT: ["    L’entrepot vous permettra de ",
                                 "créer et libérer de l’espace dans ",
                                 "votre ville en accueillant des ",
                                 "personnes, chacune occupant un ",
                                 "nombre de place spécifique."],
        TYPE_BATIMENT_GUILDE: ["    La guide vous permettra de ",
                               "créer des porteurs et d’en ",
                               "augmenter ainsi le nombre. Tout ",
                               "comme le labo elle est aussi ",
                               "capable de les améliorer pour les ",
                               "rendre plus performants. "],
        TYPE_BATIMENT_LABO: ["    Le labo améliore les capacités ",
                             "de vos porteurs dans le but de ",
                             "vous enrichir plus rapidement et ",
                             "d’accélérer le flux d’argent entre ",
                             "vos bâtiments."],
        TYPE_BATIMENT_CASERNE: ["    Ce bâtiment est dédié à la ",
                                "création, l’amélioration et ",
                                "l’entrainement de vos soldats. La ",
                                "caserne est donc primordiale pour ",
                                "vous défendre et pour attaquer ",
                                "vos ennemis."],
        TYPE_BATIMENT_CENTRE: ["    Le centre est un bâtiment ",
                               "incontournable car il renforce vos ",
                               "défenses et améliore considéra-",
                               "blement vos armes d’attaque. ",
                               "C’est votre seul moyen de ",
                               "survivre."],
        TYPE_BATIMENT_TOURELLE: ["    La tourelle est le seul bâtiment ",
                                 "capable de tirer sur vos ennemis. ",
                                 "C’est ainsi un bon moyen de ",
                                 "défense mais aussi une redou-",
                                 "table arme d’attaque surtout ",
                                 "quand elle est bien améliorée."],
        TYPE_BATIMENT_STATION: ["    La station permet à vos ",
                                "personnes de récupérer ",
                                "doucement leur vie une fois à ",
                                "l’intérieur du bâtiment. "],
        TYPE_BATIMENT_ENNEMI: ["    Les ennemis se reproduisent ",
                               "vite et progressent à chaque ",
                               "nouvelle génération. C’est ici, ",
                               "dans leur base qu’ils se créent, ",
                               "tout comme les vagues ",
                               "d’assaillants..."],
        TYPE_PERSONNE_PORTEUR: ["    Capable de puiser des ",
                                "ressources, il ne peut par contre ",
                                "participer aux constructions.",
                                "Il est néanmoins essentiel car il ",
                                "donne des vies aux bâtiments si ",
                                "besoin."],
        TYPE_PERSONNE_COLTINEUR: ["    Etant le plus rapide, le coltineur ",
                                  "vous sera utile pour transporter ",
                                  "du minerai et du liquide. Il ",
                                  "emmènera efficacement de ",
                                  "petites quantités de ressources ",
                                  "vers vos bâtiments ou vos bases."],
        TYPE_PERSONNE_CHARGEUR: ["    Le chargeur rempli ",
                                 "parfaitement sa mission : l’apport ",
                                 "d’argent sur les chantiers. Bien ",
                                 "que lent, ses gros chargements le ",
                                 "rendent très efficace."],
        TYPE_PERSONNE_SOLDAT: ["    L’unité est le soldat le moins ",
                               "couteux, mais le plus rapide. Ainsi, ",
                               "il peut parcourir de grandes dis-",
                               "tances en peu de temps. De plus  ",
                               "ce soldat peut devenir « secret ». ",
                               "L’unité est un véritable atout."],
        TYPE_PERSONNE_TIRAILLEUR: ["    Le tirailleur tire extrêmement ",
                                   "rapidement et ce déplace ",
                                   "relativement vite. Il peut donc ",
                                   "aisément aller repousser une at-",
                                   "taque. C’est un soldat  performant ",
                                   "en attaque comme en défense. "],
        TYPE_PERSONNE_TANK: ["    Le tank est certes le soldat le ",
                             "plus lent, mais il reste redoutable ",
                             "avec sa portée de tir très import-",
                             "ante et sa force de tir énorme. ",
                             "Cette puissance compense son ",
                             "temps de recharge et sa cadence."]
    },
    PARAM_F_TYPE_EXPLOSION: {
        TYPE_BATIMENT_BASE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_ENTREPOT: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_GUILDE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_LABO: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_CENTRE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_TOURELLE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_CASERNE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_STATION: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_ENNEMI: TYPE_EXPLOSION_GROSSE,
        TYPE_PERSONNE_PORTEUR: TYPE_EXPLOSION_MOYENNE,
        TYPE_PERSONNE_COLTINEUR: TYPE_EXPLOSION_MOYENNE,
        TYPE_PERSONNE_CHARGEUR: TYPE_EXPLOSION_MOYENNE,
        TYPE_PERSONNE_SOLDAT: TYPE_EXPLOSION_MOYENNE,
        TYPE_PERSONNE_TIRAILLEUR: TYPE_EXPLOSION_MOYENNE,
        TYPE_PERSONNE_TANK: TYPE_EXPLOSION_MOYENNE
    },
    # Tous les batiments :
    PARAM_F_BATIMENT_LISTE_CASES: {
        TYPE_BATIMENT_BASE: {
            TYPE_CASE_PLEINE: [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
            TYPE_CASE_S_DEPOS: [],
            TYPE_CASE_S_RELAIS: [(0, -2), (0, 2), (-2, 0), (2, 0)],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_ENTREPOT: {
            TYPE_CASE_PLEINE: [(-1, 2), (-2, -1), (2, 1), (1, -2), (-1, 1), (-1, -1), (1, 1),
                               (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)],
            TYPE_CASE_S_DEPOS: [(0, 2), (0, -2), (-2, 0), (2, 0)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_GUILDE: {
            TYPE_CASE_PLEINE: [(-2, 2), (2, -2), (-2, 1), (-1, 2), (2, -1), (1, -2), (1, 2),
                               (2, 1), (1, 1), (-2, -2), (-1, -1), (-2, -1), (-1, -2)],
            TYPE_CASE_S_DEPOS: [(0, 0)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_LABO: {
            TYPE_CASE_PLEINE: [(0, 0), (0, 1), (1, 0), (1, 1)],
            TYPE_CASE_S_DEPOS: [(0, -1), (-1, 1), (2, 0)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_CASERNE: {
            TYPE_CASE_PLEINE: [(2, 2), (2, 1), (1, 2), (1, 1), (2, 0), (0, 2), (0, 1), (1, 0), (-1, 2),
                               (2, -1), (0, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-2, 1), (1, -2),
                               (-1, -1), (-2, 0), (0, -2), (-2, -1), (-1, -2), (-2, -2)],
            TYPE_CASE_S_DEPOS: [(-2, 2), (2, -2)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_CENTRE: {
            TYPE_CASE_PLEINE: [(1, 2), (-1, 2), (1, 1), (-1, 1), (1, 0), (-1, 0), (-1, -1), (0, -1), (1, -1),
                               (-1, -2), (0, -2), (1, -2), (-2, 0), (2, 0), (-2, -1), (2, -1), (-2, -2), (2, -2)],
            TYPE_CASE_S_DEPOS: [(0, 0)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_TOURELLE: {
            TYPE_CASE_PLEINE: [(0, 0)],
            TYPE_CASE_S_DEPOS: [(-1, 0), (0, -1), (0, 1), (1, 0)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        },
        TYPE_BATIMENT_STATION: {
            TYPE_CASE_PLEINE: [(2, 1), (2, 2), (2, -1), (2, -2), (1, 2), (1, -2),
                               (-1, 2), (-1, -2), (-2, 1), (-2, 2), (-2, -1), (-2, -2)],
            TYPE_CASE_S_DEPOS: [(2, 0), (-2, 0), (0, 2), (0, -2)],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        },
        TYPE_BATIMENT_ENNEMI: {
            TYPE_CASE_PLEINE: [(i, j) for i in range(-3, 4) for j in range(-3, 4)],
            TYPE_CASE_S_DEPOS: [],
            TYPE_CASE_S_RELAIS: [],
            TYPE_CASE_S_REGEN: []
        }
    },
    PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES: {
        TYPE_BATIMENT_BASE: [(25, 20, 14), (43, 34, 23), (33, 26, 18), (43, 34, 23), (33, 26, 18),
                             (33, 26, 18), (43, 34, 23), (33, 26, 18), (43, 34, 23)],
        TYPE_BATIMENT_ENTREPOT: [(31, 31, 31), (31, 31, 31), (31, 31, 31), (31, 31, 31), (29, 29, 29), (29, 29, 29),
                                 (29, 29, 29), (29, 29, 29), (27, 27, 27), (27, 27, 27), (27, 27, 27), (27, 27, 27),
                                 (23, 23, 23)],
        TYPE_BATIMENT_GUILDE: [(22, 68, 68), (22, 68, 68), (18, 57, 58), (18, 57, 58), (18, 57, 58), (18, 57, 58),
                               (19, 60, 61), (19, 60, 61), (17, 52, 53), (17, 52, 53), (14, 45, 45), (15, 47, 48),
                               (15, 47, 48)],
        TYPE_BATIMENT_LABO: [(34, 7, 47), (23, 6, 31), (23, 6, 31), (34, 7, 47)],
        TYPE_BATIMENT_CASERNE: [(25, 6, 6), (33, 7, 7), (33, 7, 7), (40, 9, 9), (40, 9, 9), (40, 9, 9), (48, 11, 11),
                                (48, 11, 11), (48, 11, 11), (48, 11, 11), (56, 13, 13), (56, 13, 13), (56, 13, 13),
                                (63, 15, 15), (63, 15, 15), (63, 15, 15), (63, 15, 15), (71, 17, 17), (71, 17, 17),
                                (71, 17, 17), (79, 18, 18), (79, 18, 18), (86, 20, 20)],
        TYPE_BATIMENT_CENTRE: [(21, 33, 0), (21, 33, 0), (24, 38, 0), (24, 38, 0), (27, 42, 0), (27, 42, 0),
                               (30, 47, 0), (30, 47, 0), (30, 47, 0), (33, 52, 0), (33, 52, 0), (33, 52, 0),
                               (27, 44, 0), (27, 44, 0), (30, 43, 0), (30, 43, 0), (33, 54, 0), (33, 54, 0)],
        TYPE_BATIMENT_TOURELLE: [(20, 20, 20)],
        TYPE_BATIMENT_STATION: [(0, 23, 0), (0, 10, 0), (0, 23, 0), (0, 10, 0), (0, 23, 0), (0, 23, 0), (0, 23, 0),
                                (0, 23, 0), (0, 23, 0), (0, 10, 0), (0, 23, 0), (0, 10, 0)],
        TYPE_BATIMENT_ENNEMI: [GRIS_FONCE for _ in range(49)]
    },
    PARAM_A_BATIMENT_NB_PLACES: {
        TYPE_BATIMENT_BASE: 5,
        TYPE_BATIMENT_ENTREPOT: 8,
        TYPE_BATIMENT_GUILDE: 0,
        TYPE_BATIMENT_LABO: 0,
        TYPE_BATIMENT_CENTRE: 0,
        TYPE_BATIMENT_TOURELLE: 0,
        TYPE_BATIMENT_CASERNE: 0,
        TYPE_BATIMENT_STATION: 0,
    },
    PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES: {
        TYPE_BATIMENT_BASE: [],
        TYPE_BATIMENT_ENTREPOT: [],
        TYPE_BATIMENT_GUILDE: [TYPE_PERSONNE_COLTINEUR],
        TYPE_BATIMENT_LABO: [],
        TYPE_BATIMENT_CENTRE: [],
        TYPE_BATIMENT_TOURELLE: [],
        TYPE_BATIMENT_CASERNE: [TYPE_PERSONNE_SOLDAT],
        TYPE_BATIMENT_STATION: [],
    },
    PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES: {
        TYPE_BATIMENT_BASE: [TYPE_AMELIORATION_BATIMENT_COMPTENU,
                             TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES,
                             TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1],
        TYPE_BATIMENT_ENTREPOT: [],
        TYPE_BATIMENT_GUILDE: [TYPE_AMELIORATION_COTINEURS_VITESSE,
                               TYPE_AMELIORATION_DEBLOQUE_CHARGEURS],
        TYPE_BATIMENT_LABO: [TYPE_AMELIORATION_DEBLOQUE_PORTEURS,
                             TYPE_AMELIORATION_PORTEURS_COMPTENU],
        TYPE_BATIMENT_CENTRE: [TYPE_AMELIORATION_SOLDATS_VIES_1,
                               TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1,
                               TYPE_AMELIORATION_TOURELLE_VIES_1,
                               TYPE_AMELIORATION_TOURELLE_TIR_1,
                               TYPE_AMELIORATION_STATION_VIES,
                               TYPE_AMELIORATION_VITESSE_RECHARGE_1,
                               TYPE_AMELIORATION_STATION_PRIX,
                               TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION],
        TYPE_BATIMENT_TOURELLE: [],
        TYPE_BATIMENT_CASERNE: [TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS,
                                TYPE_AMELIORATION_DEBLOQUE_TANK,
                                TYPE_AMELIORATION_SOLDATS_VITESSE_1,
                                TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE],
        TYPE_BATIMENT_STATION: [],
    },
    PARAM_F_BATIMENT_PEUT_TIRER: {
        TYPE_BATIMENT_BASE: False,
        TYPE_BATIMENT_ENTREPOT: False,
        TYPE_BATIMENT_GUILDE: False,
        TYPE_BATIMENT_LABO: False,
        TYPE_BATIMENT_CENTRE: False,
        TYPE_BATIMENT_TOURELLE: True,
        TYPE_BATIMENT_CASERNE: False,
        TYPE_BATIMENT_STATION: False,
    },
    PARAM_A_BATIMENT_NB_VIES_REGEN: {
        TYPE_BATIMENT_BASE: 0,
        TYPE_BATIMENT_ENTREPOT: 0,
        TYPE_BATIMENT_GUILDE: 0,
        TYPE_BATIMENT_LABO: 0,
        TYPE_BATIMENT_CENTRE: 0,
        TYPE_BATIMENT_TOURELLE: 0,
        TYPE_BATIMENT_CASERNE: 0,
        TYPE_BATIMENT_STATION: 8,
    },
    # Toutes les constructions (batiments + personnes) :
    PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION: {
        TYPE_BATIMENT_BASE: 150,
        TYPE_BATIMENT_ENTREPOT: 70,
        TYPE_BATIMENT_GUILDE: 80,
        TYPE_BATIMENT_LABO: 90,
        TYPE_BATIMENT_CASERNE: 150,
        TYPE_BATIMENT_CENTRE: 100,
        TYPE_BATIMENT_TOURELLE: 70,
        TYPE_BATIMENT_STATION: 45,
        TYPE_PERSONNE_PORTEUR: 30,
        TYPE_PERSONNE_COLTINEUR: 20,
        TYPE_PERSONNE_CHARGEUR: 50,
        TYPE_PERSONNE_TIRAILLEUR: 100,
        TYPE_PERSONNE_SOLDAT: 60,
        TYPE_PERSONNE_TANK: 150
    },
    PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION: {
        TYPE_BATIMENT_BASE: 0,
        TYPE_BATIMENT_ENTREPOT: 0,
        TYPE_BATIMENT_GUILDE: 20,
        TYPE_BATIMENT_LABO: 75,
        TYPE_BATIMENT_CASERNE: 0,
        TYPE_BATIMENT_CENTRE: 75,
        TYPE_BATIMENT_TOURELLE: 30,
        TYPE_BATIMENT_STATION: 30,
        TYPE_PERSONNE_PORTEUR: 15,
        TYPE_PERSONNE_COLTINEUR: 0,
        TYPE_PERSONNE_CHARGEUR: 40,
        TYPE_PERSONNE_SOLDAT: 10,
        TYPE_PERSONNE_TIRAILLEUR: 20,
        TYPE_PERSONNE_TANK: 50
    },
    PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION: {
        TYPE_BATIMENT_BASE: 500,
        TYPE_BATIMENT_ENTREPOT: 275,
        TYPE_BATIMENT_GUILDE: 350,
        TYPE_BATIMENT_LABO: 325,
        TYPE_BATIMENT_CASERNE: 425,
        TYPE_BATIMENT_CENTRE: 400,
        TYPE_BATIMENT_TOURELLE: 250,
        TYPE_BATIMENT_STATION: 200,
        TYPE_PERSONNE_PORTEUR: 175,
        TYPE_PERSONNE_COLTINEUR: 140,
        TYPE_PERSONNE_CHARGEUR: 400,
        TYPE_PERSONNE_SOLDAT: 170,
        TYPE_PERSONNE_TIRAILLEUR: 245,
        TYPE_PERSONNE_TANK: 425
    },
    # Tous les éléments mobiles :
    PARAM_F_ELEMENT_MOBILE_CHEMIN_IMAGE: {
        TYPE_PERSONNE_PORTEUR: 'Images/porteur.png',
        TYPE_PERSONNE_COLTINEUR: 'Images/coltineur.png',
        TYPE_PERSONNE_CHARGEUR: 'Images/chargeur.png',
        TYPE_PERSONNE_TIRAILLEUR: 'Images/tirailleur.png',
        TYPE_PERSONNE_SOLDAT: 'Images/soldat.png',
        TYPE_PERSONNE_TANK: 'Images/tank.png'
    },
    PARAM_F_ELEMENT_MOBILE_RAYON: {
        TYPE_PERSONNE_PORTEUR: 31,
        TYPE_PERSONNE_COLTINEUR: 30,
        TYPE_PERSONNE_CHARGEUR: 36,
        TYPE_PERSONNE_TIRAILLEUR: 36,
        TYPE_PERSONNE_SOLDAT: 29,
        TYPE_PERSONNE_TANK: 38
    },
    PARAM_F_ELEMENT_MOBILE_SCALE_IMAGE_ZOOM: {
        TYPE_PERSONNE_PORTEUR: 0.62,
        TYPE_PERSONNE_COLTINEUR: 0.52,
        TYPE_PERSONNE_CHARGEUR: 0.7,
        TYPE_PERSONNE_TIRAILLEUR: 0.8,
        TYPE_PERSONNE_SOLDAT: 0.7,
        TYPE_PERSONNE_TANK: 0.8
    },
    PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT: {
        TYPE_PERSONNE_PORTEUR: 8,
        TYPE_PERSONNE_COLTINEUR: 8,
        TYPE_PERSONNE_CHARGEUR: 3.2,
        TYPE_PERSONNE_SOLDAT: 8.6,
        TYPE_PERSONNE_TIRAILLEUR: 8,
        TYPE_PERSONNE_TANK: 3.2
    },
    PARAM_F_ELEMENT_MOBILE_MASSE_RELATIVE: {
        TYPE_PERSONNE_PORTEUR: 6,
        TYPE_PERSONNE_COLTINEUR: 4,
        TYPE_PERSONNE_CHARGEUR: 12,
        TYPE_PERSONNE_SOLDAT: 5,
        TYPE_PERSONNE_TIRAILLEUR: 7,
        TYPE_PERSONNE_TANK: 20
    },
    # Toutes les personnes
    PARAM_F_PERSONNE_TYPE_CLASS: {
        TYPE_PERSONNE_PORTEUR: TYPE_PERSONNE_CLASS_PORTEUR,
        TYPE_PERSONNE_COLTINEUR: TYPE_PERSONNE_CLASS_PORTEUR,
        TYPE_PERSONNE_CHARGEUR: TYPE_PERSONNE_CLASS_PORTEUR,
        TYPE_PERSONNE_SOLDAT: TYPE_PERSONNE_CLASS_SOLDAT,
        TYPE_PERSONNE_TIRAILLEUR: TYPE_PERSONNE_CLASS_SOLDAT,
        TYPE_PERSONNE_TANK: TYPE_PERSONNE_CLASS_SOLDAT
    },
    PARAM_A_PERSONNE_NB_PLACES: {
        TYPE_PERSONNE_PORTEUR: 1,
        TYPE_PERSONNE_COLTINEUR: 1,
        TYPE_PERSONNE_CHARGEUR: 2,
        TYPE_PERSONNE_SOLDAT: 1,
        TYPE_PERSONNE_TIRAILLEUR: 2,
        TYPE_PERSONNE_TANK: 3
    },
    # Tous les compteneurs (batiments + porteurs)
    PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX: {
        TYPE_BATIMENT_BASE: math.inf,
        TYPE_BATIMENT_ENTREPOT: 0,
        TYPE_BATIMENT_GUILDE: 200,
        TYPE_BATIMENT_LABO: 200,
        TYPE_BATIMENT_CASERNE: 400,
        TYPE_BATIMENT_CENTRE: 300,
        TYPE_BATIMENT_TOURELLE: 0,
        TYPE_BATIMENT_STATION: 0,
        TYPE_PERSONNE_PORTEUR: 2,
        TYPE_PERSONNE_COLTINEUR: 2,
        TYPE_PERSONNE_CHARGEUR: 10
    },
    # Tous les porteurs
    PARAM_A_PORTEUR_PEUT_RECOLTER: {
        TYPE_PERSONNE_PORTEUR: True,
        TYPE_PERSONNE_COLTINEUR: True,
        TYPE_PERSONNE_CHARGEUR: False,
    },
    PARAM_A_PORTEUR_PEUT_DONNER_VIES: {
        TYPE_PERSONNE_PORTEUR: 12,
        TYPE_PERSONNE_COLTINEUR: False,
        TYPE_PERSONNE_CHARGEUR: False,
    },
    PARAM_F_PORTEUR_DISTANCE_RESSOURCE: {
        TYPE_PERSONNE_PORTEUR: 35,
        TYPE_PERSONNE_COLTINEUR: 32,
        TYPE_PERSONNE_CHARGEUR: 36
    },
    PARAM_F_PORTEUR_RAYON_RESSOURCE: {
        TYPE_PERSONNE_PORTEUR: 15,
        TYPE_PERSONNE_COLTINEUR: 15,
        TYPE_PERSONNE_CHARGEUR: 20
    },
    # Tous les tireurs (soldats + tourelles) :
    PARAM_A_TIREUR_FORCE_TIR: {
        TYPE_PERSONNE_SOLDAT: 18,
        TYPE_PERSONNE_TIRAILLEUR: 10,
        TYPE_PERSONNE_TANK: 250,
        TYPE_BATIMENT_TOURELLE: 10
    },
    PARAM_A_TIREUR_PORTEE_TIR: {
        TYPE_PERSONNE_SOLDAT: 160,
        TYPE_PERSONNE_TIRAILLEUR: 200,
        TYPE_PERSONNE_TANK: 250,
        TYPE_BATIMENT_TOURELLE: 250
    },
    PARAM_A_TIREUR_DELAY_TIR: {
        TYPE_PERSONNE_SOLDAT: 10,
        TYPE_PERSONNE_TIRAILLEUR: 7,
        TYPE_PERSONNE_TANK: 55,
        TYPE_BATIMENT_TOURELLE: 8
    },
    PARAM_A_TIREUR_PORTEE_VISION: {
        TYPE_PERSONNE_SOLDAT: 200,
        TYPE_PERSONNE_TIRAILLEUR: 240,
        TYPE_PERSONNE_TANK: 250,
        TYPE_BATIMENT_TOURELLE: 250
    },
    PARAM_A_TIREUR_INTELLIGENCE: {
        TYPE_PERSONNE_SOLDAT: 2,
        TYPE_PERSONNE_TIRAILLEUR: 3,
        TYPE_PERSONNE_TANK: 4,
        TYPE_BATIMENT_TOURELLE: 1
    },
    PARAM_A_TIREUR_CIBLE_VISIBLE: {
        TYPE_PERSONNE_SOLDAT: True,
        TYPE_PERSONNE_TIRAILLEUR: True,
        TYPE_PERSONNE_TANK: True,
        TYPE_BATIMENT_TOURELLE: True
    },
    PARAM_F_TIREUR_TYPE_EXPLOSION_TIR: {
        TYPE_PERSONNE_SOLDAT: TYPE_EXPLOSION_PETITE,
        TYPE_PERSONNE_TIRAILLEUR: TYPE_EXPLOSION_PETITE,
        TYPE_PERSONNE_TANK: TYPE_EXPLOSION_PETITE,
        TYPE_BATIMENT_TOURELLE: TYPE_EXPLOSION_PETITE
    },
    PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE: {
        TYPE_PERSONNE_SOLDAT: 26,
        TYPE_PERSONNE_TIRAILLEUR: 34,
        TYPE_PERSONNE_TANK: 23,
        TYPE_BATIMENT_TOURELLE: 30
    },
    # Tous les batiments tireurs (tourelles) :
    PARAM_F_BATIMENT_TIREUR_CHEMIN_IMAGE_CANON: {
        TYPE_BATIMENT_TOURELLE: 'Images/canonTourelle.png'
    },
    PARAM_F_BATIMENT_TIREUR_SCALE_IMAGE_CANON_ZOOM: {
        TYPE_BATIMENT_TOURELLE: 0.8
    }
}

LISTE_TYPES_BATIMENTS_CONSTRUCTIBLE = [TYPE_BATIMENT_BASE, TYPE_BATIMENT_ENTREPOT, TYPE_BATIMENT_GUILDE,
                                       TYPE_BATIMENT_LABO, TYPE_BATIMENT_CASERNE, TYPE_BATIMENT_CENTRE,
                                       TYPE_BATIMENT_STATION, TYPE_BATIMENT_TOURELLE]

NB_CONSTRUCTION_EN_ATTENTE_MAX = 4
NB_CONSTRUCTION_POSSIBLE_MAX = 3

COEF_VITESSE_RECHAGRE_VIES = 0.2

COEF_RAYONS_PERSONNES_CHEVAUCHEMENT = 0.8
VITESSE_REPOUSSEMENT_CHEVAUCHEMENTS = 4
ALEA_MAX_PORTEURS_DEPLACEMENT_AUTO = 10
ALEA_MAX_PERSONNES_DEPLACEMENT_GROUPE = lambda n: int(2 * math.sqrt(n) + 18)
ALEA_MAX_PERSONNES_DEPLACEMENT_SEUL = 0
ALEA_MAX_PERSONNES_SORTIE_BATIMENT = 10
ALEA_MAX_PERSONNES_UPDATE_CHEMIN = 0
ALEA_MAX_CREATION_ENNEMI = 100
NB_CHOC_AVANT_ABANDON_OBJECTIF = 100
COEF_RAYONS_DISTANCE_MAX_ABANDON_OBJECTIF = 0.8
COEF_NB_CHOC_AVANT_ABANDON_OBJECTIF_GENERAL_PORTEUR = 10
COEF_NB_CHOC_AVANT_ABANDON_OBJECTIF_CIBLE_SOLDAT = 4

COULEUR_ELEMENT_SELECTION = ROUGE
ANNEAU_SELECTION_DISTANCE = 10
MARGE_OBJECTIF_ATTEIND = 2

TYPE_TRANSACTION_GIVE = 'give'
TYPE_TRANSACTION_GET = 'get'

COULEUR_PORTER_TIR_TIREUR_SELECTION = VERT, 50

DISTANCE_MAX_ADVERSAIRE_AU_DELA_VISION = 250

RATE_MIN = -50000


def rate_adversaire_niv_intelligence_max(distance_carree: float, vies: float, force_sur_cadence_tir: float,
                                         tireur: bool, tireur_actif: bool, ma_force_tir: int):
    vies_malus = vies - ma_force_tir
    if vies_malus < 0:
        vies_malus *= -0.04
    else:
        vies_malus -= int(vies_malus) % ma_force_tir * 0.9
    rate = 100 * force_sur_cadence_tir - vies_malus - 0.008 * distance_carree
    if tireur:
        rate += 1000
        if tireur_actif:
            rate += 1000
    return rate


# VIII. Les ennemis
# =================
ENTREE_MAX = 0
VALEUR_MIN = 1
VALEUR_MAX = 2

DIC_ENNEMIS = {
    PARAM_A_VIES: {
        ENTREE_MAX: 200,
        VALEUR_MIN: 100,
        VALEUR_MAX: 15000
    },
    PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT: {
        ENTREE_MAX: 80,
        VALEUR_MIN: 2,
        VALEUR_MAX: 16
    },
    PARAM_A_TIREUR_FORCE_TIR: {
        ENTREE_MAX: 130,
        VALEUR_MIN: 10,
        VALEUR_MAX: 710
    },
    PARAM_A_TIREUR_DELAY_TIR: {
        ENTREE_MAX: 140,
        VALEUR_MIN: 100,
        VALEUR_MAX: None
    },
    PARAM_A_TIREUR_PORTEE_TIR: {
        ENTREE_MAX: 100,
        VALEUR_MIN: 90,
        VALEUR_MAX: 400
    },
    PARAM_A_TIREUR_PORTEE_VISION: {
        ENTREE_MAX: 30,
        VALEUR_MIN: 0,
        VALEUR_MAX: 50
    },
    PARAM_A_TIREUR_INTELLIGENCE: {
        ENTREE_MAX: 30,
        VALEUR_MIN: 1,
        VALEUR_MAX: 6
    }
}

LISTE_PARAMS_ENNEMIS = [PARAM_A_VIES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT, PARAM_A_TIREUR_FORCE_TIR,
                        PARAM_A_TIREUR_PORTEE_TIR, PARAM_A_TIREUR_DELAY_TIR, PARAM_A_TIREUR_PORTEE_VISION,
                        PARAM_A_TIREUR_INTELLIGENCE]

NB_ENTREES_PAR_VAGUES = [ne for ne in range(30, 90, 3)] + [ne for ne in range(90, 140, 4)] + \
                        [ne for ne in range(140, 170, 3)] + [ne for ne in range(170, 200, 2)] + \
                        [ne for ne in range(200, 250, 1)]
NB_ENTREES_SUP_MAX = 20
NB_ENTREES_CHANGEES_PAR_VAGUES = 5
NB_ENNEMIS_PAR_VAGUE_LISTE = [4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 8]
DELAY_ENTRE_VAGUES = 1100
VARIATION_MAX_DELAY_ENTRE_VAGUES = 400
NB_ENNEMIS_MEMOIRE_STATS = 20
PROBA_VAGUE_NOUVELLE = 8

DIC_ELEMENTS[PARAM_F_NOM][TYPE_ENNEMI] = "Ennemi"
DIC_ELEMENTS[PARAM_F_DESCRIPTION][TYPE_ENNEMI] = ["    Les ennemis sont contre vous et ",
                                                  "veulent vous anéantir... Pas de ",
                                                  "panique,  vous avez à votre ",
                                                  "disposition de quoi les faire ",
                                                  "reculer, reste à savoir si vous en ",
                                                  "serez capable..."]
DIC_ELEMENTS[PARAM_F_TYPE_EXPLOSION][TYPE_ENNEMI] = TYPE_EXPLOSION_MOYENNE
DIC_ELEMENTS[PARAM_F_ELEMENT_MOBILE_CHEMIN_IMAGE][TYPE_ENNEMI] = 'Images/ennemi.png'
DIC_ELEMENTS[PARAM_F_ELEMENT_MOBILE_RAYON][TYPE_ENNEMI] = 31
DIC_ELEMENTS[PARAM_F_ELEMENT_MOBILE_SCALE_IMAGE_ZOOM][TYPE_ENNEMI] = 0.65
DIC_ELEMENTS[PARAM_F_TIREUR_TYPE_EXPLOSION_TIR][TYPE_ENNEMI] = TYPE_EXPLOSION_PETITE
DIC_ELEMENTS[PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE][TYPE_ENNEMI] = 30
DIC_ELEMENTS[PARAM_F_ELEMENT_MOBILE_MASSE_RELATIVE][TYPE_ENNEMI] = 7

COEF_NOTE_ENNEMI_DEGAS_BATIMENT = 1
COEF_NOTE_ENNEMI_DEGAS_ELEMENT_MOBILE = 1.2
COEF_NOTE_ENNEMI_VICTIME = 2

TYPE_VAGUE_ENNEMI_DEFFENCEIVE_IMMOBILE = 0
TYPE_VAGUE_ENNEMI_DEFFENCEIVE_LIBRE = 1
TYPE_VAGUE_ENNEMI_OFFENCIVE = 2
LISTE_VAGUES_ENNEMIS = [TYPE_VAGUE_ENNEMI_DEFFENCEIVE_IMMOBILE] * 1 + \
                       [TYPE_VAGUE_ENNEMI_DEFFENCEIVE_LIBRE] * 12 + \
                       [TYPE_VAGUE_ENNEMI_OFFENCIVE] * 2
NB_VAGUES_ENNEMIS_INIT = 10

NUM_BASE_ENNEMIE_DETRUITE = -1

# IX. Les améliorations
# =====================
PARAM_AMELIORATION_PRIX_ARGENT = 0
PARAM_AMELIORATION_PRIX_LIQUIDE = 1
PARAM_AMELIORATION_LISTE__TYPE_PARAM_VALUE = 2
PARAM_AMELIORATION_LISTE_TPV_AFFICHAGE = 3
PARAM_AMELIORATION_DUREE = 4
PARAM_AMELIORATION_NOM = 5

DIC_AMELIORATIONS = {
    PARAM_AMELIORATION_PRIX_ARGENT: {
        TYPE_AMELIORATION_PORTEURS_COMPTENU: 120,
        TYPE_AMELIORATION_COTINEURS_VITESSE: 80,
        TYPE_AMELIORATION_DEBLOQUE_PORTEURS: 90,
        TYPE_AMELIORATION_PORTEURS_VIES: 150,
        TYPE_AMELIORATION_PORTEURS_VIES_2: 200,
        TYPE_AMELIORATION_CHARGEURS_COMPTENU: 120,
        TYPE_AMELIORATION_DEBLOQUE_CHARGEURS: 150,
        TYPE_AMELIORATION_CHARGEURS_VITESSE: 200,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1: 150,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2: 200,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3: 250,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4: 300,
        TYPE_AMELIORATION_SOLDATS_VIES_1: 150,
        TYPE_AMELIORATION_SOLDATS_VIES_2: 200,
        TYPE_AMELIORATION_SOLDATS_VIES_3: 250,
        TYPE_AMELIORATION_SOLDATS_VIES_4: 300,
        TYPE_AMELIORATION_SOLDATS_VITESSE_1: 110,
        TYPE_AMELIORATION_SOLDATS_VITESSE_2: 140,
        TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE: 100,
        TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS: 100,
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1: 130,
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2: 160,
        TYPE_AMELIORATION_DEBLOQUE_TANK: 150,
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_1: 150,
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_2: 180,
        TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE: 200,
        TYPE_AMELIORATION_BATIMENT_COMPTENU: 0,
        TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES: 0,
        TYPE_AMELIORATION_TOURELLE_VIES_1: 125,
        TYPE_AMELIORATION_TOURELLE_VIES_2: 175,
        TYPE_AMELIORATION_TOURELLE_TIR_1: 200,
        TYPE_AMELIORATION_TOURELLE_TIR_2: 250,
        TYPE_AMELIORATION_TOURELLE_TIR_3: 300,
        TYPE_AMELIORATION_STATION_VIES: 200,
        TYPE_AMELIORATION_VITESSE_RECHARGE_1: 200,
        TYPE_AMELIORATION_VITESSE_RECHARGE_2: 250,
        TYPE_AMELIORATION_STATION_PRIX: 300,
        TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION: 115,
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1: 0,
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2: 0
    },
    PARAM_AMELIORATION_PRIX_LIQUIDE: {
        TYPE_AMELIORATION_PORTEURS_COMPTENU: 80,
        TYPE_AMELIORATION_COTINEURS_VITESSE: 50,
        TYPE_AMELIORATION_DEBLOQUE_PORTEURS: 70,
        TYPE_AMELIORATION_PORTEURS_VIES: 100,
        TYPE_AMELIORATION_PORTEURS_VIES_2: 120,
        TYPE_AMELIORATION_CHARGEURS_COMPTENU: 80,
        TYPE_AMELIORATION_DEBLOQUE_CHARGEURS: 50,
        TYPE_AMELIORATION_CHARGEURS_VITESSE: 150,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1: 50,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2: 100,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3: 150,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4: 200,
        TYPE_AMELIORATION_SOLDATS_VIES_1: 50,
        TYPE_AMELIORATION_SOLDATS_VIES_2: 100,
        TYPE_AMELIORATION_SOLDATS_VIES_3: 150,
        TYPE_AMELIORATION_SOLDATS_VIES_4: 200,
        TYPE_AMELIORATION_SOLDATS_VITESSE_1: 60,
        TYPE_AMELIORATION_SOLDATS_VITESSE_2: 80,
        TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE: 80,
        TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS: 80,
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1: 80,
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2: 100,
        TYPE_AMELIORATION_DEBLOQUE_TANK: 100,
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_1: 100,
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_2: 120,
        TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE: 150,
        TYPE_AMELIORATION_BATIMENT_COMPTENU: 275,
        TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES: 400,
        TYPE_AMELIORATION_TOURELLE_VIES_1: 75,
        TYPE_AMELIORATION_TOURELLE_VIES_2: 125,
        TYPE_AMELIORATION_TOURELLE_TIR_1: 75,
        TYPE_AMELIORATION_TOURELLE_TIR_2: 125,
        TYPE_AMELIORATION_TOURELLE_TIR_3: 175,
        TYPE_AMELIORATION_STATION_VIES: 50,
        TYPE_AMELIORATION_VITESSE_RECHARGE_1: 100,
        TYPE_AMELIORATION_VITESSE_RECHARGE_2: 150,
        TYPE_AMELIORATION_STATION_PRIX: 0,
        TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION: 115,
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1: 150,
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2: 150
    },
    PARAM_AMELIORATION_LISTE__TYPE_PARAM_VALUE: {
        TYPE_AMELIORATION_PORTEURS_COMPTENU: [(TYPE_PERSONNE_PORTEUR,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 3),
                                              (TYPE_PERSONNE_COLTINEUR,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 3),
                                              (TYPE_PERSONNE_CHARGEUR,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 16),
                                              (TYPE_BATIMENT_LABO, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                               TYPE_AMELIORATION_CHARGEURS_COMPTENU)],
        TYPE_AMELIORATION_COTINEURS_VITESSE: [(TYPE_PERSONNE_COLTINEUR,
                                               PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT, 10)],
        TYPE_AMELIORATION_DEBLOQUE_PORTEURS: [(TYPE_BATIMENT_GUILDE, PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES,
                                               TYPE_PERSONNE_PORTEUR),
                                              (TYPE_BATIMENT_LABO, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                               TYPE_AMELIORATION_PORTEURS_VIES)],
        TYPE_AMELIORATION_PORTEURS_VIES: [(TYPE_PERSONNE_PORTEUR, PARAM_A_VIES, 3000),
                                          (TYPE_BATIMENT_LABO, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                           TYPE_AMELIORATION_PORTEURS_VIES_2)],
        TYPE_AMELIORATION_PORTEURS_VIES_2: [(TYPE_PERSONNE_PORTEUR, PARAM_A_VIES, 5000),
                                            (TYPE_PERSONNE_PORTEUR, PARAM_F_ELEMENT_MOBILE_SCALE_IMAGE_ZOOM, 0.7),
                                            (TYPE_PERSONNE_PORTEUR, PARAM_F_ELEMENT_MOBILE_RAYON, 33),
                                            (TYPE_PERSONNE_PORTEUR, PARAM_F_ELEMENT_MOBILE_MASSE_RELATIVE, 8)],
        TYPE_AMELIORATION_CHARGEURS_COMPTENU: [(TYPE_PERSONNE_CHARGEUR,
                                                PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 24)],
        TYPE_AMELIORATION_DEBLOQUE_CHARGEURS: [(TYPE_BATIMENT_GUILDE, PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES,
                                                TYPE_PERSONNE_CHARGEUR),
                                               (TYPE_BATIMENT_GUILDE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                TYPE_AMELIORATION_CHARGEURS_VITESSE)],
        TYPE_AMELIORATION_CHARGEURS_VITESSE: [(TYPE_PERSONNE_CHARGEUR,
                                               PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT, 4.6)],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_FORCE_TIR, 23),
                                                (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_FORCE_TIR, 14),
                                                (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_FORCE_TIR, 275),
                                                (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                 TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2)],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_FORCE_TIR, 28),
                                                (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_FORCE_TIR, 18),
                                                (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_FORCE_TIR, 325),
                                                (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                 TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3)],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_FORCE_TIR, 35),
                                                (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_FORCE_TIR, 22),
                                                (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_FORCE_TIR, 400),
                                                (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                 TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4)],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_FORCE_TIR, 45),
                                                (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_FORCE_TIR, 28),
                                                (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_FORCE_TIR, 500)],
        TYPE_AMELIORATION_SOLDATS_VIES_1: [(TYPE_PERSONNE_SOLDAT, PARAM_A_VIES, 1800),
                                           (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_VIES, 2200),
                                           (TYPE_PERSONNE_TANK, PARAM_A_VIES, 3450),
                                           (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                            TYPE_AMELIORATION_SOLDATS_VIES_2)],
        TYPE_AMELIORATION_SOLDATS_VIES_2: [(TYPE_PERSONNE_SOLDAT, PARAM_A_VIES, 1950),
                                           (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_VIES, 2450),
                                           (TYPE_PERSONNE_TANK, PARAM_A_VIES, 3750),
                                           (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                            TYPE_AMELIORATION_SOLDATS_VIES_3)],
        TYPE_AMELIORATION_SOLDATS_VIES_3: [(TYPE_PERSONNE_SOLDAT, PARAM_A_VIES, 2200),
                                           (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_VIES, 2700),
                                           (TYPE_PERSONNE_TANK, PARAM_A_VIES, 4000),
                                           (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                            TYPE_AMELIORATION_SOLDATS_VIES_4)],
        TYPE_AMELIORATION_SOLDATS_VIES_4: [(TYPE_PERSONNE_SOLDAT, PARAM_A_VIES, 2500),
                                           (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_VIES, 3050),
                                           (TYPE_PERSONNE_TANK, PARAM_A_VIES, 4300)],
        TYPE_AMELIORATION_SOLDATS_VITESSE_1: [(TYPE_PERSONNE_SOLDAT, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT, 9.8),
                                              (TYPE_BATIMENT_CASERNE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                               TYPE_AMELIORATION_SOLDATS_VITESSE_2),
                                              ],
        TYPE_AMELIORATION_SOLDATS_VITESSE_2: [(TYPE_PERSONNE_SOLDAT, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT, 10.2)],
        TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_CIBLE_VISIBLE, False)],
        TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS: [(TYPE_BATIMENT_CASERNE,
                                                  PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES,
                                                  TYPE_PERSONNE_TIRAILLEUR),
                                                 (TYPE_BATIMENT_CASERNE,
                                                  PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                  TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1)],
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1: [(TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_DELAY_TIR, 5),
                                                    (TYPE_BATIMENT_CASERNE,
                                                     PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                     TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2)],
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2: [(TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_DELAY_TIR, 2)],
        TYPE_AMELIORATION_DEBLOQUE_TANK: [(TYPE_BATIMENT_CASERNE,
                                           PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES,
                                           TYPE_PERSONNE_TANK),
                                          (TYPE_BATIMENT_CASERNE,
                                           PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                           TYPE_AMELIORATION_TANKS_PORTEE_TIR_1),
                                          (TYPE_BATIMENT_CASERNE,
                                           PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                           TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE)],
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_1: [(TYPE_PERSONNE_TANK, PARAM_A_TIREUR_PORTEE_TIR, 300),
                                               (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_PORTEE_VISION, 300),
                                               (TYPE_BATIMENT_CASERNE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                TYPE_AMELIORATION_TANKS_PORTEE_TIR_2)],
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_2: [(TYPE_PERSONNE_TANK, PARAM_A_TIREUR_PORTEE_TIR, 370),
                                               (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_PORTEE_VISION, 370)],
        TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE: [(TYPE_PERSONNE_TANK, PARAM_A_TIREUR_DELAY_TIR, 45),
                                                       (TYPE_PERSONNE_TANK, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT,
                                                        3.8)],
        TYPE_AMELIORATION_BATIMENT_COMPTENU: [(TYPE_BATIMENT_GUILDE,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 300),
                                              (TYPE_BATIMENT_LABO,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 300),
                                              (TYPE_BATIMENT_CASERNE,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 600),
                                              (TYPE_BATIMENT_CENTRE,
                                               PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, 450)],
        TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES: [(TYPE_BATIMENT_ENTREPOT, PARAM_A_BATIMENT_NB_PLACES, 14),
                                                       (TYPE_BATIMENT_BASE, PARAM_A_BATIMENT_NB_PLACES, 10)],
        TYPE_AMELIORATION_TOURELLE_VIES_1: [(TYPE_BATIMENT_TOURELLE, PARAM_A_VIES, 3000),
                                            (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                             TYPE_AMELIORATION_TOURELLE_VIES_2)],
        TYPE_AMELIORATION_TOURELLE_VIES_2: [(TYPE_BATIMENT_TOURELLE, PARAM_A_VIES, 4000)],
        TYPE_AMELIORATION_TOURELLE_TIR_1: [(TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_FORCE_TIR, 20),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_DELAY_TIR, 7),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_PORTEE_TIR, 270),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_PORTEE_VISION, 270),
                                           (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                            TYPE_AMELIORATION_TOURELLE_TIR_2)],
        TYPE_AMELIORATION_TOURELLE_TIR_2: [(TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_FORCE_TIR, 28),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_DELAY_TIR, 5),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_PORTEE_TIR, 300),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_PORTEE_VISION, 300),
                                           (TYPE_BATIMENT_CENTRE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                            TYPE_AMELIORATION_TOURELLE_TIR_3)],
        TYPE_AMELIORATION_TOURELLE_TIR_3: [(TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_FORCE_TIR, 30),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_DELAY_TIR, 4),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_PORTEE_TIR, 360),
                                           (TYPE_BATIMENT_TOURELLE, PARAM_A_TIREUR_PORTEE_VISION, 360)],
        TYPE_AMELIORATION_STATION_VIES: [(TYPE_BATIMENT_STATION, PARAM_A_VIES, 1600)],
        TYPE_AMELIORATION_VITESSE_RECHARGE_1: [(TYPE_BATIMENT_STATION, PARAM_A_BATIMENT_NB_VIES_REGEN, 12),
                                               (TYPE_PERSONNE_PORTEUR, PARAM_A_PORTEUR_PEUT_DONNER_VIES, 18),
                                               (TYPE_BATIMENT_CENTRE,
                                                PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                TYPE_AMELIORATION_VITESSE_RECHARGE_2)],
        TYPE_AMELIORATION_VITESSE_RECHARGE_2: [(TYPE_BATIMENT_STATION, PARAM_A_BATIMENT_NB_VIES_REGEN, 20),
                                               (TYPE_PERSONNE_PORTEUR, PARAM_A_PORTEUR_PEUT_DONNER_VIES, 28)],
        TYPE_AMELIORATION_STATION_PRIX: [(TYPE_BATIMENT_STATION,
                                          PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION, 24),
                                         (TYPE_BATIMENT_STATION,
                                          PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION, 40)],
        TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION: [(TYPE_BATIMENT_TOURELLE,
                                                                      PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION,
                                                                      150),
                                                                     (TYPE_BATIMENT_STATION,
                                                                      PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION,
                                                                      100)],
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_INTELLIGENCE, 3),
                                                   (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_INTELLIGENCE, 4),
                                                   (TYPE_PERSONNE_TANK, PARAM_A_TIREUR_INTELLIGENCE, 6),
                                                   (TYPE_BATIMENT_BASE, PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES,
                                                    TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2)],
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2: [(TYPE_PERSONNE_SOLDAT, PARAM_A_TIREUR_INTELLIGENCE, 6),
                                                   (TYPE_PERSONNE_TIRAILLEUR, PARAM_A_TIREUR_INTELLIGENCE, 6)]
    },
    PARAM_AMELIORATION_LISTE_TPV_AFFICHAGE: {
        TYPE_AMELIORATION_PORTEURS_COMPTENU: [True, True, True, True],
        TYPE_AMELIORATION_COTINEURS_VITESSE: [True],
        TYPE_AMELIORATION_DEBLOQUE_PORTEURS: [True, True],
        TYPE_AMELIORATION_PORTEURS_VIES: [True, True],
        TYPE_AMELIORATION_PORTEURS_VIES_2: [True, False, False, False],
        TYPE_AMELIORATION_CHARGEURS_COMPTENU: [True],
        TYPE_AMELIORATION_DEBLOQUE_CHARGEURS: [True, True],
        TYPE_AMELIORATION_CHARGEURS_VITESSE: [True],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4: [True, True, True],
        TYPE_AMELIORATION_SOLDATS_VIES_1: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_VIES_2: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_VIES_3: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_VIES_4: [True, True, True],
        TYPE_AMELIORATION_SOLDATS_VITESSE_1: [True, True],
        TYPE_AMELIORATION_SOLDATS_VITESSE_2: [True],
        TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE: [True],
        TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS: [True, True],
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1: [True, True],
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2: [True],
        TYPE_AMELIORATION_DEBLOQUE_TANK: [True, True, True],
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_1: [True, False, True],
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_2: [True, False],
        TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE: [True, True],
        TYPE_AMELIORATION_BATIMENT_COMPTENU: [True, True, True, True],
        TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES: [True, True],
        TYPE_AMELIORATION_TOURELLE_VIES_1: [True, True],
        TYPE_AMELIORATION_TOURELLE_VIES_2: [True],
        TYPE_AMELIORATION_TOURELLE_TIR_1: [True, True, True, False, True],
        TYPE_AMELIORATION_TOURELLE_TIR_2: [True, True, True, False, True],
        TYPE_AMELIORATION_TOURELLE_TIR_3: [True, True, True, False],
        TYPE_AMELIORATION_STATION_VIES: [True],
        TYPE_AMELIORATION_VITESSE_RECHARGE_1: [True, True, True],
        TYPE_AMELIORATION_VITESSE_RECHARGE_2: [True, True],
        TYPE_AMELIORATION_STATION_PRIX: [True, True],
        TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION: [True, True],
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1: [True, True, True, True],
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2: [True, True]
    },
    PARAM_AMELIORATION_DUREE: {
        TYPE_AMELIORATION_PORTEURS_COMPTENU: 2000,
        TYPE_AMELIORATION_COTINEURS_VITESSE: 1000,
        TYPE_AMELIORATION_DEBLOQUE_PORTEURS: 1500,
        TYPE_AMELIORATION_PORTEURS_VIES: 2200,
        TYPE_AMELIORATION_PORTEURS_VIES_2: 2200,
        TYPE_AMELIORATION_CHARGEURS_COMPTENU: 2000,
        TYPE_AMELIORATION_DEBLOQUE_CHARGEURS: 1500,
        TYPE_AMELIORATION_CHARGEURS_VITESSE: 2600,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1: 2200,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2: 2300,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3: 2400,
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4: 2500,
        TYPE_AMELIORATION_SOLDATS_VIES_1: 2200,
        TYPE_AMELIORATION_SOLDATS_VIES_2: 2300,
        TYPE_AMELIORATION_SOLDATS_VIES_3: 2400,
        TYPE_AMELIORATION_SOLDATS_VIES_4: 2500,
        TYPE_AMELIORATION_SOLDATS_VITESSE_1: 2000,
        TYPE_AMELIORATION_SOLDATS_VITESSE_2: 2100,
        TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE: 2000,
        TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS: 1600,
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1: 2000,
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2: 2100,
        TYPE_AMELIORATION_DEBLOQUE_TANK: 1700,
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_1: 2000,
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_2: 2100,
        TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE: 2200,
        TYPE_AMELIORATION_BATIMENT_COMPTENU: 2100,
        TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES: 2200,
        TYPE_AMELIORATION_TOURELLE_VIES_1: 1700,
        TYPE_AMELIORATION_TOURELLE_VIES_2: 1700,
        TYPE_AMELIORATION_TOURELLE_TIR_1: 2000,
        TYPE_AMELIORATION_TOURELLE_TIR_2: 2000,
        TYPE_AMELIORATION_TOURELLE_TIR_3: 2000,
        TYPE_AMELIORATION_STATION_VIES: 1700,
        TYPE_AMELIORATION_VITESSE_RECHARGE_1: 2000,
        TYPE_AMELIORATION_VITESSE_RECHARGE_2: 2000,
        TYPE_AMELIORATION_STATION_PRIX: 1700,
        TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION: 1700,
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1: 1500,
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2: 5100
    },
    PARAM_AMELIORATION_NOM: {
        TYPE_AMELIORATION_PORTEURS_COMPTENU: "Comptenu porteurs",
        TYPE_AMELIORATION_COTINEURS_VITESSE: "Vitesse Coltineur",
        TYPE_AMELIORATION_DEBLOQUE_PORTEURS: "Débloque Soigneur",
        TYPE_AMELIORATION_PORTEURS_VIES: "Vies Soigneur 1",
        TYPE_AMELIORATION_PORTEURS_VIES_2: "Vies Soigneur 2",
        TYPE_AMELIORATION_CHARGEURS_COMPTENU: "Comptenu Chargeur",
        TYPE_AMELIORATION_DEBLOQUE_CHARGEURS: "Débloque Chargeur",
        TYPE_AMELIORATION_CHARGEURS_VITESSE: "Vitesse Chargeur",
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_1: "Force tir soldats 1",
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_2: "Force tir soldats 2",
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_3: "Force tir soldats 3",
        TYPE_AMELIORATION_SOLDATS_FORCE_TIR_4: "Force tir soldats 4",
        TYPE_AMELIORATION_SOLDATS_VIES_1: "Vies soldats 1",
        TYPE_AMELIORATION_SOLDATS_VIES_2: "Vies soldats 2",
        TYPE_AMELIORATION_SOLDATS_VIES_3: "Vies soldats 3",
        TYPE_AMELIORATION_SOLDATS_VIES_4: "Vies soldats 4",
        TYPE_AMELIORATION_SOLDATS_VITESSE_1: "Vitesse Unité 1",
        TYPE_AMELIORATION_SOLDATS_VITESSE_2: "Vitesse Unité 2",
        TYPE_AMELIORATION_SOLDATS_SECRET_CIBLE: "Secret cible Unité",
        TYPE_AMELIORATION_DEBLOQUE_TIRAILLEURS: "Débloque Tirailleur",
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_1: "Cadence tir Tirailleur 1",
        TYPE_AMELIORATION_TIRAILLEURS_DELAY_TIR_2: "Cadence tir Tirailleur 2",
        TYPE_AMELIORATION_DEBLOQUE_TANK: "Débloque Tank",
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_1: "Portée tir Tank 1",
        TYPE_AMELIORATION_TANKS_PORTEE_TIR_2: "Portée tir Tank 2",
        TYPE_AMELIORATION_TANKS_DELAY_TIR_ET_VITESSE: "Vitesse et cadence Tank",
        TYPE_AMELIORATION_BATIMENT_COMPTENU: "Comptenu batiments",
        TYPE_AMELIORATION_ENTREPOS_ET_BASE_NB_PLACES: "Plus de places",
        TYPE_AMELIORATION_TOURELLE_VIES_1: "Vies Tourelle 1",
        TYPE_AMELIORATION_TOURELLE_VIES_2: "Vies Tourelle 2",
        TYPE_AMELIORATION_TOURELLE_TIR_1: "Tir Tourelle 1",
        TYPE_AMELIORATION_TOURELLE_TIR_2: "Tir Tourelle 2",
        TYPE_AMELIORATION_TOURELLE_TIR_3: "Tir Tourelle 3",
        TYPE_AMELIORATION_STATION_VIES: "Vies Station",
        TYPE_AMELIORATION_VITESSE_RECHARGE_1: "Vitesse recharge vies 1",
        TYPE_AMELIORATION_VITESSE_RECHARGE_2: "Vitesse recharge vies 2",
        TYPE_AMELIORATION_STATION_PRIX: "Prix Station 1",
        TYPE_AMELIORATION_TOURELLE_ET_STATION_VITESSE_CONSTRUCTION: "Vitesse construction",
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_1: 'Intelligence soldats 1',
        TYPE_AMELIORATION_SOLDATS_INTELLIGENCE_2: 'Intelligence soldats 2'
    }
}

# X. Les panneaux
# ===============
COULEUR_FOND_PANNEAUX = BLANC
# A. Le panneau infos
# -------------------
m = 10
LARGEUR_PANNEAU_INFOS = 220
HAUTEUR_PANNEAU_INFOS = 40
X_PANNEAU_INFOS = X_CARTE + LARGEUR_CARTE - m - LARGEUR_PANNEAU_INFOS
Y_PANNEAU_INFOS = Y_CARTE + m

TAILLE_TEXTE_PANNEAU_INFOS = 20
COULEUR_COMPTENU_PANNEAU_INFOS = NOIR
COULEUR_COMPTENU_MAUVAIS_PANNEAU_INFOS = (200, 0, 0)
CONTOURS_PANNEAU_INFOS = 2

ESPACEMENT_INFOS_PANNEAU_INFOS = 5
RAYON_RESSOURCE_PANNEAU_INFOS = 10
PANNEAU_INFOS_CHEMIN_IMAGE_NB_PERSONNES = 'Images/nbPesonnes.png'

# B. Le panneau constructions
# ---------------------------
PANNEAU_CONSTRUCTION_COTE_CASE_BATIMENT = 10
TAILLE_TEXTE_PANNEAU_CONSTRUCTION = 18
COULEUR_COMPTENU_PANNEAU_CONSTRUCTION = NOIR
CONTOURS_PANNEAU_CONSTRUCTION = 2

ESPACEMENT_VIGNETTES_BATIMENTS_PANNEAU_CONSTRUCTION = 10
RAYON_RESSOURCE_PANNEAU_VIGNETTES = 6

NB_VIGNETTES_PANNEAU_CONSTRUCTION_LARGEUR = 4
NB_VIGNETTES_PANNEAU_CONSTRUCTION_HAUTEUR = 2

# C. Le panneau selection
# -----------------------
TEXTE_PANNEAU_SELECTION_WALL_WAR = "WALL WAR"
COULEUR_FOND_BULLE_PANNEAU_SELECTION = (210, 210, 210)
TAILLE_TEXTE_PANNEAU_SELECTION = 15
COULEUR_COMPTENU_PANNEAU_SELECTION = NOIR
COULEUR_COMPTENU_GRISEE_PANNEAU_SELECTION = (100, 100, 100)
COULEUR_SECONDAIRE_COMPTENU_PANNEAU_SELECTION = GRIS_FONCE
PANNEAU_SELECTION_COTE_CASE_BATIMENT = 24
COULEUR_BOUTONS_ACTIONS_MENU = GRIS_CLAIR

DIMENTION_ILLUSTRATION_PANNEAU_SELECTION = 130, 130
MARGE_PANNEAU_SELECTION = 8
CONTOURS_BULLE_PANNEAU_SELECTION = 2
COULEUR_BOUTONS_PANNEAU_SELECTION = (90, 90, 90)
COULEUR_TEXTE_BOUTONS_PANNEAU_SELECTION = NOIR

DIMENTION_BARRES_PANNEAU_SELECTION = 250, 30
DIMENTION_BARRES_VIE_PANNEAU_SELECTION = 300, 25
COULEUR_BARRES_VIE_PANNEAU_SELECTION = VERT, 150
CHEMIN_IMAGE_VIES_PANNEAU_SELECTION = 'Images/coeur.png'

DIC_TEXTE_PARAM_PANNEAU_INFOS_ELEMENT_SELECT = {
    PARAM_A_VIES: lambda n: f"Nombre de vies max : {n}",
    PARAM_A_PERSONNE_NB_PLACES: lambda n: f"Nombre de place(s) : {n}",
    PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT: lambda v: f"Vitesse de déplacement : {v}",
    PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX: lambda c: f"Capacité de stockage : {c}",
    PARAM_A_PORTEUR_PEUT_RECOLTER: lambda peut_recolter: ("Peut récolter" if peut_recolter else "Ne peut pas récolter"),
    PARAM_A_PORTEUR_PEUT_DONNER_VIES: lambda n: (f"Vitesse recharge batiments : {n}" if n else
                                                 "Ne peut pas donner de vies"),
    PARAM_A_TIREUR_FORCE_TIR: lambda f: f"Force de tir : {f}",
    PARAM_A_TIREUR_DELAY_TIR: lambda d: f"Delais entre chaque tir : {d}",
    PARAM_A_TIREUR_PORTEE_TIR: lambda p: f"Portée de tir : {p}",
    PARAM_A_BATIMENT_NB_PLACES: lambda n: f"Nombre de places : {n}",
    PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES:
        lambda t: f"Débloque construction : {DIC_ELEMENTS[PARAM_F_NOM][t]}",
    PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES:
        lambda t: f"Débloque : {DIC_AMELIORATIONS[PARAM_AMELIORATION_NOM][t]}",
    PARAM_A_BATIMENT_NB_VIES_REGEN: lambda n: f"Vitesse vies régen : {n}",
    PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION: lambda d: f"Durée construction : {d}",
    PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION: lambda p: f"Prix argent : {p}",
    PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION: lambda p: f"Prix liquide : {p}",
    PARAM_A_TIREUR_INTELLIGENCE: lambda n: f"Niveau d'intelligence : {n}",
    PARAM_A_TIREUR_CIBLE_VISIBLE: lambda b: "Cible non secrète" if b else "Cible secrète"
}

# 1. Les batiments
LISTE_PARAM_PANNEAU_INFOS_BATIMENT = [PARAM_A_VIES, PARAM_A_BATIMENT_NB_PLACES,
                                      PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX]
LISTE_PARAM_PANNEAU_INFOS_BATIMENT_REGEN = [PARAM_A_VIES, PARAM_A_BATIMENT_NB_PLACES,
                                            PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX,
                                            PARAM_A_BATIMENT_NB_VIES_REGEN]
LISTE_PARAM_PANNEAU_INFOS_BATIMENT_PEUT_TIRER = [PARAM_A_VIES, PARAM_A_BATIMENT_NB_PLACES,
                                                 PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, PARAM_A_TIREUR_FORCE_TIR,
                                                 PARAM_A_TIREUR_DELAY_TIR, PARAM_A_TIREUR_PORTEE_TIR]

MARGE_ET_HAUTEUR_BARRE_CONSTRUCTION_GENERALE_PANNEAU_SELECTION = 40
COULEUR_BARRE_ETAPE_NEUTRE_PANNEAU_CONSTRUCTION = NOIR, 200
RAYON_ETIQUETTE_ETAPES_CONSTRUCTION_PANNEAU_SELECTION = 15

TEXTE_PANNEAU_SELECTION_BATIMENT_EN_CONSTRUCTION = 'Batiment en cours de construction'
TEXTE_PANNEAU_SELECTION_BATIMENT_CONSTRUIT = 'Batiment opérationnel'
TEXTE_PANNEAU_SELECTION_FENETRE_CONSTRUCTION = 'Constructions'
TEXTE_PANNEAU_SELECTION_FENETRE_AMELIORATION = 'Améliorations'
TEXTE_PANNEAU_SELECTION_FENETRE_INFORMATIONS = 'Informations'
COULEUR_PANNEAU_SELECTION_FENETRE_GRISEE = GRIS_CLAIR

TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_1 = 'Prix liquide'
TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_2 = 'Position'
TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_3 = 'Prix argent'
TEXTE_PANNEAU_SELECTION_BATIMENT_ETAPE_4 = 'Construction'

DIMENTION_BOUTON_ANNULER_CONSTRUCTION_PANNEAU_SELECTION = 270, 32
TEXTE_BOUTON_ANNULER_CONSTRUCTION_PANNEAU_SELECTION = 'Annuler la construction'

DIMENTION_CONSTRUCTION_EN_ATTENTE = (64, 59)
NB_CONSTRUCTION_EN_ATTENTE_PAR_LIGNE = 2
COTE_CARRE_ILLUSTRATION = 50

TEXTE_AUCUNE_AMELIORATION_POSSIBLE = ["Aucune amélioration n'est ",
                                      "disponible dans ce batiment !"]
TEXTE_AUCUNE_CONSTRUCTION_POSSIBLE = ["Aucune construction n'est ",
                                      "disponible dans ce batiment !"]

LARGEUR_PANNEAU_INFOS_AMELIORATION = LARGEUR_PANNEAU_ACTIONS - 140
TAILLE_FLECHES_AMELIORATIONS = 10
COEF_PROPORTION_TITRE_ARGENT_PANNEAU_AMELIORATION = 0.65
TEXTE_BOUTON_AMELIORATION = 'A'
TEXTE_BOUTON_AMELIORATION_STOP = 'S'

# 2. Les sources
TEXTE_PANNEAU_SELECTION_SOURCE_NON_EPUISEE = 'Source non épuisée'
DIC_TEXTE_PANNEAU_SELECTION_RESSOURCES_RESTANTES = {
    TYPE_SOURCE_MINERAI: ["Il reste ", " minerais à récolter", "dans cette source !"],
    TYPE_SOURCE_LIQUIDE: ["Il reste ", " liquides à puiser", "dans cette source !"]
}

# 3. Les personnes
NB_PANNEAU_SELECTION_PERSONNES_AFFICHAGE_MAX = 256
TEXTE_PANNEAU_SELECTION_GROUPE = 'Groupe'
TEXTE_PANNEAU_SELECTION_PERSONNE_ACTIVE = 'Personne active'
TEXTE_PANNEAU_SELECTION_PERSONNE_INACTIVE = 'Personne inactive'

X_PANNEAU_INFOS_ELEMENT_MOBILE = 113
LARGEUR_PANNEAU_INFOS_ELEMENT_MOBILE = 200
TEXTE_TITRE_PANNEAU_INFOS_ELEMENT_MOBILE = ' Informations :'
DIC_LISTE_PARAM_PANNEAU_INFOS_PERSONNES = {
    TYPE_PERSONNE_CLASS_PERSONNE: [PARAM_A_VIES, PARAM_A_PERSONNE_NB_PLACES,
                                   PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT],
    TYPE_PERSONNE_CLASS_PORTEUR: [PARAM_A_VIES, PARAM_A_PERSONNE_NB_PLACES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT,
                                  PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, PARAM_A_PORTEUR_PEUT_RECOLTER,
                                  PARAM_A_PORTEUR_PEUT_DONNER_VIES],
    TYPE_PERSONNE_CLASS_SOLDAT: [PARAM_A_VIES, PARAM_A_PERSONNE_NB_PLACES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT,
                                 PARAM_A_TIREUR_FORCE_TIR, PARAM_A_TIREUR_DELAY_TIR, PARAM_A_TIREUR_PORTEE_TIR,
                                 PARAM_A_TIREUR_INTELLIGENCE],
}

TEXTE_PANNEAU_SELECTION_EN_TOUT = 'En tout :'
ECART_TEXTE_PANNEAU_SELECTION_RESSOURCE_EN_TOUT = 30

TEXTE_PANNEAU_SELECTION_CIBLE = 'Cible'
TEXTE_PANNEAU_SELECTION_NB_VICTIMES_SOLDAT = 'victimes'

TYPE_BOUTON_IMAGE_STOP = 'stop'
TYPE_BOUTON_IMAGE_IMMOBILE = 'immobile'
DIC_CHEMIN_IMAGE_TYPE_BOUTON_IMAGE = {
    TYPE_BOUTON_IMAGE_STOP: 'Images/boutonStop.png',
    TYPE_BOUTON_IMAGE_IMMOBILE: 'Images/boutonImmobile.png'
}
KEY_STOP = 120
KEY_IMMOBILE = 105

# Les ennemis
LISTE_PARAM_PANNEAU_INFOS_ENNEMIS = [PARAM_A_VIES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT,
                                     PARAM_A_TIREUR_FORCE_TIR, PARAM_A_TIREUR_DELAY_TIR, PARAM_A_TIREUR_PORTEE_TIR,
                                     PARAM_A_TIREUR_INTELLIGENCE]

TEXTE_PANNEAU_SELECTION_ENNEMI_ACTIF = 'Ennemi actif'
TEXTE_PANNEAU_SELECTION_ENNEMI_INACTIF = 'Ennemi inactif'
