import pygame, time, random, sys

fps = 60
screen_size = (500, 500)
bullet = False
bullet_y = 400
period = 1
start_time = 0
enemy_bool = False
enemy_y = 0
all_x_enemy = [i for i in range(0, 351, 50)]
speed_enemy = [1, 2, 3]
running = 2
stat_kills = 0
best_result = 0
fon_music = 0

path = 'cumoletik/'

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('cumoletiki')

player_x, player_y = 225, 400
pole = pygame.Surface((400, 400))
player = pygame.Surface((50, 50))
bullet_surf = pygame.Surface((10, 25))
bullet_surf.fill((0, 171, 255))
enemy = pygame.Surface((50, 50))
pygame.font.init()
arial = pygame.font.Font(path + 'fonts/arial.ttf', 40)
lose_label = arial.render('Game over!', False, (48, 16, 255))
restart_label = arial.render('Заново', False, (48, 16, 255))

on_button = arial.render('on', False, (48, 16, 255))
off_button = arial.render('off', False, (48, 16, 255))

pygame.mixer.init()
shoot = pygame.mixer.Sound(path + 'music/pew.mp3')
locked_music = pygame.mixer.Sound(path + 'music/lockedin.mp3')
normal_music = pygame.mixer.Sound(path + 'music/fon_melody.mp3')

locked_fon = pygame.image.load(path + 'images/lockedinalien.png').convert_alpha()

while True:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    time.sleep(1 / fps)
    if running == 1:
        screen.fill((50, 87, 174))
        screen.blit(pole, (50, 50))
        if fon_music == 0:
            pole.fill((255, 255, 255))
        else:
            pole.blit(locked_fon, (0, 0))
        
        if keys[pygame.K_a] and player_x > 50:
            player_x -= 10
        elif keys[pygame.K_d] and player_x < screen_size[1] - 100:
            player_x += 10
        screen.blit(player, (player_x, player_y))
        player.fill((0, 255, 0))
        
        if keys[pygame.K_SPACE] and not bullet:
            bullet = True
            bullet_x = player_x
            shoot.play()
        if bullet:
            screen.blit(bullet_surf, (bullet_x + 25, bullet_y))
            bullet_y -= 20
        if bullet_y < 50:
            bullet = False
            bullet_y = 400
        
        if not enemy_bool:
            if start_time == 0:
                start_time = int(time.time())
            if int(time.time()) - start_time == period:
                enemy_x = random.choice(all_x_enemy)
                enemy_speed = random.choice(speed_enemy)
                enemy_bool = True
        
        if enemy_bool:
            pole.blit(enemy, (enemy_x, enemy_y))
            if enemy_y < 400:
                enemy_y += enemy_speed
            else:
                enemy_bool = False
                enemy_y = 0
                start_time = 0
                running = 0
        
        if enemy_bool and bullet:
            if enemy_x + 10 <= bullet_x <= enemy_x + 70 and enemy_y <= bullet_y <= enemy_y + 50:
                enemy_bool = False
                bullet = False
                enemy_y = 0
                start_time = 0
                bullet_y = 400
                stat_kills += 1
        
        stat = arial.render(f'Попадания: {stat_kills}', False, (0, 0, 0))
        screen.blit(stat, (200, 450))
        if stat_kills // 10 == 1:
            speed_enemy = [2, 3, 4]
        elif stat_kills // 10 == 3:
            speed_enemy = [3, 4, 5]
        elif stat_kills // 10 == 5:
            speed_enemy = [4, 5, 6]
        elif stat_kills // 10 == 10:
            speed_enemy = [5, 6, 7]
        
    elif running == 0:
        difficulty = 3
        locked_music.stop(), normal_music.stop()
        if stat_kills > best_result:
            best_result = stat_kills
        stat_kills = 0
        screen.fill((184, 255, 129))
        w_lose = lose_label.get_width()
        screen.blit(lose_label, (250 - w_lose // 2, 100))
        h_res, w_res = restart_label.get_height(), restart_label.get_width()
        if (250 - w_res // 2) < mouse[0] < (250 - w_res // 2) + w_res and 200 < mouse[1] < 200 + h_res:
            if pygame.mouse.get_pressed()[0]:
                running = 1
                if fon_music == 1:
                    locked_music.play(999)
                else:
                    normal_music.play(999)
            pygame.draw.rect(screen, (255, 255, 255), ((250 - w_res // 2), 200, w_res, h_res), border_radius=5)
        screen.blit(restart_label, ((250 - w_res // 2), 200))
        mainmenu_label = arial.render('Главное меню', False, (48, 16, 255))
        h_main, w_main = mainmenu_label.get_height(), mainmenu_label.get_width()
        if (250 - w_main // 2) < mouse[0] < (250 - w_main // 2) + w_main and 250 < mouse[1] < 250 + h_main:
            if pygame.mouse.get_pressed()[0]:
                running = 2
                if fon_music == 1:
                    locked_music.play(999)
                else:
                    normal_music.play(999)
            pygame.draw.rect(screen, (255, 255, 255), ((250 - w_main // 2), 250, w_main, h_main), border_radius=5)
        screen.blit(mainmenu_label, ((250 - w_main // 2), 250))
        w_stat = stat.get_width()
        screen.blit(stat, (250 - w_stat // 2, 350))
        best = arial.render(f'Лучший: {best_result}', False, (48, 16, 255))
        w_best = best.get_width()
        screen.blit(best, (250 - w_best // 2, 400))
    elif running == 2:
        difficulty = 3
        locked_music.stop(), normal_music.stop()
        screen.fill((184, 255, 129))
        start_label = arial.render('Начать!', False, (48, 16, 255))
        w_start, h_start = start_label.get_width(), start_label.get_height()
        best = arial.render(f'Лучший: {best_result}', False, (48, 16, 255))
        w_best = best.get_width()
        screen.blit(best, (250 - w_best // 2, 400))
        
        locked_label = arial.render(f'locked_in music {'on' if fon_music == 1 else 'off'}', False, (48, 16, 255))
        w_locked = locked_label.get_width()
        screen.blit(locked_label, ((250 - w_locked // 2), 100))
        
        w_on, w_off, h_on, h_off = on_button.get_width(), off_button.get_width(), on_button.get_height(), off_button.get_height()
        if (250 - w_locked // 2) <= mouse[0] <= (250 - w_locked // 2) + w_on and 140 <= mouse[1] <= 140 + h_on:
            if pygame.mouse.get_pressed()[0]:
                fon_music = 1
            pygame.draw.rect(screen, (255, 255, 255), ((250 - w_locked // 2), 140, w_on, h_on), border_radius=5)
        screen.blit(on_button, ((250 - w_locked // 2), 140))
        
        if ((250 + w_locked // 2) - w_off) <= mouse[0] <= (250 + w_locked // 2) and 140 <= mouse[1] <= 140 + h_off:
            if pygame.mouse.get_pressed()[0]:
                fon_music = 0
            pygame.draw.rect(screen, (255, 255, 255), ((250 + w_locked // 2) - w_off, 140, w_off, h_off), border_radius=5)
        screen.blit(off_button, ((250 + w_locked // 2) - w_off, 140))
        
        if (250 - w_start // 2) < mouse[0] < (250 - w_start // 2) + w_start and 300 < mouse[1] < 300 + h_start:
            if pygame.mouse.get_pressed()[0]:
                running = 1
                if fon_music == 1:
                    locked_music.play(999)
                else:
                    normal_music.play(999)
            pygame.draw.rect(screen, (255, 255, 255), ((250 - w_start // 2), 300, w_start, h_start), border_radius=5)
        screen.blit(start_label, ((250 - w_start // 2), 300))
        
        
    pygame.display.flip()