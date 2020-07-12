# coding: utf-8

from partie import *


if __name__ == "__main__":
    partie = Partie()

    while partie.running:
        partie.update()
        partie.affiche()
