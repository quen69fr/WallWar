# coding: utf-8

from drawing_box import *


class Sommet:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.liste_aretes = []

    def add_arrete(self, arete):
        if arete not in self.liste_aretes:
            self.liste_aretes.append(arete)
            return True
        return False

    def remove_arrete(self, arete):
        if arete in self.liste_aretes:
            self.liste_aretes.remove(arete)
            return True
        return False


class Arete:
    def __init__(self, sommet1: Sommet, sommet2: Sommet, liste_cases_traversees: list):
        self.sommet1 = sommet1
        self.sommet2 = sommet2
        self.longueur = 0
        self.calcule_longueur()
        for sommet in [self.sommet1, self.sommet2]:
            sommet.add_arrete(self)
        self.liste_cases_traversees = liste_cases_traversees

    def calcule_longueur(self):
        self.longueur = math.sqrt((self.sommet2.i - self.sommet1.i) ** 2 + (self.sommet2.j - self.sommet1.j) ** 2)


def get_cases_traversent_segment_oblique(point1: (int, int), point2: (int, int), marge_approximation=0.0000000001):
    x1, y1 = point1
    x2, y2 = point2
    step_y = (y2 - y1) / (x2 - x1)
    liste_cases = []

    if x2 > x1:
        x_min = x1
        x_max = x2
        y_stop = y1
    else:
        x_min = x2
        x_max = x1
        y_stop = y2

    if step_y > 0:
        for x in range(x_min, x_max):
            y_start = y_stop
            y_stop += step_y
            for y in range(int(y_start + marge_approximation), math.ceil(y_stop - marge_approximation)):
                liste_cases.append((x, y))
    else:
        for x in range(x_min, x_max):
            y_start = y_stop
            y_stop += step_y
            for y in range(int(y_stop + marge_approximation), math.ceil(y_start - marge_approximation)):
                liste_cases.append((x, y))
    return liste_cases


class Graph:
    def __init__(self, nb_cases_i, nb_cases_j):
        self.nb_cases_i = nb_cases_i
        self.nb_cases_j = nb_cases_j
        self.grille = [[CASE_VIDE_GRILLE_CHEMIN for _ in range(self.nb_cases_j)] for _ in range(self.nb_cases_i)]
        self.liste_sommets = []
        self.liste_aretes = []
        self.liste_sommets_temp = []

        self.new_cases_pleines = []
        self.new_cases_vides = []

    def ij_case_existe(self, i: int, j: int):
        if 0 <= i < self.nb_cases_i and 0 <= j < self.nb_cases_j:
            return True
        return False

    def get_cases_grille(self, i, j):
        if self.ij_case_existe(i, j):
            return self.grille[i][j]
        return TYPE_CASE_INEXISTANTE

    def get_all_cases_pleines(self):
        liste_case_pleines = []
        for i, colone in enumerate(self.grille):
            for j, case in enumerate(colone):
                if case == CASE_PLEINE_GRILLE_CHEMIN:
                    liste_case_pleines.append((i, j))
        return liste_case_pleines

    def add_case_pelines(self, liste_coordonnees_cases):
        for i, j in liste_coordonnees_cases:
            if not self.grille[i][j] == CASE_PLEINE_GRILLE_CHEMIN:
                self.grille[i][j] = CASE_PLEINE_GRILLE_CHEMIN
                if (i, j) in self.new_cases_vides:
                    self.new_cases_vides.remove((i, j))
                else:
                    self.new_cases_pleines.append((i, j))

    def add_case_vide(self, liste_coordonnees_cases):
        for i, j in liste_coordonnees_cases:
            if not self.grille[i][j] == CASE_VIDE_GRILLE_CHEMIN:
                self.grille[i][j] = CASE_VIDE_GRILLE_CHEMIN
                if (i, j) in self.new_cases_pleines:
                    self.new_cases_pleines.remove((i, j))
                else:
                    self.new_cases_vides.append((i, j))

    def update(self):
        if len(self.new_cases_pleines) > 0 or len(self.new_cases_vides) > 0:
            self.liste_sommets = []
            self.liste_aretes = []
            self.clear_liste_sommets_temp()
            self.make_all_sommets()
            self.new_cases_pleines = []
            self.new_cases_vides = []
            return True
        return False

    def make_all_sommets(self):
        for i, j in self.get_all_cases_pleines():
            liste_coordonnees_sommets = [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]
            for i_s, j_s in liste_coordonnees_sommets[:]:
                if (not self.ij_case_existe(i_s, j_s)) or self.get_cases_grille(i_s, j_s) == CASE_PLEINE_GRILLE_CHEMIN \
                        or (i_s, j_s) in self.liste_sommets:
                    liste_coordonnees_sommets.remove((i_s, j_s))
            if len(liste_coordonnees_sommets) == 0:
                continue
            for i_a, j_a in [(i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)]:
                if self.get_cases_grille(i_a, j_a) == CASE_PLEINE_GRILLE_CHEMIN:
                    if self.ij_case_existe(i_a, j_a):
                        for i_s, j_s in liste_coordonnees_sommets[:]:
                            if i_a == i_s or j_a == j_s:
                                liste_coordonnees_sommets.remove((i_s, j_s))
                                if len(liste_coordonnees_sommets) == 0:
                                    break
                        if len(liste_coordonnees_sommets) == 0:
                            break
            if len(liste_coordonnees_sommets) == 0:
                continue
            self.add_sommets(liste_coordonnees_sommets)

    def liste_cases_aretes_si_possible_sommets(self, sommet1, sommet2):
        return self.liste_cases_aretes_si_possible(sommet1.i, sommet1.j, sommet2.i, sommet2.j)

    def liste_cases_aretes_si_possible(self, i1, j1, i2, j2):
        liste_cases_traversees = []
        if i1 == i2:
            for j in range(min(j1, j2), max(j1, j2) + 1):
                if self.get_cases_grille(i1, j) == CASE_PLEINE_GRILLE_CHEMIN:
                    return None
                liste_cases_traversees.append((i1, j))
        elif j1 == j2:
            for i in range(min(i1, i2), max(i1, i2) + 1):
                if self.get_cases_grille(i, j1) == CASE_PLEINE_GRILLE_CHEMIN:
                    return None
                liste_cases_traversees.append((i, j1))
        else:
            for i, j in get_cases_traversent_segment_oblique((i1, j1), (i2, j2)):
                for i2 in [i, i + 1]:
                    for j2 in [j, j + 1]:
                        if (i2, j2) not in liste_cases_traversees and self.ij_case_existe(i, j):
                            if self.get_cases_grille(i2, j2) == CASE_PLEINE_GRILLE_CHEMIN:
                                return None
                            liste_cases_traversees.append((i2, j2))
        return liste_cases_traversees

    def add_aretes_sommet(self, sommet: Sommet):
        added = False
        for sommet2 in self.liste_sommets:
            if not sommet == sommet2:
                liste_cases_traversees = self.liste_cases_aretes_si_possible_sommets(sommet, sommet2)
                if liste_cases_traversees is not None:
                    self.add_arete(sommet, sommet2, liste_cases_traversees)
                    added = True
        return added

    def add_sommets(self, liste_coordonnees_sommets: list):
        for i, j in liste_coordonnees_sommets:
            sommet = Sommet(i, j)
            self.liste_sommets.append(sommet)
            self.add_aretes_sommet(sommet)

    def add_arete(self, sommet1: Sommet, sommet2: Sommet, liste_cases: list):
        self.liste_aretes.append(Arete(sommet1, sommet2, liste_cases))

    def delete_arete(self, arete: Arete):
        if arete in self.liste_aretes:
            self.liste_aretes.remove(arete)
            for sommet in [arete.sommet1, arete.sommet2]:
                sommet.remove_arrete(arete)

    def delete_aretes_deleted_sommet(self, sommet):
        liste_arete_to_delete = []
        for arete in self.liste_aretes:
            if sommet in [arete.sommet1, arete.sommet2]:
                liste_arete_to_delete.append(arete)
        for arete_to_delete in liste_arete_to_delete:
            self.delete_arete(arete_to_delete)

    def delete_sommet(self, sommet):
        if sommet in self.liste_sommets:
            self.delete_aretes_deleted_sommet(sommet)
            self.liste_sommets.remove(sommet)

    def delete_sommet_temp(self, sommet_temp):
        if sommet_temp in self.liste_sommets_temp:
            self.delete_aretes_deleted_sommet(sommet_temp)
            self.liste_sommets_temp.remove(sommet_temp)

    def clear_liste_sommets_temp(self):
        for sommet_temp in self.liste_sommets_temp[:]:
            self.delete_sommet_temp(sommet_temp)

    def cherche_sommet_in_liste_sommets_temp(self, i, j):
        for sommet in self.liste_sommets_temp:
            if sommet.i == i and sommet.j == j:
                return sommet
        return None

    def test_doublons_sommets_et_aretes(self):
        reele_liste_aretes = []
        liste_aretes_selon_les_sommets = []
        reele_liste_sommets = []
        liste_sommets_selon_les_aretes = []
        for arete in self.liste_aretes:
            if arete in reele_liste_aretes:
                print('Erreur : Une même arete est stockée 2 fois !')
            else:
                reele_liste_aretes.append(arete)
            for sommet in [arete.sommet1, arete.sommet2]:
                if sommet not in liste_sommets_selon_les_aretes:
                    liste_sommets_selon_les_aretes.append(sommet)
        for sommet in self.liste_sommets + self.liste_sommets_temp:
            if sommet in reele_liste_sommets:
                print('Erreur : Un même sommet est stocké 2 fois !')
            else:
                reele_liste_sommets.append(sommet)
            for arete in sommet.liste_aretes:
                if arete not in liste_aretes_selon_les_sommets:
                    liste_aretes_selon_les_sommets.append(arete)

        sorted(reele_liste_aretes, key=lambda a: a.__str__()[30:40])
        sorted(liste_aretes_selon_les_sommets, key=lambda a: a.__str__()[30:40])
        sorted(reele_liste_sommets, key=lambda s: s.__str__()[31:41])
        sorted(liste_sommets_selon_les_aretes, key=lambda s: s.__str__()[31:41])

        print('Le tri ne marche pas !')
        if not reele_liste_aretes == liste_aretes_selon_les_sommets:
            print('Erreur : Les aretes stockées dans les sommets ne correspondent pas avec la liste des aretes :')
            print(f'  -> Liste réele :             {reele_liste_aretes}')
            print(f'  -> Liste selon les sommets : {liste_aretes_selon_les_sommets}')
        if not reele_liste_sommets == liste_sommets_selon_les_aretes:
            print('Erreur : Les sommets stockés dans les aretes ne correspondent pas avec la liste des sommets :')
            print(f'  -> Liste réele :            {reele_liste_sommets}')
            print(f'  -> Liste selon les aretes : {liste_sommets_selon_les_aretes}')

    def trouve_trajectoire_ij(self, i_depart, j_depart, liste_ij_arrivee):
        chemin_le_plus_court = []
        distance_chemin_le_plus_court = math.inf

        for i_arrivee, j_arrivee in liste_ij_arrivee:
            liste_cases_aretes = self.liste_cases_aretes_si_possible(i_depart, j_depart, i_arrivee, j_arrivee)
            if liste_cases_aretes is not None:
                if len(liste_ij_arrivee) == 1:
                    return [(i_depart, j_depart), (i_arrivee, j_arrivee)]
                else:
                    new_distance = math.sqrt((i_arrivee - i_depart) ** 2 + (j_arrivee - j_depart) ** 2)
                    if distance_chemin_le_plus_court > new_distance:
                        chemin_le_plus_court = [(i_depart, j_depart), (i_arrivee, j_arrivee)]
                        distance_chemin_le_plus_court = new_distance

        return_chemin = False

        sommet_depart = self.cherche_sommet_in_liste_sommets_temp(i_depart, j_depart)
        if sommet_depart is None:
            sommet_depart = Sommet(i_depart, j_depart)
            self.liste_sommets_temp.append(sommet_depart)
            if not self.add_aretes_sommet(sommet_depart) and len(chemin_le_plus_court) == 0:
                return_chemin = True
        else:
            if len(sommet_depart.liste_aretes) == 0 and len(chemin_le_plus_court) == 0:
                return_chemin = True

        liste_sommet_arrivee = []
        if not return_chemin:
            if len(chemin_le_plus_court) == 0:
                return_chemin = True
            for i_arrivee, j_arrivee in liste_ij_arrivee:
                sommet_arrivee = self.cherche_sommet_in_liste_sommets_temp(i_arrivee, j_arrivee)
                if sommet_arrivee is None:
                    sommet_arrivee = Sommet(i_arrivee, j_arrivee)
                    self.liste_sommets_temp.append(sommet_arrivee)
                    if self.add_aretes_sommet(sommet_arrivee):
                        return_chemin = False
                else:
                    if len(sommet_arrivee.liste_aretes) > 0:
                        return_chemin = False
                liste_sommet_arrivee.append(sommet_arrivee)

        if not return_chemin:
            liste_sommets_non_traites = [sommet for sommet in self.liste_sommets + liste_sommet_arrivee]
            dic_distance_sommet = {sommet: math.inf for sommet in self.liste_sommets + liste_sommet_arrivee}
            dic_chemin_sommet = {sommet: [] for sommet in self.liste_sommets + liste_sommet_arrivee}
            liste_sommets_non_traites.append(sommet_depart)
            dic_distance_sommet[sommet_depart] = 0
            dic_chemin_sommet[sommet_depart] = [(sommet_depart.i, sommet_depart.j)]
            while len(liste_sommets_non_traites) > 0:
                sommet = min(liste_sommets_non_traites, key=lambda sommet: dic_distance_sommet[sommet])
                if dic_distance_sommet[sommet] == math.inf or \
                        dic_distance_sommet[sommet] > distance_chemin_le_plus_court:
                    break
                liste_sommets_non_traites.remove(sommet)
                for arete in sommet.liste_aretes:
                    sommet2 = arete.sommet1 if arete.sommet2 == sommet else arete.sommet2
                    if sommet2 in liste_sommets_non_traites:
                        if dic_distance_sommet[sommet] < dic_distance_sommet[sommet2]:
                            new_distance = dic_distance_sommet[sommet] + arete.longueur
                            if new_distance < dic_distance_sommet[sommet2]:
                                dic_distance_sommet[sommet2] = new_distance
                                dic_chemin_sommet[sommet2] = dic_chemin_sommet[sommet] + [(sommet2.i, sommet2.j)]

            for sommet_arrivee in liste_sommet_arrivee:
                if not dic_distance_sommet[sommet_arrivee] == math.inf and \
                        dic_distance_sommet[sommet_arrivee] < distance_chemin_le_plus_court:
                    chemin_le_plus_court = dic_chemin_sommet[sommet_arrivee]
                    distance_chemin_le_plus_court = dic_distance_sommet[sommet_arrivee]

        return chemin_le_plus_court
