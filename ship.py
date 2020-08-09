import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Класс корабля игрока"""

    def __init__(self, ai_settings, screen):
        """Создает корабль и задает его начальную позицию"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # загрузка изображения корабля и получение прямоугольника
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # каждый корабль поялвяется у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        # флаги перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += float(self.ai_settings.speed_ship)
        if self.moving_left and self.rect.left > 0:
            self.center -= float(self.ai_settings.speed_ship)
        self.rect.centerx = self.center

    def blitme(self):
        """Рисуем корабль """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx

