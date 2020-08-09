import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):
    """Класс падающая звезда"""

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('space.png')
        self.rect = self.image.get_rect()
        # Рендомное значение звезде по оси Х
        self.rect.x = self.rect.width
        # Инициализируем экрану прямоугольник и низ звезды = вверху экрана
        self.screen_rect = screen.get_rect()
        self.rect.bottom = self.screen_rect.top
        self.speed_factor = self.ai_settings.stars_speed
        self.y = float(self.rect.y)
        self.drawing = randint(0, 7)
    def blitme(self):
        """Функция отрисовки звезды на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self, stars):
        """Обновление координаты Y у звезд"""
        self.rect.y += float(self.speed_factor)
        for star in stars.copy():
            if star.rect.top >= self.ai_settings.screen_height:
                star.rect.bottom = self.screen_rect.top
