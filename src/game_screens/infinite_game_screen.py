import random
import math

from pygame.locals import QUIT, KEYUP
from src.game_screens.screen import Screen
from src.game_screens.game_screen import Game_screen
from src.misc.game_enums import Game_mode
from src.ui.image import Image
from src.ui.text import Text

from src.objects import *


class Infinite_Game_Screen(Game_screen):
    def __init__(self, pygame, res, surface, size, gameclock, game_manager):
        Game_screen.__init__(self, pygame, res, surface,
                             size, gameclock, game_manager)

    def update(self, events):
        # if we are restarting the game
        if self.need_reset:
            self.reset_before_restart()

        # if watiting after death for explosion animation to get over
        if self.waiting_death_explosion:
            self.surface.blit(self.pygame.transform.scale(
                self.res.BG, self.size), (0, 0))
            self.cart.draw()
            self.animation_manager.draw_animations()
            self.pygame.display.flip()
            self.wait_death_timer += 1

            if self.wait_death_timer > self.wait_death_time:
                self.need_reset = True
                return Game_mode.GAME_OVER
            else:
                return Game_mode.INFINITE

        self.params = self.game_manager.params

        self.cart.move()
        self.surface.blit(self.pygame.transform.scale(
            self.res.BG, self.size), (0, 0))

        for image in self.images:
            self.images[image].draw()

        for text in self.texts:
            self.texts[text].draw()

        c = self.get_random_entity()
        if c is not None:
            self.coinlist.append(c)

        # checking if any coin has reached the bottom, then destroying them
        for c in self.coinlist:
            if self.death_zone.check_collision(c):
                self.coinlist.remove(c)
                del c

        for c in self.coinlist:
            c.draw()
            c.fall()
            self.cart.collect_item(c, self.params)

        self.cart.draw()

        self.animation_manager.draw_animations()

        # Update time
        seconds = self.gameclock.get_time() / 1000.0
        self.timer += seconds

        # returns real value of timer to int value
        int_timer = math.trunc(self.timer)
        self.texts['Score'].change_text('Score: ' + str(int(self.cart.points)))
        self.texts['Time'].change_text('Time: ' + str(int_timer))

        self.pygame.display.flip()

        if self.cart.dead:
            self.game_manager.score = int(self.cart.points)
            self.waiting_death_explosion = True

        for event in events:
            if event.type == QUIT:
                return Game_mode.QUIT

        return Game_mode.INFINITE