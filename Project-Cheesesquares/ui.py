"""
pygame UI library. copyright Oskar Pietzsch, 2022
"""

import spritesheet
import pygame

pygame.init()
nfont: pygame.font.Font = pygame.font.SysFont("Arial", 15)

all = []
_total_ids = 0

# ---states---#
IDLE = 0
HOVER = 1
SELECT = 3  # select = hover + toggle
TOGGLE = 2
LOCKED = 4

# ---align---#
TOPLEFT = 0
TOPRIGHT = 1
BOTTOMLEFT = 2
BOTTOMRIGHT = 3

BUTTONPRESS: int = pygame.event.custom_type()


def clear() -> None:
    """
    clears all UI

    :return:
    """
    global all, _total_ids
    all = []
    _total_ids = 0


def vupdate(x: int, y: int, size: pygame.rect.Rect) -> None:
    """
    Updates every UI

    :param x: mouse x
    :param y: mouse y
    :param size: screen size
    :return:
    """
    for ui in all:
        ui.vupdate(x, y, size)


class UI:
    """
    Represents a visible UI
    """

    def __init__(self, align=TOPLEFT):
        self.surface = None
        self.visible: bool = False
        self.rect = None
        self.position = pygame.Vector2(0, 0)
        self.align = align
        self.rel_pos = pygame.Vector2(0, 0)
        all.append(self)

    def clickupdate(self):
        return False

    def draw(self):
        if self.surface is not None and self.visible:
            return self.surface

    def vupdate(self, mx, my, size):
            if self.align == BOTTOMRIGHT:
                self.rel_pos = pygame.Vector2(size[0] - self.position.x, size[1] - self.position.y)
            elif self.align == BOTTOMLEFT:
                self.rel_pos = pygame.Vector2(self.position.x, size[1] - self.position.y)
            elif self.align == TOPLEFT:
                self.rel_pos = self.position
            elif self.align == TOPRIGHT:
                self.rel_pos = pygame.Vector2(size[0] - self.position.x, self.position.y)


    def hide(self):
        self.visible = False


    def show(self):
        self.visible = True

class NPatch(spritesheet._Spritesheet, UI):
    """
    A scalable UI background
    """

    def __init__(self, rect, skin, parent=None, align=TOPLEFT, children=[]):
        self.rect = rect
        self.children = children
        self.parent = parent
        self.contents = []
        self.visible = False
        self.rel_pos = [rect.x, rect.y]
        self.align = align
        self.hover = False

        super().__init__(skin, use_alpha=True)

        # 9-Patch underground
        self.upper_left_edge = self.get_at(pygame.rect.Rect(0, 0, 16, 16))
        self.upper_cant = self.get_at(pygame.rect.Rect(16, 0, 16, 16))
        self.upper_right_edge = self.get_at(pygame.rect.Rect(32, 0, 16, 16))
        self.left_cant = self.get_at(pygame.rect.Rect(0, 16, 16, 16))
        self.center = self.get_at(pygame.rect.Rect(16, 16, 16, 16))
        self.right_cant = self.get_at(pygame.rect.Rect(32, 16, 16, 16))
        self.lower_left_edge = self.get_at(pygame.rect.Rect(0, 32, 16, 16))
        self.lower_cant = self.get_at(pygame.rect.Rect(16, 32, 16, 16))
        self.lower_right_edge = self.get_at(pygame.rect.Rect(32, 32, 16, 16))

        self._abandon_sheet()
        all.append(self)

    def draw(self):
        size = self.rect.size
        surf = pygame.Surface(size, pygame.SRCALPHA)
        #surf.fill(pygame.Color(0, 0, 0, 0))
        surf.blits(((self.upper_left_edge, (0, 0)),
                    (pygame.transform.scale(self.upper_cant, (size[0] - 32, 16)), (16, 0)),
                    (self.upper_right_edge, (size[0] - 16, 0)),
                    (pygame.transform.scale(self.left_cant, (16, size[1] - 32)), (0, 16)),
                    (pygame.transform.scale(self.center, (size[0] - 32, size[1] - 32)), (16, 16)),
                    (pygame.transform.scale(self.right_cant, (16, size[1] - 32)), (size[0] - 16, 16)),
                    (self.lower_left_edge, (0, size[1] - 16)),
                    (pygame.transform.scale(self.lower_cant, (size[0] - 32, 16)), (16, size[1] - 16)),
                    (self.lower_right_edge, (size[0] - 16, size[1] - 16)),
                    ))

        if self.contents != []:
            surf.blits(self.contents)

        return surf

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def setlines(self, text, color=(255, 255, 255)):
        self.contents = []
        i = 0
        for line in text.split("\n"):
            self.contents.append((nfont.render(line, False, color), (16, 9 + 25 * (i))))
            i += 1

    def appendlines(self, text, color=(255, 255, 255)):
        i = len(self.contents)
        for line in text.split("\n"):
            self.contents.append((nfont.render(line, False, color), (16, 9 + 25 * (i))))
            i += 1

    def vupdate(self, mx, my, size):
        self.hover = mx > self.rel_pos[0] and mx < self.rect.w + self.rel_pos[0] and my > self.rel_pos[1] and my < self.rect.h\
                + self.rel_pos[1] and self.visible
        if self.align == TOPRIGHT or self.align == BOTTOMRIGHT:
            self.rel_pos[0] = size[0] - self.rect.y
        if self.align == BOTTOMLEFT or self.align == BOTTOMRIGHT:
            self.rel_pos[1] = size[1] - self.rect.x

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def clickupdate(self):
        return self.hover


class Button(UI):
    """
    A clickable Button
    """

    def __init__(self, text, im_idle, im_hover, im_select, rect, use_images=False, parent=None, align=TOPLEFT,
                 click_len=1, toggle=False, im_toggled=None, font_type=nfont,
                 font_colors=[(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]):
        super().__init__()
        global _total_ids
        # self.children = []
        self.text = text
        self.font = font_type
        self.rect = rect
        self.state = IDLE
        self.id = _total_ids
        self.align = align
        self.parent = parent
        self.font_colors = font_colors
        _total_ids += 1
        if self.parent is None:
            all.append(self)
        else:
            parent.children.append(self)
        self.rel_pos = (rect.x, rect.y)
        if use_images:
            self.images = [im_idle, im_hover, None, im_select]
        else:
            self.images = [pygame.image.load("assets/ui/" + im_idle),
                           pygame.image.load("assets/ui/" + im_hover), None,
                           pygame.image.load("assets/ui/" + im_select),
                           ]
        self.toggle_mode = bool(toggle)
        self.visible = True
        self.click_len = click_len
        self.__cl = 0
        if self.toggle_mode:
            if use_images:
                self.images[2] = im_toggled
            else:
                self.images[2] = pygame.image.load("assets/ui/" + im_toggled)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def is_pressed(self):
        return self.state == TOGGLE or self.state == SELECT

    def vupdate(self, mx, my, size):
        if self.align == TOPRIGHT or self.align == BOTTOMRIGHT:
            x = size[0] - self.rect.x
        else: x = self.rect.x
        if self.align == BOTTOMLEFT or self.align == BOTTOMRIGHT:
            y = size[1] - self.rect.y
        else: y = self.rect.y
        self.rel_pos = pygame.Vector2(x, y)
        self.__cl -= 1
        if mx > self.rel_pos[0] and mx < self.rect.w + self.rel_pos[0] and my > self.rel_pos[1] and my < self.rect.h\
                + self.rel_pos[1] and self.visible:
            self.state = self.state | HOVER
        else:
            if self.state & HOVER: self.state -= HOVER

        if self.state & TOGGLE and self.__cl < 1: self.state -= TOGGLE

    def get_id(self):
        return self.id

    def draw(self):
        if self.visible:
            a = self.images[self.state].copy()
            a.blit(self.font.render(self.text, False, self.font_colors[self.state]),
                   (self.rect.width / 2 - self.font.size(self.text)[0] / 2,self.rect.height / 2 -  self.font.size(self.text)[1] / 2))
            return a

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def clickupdate(self):
        if self.state & HOVER:
            pygame.event.post(pygame.event.Event(BUTTONPRESS, {"id": self.id}))
            self.state = self.state | TOGGLE
            self.__cl = self.click_len
            return True
        return False
