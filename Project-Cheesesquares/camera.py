import pygame


x: int = 200
y: int = 200
CSPEED = 5  # const for camera speed

def limit(amount: float, max: float)->float:
    """
    returns a limited number

    :param amount: integer to limit
    :param max: maximum before limiting
    :return:
    """
    if amount <= max: return amount
    return max

def update(keys: pygame.key.ScancodeWrapper) -> None:
    """
    updates the camera position

    :param keys: list of pressed keys
    :return:
    """
    global x, y, CSPEED
    if keys[pygame.K_w]:
        y += CSPEED
    elif keys[pygame.K_s]:
        y -= CSPEED

    if keys[pygame.K_a]:
        x += CSPEED
    elif keys[pygame.K_d]:
        x -= CSPEED


def get_v2() -> pygame.Vector2:
    """
    returns the position as a pygame.Vector2
    :return:
    """
    return pygame.Vector2(x, y)
