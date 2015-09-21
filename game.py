#ZOLT is my mix of Titan Souls and The Legend of Zelda.
#Sprites are not mine, they are from ...

import pygame
import character, event_handler, constants

def game():
    screen = pygame.display.set_mode((constants.WINDOWX, constants.WINDOWY))
    clock = pygame.time.Clock()
    game_exit = False
    user = character.character_user()
    eh = event_handler.EventHandler()
    frame = 0

    while not game_exit:
        frame += 1

        #event_handler updates game exit on any exit command (X button ect)
        game_exit = eh.check_quit_status()
        #event_handler handles the click events and updates the 'user' object
        eh.update(user, frame, pygame.event.get())

        #clear the screen of past image
        screen.fill((0,0,0))
        #the main character is always in the middle of the screen
        #the map moves around the character
        user.draw_map(screen)
        user.draw_char(screen, frame)
        user.map.draw_enemies(screen, frame, user.x, user.y)

        #boilerplate
        pygame.display.update()
        clock.tick(constants.FPS)

if __name__ == "__main__":
    game()