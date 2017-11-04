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
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

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

    rooms = []
    num_rooms = 0

    for r in range(screen.MAX_ROOMS):
        # random width and height
        w = libtcod.random_get_int(0, screen.ROOM_MIN_SIZE, screen.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, screen.ROOM_MIN_SIZE, screen.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, screen.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, screen.MAP_HEIGHT - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1


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
