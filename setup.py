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

def make_map():
    global map

    map = [[Tile(False)
            for y in range(screen.MAP_HEIGHT)]
           for x in range(screen.MAP_WIDTH)]
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True

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

#Create a test npc using the Object class
npc = Object(screen.SCREEN_WIDTH/2 - 5, screen.SCREEN_HEIGHT/2, '@', libtcod.yellow)

#Initialize an array containing hitherto created objects
objects = [npc, player]

make_map()
