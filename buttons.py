import pygame.font


class Button(object):
    """Класс кнопки"""
    def __init__(self, ai_settings, screen, msg):
        self.ai_settings = ai_settings
        self.screen = screen
        # Создаем размеры кнопки и цвет
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.msg_color = (255, 255, 255)
        # Задаем место расположения кнопки
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.screen_rect = screen.get_rect()
        self.rect.center = self.screen_rect.center
        # Подготавливаем font None - обычный шрифт, 48 - размер текста
        self.font = pygame.font.SysFont(None, 48)
        # Надпись создается только раз
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Создаем надпись на кнопке"""
        # создаем текст на базе font, msg -текст, True - cглаживание текста, и сохраняем все в image_msg
        self.image_msg = self.font.render(msg, True, self.msg_color, self.button_color)
        # Для текста создаем прямоугольник и выравнивает прямоугольник текста на прямоугольник кнопки
        self.image_msg_rect = self.image_msg.get_rect()
        self.image_msg_rect.center = self.rect.center

    def draw_button(self):
        """Отображение кнопки на экране"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.image_msg, self.image_msg_rect)