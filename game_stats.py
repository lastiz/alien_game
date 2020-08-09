class GameStats(object):
    """Класс для сбора статистики в игре"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.record_score = self.record_read()

    def reset_stats(self):
        """Инициализирует статистику, изменяющиюся в игре"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def record_read(self):
        """Инициализирует рекорд из файла"""
        try:
            with open('record.txt', 'r') as file:
                record = file.read()
                return int(record.strip())
        except FileNotFoundError:
            return 0
