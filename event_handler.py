import pygame.event

class EventHandler:

    dash_keys = {pygame.K_UP: (0,1),
                 pygame.K_DOWN: (0,-1),
                pygame.K_LEFT: (1,0),
                pygame.K_RIGHT: (-1,0)}

    keys_held = {pygame.K_UP: False,
                 pygame.K_DOWN: False,
                 pygame.K_LEFT: False,
                 pygame.K_RIGHT: False,
                 pygame.K_SPACE: False,}

    direction = {pygame.K_UP: 'n',
                 pygame.K_DOWN: 's',
                 pygame.K_LEFT: 'w',
                 pygame.K_RIGHT: 'e'}

    def __init__(self):
        self.is_game_exit = False

    def update(self, user, frame, events):
        # this manages key presses and sends appropriate information to the user object

        for event in events:
            # the 'check quit status' method is called every frame
            if event.type == pygame.QUIT:
                self.is_game_exit = True

            if event.type == pygame.KEYDOWN:
                # keydown events are when a key is pressed. dash keys check if the user has hit a key within the last
                # 0.2 seconds
                if event.key in self.dash_keys:
                    user.check_dash(self.dash_keys[event.key], frame)

                # keys_held is a dict that stores the held keys
                self.keys_held[event.key] = True

            if event.type == pygame.KEYUP:
                    self.keys_held[event.key] = False

        tup = (self.keys_held[pygame.K_LEFT] - self.keys_held[pygame.K_RIGHT],
               self.keys_held[pygame.K_UP] - self.keys_held[pygame.K_DOWN])

        # whenever the sword is out, check for collisions
        if self.keys_held[pygame.K_SPACE]:
            user.map.check_hits(user.facing, user.x, user.y)
        user.move(tup, bool(self.keys_held[pygame.K_SPACE]))
        user.map.update_enemies(user.x, user.y)

    def check_quit_status(self):
        return self.is_game_exit