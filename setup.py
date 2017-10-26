import libtcodpy as libtcod


# INPUT ################################################################################################################

def handle_keys():
    global player_x, player_y

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    # Arrow Keys -------------------------------------------------------------------------------------------------------
    if key.vk == libtcod.KEY_UP:
        player_y -= 1
    
    elif key.vk == libtcod.KEY_DOWN:
        player_y += 1

    elif key.vk == libtcod.KEY_LEFT:
        player_x -= 1

    elif key.vk == libtcod.KEY_RIGHT:
        player_x += 1


# GENERAL SET UP #######################################################################################################

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20  # 20 frames-per-second maximum
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Loomings', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)

player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT / 2


# PRIMARY EVENT LOOP ###################################################################################################

while not libtcod.console_is_window_closed():

    # Draw the Player --------------------------------------------------------------------------------------------------
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

    exit = handle_keys()
    if exit:
        break
