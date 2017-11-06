import libtcodpy as libtcod
import setup
from setup import render_all
from setup import objects
from setup import handle_keys

while not libtcod.console_is_window_closed():
    render_all()

#Refreshes the screen (console in the library's parlance)
    libtcod.console_flush()

#Every object in the array objects is cleared, for purposes of refreshing and rerendering
    for object in objects:
        object.clear()

#If the exit key is detected, the loop is broken from, thereby ending the game
    player_action = handle_keys()
    if player_action == 'exit':
        break

    if setup.game_state == 'playing' and player_action != 'didnt-take-turn':
        for object in objects:
            if object.ai:
                object.ai.take_turn()
