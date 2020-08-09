import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard(object):
    """Класс для подсчета очков"""

    def __init__(self, ai_settings, stats, screen):
        self.ai_settings = ai_settings
        self.stats = stats
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Функция записи очков"""
        round_score = round(self.stats.score, -1)
        self.score_str = '{:,}'.format(round_score)
        self.score_image = self.font.render(self.score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.ai_settings.screen_width - 20
        self.score_rect.top = 20

    def show_score(self):
        """"Функция показа очков и рекорда"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """функция записи рекорда"""
        high_score = round(self.stats.record_score, -1)
        high_score = '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score, True,
                                                 self.text_color,
                                                 self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        """Показывает левел"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                      self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 20

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.y = 20
            ship.rect.left = 10 + ship_number * ship.rect.width
            self.ships.add(ship)

