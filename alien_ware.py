import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from buttons import Button
from score_board import Scoreboard


def run_game():
    """Инициализирует пайгейм настройки и создает обьект экран"""
    # инициализируем пайгейм
    pygame.init()
    # инициализируем настройки
    ai_settings = Settings()
    # задаем цвет экрану
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Ware')
    play_button = Button(ai_settings, screen, 'Play')
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, stats, screen)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    gf.create_line_stars(ai_settings, stars, screen)
    # Запускаем цикл игры
    while True:
        # запускаем цикл для событий клавы и мыши
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stars, stats, play_button, sb)


run_game()
