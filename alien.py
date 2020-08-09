import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс пришельца"""

    def __init__(self, ai_settings, screen):
        """Инициализируем атрибуты пришельца"""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        # Загружаем картинку пришельца
        self.image = pygame.image.load('alien.bmp')
        # Рисуем прямоугольник для картинки пришельца
        self.rect = self.image.get_rect()
        # Задаем координаты пришельца
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Сохраняем координаты х в вещественном формате
        self.x = float(self.rect.x)

    def blitme(self):
        """Создание пришельца"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещает пришельца"""
        self.x += (self.ai_settings.aliens_speed * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_direction(self):
        self.screen_rect = self.screen.get_rect()
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
