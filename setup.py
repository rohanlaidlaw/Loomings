import libtcodpy as libtcod
import screen

########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################

class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        libtcod.console_set_default_foreground(screen.con, self.color)
        libtcod.console_put_char(screen.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        libtcod.console_put_char(screen.con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

########################################################################################################################
# INPUT ################################################################################################################
########################################################################################################################

def handle_keys():
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    # Arrow Keys -------------------------------------------------------------------------------------------------------
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)

########################################################################################################################
# FUNCTIONS ############################################################################################################
########################################################################################################################

class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

def create_room(room):
    global map
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global map
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def make_map():
    global map

    # fill map with "blocked" tiles
    map = [[Tile(True)
        for y in range(screen.MAP_HEIGHT)]
           for x in range(screen.MAP_WIDTH)]

    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(50, 15, 10, 15)
    create_room(room1)
    create_room(room2)
    create_h_tunnel(25, 55, 23)

def render_all():
    global color_light_wall
    global color_light_ground

    for y in range(screen.MAP_HEIGHT):
        for x in range(screen.MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(screen.con, x, y, screen.color_dark_wall, libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(screen.con, x, y, screen.color_dark_ground, libtcod.BKGND_SET)

    for object in objects:
        object.draw()

    libtcod.console_blit(screen.con, 0, 0, screen.SCREEN_WIDTH, screen.SCREEN_HEIGHT, 0, 0, 0)

########################################################################################################################
# GENERAL SET UP #######################################################################################################
########################################################################################################################

#Create the player using the Object class
player = Object(screen.SCREEN_WIDTH/2, screen.SCREEN_HEIGHT/2, '@', libtcod.white)
player.x = 25
player.y = 23

#Create a test npc using the Object class
npc = Object(screen.SCREEN_WIDTH/2 - 5, screen.SCREEN_HEIGHT/2, '@', libtcod.yellow)

#Initialize an array containing hitherto created objects
objects = [npc, player]

make_map()
