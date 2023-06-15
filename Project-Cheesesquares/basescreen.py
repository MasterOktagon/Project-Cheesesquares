import pygame
import os
import camera
import ui
from uiclasses import *

root: None|pygame.Surface = None
clock: pygame.time.Clock = pygame.time.Clock()
t: None|Tutorial = None
tclose: None|ui.Button = None
topen: None|ui.Button = None
debuglog: list[str] = []
debugpatch: None|ui.NPatch = None
lightup: pygame.Vector2 = pygame.Vector2()
grid = None
power: Power|None = None
font = pygame.font.SysFont("Arial",30)
pls: list = []




def init() -> None:
    """
    init the base screen

    :param grid: the game's grid
    :param players: list of availble players
    :return:
    """
    global root, t, tclose, topen, debugpatch
    try:
        if os.name == "nt":
            from subprocess import Popen, PIPE
            print("Os: Windows")
            pipe = Popen("powershell -ExecutionPolicy Bypass .\winres.ps1", stdout=PIPE, stderr=PIPE)
            s = (pipe.stdout.readline()[:-2], pipe.stdout.readline()[:-2])
            print(s)

            wh: tuple[int, int] = (int(s[0]),int(s[1]))
        else:
            from subprocess import Popen, PIPE
            print("Os: Unix/Linux")
            pipe = Popen("xdpyinfo | grep dimensions", stdout=PIPE, stderr=PIPE)
            s = pipe.stdout.readline()
            s.split()[0]
            s.split("x")
            wh = (s[0], s[1])
    except: wh = (1920, 1080)

    root = pygame.display.set_mode(wh, pygame.FULLSCREEN)
    pygame.display.set_caption("Project Cheesesquares")


def initgame(grid, players: list) -> None:
    """
    init the game screen

    :param grid:
    :param players:
    :return:
    """
    global t, debugpatch, tclose, topen, power
    ui.all.clear()
    t = Tutorial()
    power = Power(grid)
    debugpatch = ui.NPatch(pygame.rect.Rect(400, 400, 400, 400), "assets/ui/npatch.png", align=ui.BOTTOMRIGHT)
    tclose = ui.Button("", "x.png", "x-hover.png", "x-clicked.png", pygame.rect.Rect(420, 22, 16, 16))
    topen = ui.Button("", "opentut.png", "opentut-hover.png", "opentut-hover.png", pygame.rect.Rect(0, 30, 32, 48))
    topen.hide()
    debug("This is the Debug console.\nopen/close it with 'u'. clear it with 'i'.")

    for p in range(len(players)):
        pl = PlayerActive(players[p])
        pl.position = pygame.Vector2(100, 30*p)
        pl.show()
        pls.append(pl)


def debug(*strs: str) -> None:
    """
    Logs on the console (open with 'u')

    :param strs: things to log. Accepts multiple arguments
    :return:
    """
    global debuglog
    debuglog.insert(0, "".join(strs) + "\n")
    if len(debuglog) > 13:
        debuglog = debuglog[:13]


def debug_clear() -> None:
    """
    clears the Debug log

    :return:
    """
    global debuglog
    debuglog.clear()


def update(grd, player) -> None:
    """
    update the grid data and player data

    :param grd:
    :param player:
    :return:
    """
    global grid, power
    grid = grd
    power.update()
    for p in pls:
        p.update(player)


def listen() -> pygame.Vector2|None:
    """
    Update the main screen and return a Vector2 if clicked on the map

    :return: None if not clicked, Vector2 if clicked
    """
    global lightup
    clock.tick()

    m = pygame.mouse.get_pos()
    camera.update(pygame.key.get_pressed())
    rsize = root.get_rect().size
    ui.vupdate(m[0], m[1], rsize)  # update ui
    debugpatch.setlines("\n---DEBUG---")  # update debug
    debugpatch.appendlines("".join(debuglog), (100, 255, 255))
    frag_size = ((m[0] - camera.x - 50*(((m[1])//100-1) % 2)) / 100, (m[1] - camera.y - 25) / 50)
    lightup = pygame.Vector2(int(frag_size[0]), int(frag_size[1]))

    root.fill(pygame.Color(0, 50, 50))  # Fill window background
    pygame.draw.circle(root, pygame.Color(0, 60, 60), pygame.Vector2(lightup.x * 100 + ((lightup.y+1)%2*-50) + 50, (lightup.y) * 50 + 50) + pygame.Vector2(camera.x, camera.y), 25)

    #--- Draw Edges ---#
    for x in range(grid.width):
        for y in range(grid.height):
            if grid.grid[x][y].owner is not None:
                pygame.draw.rect(root, grid.grid[x][y].owner.color - pygame.Color(128, 128, 128), pygame.Rect(x*100+camera.x, y*100+camera.y, 100, 100))

            if grid.grid[x][y].north is not None:
                pygame.draw.line(root, grid.grid[x][y].north.color, pygame.Vector2(x*100, y*100)+pygame.Vector2(camera.x, camera.y),\
                                 (x*100+100, y*100)+pygame.Vector2(camera.x, camera.y), 10)
            if grid.grid[x][y].east is not None:
                pygame.draw.line(root, grid.grid[x][y].east.color, pygame.Vector2(x*100+100, y*100)+pygame.Vector2(camera.x, camera.y),\
                                 (x*100+100, y*100+100)+pygame.Vector2(camera.x, camera.y), 10)
            if grid.grid[x][y].west is not None:
                pygame.draw.line(root, grid.grid[x][y].west.color, pygame.Vector2(x*100, y*100)+pygame.Vector2(camera.x, camera.y),\
                                 (x*100, y*100+100)+pygame.Vector2(camera.x, camera.y), 10)
            if grid.grid[x][y].south is not None:
                pygame.draw.line(root, grid.grid[x][y].south.color, pygame.Vector2(x*100, y*100+100)+pygame.Vector2(camera.x, camera.y),\
                                 (x*100+100,y*100+100)+pygame.Vector2(camera.x, camera.y), 10)


    #--- Draw Points ---#
    for x in range(grid.width + 1):
        for y in range(grid.height + 1):
            pygame.draw.circle(root, pygame.Color(0, 0, 0), pygame.Vector2(camera.x, camera.y) + pygame.Vector2(x*100, y*100), 20)

    #--- Draw UI ---#
    label = font.render(str(lightup + pygame.Vector2(0, 2)), False, pygame.Color(255,255,255))
    root.blit(label, (0, 0))
    for u in ui.all:  # draw ui
        if u.visible:
            root.blit(u.draw(), u.rel_pos)
    pygame.display.flip()  # update Display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 'X' clicked
            pygame.quit()
            exit()
        elif event.type == ui.BUTTONPRESS:  # Handle Button Events
            if event.id == tclose.get_id():  # => close tutorial
                tclose.hide()
                t.hide()
                topen.show()

            if event.id == topen.get_id():  # => open tutorial
                topen.hide()
                tclose.show()
                t.show()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                debugpatch.visible = not debugpatch.visible  # toggle debug visibility
            elif event.key == pygame.K_i:
                debug_clear()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                a = False  # check if any of the buttons is clicked and mute the input if true
                ul = ui.all.copy()
                ul.reverse()
                for u in ul:  # Button update
                    if u.clickupdate():  # if button is clicked returns true
                        debug("clicked", str(u))
                        a = True
                        break  # you cannot click multiple overlapping buttons
                if not a:
                    return lightup
    return None


