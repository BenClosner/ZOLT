import pygame.image, pygame.surface
import collections
import constants

class item:
    pass

sprites = pygame.image.load('bsprite2.png')

class sword(item):
    def __init__(self):
        self.images = collections.defaultdict(list)
        points = [[(72,0,16,16), (90,0,16,16)],[(72,18,16,16),(90,18,16,16)],[(72,36,32,16),(108,36,36,16)],[(72,54,32,16),(108,54,36,16)] ]
        for dir, point_lst in zip('ewsn',points):
            for point in point_lst:
                blank = pygame.Surface((32,32), pygame.SRCALPHA)
                blank.blit(sprites, (0,0), point)
                self.images[dir].append(pygame.transform.scale(blank, (constants.SPRITEX * 2, constants.SPRITEY * 2)))
