# coding: utf-8

from trajectoires import *
import random


def test_get_cases_traversent_segment_oblique(cote_case=6, nb_trais=15, largeur=1200, hauteur=600):
    screen = pygame.display.set_mode((largeur, hauteur))
    screen.fill(BLANC)
    for i in range(nb_trais):
        p1 = random.randint(0, int(largeur / cote_case)), random.randint(0, int(hauteur / cote_case))
        p2 = random.randint(0, int(largeur / cote_case)), random.randint(0, int(hauteur / cote_case))
        if not p1[0] == p2[0] and not p1[1] == p2[1]:
            for x, y in get_cases_traversent_segment_oblique(p1, p2):
                c = random.randint(0, 100)
                pygame.draw.rect(screen, (c, c, c), (x * cote_case, y * cote_case, cote_case, cote_case))
            pygame.gfxdraw.line(screen, p1[0] * cote_case, p1[1] * cote_case, p2[0] * cote_case, p2[1] * cote_case,
                                ROUGE)
            draw_filled_circle(screen, (p1[0] * cote_case, p1[1] * cote_case), max(int(cote_case / 2), 1), BLEU)
            draw_filled_circle(screen, (p2[0] * cote_case, p2[1] * cote_case), max(int(cote_case / 3), 1), BLEU)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            pygame.display.update()
            pygame.time.Clock().tick(FPS)


test_get_cases_traversent_segment_oblique()
