import time

import pygame
import random
import ui
import basescreen
import player
import computer
import time

headerfont = pygame.font.SysFont("Impact", 120)

def menu() -> list:
    """
    main menu
    :return:
    """
    random.seed(time.time())
    running = True
    ui.clear()
    exitbutton = ui.Button("Exit game", "button.png", "button_hover.png", "button_select.png", pygame.Rect(200, 100, 128, 64), align=ui.BOTTOMRIGHT)
    pvp = ui.Button("2 Player", "button.png", "button_hover.png", "button_select.png", pygame.Rect(200, 200, 128, 64), align=ui.BOTTOMRIGHT)
    pve = ui.Button("vs Computer", "button.png", "button_hover.png", "button_select.png", pygame.Rect(200, 300, 128, 64), align=ui.BOTTOMRIGHT)
    p1input = ui.Button("Input Player 1 name", "inputbar.png", "inputbar_hover.png", "inputbar_select.png",
                    pygame.Rect(600, 300, 299, 32), align=ui.BOTTOMRIGHT, click_len=4)
    p2input = ui.Button("Input Player 2 name", "inputbar.png", "inputbar_hover.png", "inputbar_select.png",
                        pygame.Rect(600, 200, 299, 32), align=ui.BOTTOMRIGHT, click_len=4)
    p1inputting: bool = False
    p2inputting: bool = False
    preview = ui.UI(align=ui.BOTTOMLEFT)
    preview.surface = pygame.image.load("preview.png").convert()
    preview.position = pygame.Vector2(-100, 500)
    preview.show()

    while running:
        m = pygame.mouse.get_pos()
        ui.vupdate(m[0], m[1], basescreen.root.get_rect().size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # close the window
                exit(0)
            elif event.type == ui.BUTTONPRESS:
                if event.id == pve.get_id():
                    running = False
                    p1inputting = False
                    return [computer.Computer(),
                        player.Player(p1input.text[:-1], (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))),
                            ]
                elif event.id == pvp.get_id():
                    running = False
                    p1inputting = False
                    return [player.Player(p1input.text[:-1], (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))),
                            player.Player(p2input.text[:-1], (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)))]
                elif event.id == p1input.get_id():
                    if p1input.text == "Input Player 1 name": p1input.text = "|"
                    p1inputting = True
                    p2inputting = False
                elif event.id == exitbutton.get_id():
                    pygame.quit()
                    exit(0)

                elif event.id == p2input.get_id():
                    if p2input.text == "Input Player 2 name": p2input.text = "|"
                    p2inputting = True
                    p1inputting = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if p1inputting:
                        if len(p1input.text) > 0: p1input.text = p1input.text[:-2] + "|"
                    elif p2inputting:
                        if len(p2input.text) > 0: p2input.text = p2input.text[:-2] + "|"
                elif p1inputting:
                    p1input.text = p1input.text[:-1] + event.unicode + "|"
                elif p2inputting:
                    p2input.text = p2input.text[:-1] + event.unicode + "|"


            elif event.type == pygame.MOUSEBUTTONDOWN:
                ab = True
                for u in ui.all:
                    u.clickupdate()

        basescreen.root.fill(pygame.Color(0, 50, 50))
        basescreen.root.blit(headerfont.render("Project CHEESESQUARES", False, pygame.Color(255,255,255)), (300, 80))

        for u in ui.all:
            basescreen.root.blit(u.draw(), u.rel_pos)

        pygame.display.flip()
        basescreen.clock.tick(60)
    return []


def winscreen(winner):
    basescreen.listen()
    ui.clear()
    wstr = winner.name + " wins!"
    size = basescreen.root.get_rect().size
    backbutton = ui.Button("Main Menu", "button.png", "button_hover.png", "button_select.png",\
                           pygame.Rect(size[0] // 2 - 64, size[1] // 2 + 120, 128, 64))
    while True:
        m = pygame.mouse.get_pos()
        size = basescreen.root.get_rect().size
        ui.vupdate(m[0], m[1], size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # close the window
                exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui.all[0].clickupdate()

            elif event.type == ui.BUTTONPRESS:
                return

        pygame.draw.rect(basescreen.root, winner.color, pygame.Rect(0, int(size[1] / 2) - 100, size[0], 200))
        basescreen.root.blit(headerfont.render(wstr, False,(255, 255, 255)), (int(size[0] / 2 - headerfont.size(wstr)[0] / 2),\
                                                                              int(size[1] / 2 - headerfont.size(wstr)[1] / 2)))
        for u in ui.all:
            basescreen.root.blit(u.draw(), u.rel_pos)
        pygame.display.flip()
        basescreen.clock.tick(60)