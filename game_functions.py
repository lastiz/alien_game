import sys

import pygame
from bullet import Bullet
from alien import Alien
from space import Star
from time import sleep


def fie_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fie_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(stats, aliens, bullets, ship, ai_settings, screen, sb)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, ai_settings, screen, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, ai_settings, screen, sb):
    """Чекает нажатие на кнопку плей"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        start_game(stats, aliens, bullets, ship, ai_settings, screen, sb)


def start_game(stats, aliens, bullets, ship, ai_settings, screen, sb):
    if not stats.game_active:
        reset_scoreboard(sb, stats)
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)


def reset_scoreboard(sb, stats):
    """Инициализирует новые данные в доску"""
    stats.reset_stats()
    sb.prep_level()
    sb.prep_score()
    sb.prep_ships()
    sb.prep_high_score()


def update_screen(ai_settings, screen, ship, bullets, aliens, stars, stats, play_button, sb):
    """Обновляет изображение на экране и отображает новый экран"""
    # при кадом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    # появляется корабль
    ship.blitme()
    aliens.draw(screen)
    if stats.game_active:
        ship.update()
        stars.update(stars)
        update_aliens(ai_settings, aliens, ship, bullets, stats, screen, sb)
        update_bullets(ai_settings, aliens, ship, bullets, screen, sb, stats)
    sb.show_score()
    if not stats.game_active:
        sb.show_score()
        ai_settings.changing_settings()
        play_button.draw_button()
    # отображает последний прорисованный экран
    pygame.display.flip()


def get_row_alien_x(ai_settings, alien_height, ship_height):
    aviablable_space_x = ai_settings.screen_height - 3 * alien_height - ship_height
    row_numbers = int(aviablable_space_x / (2 * alien_height))
    return row_numbers


def get_numbers_alien_x(ai_settings, alien_width):
    """Вычисляет кол-во пришельцов в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    numbers_alien = int(available_space_x / (2 * alien_width))
    return numbers_alien


def create_alien(ai_settings, screen, aliens, alien_number, row_numbers):
    """Создает пришельца и помещает его в ряду"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_numbers
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    # Создает экземпляр пришельца
    alien = Alien(ai_settings, screen)
    # Получаем кол-во возможных пришельцов в ряду благодаря функции
    # get_numbers_alien_x
    numbers_alien_x = get_numbers_alien_x(ai_settings, alien.rect.width)
    # Получаем кол-во строк пришельцев
    row_numbers = get_row_alien_x(ai_settings, alien.rect.height, ship.rect.height)
    # Создаем строки пришельцов с кол-вом в строке numbers_alien_x
    for row_number in range(row_numbers):
        # Создаем ряд пришельцов блягодаря функции create_alien
        for alien_number in range(numbers_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet(ai_settings, aliens):
    """Обновляет координаты каждого пришельца"""
    ai_settings.fleet_direction *= -1
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.aliens_speed_height


def check_fleet(ai_settings, aliens):
    """Проверяет достиг ли пришелец края"""
    for alien in aliens.sprites():
        if alien.check_direction():
            change_fleet(ai_settings, aliens)
            break


def update_aliens(ai_settings, aliens, ship, bullets, stats, screen, sb):
    """Обновляет координаты флота пришельцев"""
    check_fleet(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, bullets, aliens, ai_settings, screen, ship, sb)
    check_aliens_bottom(stats, bullets, aliens, ai_settings, screen, ship, sb)


def check_aliens_bottom(stats, bullets, aliens, ai_settings, screen, ship, sb):
    """Функция проверяет достижение алиенсами низа экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, bullets, aliens, ai_settings, screen, ship, sb)
            break


def ship_hit(stats, bullets, aliens, ai_settings, screen, ship, sb):
    """Функция, которая обрабатывает столкновение с кораблем"""
    # Уменьшаем корабли на 1
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        # Удаляем и создаем все пули и пришельцев
        bullets.empty()
        aliens.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        # Возвращаем корабль в центр поля
        ship.center_ship()
        # Останавливаем игру на 0.5с
        sleep(1)
    else:
        ship.center_ship()
        aliens.empty()
        bullets.empty()
        stats.game_active = False
        write_record(stats)
        stats.reset_stats()
        ai_settings.changing_settings()
        pygame.mouse.set_visible(True)


def write_record(stats):
    """Записывает рекорд"""
    if stats.score >= stats.record_score:
        print('111')
        with open('record.txt', 'w') as file:
            file.write(str(stats.score))


def update_bullets(ai_settings, aliens, ship, bullets, screen, sb, stats):
    """"Обновляет позиции пуль """
    bullets.update()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    get_collisions_aliens_bullets(bullets, aliens, sb, stats, ai_settings)
    if len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        ai_settings.complexity()
        create_fleet(ai_settings, screen, ship, aliens)


def get_collisions_aliens_bullets(bullets, aliens, sb, stats, ai_settings):
    """обрабатывает коллизии пришельцев и пуль"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.aliens_score * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)


def check_high_score(stats, sb):
    """Выводит рекорд счет на экран"""
    if stats.score > stats.record_score:
        stats.record_score = stats.score
        sb.prep_high_score()


def get_number_stars(ai_settings, star_width):
    """Вычисляет сколько всего поместится звезд в строке"""
    available_width_line = ai_settings.screen_width - 2 * star_width
    line_total_star = int(available_width_line / (star_width * 3))
    return line_total_star


def get_row_stars(ai_settings, star_height):
    available_height_row = ai_settings.screen_height - 2 * star_height
    row_total_stars = int(available_height_row / (star_height * 3))
    return row_total_stars


def create_star(ai_settings, stars, screen, number_star, row_number):
    """Создает звезду в строку"""
    star = Star(ai_settings, screen)
    star_width = star.rect.width
    star.rect.x = star_width + 3 * star_width * number_star
    star.rect.y = star.rect.height + 3 * star.rect.height * row_number
    if star.drawing == 5:
        stars.add(star)


def create_line_stars(ai_settings, stars, screen):
    """Создает строку капель"""
    star = Star(ai_settings, screen)
    line_total_star = get_number_stars(ai_settings, star.rect.width)
    row_total_stars = get_row_stars(ai_settings, star.rect.height)
    for row_number in range(row_total_stars):
        for number_star in range(line_total_star):
            create_star(ai_settings, stars, screen, number_star, row_number)
