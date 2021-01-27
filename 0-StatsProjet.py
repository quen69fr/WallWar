# coding: utf-8

import os

nb_fichiers = 0
nb_lignes = 0
nb_lignes_pleines = 0
nb_caracteres = 0
nb_espaces = 0
nb_classes = 0
nb_fonctions = 0

for nom_fichier in os.listdir():
    if nom_fichier.endswith('.py'):
        nb_fichiers += 1
        fichier = open(nom_fichier)
        for ligne in fichier:
            ligne = ligne[:-1]
            nb_espaces += ligne.count(' ')
            nb_lignes += 1
            mots = ligne.rsplit(' ')
            ligne_pleine = False
            for mot in mots:
                if not mot == '':
                    nb_caracteres += len(mot)
                    if not ligne_pleine:
                        ligne_pleine = True
                        nb_lignes_pleines += 1
                    if mot == 'def':
                        nb_fonctions += 1
                    elif mot == 'class':
                        nb_classes += 1

print('------------ Stats code WALL WAR ------------')
print('nb_fichiers :', nb_fichiers)
print('nb_lignes :', nb_lignes)
print('nb_lignes_pleines :', nb_lignes_pleines, f'({round(nb_lignes_pleines / nb_lignes * 100, 2)} %)')
print('nb_caracteres :', nb_caracteres, '+', nb_espaces, 'espaces')
print('nb_classes :', nb_classes)
print('nb_fonctions :', nb_fonctions)
