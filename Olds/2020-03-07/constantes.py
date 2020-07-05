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

# VIII. Les améliorations
# =======================

# IX. Les panneaux
# ================
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
CAPTION = 'WallWar'
FULL_SCREEN = True

LARGEUR = 1360
HAUTEUR = 700

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
TYPE_BATIMENT_MURAILLE = 27

TYPE_PERSONNE_CLASS_PERSONNE = 300
TYPE_PERSONNE_CLASS_PORTEUR = 301
TYPE_PERSONNE_CLASS_SOLDAT = 302
TYPE_PERSONNE_PORTEUR = 30
TYPE_PERSONNE_COLTINEUR = 31
TYPE_PERSONNE_CHARGEUR = 32
TYPE_PERSONNE_SOLDAT = 33
TYPE_PERSONNE_TIRAILLEUR = 34
TYPE_PERSONNE_TANK = 35

TYPE_PERSONNE_CLASS_ENNEMI = 400

TYPE_EXPLOSION_PETITE = 50
TYPE_EXPLOSION_MOYENNE = 51
TYPE_EXPLOSION_GROSSE = 52


# III. La description du monde (init)
# ===================================
NB_CASE_X_GRILLE = 100
NB_CASE_Y_GRILLE = 100
COTE_CASES_GRILLE = 60
ZOOM_INIT = 0.5

NB_ARGENT_INIT = 150
NB_LIQUIDE_INIT = 50
LISTE_BATIMENTS_INIT = [((8, 8), TYPE_BATIMENT_BASE),
                        ((18, 3), TYPE_BATIMENT_ENTREPOT)]
LISTE_SOURCES_INIT = [([(0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 5),
                        (2, 2), (2, 3), (3, 3), (2, 4)], TYPE_SOURCE_MINERAI, 1873),
                      ([(50, 50), (51, 51), (50, 51), (51, 50), (52, 51),
                        (51, 52), (52, 52)], TYPE_SOURCE_MINERAI, 500),
                      ([(12, 1), (12, 2), (12, 3), (13, 2), (13, 3), (14, 2)], TYPE_SOURCE_LIQUIDE, 662)]
LISTE_PERSONNE_INIT = [(TYPE_PERSONNE_CHARGEUR, 720, 360),
                       (TYPE_PERSONNE_PORTEUR, 500, 360),
                       (TYPE_PERSONNE_COLTINEUR, 440, 240),
                       (TYPE_PERSONNE_COLTINEUR, 600, 260),
                       (TYPE_PERSONNE_TIRAILLEUR, 800, 800),
                       (TYPE_PERSONNE_SOLDAT, 720, 800),
                       (TYPE_PERSONNE_SOLDAT, 720, 720),
                       (TYPE_PERSONNE_SOLDAT, 800, 720)]


# IV. La carte et les cases
# =========================
CARTE_CHEMIN_IMAGE_FOND_PAVAGE_SABLE = 'Images/fondPavage.png'
COULEUR_TEXTE_SUR_SABLE = (127, 109, 82)
CARTE_MARGE_BORD_DEPLACEMENT = 28
CARTE_VITESSE_DEPLACEMENT = 20
CARTE_COEF_ZOOM = 0.1
CARTE_COTE_CASE_ZOOM_MAX = 200

CASE_VIDE_GRILLE_CHEMIN = -1
CASE_PLEINE_GRILLE_CHEMIN = -99

PARAM_CASE_S_COULEUR = 0

DIC_CASES_SPECIALES = {
    PARAM_CASE_S_COULEUR: {
        TYPE_CASE_S_DEPOS: (BLANC, 90),
        TYPE_CASE_S_RELAIS: (NOIR, 100),
        TYPE_CASE_S_POSSIBLE: (VERT, 180),
        TYPE_CASE_S_IMPOSSIBLE: (ROUGE, 120),
        TYPE_CASE_S_SELECTIONNEE: (BLANC, 70),
        TYPE_CASE_S_NON_CONSTRUITE: NOIR
    }
}


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
    PARAM_SOURCE_DESCRIPTION: {  # MAX : 35 chars
        TYPE_SOURCE_MINERAI: ["    Les sources de minerai permet-",
                              "tent de se procurer de l'argent. ",
                              "En ramenant le minerai dans une ",
                              "de vos bases, il est transformé en ",
                              "en argent. L'argent est indispen-",
                              "sable pour tous vos projets !"],
        TYPE_SOURCE_LIQUIDE: ["    Les sources de liquide sont ",
                              "utile pour lancer la création de ",
                              "certains batiments ainsi que pour ",
                              "fabriquer certains personnages et ",
                              "faire certaines améliorations."]
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
        TYPE_EXPLOSION_PETITE: 0.5,
        TYPE_EXPLOSION_MOYENNE: 3,
        TYPE_EXPLOSION_GROSSE: 6
    }
}


# VII. Les éléments
# ================
PARAM_A_VIES = 0
PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT = 1
PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX = 2
PARAM_A_BATIMENT_NB_PLACES = 3
PARAM_A_TIREUR_FORCE_TIR = 4
PARAM_A_TIREUR_PORTEE_TIR = 5
PARAM_A_TIREUR_DELAY_TIR = 6
PARAM_A_PORTEUR_PEUT_RECOLTER = 7

PARAM_F_NOM = 8
PARAM_F_DESCRIPTION = 9
PARAM_F_TYPE_EXPLOSION = 10
PARAM_F_BATIMENT_LISTE_CASES = 11
PARAM_F_BATIMENT_LISTE_COULEURS_CASES_PLEINES = 12
PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION = 13
PARAM_F_BATIMENT_PERSONNE_PRIX_LIQUIDE_CONSTRUCTION = 14
PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION = 15
PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES = 16
PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES = 17
PARAM_F_ELEMENT_MOBILE_CHEMIN_IMAGE = 18
PARAM_F_ELEMENT_MOBILE_RAYON = 19
PARAM_F_ELEMENT_MOBILE_SCALE_IMAGE_ZOOM = 20
PARAM_F_ELEMENT_PERSONNE_TYPE_CLASS = 21
PARAM_F_PORTEUR_DISTANCE_RESSOURCE = 22
PARAM_F_PORTEUR_RAYON_RESSOURCE = 23
PARAM_F_TIREUR_TYPE_EXPLOSION_TIR = 24
PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE = 25


DIC_ELEMENTS = {
    # Tous les éléments :
    PARAM_A_VIES: {
        TYPE_BATIMENT_BASE: 600,
        TYPE_BATIMENT_ENTREPOT: 500,
        TYPE_BATIMENT_GUILDE: 200,
        TYPE_BATIMENT_LABO: 200,
        TYPE_BATIMENT_CENTRE: 200,
        TYPE_BATIMENT_TOURELLE: 250,
        TYPE_BATIMENT_CASERNE: 200,
        TYPE_BATIMENT_MURAILLE: 500,
        TYPE_PERSONNE_PORTEUR: 50,
        TYPE_PERSONNE_COLTINEUR: 20,
        TYPE_PERSONNE_CHARGEUR: 50,
        TYPE_PERSONNE_SOLDAT: 40,
        TYPE_PERSONNE_TIRAILLEUR: 50,
        TYPE_PERSONNE_TANK: 80
    },
    PARAM_F_NOM: {
        TYPE_BATIMENT_BASE: 'Base',
        TYPE_BATIMENT_ENTREPOT: 'Entrepot',
        TYPE_BATIMENT_GUILDE: 'Guilde',
        TYPE_BATIMENT_LABO: 'Labo',
        TYPE_BATIMENT_CENTRE: 'Centre',
        TYPE_BATIMENT_TOURELLE: 'Tourelle',
        TYPE_BATIMENT_CASERNE: 'Caserne',
        TYPE_BATIMENT_MURAILLE: 'Muraille',
        TYPE_PERSONNE_PORTEUR: 'Porteur',
        TYPE_PERSONNE_COLTINEUR: 'Coltineur',
        TYPE_PERSONNE_CHARGEUR: 'Chargeur',
        TYPE_PERSONNE_SOLDAT: 'Soldat',
        TYPE_PERSONNE_TIRAILLEUR: 'Tirailleur',
        TYPE_PERSONNE_TANK: 'Tank'
    },
    PARAM_F_DESCRIPTION: {  # MAX : 35 chars
        TYPE_BATIMENT_BASE: ["    La Base est le seul batiment ",
                             "permettant de convertir le minerai ",
                             "en argent qui permet de construire ",
                             "tous les batiments. Elle sert de ",
                             "plus d'entrepos en généralisant le ",
                             "liquide et surtout l'argent !"],
        TYPE_BATIMENT_ENTREPOT: ["    L'entrepot est le seule batiment ",
                                 "autre que la base qui vous permet ",
                                 "de créer des places (10 et la base ",
                                 "n'en créé que 5) afins de construire",
                                 " de nouvelles personnes. Chaque ",
                                 "personne à besoin d'une place !"],
        TYPE_BATIMENT_GUILDE: ["    La Guilde permet de créer et ",
                               "d'améliorer des porteurs qui sont ",
                               "indispensables pour récolter les ",
                               "ressource et pour les transporter ",
                               "vers n'importe tous vos batiments. "],
        TYPE_BATIMENT_LABO: ["    Le Labo vous permet d'améliorer ",
                             "certines capacités de vos person-",
                             "nages et de vos batiments. Celles-",
                             "ci vous seront cruciales pour ",
                             "résister contre l'envahisseur."],
        TYPE_BATIMENT_CASERNE: ["    La Caserne est le batiment qui ",
                                "dédier à la construction et l'en-",
                                "trainement de vos soldats. Sans ",
                                "celui-ci, vos défences sont très ",
                                "limitées et affaiblies."],
        TYPE_BATIMENT_CENTRE: ["    Le Centre est un batiment incon-",
                               "tournable. Il vous permet en effet ",
                               "de renforcer vos défences et d'amé-",
                               "liorer considérablement vos armes ",
                               "d'attaque. Seules ces amélorations ",
                               "vous permetteront de survivre !"],
        TYPE_BATIMENT_TOURELLE: ["    La Tourelle ... "],  # TODO
        TYPE_BATIMENT_MURAILLE: ["    La Muraille ... "],  # TODO
        TYPE_PERSONNE_PORTEUR: ["    Le Porteur est le transporteur le ",
                                "plus résistant, il vous permet de ",
                                "récolter ou d'apporter du minerai, ",
                                "du liquide ou de l'argent dans des ",
                                "zones ou vous riquez de vous faire ",
                                "attaquer..."],
        TYPE_PERSONNE_COLTINEUR: ["    Le Coltineur est le porteur le ",
                                  "plus rapide. Il est efficace pour ",
                                  "récolter du minerai ou du liquide. ",
                                  "Il peut également transporter de ",
                                  "l'argent vers un de vos batiments. "],
        TYPE_PERSONNE_CHARGEUR: ["    Le Chargeur vous permet de ",
                                 "transfèrer de l'argent de manière ",
                                 "efficace d'une de vos bass vers un ",
                                 "autre batiment. Cependant, il ne ",
                                 "peut pas récolter du minerai ou du ",
                                 "liquide."],
        TYPE_PERSONNE_SOLDAT: ["    Le Soldat ..."],  # TODO
        TYPE_PERSONNE_TIRAILLEUR: ["    Le Tirailleur ..."],  # TODO
        TYPE_PERSONNE_TANK: ["    La tank ..."]  # TODO
    },
    PARAM_F_TYPE_EXPLOSION: {
        TYPE_BATIMENT_BASE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_ENTREPOT: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_GUILDE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_LABO: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_CENTRE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_TOURELLE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_CASERNE: TYPE_EXPLOSION_GROSSE,
        TYPE_BATIMENT_MURAILLE: TYPE_EXPLOSION_GROSSE,
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
            TYPE_CASE_S_RELAIS: [(0, -2), (0, 2), (-2, 0), (2, 0)]
        },
        TYPE_BATIMENT_ENTREPOT: {
            TYPE_CASE_PLEINE: [(-1, 2), (-2, -1), (2, 1), (1, -2), (-1, 1), (-1, -1), (1, 1),
                               (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)],
            TYPE_CASE_S_DEPOS: [(0, 2), (0, -2), (-2, 0), (2, 0)],
            TYPE_CASE_S_RELAIS: []
        },
        TYPE_BATIMENT_GUILDE: {
            TYPE_CASE_PLEINE: [(-2, 2), (2, -2), (-2, 1), (-1, 2), (2, -1), (1, -2), (1, 2),
                               (2, 1), (1, 1), (-2, -2), (-1, -1), (-2, -1), (-1, -2)],
            TYPE_CASE_S_DEPOS: [(0, 0)],
            TYPE_CASE_S_RELAIS: []
        },
        TYPE_BATIMENT_LABO: {
            TYPE_CASE_PLEINE: [(0, 0), (0, 1), (1, 0), (1, 1)],
            TYPE_CASE_S_DEPOS: [(0, -1), (-1, 1), (2, 0)],
            TYPE_CASE_S_RELAIS: []
        },
        TYPE_BATIMENT_CASERNE: {
            TYPE_CASE_PLEINE: [(2, 2), (2, 1), (1, 2), (1, 1), (2, 0), (0, 2), (0, 1), (1, 0), (-1, 2),
                               (2, -1), (0, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-2, 1), (1, -2),
                               (-1, -1), (-2, 0), (0, -2), (-2, -1), (-1, -2), (-2, -2)],
            TYPE_CASE_S_DEPOS: [(-2, 2), (2, -2)],
            TYPE_CASE_S_RELAIS: []
        },
        TYPE_BATIMENT_CENTRE: {
            TYPE_CASE_PLEINE: [(1, 2), (-1, 2), (1, 1), (-1, 1), (1, 0), (-1, 0), (-1, -1), (0, -1), (1, -1),
                               (-1, -2), (0, -2), (1, -2), (-2, 0), (2, 0), (-2, -1), (2, -1), (-2, -2), (2, -2)],
            TYPE_CASE_S_DEPOS: [(0, 0)],
            TYPE_CASE_S_RELAIS: []
        },
        TYPE_BATIMENT_TOURELLE: {
            TYPE_CASE_PLEINE: [],
            TYPE_CASE_S_DEPOS: [(0, 0), (0, 1), (1, 0), (1, 1)],
            TYPE_CASE_S_RELAIS: []
        },
        TYPE_BATIMENT_MURAILLE: {
            TYPE_CASE_PLEINE: [],
            TYPE_CASE_S_DEPOS: [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)],
            TYPE_CASE_S_RELAIS: []
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
        TYPE_BATIMENT_TOURELLE: [],
        TYPE_BATIMENT_MURAILLE: []
    },
    PARAM_A_BATIMENT_NB_PLACES: {
        TYPE_BATIMENT_BASE: 5,
        TYPE_BATIMENT_ENTREPOT: 10,
        TYPE_BATIMENT_GUILDE: 0,
        TYPE_BATIMENT_LABO: 0,
        TYPE_BATIMENT_CENTRE: 0,
        TYPE_BATIMENT_TOURELLE: 0,
        TYPE_BATIMENT_CASERNE: 0,
        TYPE_BATIMENT_MURAILLE: 0
    },
    PARAM_F_BATIMENT_LISTES_CONSTRUCTIONS_POSSIBLES: {
        TYPE_BATIMENT_BASE: [],
        TYPE_BATIMENT_ENTREPOT: [],
        TYPE_BATIMENT_GUILDE: [TYPE_PERSONNE_CHARGEUR,
                               TYPE_PERSONNE_COLTINEUR,
                               TYPE_PERSONNE_PORTEUR],
        TYPE_BATIMENT_LABO: [],
        TYPE_BATIMENT_CENTRE: [],
        TYPE_BATIMENT_TOURELLE: [],
        TYPE_BATIMENT_CASERNE: [TYPE_PERSONNE_SOLDAT, TYPE_PERSONNE_TIRAILLEUR, TYPE_PERSONNE_TANK],
        TYPE_BATIMENT_MURAILLE: []
    },
    PARAM_F_BATIMENT_LISTES_AMELIORATIONS_POSSIBLES: {
        TYPE_BATIMENT_BASE: [],
        TYPE_BATIMENT_ENTREPOT: [],
        TYPE_BATIMENT_GUILDE: [],
        TYPE_BATIMENT_LABO: [],
        TYPE_BATIMENT_CENTRE: [],
        TYPE_BATIMENT_TOURELLE: [],
        TYPE_BATIMENT_CASERNE: [],
        TYPE_BATIMENT_MURAILLE: []
    },
    # Toutes les constructions (batiments + personnes) :
    PARAM_F_BATIMENT_PERSONNE_PRIX_ARGENT_CONSTRUCTION: {
        TYPE_BATIMENT_BASE: 150,
        TYPE_BATIMENT_ENTREPOT: 70,
        TYPE_BATIMENT_GUILDE: 80,
        TYPE_BATIMENT_LABO: 90,
        TYPE_BATIMENT_CASERNE: 150,
        TYPE_BATIMENT_CENTRE: 100,
        TYPE_BATIMENT_TOURELLE: 10,
        TYPE_BATIMENT_MURAILLE: 25,
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
        TYPE_BATIMENT_TOURELLE: 10,
        TYPE_BATIMENT_MURAILLE: 25,
        TYPE_PERSONNE_PORTEUR: 10,
        TYPE_PERSONNE_COLTINEUR: 0,
        TYPE_PERSONNE_CHARGEUR: 40,
        TYPE_PERSONNE_SOLDAT: 10,
        TYPE_PERSONNE_TIRAILLEUR: 20,
        TYPE_PERSONNE_TANK: 50
    },
    PARAM_F_BATIMENT_PERSONNE_DUREE_CONSTRUCTION: {
        TYPE_BATIMENT_BASE: 800,
        TYPE_BATIMENT_ENTREPOT: 400,
        TYPE_BATIMENT_GUILDE: 350,
        TYPE_BATIMENT_LABO: 300,
        TYPE_BATIMENT_CASERNE: 500,
        TYPE_BATIMENT_CENTRE: 300,
        TYPE_BATIMENT_TOURELLE: 120,
        TYPE_BATIMENT_MURAILLE: 220,
        TYPE_PERSONNE_PORTEUR: 300,
        TYPE_PERSONNE_COLTINEUR: 200,
        TYPE_PERSONNE_CHARGEUR: 800,
        TYPE_PERSONNE_SOLDAT: 300,
        TYPE_PERSONNE_TIRAILLEUR: 400,
        TYPE_PERSONNE_TANK: 850
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
        TYPE_PERSONNE_PORTEUR: 32,
        TYPE_PERSONNE_COLTINEUR: 32,
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
        TYPE_PERSONNE_PORTEUR: 4,
        TYPE_PERSONNE_COLTINEUR: 5,
        TYPE_PERSONNE_CHARGEUR: 1.6,
        TYPE_PERSONNE_SOLDAT: 4.8,
        TYPE_PERSONNE_TIRAILLEUR: 4,
        TYPE_PERSONNE_TANK: 1.8
    },
    PARAM_F_ELEMENT_PERSONNE_TYPE_CLASS: {
        TYPE_PERSONNE_PORTEUR: TYPE_PERSONNE_CLASS_PORTEUR,
        TYPE_PERSONNE_COLTINEUR: TYPE_PERSONNE_CLASS_PORTEUR,
        TYPE_PERSONNE_CHARGEUR: TYPE_PERSONNE_CLASS_PORTEUR,
        TYPE_PERSONNE_SOLDAT: TYPE_PERSONNE_CLASS_SOLDAT,
        TYPE_PERSONNE_TIRAILLEUR: TYPE_PERSONNE_CLASS_SOLDAT,
        TYPE_PERSONNE_TANK: TYPE_PERSONNE_CLASS_SOLDAT
    },
    # Tous les compteneurs (batiments sauf la base + porteurs)
    PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX: {
        TYPE_BATIMENT_BASE: 1000,
        TYPE_BATIMENT_ENTREPOT: 0,
        TYPE_BATIMENT_GUILDE: 200,
        TYPE_BATIMENT_LABO: 200,
        TYPE_BATIMENT_CENTRE: 200,
        TYPE_BATIMENT_TOURELLE: 100,
        TYPE_BATIMENT_CASERNE: 800,
        TYPE_BATIMENT_MURAILLE: 100,
        TYPE_PERSONNE_PORTEUR: 2,
        TYPE_PERSONNE_COLTINEUR: 2,
        TYPE_PERSONNE_CHARGEUR: 16
    },
    # Tous les porteurs
    PARAM_A_PORTEUR_PEUT_RECOLTER: {
        TYPE_PERSONNE_PORTEUR: True,
        TYPE_PERSONNE_COLTINEUR: True,
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
    # Tous les tireurs (soldats) :
    PARAM_A_TIREUR_FORCE_TIR: {
        TYPE_PERSONNE_SOLDAT: 4,
        TYPE_PERSONNE_TIRAILLEUR: 2,
        TYPE_PERSONNE_TANK: 70
    },
    PARAM_A_TIREUR_PORTEE_TIR: {
        TYPE_PERSONNE_SOLDAT: 160,
        TYPE_PERSONNE_TIRAILLEUR: 200,
        TYPE_PERSONNE_TANK: 350
    },
    PARAM_A_TIREUR_DELAY_TIR: {
        TYPE_PERSONNE_SOLDAT: 20,
        TYPE_PERSONNE_TIRAILLEUR: 5,
        TYPE_PERSONNE_TANK: 120
    },
    PARAM_F_TIREUR_TYPE_EXPLOSION_TIR: {
        TYPE_PERSONNE_SOLDAT: TYPE_EXPLOSION_PETITE,
        TYPE_PERSONNE_TIRAILLEUR: TYPE_EXPLOSION_PETITE,
        TYPE_PERSONNE_TANK: TYPE_EXPLOSION_PETITE
    },
    PARAM_F_TIREUR_EXPLOSION_TIR_DISTANCE: {
        TYPE_PERSONNE_SOLDAT: 26,
        TYPE_PERSONNE_TIRAILLEUR: 34,
        TYPE_PERSONNE_TANK: 23
    }
}

LISTE_TYPES_BATIMENTS = [TYPE_BATIMENT_BASE, TYPE_BATIMENT_ENTREPOT, TYPE_BATIMENT_GUILDE, TYPE_BATIMENT_LABO,
                         TYPE_BATIMENT_CASERNE, TYPE_BATIMENT_CENTRE, TYPE_BATIMENT_TOURELLE, TYPE_BATIMENT_MURAILLE]

NB_CONSTRUCTION_EN_ATTENTE_MAX = 4
NB_CONSTRUCTION_POSSIBLE_MAX = 3

COULEUR_ELEMENT_SELECTION = ROUGE
ANNEAU_SELECTION_DISTANCE = 10
MARGE_OBJECTIF_ATTEIND = 1

TYPE_TRANSACTION_GIVE = 'give'
TYPE_TRANSACTION_GET = 'get'

COULEUR_PORTER_TIT_TIREUR_SELECTION = VERT, 50


# VIII. Les améliorations
# =======================
# TODO


# IX. Les panneaux
# ================
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
TEXTE_PANNEAU_SELECTION_WALL_WAR = ["WALL", "WAR"]
COULEUR_FOND_BULLE_PANNEAU_SELECTION = (210, 210, 210)
TAILLE_TEXTE_PANNEAU_SELECTION = 15
COULEUR_COMPTENU_PANNEAU_SELECTION = NOIR
COULEUR_SECONDAIRE_COMPTENU_PANNEAU_SELECTION = GRIS_FONCE
PANNEAU_SELECTION_COTE_CASE_BATIMENT = 24

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
    PARAM_A_VIES: "Nombre de vies : ",
    PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT: "Vitesse de déplacement : ",
    PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX: 'Capacité de stockage : ',
    PARAM_A_PORTEUR_PEUT_RECOLTER: {True: "Peut récolter",
                                    False: "Ne peut pas récolter"},
    PARAM_A_TIREUR_FORCE_TIR: "Force de tir : ",
    PARAM_A_TIREUR_DELAY_TIR: "Delais entre chaque tir : ",
    PARAM_A_TIREUR_PORTEE_TIR: "Portée de tir : ",
    PARAM_A_BATIMENT_NB_PLACES: "Nombre de places : ",
}

# 1. Les batiments
LISTE_PARAM_PANNEAU_INFOS_BATIMENT = [PARAM_A_VIES, PARAM_A_BATIMENT_NB_PLACES,
                                      PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX]

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
DIC_LISTE_PARAM_PANNEAU_INFOS_ELEMENT_MOBILE = {
    TYPE_PERSONNE_CLASS_PERSONNE: [PARAM_A_VIES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT],
    TYPE_PERSONNE_CLASS_PORTEUR: [PARAM_A_VIES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT,
                                  PARAM_A_BATIMENT_PORTEUR_ARGENT_COMPTENU_MAX, PARAM_A_PORTEUR_PEUT_RECOLTER],
    TYPE_PERSONNE_CLASS_SOLDAT: [PARAM_A_VIES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT,
                                 PARAM_A_TIREUR_FORCE_TIR, PARAM_A_TIREUR_DELAY_TIR, PARAM_A_TIREUR_PORTEE_TIR],
    TYPE_PERSONNE_CLASS_ENNEMI: [PARAM_A_VIES, PARAM_A_ELEMENT_MOBILE_VITESSE_DEPLACEMENT],
}

TEXTE_PANNEAU_SELECTION_EN_TOUT = 'En tout :'
ECART_TEXTE_PANNEAU_SELECTION_RESSOURCE_EN_TOUT = 30

TEXTE_PANNEAU_SELECTION_CIBLE_SOLDAT = 'Cible'
TEXTE_PANNEAU_SELECTION_NB_VICTIMES_SOLDAT = 'victimes'

TYPE_BOUTON_IMAGE_STOP = 'stop'
TYPE_BOUTON_IMAGE_IMMOBILE = 'immobile'
DIC_CHEMIN_IMAGE_TYPE_BOUTON_IMAGE = {
    TYPE_BOUTON_IMAGE_STOP: 'Images/boutonStop.png',
    TYPE_BOUTON_IMAGE_IMMOBILE: 'Images/boutonImmobile.png'
}
