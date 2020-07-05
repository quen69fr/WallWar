# coding: utf-8

from element_mobile import *


class Ennemi(ElementMobile):
    def __init__(self, type_element_mobil, carte: Carte, x_sur_carte: int, y_sur_carte: int):
        ElementMobile.__init__(self, type_element_mobil, carte, x_sur_carte, y_sur_carte, False)
