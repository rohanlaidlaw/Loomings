import libtcodpy as libtcod


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

MAX_ROOM_MONSTERS = 3

#Sets the colour of the tiles out of the player's line of sight
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

LIMIT_FPS = 20

#The bedrock layer of the library's screen handling. Where the UI and panels are drawn
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Loomings', False)

#A buffer console whereupon the sprites will be written is drawn over the root console
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)

