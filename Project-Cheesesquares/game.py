import player
import grid
import basescreen
import menu

def main():
    """
    main game loop
    :return:
    """
    in_game: bool = True
    basescreen.init()
    while in_game:
        players: list[player.Player] = menu.menu()

        g: grid.Grid = grid.Grid(5, 5, players)
        basescreen.initgame(g, players)
        basescreen.update(g, g.players[g.active_player])

        while g.winner() is None:
            g.next_turn()
            basescreen.update(g, g.players[g.active_player])

        menu.winscreen(g.winner())

main()
