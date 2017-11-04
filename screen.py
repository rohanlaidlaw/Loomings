import libtcodpy as libtcod


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

#Sets the colour of the tiles out of the player's line of sight
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

LIMIT_FPS = 20

#The bedrock layer of the library's screen handling. Where the UI and panels are drawn
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Loomings', False)

#A buffer console whereupon the sprites will be written is drawn over the root console
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)