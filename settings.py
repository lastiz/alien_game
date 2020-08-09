class Settings(object):
    """Класс для хранения всех настроек alien ware"""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (1, 1, 1)
        self.speed_ship = 3.5
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.stars_speed = 5
        self.increasing_game = 1.1
        self.ship_limit = 3

    def changing_settings(self):
        """Изменяющиеся настройки"""
        self.aliens_speed = 1.2
        self.aliens_speed_height = 10
        # 1 - right, -1 - left
        self.fleet_direction = 1
        self.aliens_score = 50

    def complexity(self):
        """функция увелечения сложности"""
        self.aliens_speed *= self.increasing_game
        self.aliens_speed_height *= self.increasing_game
        # 1 - right, -1 - left
        self.fleet_direction *= self.increasing_game
        self.aliens_score = int(self.aliens_score * self.increasing_game)
