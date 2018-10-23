import libtcodpy as libtcod
import const
import math
import textwrap
import shelve

########################################################################################################################
# CLASSES ##############################################################################################################
########################################################################################################################

class Object:
    def __init__(self, x, y, char, name, color, blocks=False, ai=None):
        self.name = name
        self.blocks = blocks
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.ai = ai
        if self.ai:  # set ownership of the AI component
            self.ai.owner = self

    def move(self, dx, dy):
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def move_towards(self, target_x, target_y):
        # vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        # return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self):
        # only show if it's visible to the player
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            (x, y) = to_camera_coordinates(self.x, self.y)

            if x is not None:
                # set color and then draw the character that represents this object at its position
                libtcod.console_set_default_foreground(const.con, self.color)
                libtcod.console_put_char(const.con, x, y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        (x, y) = to_camera_coordinates(self.x, self.y)
        if x is not None:
            libtcod.console_put_char(const.con, x, y, ' ', libtcod.BKGND_NONE)

class BasicNPC:
    # AI for a basic monster.
    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            # move towards player if far away
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

########################################################################################################################
# INPUT ################################################################################################################
########################################################################################################################

def handle_keys():
    global fov_recompute
    global looking

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_CHAR:
        if key.c == ord('l'):
            if looking == False:
                        looking = True
                        look_cursor.x = player.x
                        look_cursor.y = player.y
            elif looking:
                look_cursor.x = -100
                look_cursor.y = -100
                looking = False

    elif key.vk == libtcod.KEY_ESCAPE:
            return 'exit'


    # Arrow Keys (Moving) ----------------------------------------------------------------------------------------------
    if game_state == 'playing':
        if looking == False:
            if libtcod.console_is_key_pressed(libtcod.KEY_UP):
                player_move_or_attack(0, -1)

            elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
                player_move_or_attack(0, 1)

            elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
                player_move_or_attack(-1, 0)

            elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
                player_move_or_attack(1, 0)

            else:
                if key.c == ord('i'):
                    # show the inventory
                    inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                return 'didnt-take-turn'

    # Arrow Keys (Looking) ---------------------------------------------------------------------------------------------
    if game_state == 'playing':
        if looking == True:
            if libtcod.console_is_key_pressed(libtcod.KEY_UP):
                if libtcod.map_is_in_fov(fov_map, look_cursor.x, (look_cursor.y - 1)):
                    look_cursor.y -= 1


            elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
                if libtcod.map_is_in_fov(fov_map, look_cursor.x, (look_cursor.y + 1)):
                    look_cursor.y += 1


            elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
                if libtcod.map_is_in_fov(fov_map, (look_cursor.x - 1), look_cursor.y):
                    look_cursor.x -= 1


            elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
                if libtcod.map_is_in_fov(fov_map, (look_cursor.x + 1), look_cursor.y):
                    look_cursor.x += 1


            return 'didnt-take-turn'



########################################################################################################################
# FUNCTIONS ############################################################################################################
########################################################################################################################

def place_objects(room):
    # choose random number of monsters
    num_monsters = libtcod.random_get_int(0, 0, const.MAX_ROOM_MONSTERS)

    for i in range(num_monsters):
        # choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1, room.x2)
        y = libtcod.random_get_int(0, room.y1, room.y2)

        # only place it if the tile is not blocked
        if not is_blocked(x, y):
            if libtcod.random_get_int(0, 0, 100) < 80:  # 80% chance of getting an orc
                # create an orc
                ai_component = BasicNPC()

                monster = Object(x, y, 'o', 'orc', libtcod.desaturated_green,
                                 blocks=True, ai=ai_component)
            else:
                # create a troll
                ai_component = BasicNPC()

                monster = Object(x, y, 'T', 'troll', libtcod.darker_green,
                                 blocks=True, ai=ai_component)

            objects.append(monster)


def looking_oracle():

    # return a string with the names of all objects under the mouse
    (x, y) = (look_cursor.x, look_cursor.y)
    (x, y) = (camera_x + x, camera_y + y)

    # create a list with the names of all objects at the looking coordinates and in FOV
    names = [obj.name for obj in objects
        if obj.name != 'look'
            if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]

    names = ', '.join(names)  # join the names, separated by commas
    return names.capitalize()

def is_blocked(x, y):
    # first test the map tile
    if map[x][y].blocked:
        return True

    # now check for any blocking objects
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True

    return False

def player_move_or_attack(dx, dy):
    global fov_recompute

    # the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    # try to find an attackable object there
    target = None
    for object in objects:
        if object.x == x and object.y == y:
            target = object
            break

    # attack if target found, move otherwise
    if target is not None:
        message('The ' + target.name + ' laughs at your puny efforts to attack him!', libtcod.red)
    else:
        player.move(dx, dy)
        fov_recompute = True


def menu(header, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(const.con, 0, 0, width, const.SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = const.SCREEN_WIDTH / 2 - width / 2
    y = const.SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    # present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:  # (special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory]

    index = menu(header, options, const.INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(inventory) == 0: return None
    return inventory[index].item

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
    # make tiles in the rectangle passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = True
            map[x][y].block_sight = True

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    libtcod.console_set_default_background(const.panel, back_color)
    libtcod.console_rect(const.panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    # now render the bar on top
    libtcod.console_set_default_background(const.panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(const.panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(const.panel, libtcod.white)
    libtcod.console_print_ex(const.panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
                             name + ': ' + str(value) + '/' + str(maximum))


def message(new_msg, color=libtcod.white):
    # split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, const.MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == const.MSG_HEIGHT:
            del game_msgs[0]

        # add the new line as a tuple, with the text and the color
        game_msgs.append((line, color))

def make_map():
    global map, objects

    objects = [player, look_cursor]

    # fill map with "open" tiles (ocean)
    map = [[Tile(False)
            for y in range(const.MAP_HEIGHT)]
           for x in range(const.MAP_WIDTH)]

    rooms = []
    num_rooms = 0

    for r in range(const.MAX_ROOMS):
        # random width and height
        w = libtcod.random_get_int(0, const.ROOM_MIN_SIZE, const.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, const.ROOM_MIN_SIZE, const.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, const.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, const.MAP_HEIGHT - h - 1)

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

            # finally, append the new room to the list
            place_objects(new_room)
            rooms.append(new_room)
            num_rooms += 1

    # place the player on an open sea tile
    player_placed = False
    while not player_placed:
        new_x_place = libtcod.random_get_int(0, 5, const.MAP_WIDTH)
        new_y_place = libtcod.random_get_int(0, 5, const.MAP_HEIGHT)
        
        if not is_blocked(new_x_place, new_y_place):
            player.x = new_x_place
            player.y = new_y_place
            player_placed = True





def move_camera(target_x, target_y):
    global camera_x, camera_y, fov_recompute

    # new camera coordinates (top-left corner of the screen relative to the map)
    x = target_x - const.CAMERA_WIDTH / 2  # coordinates so that the target is at the center of the screen
    y = target_y - const.CAMERA_HEIGHT / 2

    # make sure the camera doesn't see outside the map
    if x < 0: x = 0
    if y < 0: y = 0
    if x > const.MAP_WIDTH - const.CAMERA_WIDTH -1: x = const.MAP_WIDTH - const.CAMERA_WIDTH -1
    if y > const.MAP_HEIGHT - const.CAMERA_HEIGHT -1: y = const.MAP_HEIGHT - const.CAMERA_HEIGHT -1

    if x != camera_x or y != camera_y: fov_recompute = True

    (camera_x, camera_y) = (x, y)

def to_camera_coordinates(x, y):
    # convert coordinates on the map to coordinates on the screen
    (x, y) = (x - camera_x, y - camera_y)

    if (x < 0 or y < 0 or x >= const.CAMERA_WIDTH or y >= const.CAMERA_HEIGHT):
        return (None, None)  # if it's outside the view, return nothing

    return (x, y)

def render_all():
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute

    move_camera(player.x, player.y)

    if fov_recompute:
        # recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, const.TORCH_RADIUS, const.FOV_LIGHT_WALLS, const.FOV_ALGO)
        libtcod.console_clear(const.con)

        # go through all tiles, and set their background color according to the FOV
        for y in range(const.CAMERA_HEIGHT):
            for x in range(const.CAMERA_WIDTH):
                (map_x, map_y) = (camera_x + x, camera_y + y)
                visible = libtcod.map_is_in_fov(fov_map, map_x, map_y)

                wall = map[map_x][map_y].block_sight
                if not visible:
                    # if it's not visible right now, the player can only see it if it's explored
                    if map[map_x][map_y].explored:
                        if wall:
                            libtcod.console_set_char_background(const.con, x, y, const.color_dark_wall, libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(const.con, x, y, const.color_dark_ground, libtcod.BKGND_SET)
                else:
                    # it's visible
                    if wall:
                        libtcod.console_set_char_background(const.con, x, y, const.color_light_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(const.con, x, y, const.color_light_ground, libtcod.BKGND_SET)
                    # since it's visible, explore it
                    map[map_x][map_y].explored = True

    for object in objects:
        if object != player:
            object.draw()
    player.draw()
    look_cursor.draw()

    libtcod.console_blit(const.con, 0, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT, 0, 0, 0)

    # prepare to render the GUI panel
    libtcod.console_set_default_background(const.panel, libtcod.black)
    libtcod.console_clear(const.panel)

    # print the game messages, one line at a time
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(const.panel, color)
        libtcod.console_print_ex(const.panel, const.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    if looking == True:
        # display names of objects under the mouse
        libtcod.console_set_default_foreground(const.panel, libtcod.light_gray)
        libtcod.console_print_ex(const.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, looking_oracle())

    # show the player's stats
    render_bar(1, 1, const.BAR_WIDTH, 'HP', 28, 50,
               libtcod.light_red, libtcod.darker_red)

    # blit the contents of "panel" to the root console
    libtcod.console_blit(const.panel, 0, 0, const.SCREEN_WIDTH, const.PANEL_HEIGHT, 0, 0, const.PANEL_Y)


def initialize_fov():
    global fov_recompute, fov_map
    fov_recompute = True

    # create the FOV map, according to the generated map
    fov_map = libtcod.map_new(const.MAP_WIDTH, const.MAP_HEIGHT)
    for y in range(const.MAP_HEIGHT):
        for x in range(const.MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

    libtcod.console_clear(const.con)

def new_game():
    global player, look_cursor, looking, inventory, game_msgs, game_state

    # create object representing the player
    player = Object(0, 0, '@', 'player', libtcod.white, blocks=True)
    look_cursor = Object(0, 0, 'X', 'look', libtcod.yellow, blocks=False)

    # generate map (at this point it's not drawn to the screen)
    make_map()
    initialize_fov()

    game_state = 'playing'
    looking = False
    inventory = []

    # create the list of game messages and their colors, starts empty
    game_msgs = []

    # a warm welcoming message!
    message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)

def save_game():
    # open a new empty shelve (possibly overwriting an old one) to write the game data
    file = shelve.open('savegame', 'n')
    file['map'] = map
    file['objects'] = objects
    file['player_index'] = objects.index(player)  # index of player in objects list
    file['inventory'] = inventory
    file['game_msgs'] = game_msgs
    file['game_state'] = game_state
    file.close()


def load_game():
    # open the previously saved shelve and load the game data
    global map, objects, player, inventory, game_msgs, game_state

    file = shelve.open('savegame', 'r')
    map = file['map']
    objects = file['objects']
    player = objects[file['player_index']]  # get index of player in objects list and access it
    inventory = file['inventory']
    game_msgs = file['game_msgs']
    game_state = file['game_state']
    file.close()

    initialize_fov()

def msgbox(text, width=50):
    menu(text, [], width)

def main_menu():

    while not libtcod.console_is_window_closed():

        # show the game's title, and some credits!
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, const.SCREEN_WIDTH/2, const.SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
            'LOOMINGS')
        libtcod.console_print_ex(0, const.SCREEN_WIDTH/2, const.SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER,
            'By nsv')

        # show options and wait for the player's choice
        choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        if choice == 1:  # load last game
            try:
                load_game()
            except:
                msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2:  # quit
            break

def play_game():
    global camera_x, camera_y, player_x, player_y

    player_action = None

    (camera_x, camera_y) = (0, 0)

    while not libtcod.console_is_window_closed():
        # render the screen
        render_all()

        libtcod.console_flush()

        # erase all objects at their old locations, before they move
        for object in objects:
            object.clear()

        # handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break

        # let monsters take their turn
        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for object in objects:
                if object.ai:
                    object.ai.take_turn()

main_menu()