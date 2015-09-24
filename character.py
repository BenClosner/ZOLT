import pygame.image, pygame.transform
import constants, maps, items
import collections

sprites = pygame.image.load('bsprite2.png')

class character_base:
    def can_move(self, xy=(0,0)):
        #this calls xy to tile to find the tile the user wishes to move to (according to the xy parameter) and checks
        # if it is valid(not solid)
        return self.xyToTile(xy).solid

    def xyToTile(self, xy=(0,0), center=True):
        #Returns tile object for use of tile.solid method. Optional xy argument can be used to check if current position
        #plus xy is valid move.
        tilex = -(self.x - constants.WINDOWX//2 * center + xy[0])//64
        tiley = -(self.y - constants.WINDOWY//2 * center - constants.SPRITEY//2 + constants.SPRITEY//8 + xy[1])//64
        return maps.tiles[self.map.str_tiles[tiley][tilex]]

class character_user(character_base):
    def __init__(self):
        self.facing = 'e'
        self.x = 0
        self.y = 0
        self.dy = 0
        self.dx = 0
        self.move_speed = constants.MS
        self.last_press = None
        self.time_last_press = 0
        self.dashing = 0
        self.sword_swinging = False
        self.sword_out = False
        self.map = maps.starting_room
        self.sword = items.sword()

        #self.images is the set of sprites for the main character. the nest for loops are my attempt of
        # cleanly reading them from a sprite sheet.
        self.images = collections.defaultdict(list)
        dirs = 'ewsn'
        for dir in dirs:
            for sq in range(4):
                self.make_images(dir, (sq * 18, dirs.index(dir)*18,
                                       16 + sq * 18, 16 + dirs.index(dir)))

    def make_images(self, key, *args):
        # takes in some hard-coded values, read from the sprite sheet, makes a new blank surface and transfers
        # the said sprite to the blank sheet. Stores it in self.images, which is a dict with keys for each direction
        for x,y,w,h in args:
            blank = pygame.Surface((16,16), pygame.SRCALPHA)
            blank.blit(sprites, (0,0), (x,y,w,h))
            self.images[key].append(pygame.transform.scale(blank, (constants.SPRITEX, constants.SPRITEY)))

    def check_dash(self, last, frame):
        #checks to see if the user double taps by looking at the last button pressed and if it was
        #pressed in the last 0.2 seconds
        if self.last_press == last and (frame - self.time_last_press)/constants.FPS <= 0.2:
            self.move(last)
            self.dashing = 5
            self.last_press = None
        else:
            self.last_press = last
            self.time_last_press = frame

    def move(self, xy, s=0):
        # move updates the user object to reflect what the player wishes to do.
        x,y = xy

        if s and not self.sword_out:
            self.sword_swinging = True
        elif s and self.sword_swinging:
            self.sword_swinging = False
            self.sword_out = True
        elif not s:
            self.sword_out = False

        if s and not self.dashing:
            self.dx = 0
            self.dy = 0

        if not s and not self.dashing:
            self.dx = x
            self.dy = y
            if x == 1: self.facing = 'w'
            elif x == -1: self.facing = 'e'
            elif y == 1: self.facing = 'n'
            elif y == -1: self.facing = 's'
        self.update()

    def update(self):
        # the move method updates the user object disered direction, update changes the actual position.
        # first it checks to see if the users has died, then checks if they are dashing or leaving the map.
        # lastly, it checks if the move is a legal one and updates user.x and user.y
        self.check_if_user_hit()

        if self.dashing:
                self.move_speed = 2 * constants.MS
                self.dashing -= 1
        else:
            self.move_speed = constants.MS
        self.check_map_exit()

        if self.can_move((self.dx * self.move_speed, 0)):
            self.x += self.dx * self.move_speed
        if self.can_move((0, self.dy * self.move_speed)):
            self.y += self.dy * self.move_speed

    def draw_char(self, screen, frame):
        # first checks to see if the sword is in any position and blits it to the screen if it is. then checks
        # for the dashing animation. lastly it blits the main character to the screen
        center_x = constants.WINDOWX//2 - constants.SPRITEX//2
        center_y = constants.WINDOWY//2 - constants.SPRITEY//2
        center_of_screen = (center_x, center_y)

        sword_offset = {'s':(center_x - 30, center_y + constants.SPRITEY - 3),
                        'n':(center_x - constants.SPRITEX + 10, center_y - constants.SPRITEY),
                        'e':(center_x + constants.SPRITEX - 5, center_y + 10),
                        'w':(center_x - constants.SPRITEX, center_y + 10)}
        #some numbers are hard coded in because the sprites arent centered on the sheet

        if self.sword_swinging:
            screen.blit(self.sword.images[self.facing][0], sword_offset[self.facing])
            self.sword_swinging = False
            self.sword_out = True
        elif self.sword_out:
            screen.blit(self.sword.images[self.facing][1], sword_offset[self.facing])

        if self.dashing or self.sword_out or self.sword_swinging:
            im = self.images[self.facing][3]
        elif self.dx or self.dy:
            im = self.images[self.facing][frame % 3]
        else:
            im = self.images[self.facing][0]
        screen.blit(im, center_of_screen)

    def draw_map(self, screen):
        # draws the map. the map is drawn relative to the users position, so the map moves around the user, not the
        # other way around
        screen.blit(self.map.image, (self.x, self.y))

    def check_map_exit(self):
        # this is called every frame. user.map (the current map the user is on) changes when either
        # all the enemies have been slain in a boss room or when they hit an exit. the exit information in the
        # latter case is sotred in the tile
        # also adds enemies to a newly entered room. this code should be move soon
        if not self.map.enemy_list and self.map == maps.boss_room_closed:
            self.map = maps.boss_room_open
        if self.xyToTile((self.dx, self.dy)).is_exit:
            key = self.xyToTile((self.dx, self.dy)).next_map
            self.map = maps.map_list[key]
            if self.map != maps.starting_room:
                self.map.enemy_list= [guard(self.map, 100,100), guard(self.map, 200,200), guard(self.map, 400,400)]
            self.x = self.map.startx
            self.y = self.map.starty

    def check_if_user_hit(self):
        # simply checks if the user is being contacted by an enemy.
        # checks if the top left corner of an enemy or bottom right corner of an enemy is in users hitbox
        lowx, highx = abs(self.x - constants.WINDOWX//2), abs(self.x - constants.WINDOWX//2) + constants.SPRITEX
        lowy, highy = abs(self.y - constants.WINDOWY//2), abs(self.y - constants.WINDOWY//2) + constants.SPRITEY
        for enemy in self.map.enemy_list:
            if lowx < enemy.x < highx and lowy < enemy.y < highy:
                self.map, self.x, self.y = maps.starting_room,0,0
            if lowx < enemy.x + constants.SPRITEX < highx and lowy < enemy.y + constants.SPRITEY < highy:
                self.map, self.x, self.y = maps.starting_room,0,0


class guard(character_base):
    def __init__(self, map, start_x=0, start_y=0):
        self.images = collections.defaultdict(list)
        self.map = map
        #another ugly way to read sprites off the sprite sheet
        for dir in 'ewsn':
            for each in range(2):
                blank = pygame.Surface((16,16), pygame.SRCALPHA)
                blank.blit(sprites, (0,0), (143 + 18 * each, 18 * 'ewsn'.index(dir) , 16, 16))
                self.images[dir].append(pygame.transform.scale(blank, (constants.SPRITEX, constants.SPRITEY)))
        self.x = start_x
        self.y = start_y
        self.move_speed = constants.MS//3
        self.facing = 's'

    def update(self, user_x, user_y):
        # since the map moves relative to the user, the users xy must be know to offest this.
        # the gaurds walk straight toward the user, ajusting their facing accordingly
        # the gaurds will walk at 1/3 the users base ms
        user_x -= constants.WINDOWX//2
        user_y -= constants.WINDOWY//2

        wanted_x = user_x + self.x + constants.SPRITEX//2
        wanted_y = user_y + self.y + constants.SPRITEY//2

        dx = -1 if wanted_x < 0 else 1
        dy = -1 if wanted_y < 0 else 1

        if dx == 1: self.facing = 'w'
        elif dx == -1: self.facing = 'e'
        elif dy == 1: self.facing = 'n'
        elif dy == -1: self.facing = 's'

        self.x -= dx * self.move_speed
        self.y -= dy * self.move_speed

    def draw_self(self, screen, frame, xoff, yoff):
        # the offset is needed because the map moves relative to the user
        screen.blit(self.images[self.facing][frame % 2], (self.x + xoff, self.y + yoff))

    def check_hit(self, dir, tipx, tipy):
        # hitbox is checked to see if the tip of the sword has made contact
        # offsets are here, but should be moved
        # tipx and tipy are references to the screen, so they have to be convered to xy on the map
        # when an enemy 'dies' they are removed from the current maps enemy list.
        tipx -= constants.WINDOWX//2 - constants.SPRITEX//2
        tipy -= constants.WINDOWY//2 - constants.SPRITEY//2

        offset = { 's': (-constants.SPRITEX//4, constants.SPRITEY),
                   'n': (-constants.SPRITEX, -constants.SPRITEY * 2),
                   'e': (constants.SPRITEX, -constants.SPRITEY//4),
                   'w': (-constants.SPRITEX * 2, -constants.SPRITEY//2)}

        ox, oy = offset[dir]
        x_cond = self.x - constants.SPRITEX < abs(tipx) + ox < self.x
        y_cond = self.y - constants.SPRITEY < abs(tipy) + oy < self.y
        if x_cond and y_cond:
            self.map.enemy_list.remove(self)
