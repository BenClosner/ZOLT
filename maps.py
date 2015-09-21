import pygame.image, pygame.surface, pygame.transform

sprite_sheet = pygame.image.load('outside.png')

class tile:
    def __init__(self, solid, x, y):
        self.solid = solid
        self.is_exit = False
        blank = pygame.Surface((16, 16))
        blank.blit(sprite_sheet, (0,0), (x,y,16,16))
        #the sprites are 16x16, so i blow them up to 64x64 to get a 'grainy' quality
        self.image = pygame.transform.scale(blank, (64, 64))


class exit_tile(tile):
    def __init__(self, base_tile, next_map):
        self.solid = True
        self.image = base_tile.image
        self.is_exit = True
        self.next_map = next_map

left = tile(False, 2, 62)
up_left = tile(False, 2, 45)
up = tile(False, 19, 45)
up_right = tile(False, 36,45)
right = tile(False, 36, 62)
bot_right = tile(False, 36, 79)
bot = tile(False, 19, 79)
bot_left = tile(False, 2, 79)
floor_1 = tile(True, 19, 62)
statue1 = tile(False, 104, 62)
inv_left = tile(False, 70, 45)
inv_right = tile(False, 70, 62)
empty = tile(True, 2, 28)
exit_floor_corridor = exit_tile(floor_1, 'corridor')
exit_floor_boss = exit_tile(floor_1, 'boss room closed')
exit_starting_room = exit_tile(floor_1, 'starting room')
exit_final = exit_tile(floor_1, 'final boss')

tiles = {"l":left,
         "ul":up_left,
         "u":up,
         "ur":up_right,
         "r":right,
         "br":bot_right,
         "b":bot,
         "bl":bot_left,
         "f1":floor_1,
         "s1":statue1,
         "il":inv_left,
         "ir":inv_right,
         "ec": exit_floor_corridor,
         "ebr": exit_floor_boss,
         "esr": exit_starting_room,
         "ef": exit_final,
         "emp":empty,
         }

class map:
    def __init__(self, grid, enemies=None, startx=0, starty=0,):
        self.startx = startx
        self.starty = starty
        self.cleared = False
        self.str_tiles = grid
        self.enemy_list = enemies if enemies else []
        x, y = len(grid[0]), len(grid)
        blank = pygame.Surface((x * 64, y * 64))
        for n, row in enumerate(grid):
            for c, tile in enumerate(row):
                blank.blit(tiles[tile].image, (c * 64, n * 64))
        self.image = blank

    def update_enemies(self, to_x, to_y):
        for enemy in self.enemy_list:
            enemy.update(to_x, to_y)

    def draw_enemies(self, screen, frame, xoff, yoff):
        for enemy in self.enemy_list:
            enemy.draw_self(screen, frame, xoff, yoff)

    def check_hits(self, dir, x, y):
        for enemy in self.enemy_list:
            enemy.check_hit(dir, x, y)

basic = map([["ul", 'u', 'u', 'ur'],
            ['l', 'f1', 's1', 'r'],
            ['bl', 'b', 'b', 'br']])


starting_room =  map(
    [['emp','emp','emp','emp','ec','ec','emp', 'emp','emp','emp'],
     ['ul', 'u', 'u', 'u', 'f1', 'f1', 'u', 'u', 'ur', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['bl', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'br', 'emp'],])

corridor = map(
    [['emp', 'ul', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'ur', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 's1', 'f1', 'f1', 'f1', 'f1', 'f1', 's1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['ebr', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'ebr'],
     ['ebr', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'ebr'],
     ['emp', 'l', 'f1', 'f1', 's1', 'f1', 'f1', 'f1', 'f1', 'f1', 's1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 's1', 'f1', 'f1', 'f1', 'f1', 'f1', 's1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'bl', 'b', 'b', 'b', 'b', 'b', 'esr', 'esr', 'b', 'b', 'b', 'b', 'br', 'emp']],
        startx=-50, starty=-650)

corridor_final = map(
    [['emp', 'emp', 'emp', 'emp', 'emp', 'emp', 'ef', 'ef', 'ef', 'emp', 'emp', 'emp', 'emp', 'emp', 'emp'],
     ['emp', 'ul', 'u', 'u', 'u', 'u', 'f1', 'f1', 'f1', 'u', 'u', 'u', 'u', 'ur', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 's1', 'f1', 'f1', 'f1', 'f1', 'f1', 's1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 's1', 'f1', 'f1', 'f1', 'f1', 'f1', 's1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 's1', 'f1', 'f1', 'f1', 'f1', 'f1', 's1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['emp', 'bl', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'br', 'emp']],
        startx=-50, starty=-650)

boss_room_open = map(
    [['ul', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'ur', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'il', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'esr'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'esr'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'ir', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['bl', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'br', 'emp'],
])

boss_room_closed = map(
    [['ul', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'u', 'ur', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['l', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'f1', 'r', 'emp'],
     ['bl', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'br', 'emp'],
], startx=-350, starty=-300)

map_list = {'corridor':corridor,
            'boss room closed': boss_room_closed,
            'starting room': starting_room,
            'boss room open': boss_room_open,
            'final boss': boss_room_closed}