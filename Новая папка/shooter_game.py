from pygame import *
from random import uniform, randint
'''импортируем функцию для засекания времени, чтобы интерпретатор
 не искал эту функцию в pygame модуле time, даем ей другое название сами'''
from time import time as timer
# подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.SysFont('Corbel', 80, True)
font2 = font.SysFont('Corbel', 35, True)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
pause_text = font1.render('Пауза', True, (255, 255, 255))
lose_boss = font1.render('ХА-ХА! Пропустил босса!', True, (180, 0, 0))
restart = font2.render('R - перезапуск', True, (255, 255, 255))  # сообщение о рестарте
start = font2.render('Нажми цифру чтобы начать', True, (255, 255, 255))  # сообщение о старте
start_diff = font2.render('1 - Легко, 2 - Норм, 3 - Капец', True, (255, 0, 255))  # выбор сложности
font2 = font.SysFont('Corbel', 30, True)

delayer = time.Clock()

# фоновая музыка
#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.set_volume(0.4) # громкость музыки 40%
#fire_sound = mixer.Sound('fire.ogg')
#reload_sound = mixer.Sound('reload.ogg')
#select_sound = mixer.Sound('select_diff.ogg')
#boss_sound = mixer.Sound('boss.ogg')
#game_over_sound = mixer.Sound('game_over.ogg')
#destroy_sound = mixer.Sound('destroy.ogg')

# нам нужны такие картинки:
img_back = "image/galaxy.png"  # фон игры
img_bullet = "image/bullet.png"  # пуля
img_hero = "image/rocket.png"  # герой
img_enemy = "image/ufo.png"  # враг
img_ast = "image/asteroid.png"  # астероид
img_boss = "image/boss.png"  # босс

''' Да-да, всё равно нулю так как после выбора сложности подставим туда значения '''
score = 0  # сбито кораблей
goal = 0  # столько кораблей нужно сбить для победы
lost = 0  # пропущено кораблей
max_lost = 0  # проиграли, если пропустили столько
life = 0  # текущие жизни
max_life = 0 # нужно для рестарта, тут храним максимальное количество жизней
max_enemies = 0  # максимальное количество врагов
boss_counter = 0 # счетчик убитых боссов
reload_time = 0 # время перезарядки
boss_comming_at = 0 # храним через сколько набранных очков придёт босс
boss_comming = 0 # через сколько придет следующий босс
num_fire = 0  # переменная для подсчта выстрела

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        global is_busy
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# класс спрайта-врага
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Boss(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, lifes_count):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y, 1)
        self.lifes = lifes_count # у босса новое поле для количества жизней
    def update(self):
        global finish
        self.rect.y += self.speed
        if self.rect.y > win_height:
            #mixer.music.stop() # останавливаем музыку
            finish = True
            make_frame() # отрисовываем фон и счетчики размещая их по центру
            window.blit(lose_boss, (win_width / 2 - lose_boss.get_width() / 2, 200))
            window.blit(restart, (win_width / 2 - restart.get_width() / 2, 300))

# класс спрайта-пули
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

# Создаем окошко
# window = display.set_mode((0, 0), FULLSCREEN) # можно установить полноэкранный режим
window = display.set_mode((800, 500))           # и тогда эту строку нужно закомментировать
display.set_caption("SUPER SHOOTER!")
win_width = display.Info().current_w  # получаем ширину окна
win_height = display.Info().current_h  # получаем высоту окна
background = transform.scale(image.load(img_back), (win_width, win_height))
''' Можно так же адаптировать размеры спрайтов, чтобы была зависимость размера спрайта от размера экрана '''
# создаем спрайты
ship = Player(img_hero, 5, win_height - 60, 80, 55, 10)
boss = Boss(img_boss, randint(80, win_width - 80), -40, 80, 100, 10)

monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

finish = False # переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
run = True  # флаг сбрасывается кнопкой закрытия окна
rel_time = False  # флаг отвечающий за перезарядку
first_start = True # переменная чтобы игра не начиналась после запуска
pause = False # переменная котороя отвечает за паузу
boss_time = False # переменная которая определяет появится босс или нет

def make_ememies():
    ''' функция uniform из модуля рандом даёт нам возможность получать рандомное число, 
    но не целое, а с плавающей запятой(float). Таким образом, скорость в меньшем диапазоне
    будет наиболее разнообразней чем с целыми числами.
    '''
    for i in range(max_enemies):
        monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, uniform(1.5, 3.0)))
    for i in range(3):
        asteroids.add(Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, uniform(1.0, 2.0)))
''' 
    Зачем выность в отдельную функцию отрисовку фона и счетчиков?
    - Потому что эта часть будет повторяться три раза в ходе программы.
    1. В ходе игры. 2. При проигрыше. 3. При выигрыше.  
    
    Зачем делать это при выигрыше и проигрыше?
    - Для того чтобы счетчики корректно отображались и не врали.  
'''
def make_frame():
    window.blit(background, (0, 0))
    window.blit(font2.render("Счет: " + str(score) + "/" + str(goal), 1, (255, 255, 255)), (10, 20))
    window.blit(font2.render("Пропущено: " + str(lost) + "/" + str(max_lost), 1, (255, 255, 255)), (10, 50))
    window.blit(font2.render("Боссов: " + str(boss_counter), 1, (255, 255, 255)), (10, 80))
    
''' 
    Чтобы отобразить надпись ровно по центру нужно знать ширину и высоту окна,
    а так же ширину и высоту спрайта, в данном случае текстового. Формула ниже
'''
window.blit(start, (win_width / 2 - start.get_width() / 2 , win_height / 2 - start.get_height() / 2))
window.blit(start_diff, (win_width / 2 - start_diff.get_width() / 2 , win_height / 2 - start_diff.get_height() / 2 + 40))
display.update()
# Основной цикл игры:
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            # событие нажатия на escape - пауза (вкл/выкл)
            if e.key == K_ESCAPE:
                if pause and not first_start:
                    pause = False
                    #mixer.music.play()
                elif not pause and not first_start:
                    pause = True
                    #mixer.music.pause()
                    window.blit(pause_text, (win_width / 2 - pause_text.get_width() / 2 , win_height / 2 - pause_text.get_height() / 2))
                    display.update()
            elif e.key == K_q: # выход из игры по нажатию Q
                run = False
            # событие нажатия на пробел - спрайт стреляет
            elif e.key == K_SPACE and not finish and not pause:
                # проверяем сколько выстеров сделано и не происходит ли перезарядка
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    #fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:  # если игрок сделал 5 выстрелов
                    #reload_sound.play()
                    last_time = timer()  # засекаем время, когда это произошло
                    rel_time = True  # ставив флаг перезарядки
            # легкий уровень сложности
            elif e.key == K_1 and first_start:
                goal = 50
                reload_time = 1
                max_lost = 10
                life = max_life = 5  
                max_enemies = 5 
                boss_comming_at = boss_comming = 20 # обе переменные будут со значением 20
                #select_sound.play()
                #mixer.music.play() # воспроизводим музыку только при начале игры
                first_start = False
                make_ememies()
            # средний уровень сложности
            elif e.key == K_2 and first_start:
                goal = 125
                reload_time = 2
                max_lost = 7
                life = max_life = 4  
                max_enemies = 7 
                boss_comming_at = boss_comming = 15 # обе переменные будут со значением 15
                #select_sound.play()
                #mixer.music.play() # воспроизводим музыку только при начале игры
                first_start = False
                make_ememies()
            # сложный уровень сложности
            elif e.key == K_3 and first_start:
                goal = 300
                reload_time = 3
                max_lost = 5
                life = max_life = 3  
                max_enemies = 10 
                boss_comming_at = boss_comming = 10 # обе переменные будут со значением 10
                #select_sound.play()
                #mixer.music.play() # воспроизводим музыку только при начале игры
                first_start = False
                make_ememies()
            # рестарт - клавиша R, сработает только если игра закончена
            elif e.key == K_r and finish:  
                # обнуляемся
                score = 0
                lost = 0
                life = max_life # вот для этого нужна max_life, чтобы помнить сколько жизней должно быть в максимальном значении
                boss_counter = 0
                num_fire = 0
                boss_comming = boss_comming_at
                for monster in monsters:
                    monster.kill() # убираем всех врагов
                for asteroid in asteroids:
                    asteroid.kill() # убиваем все астероиды
                make_ememies()
                for bullet in bullets:
                    ''' удаляем все пули которые на сцене, если этого
                        не сделать они продолжат лететь после рестарта '''
                    bullet.kill()
                if boss_time:
                    boss.kill()
                    boss_time = False
                finish = False
                #mixer.music.play() # воспроизводим музыку только при начале игры
    if not first_start:
        if not pause:
            # сама игра: действия спрайтов, проверка правил игры, перерисовка
            if not finish:
                # отрисовываем фон и счетчики
                make_frame() 

                # производим движения спрайтов
                ship.update()
                monsters.update()
                asteroids.update()
                bullets.update()

                # обновляем их в новом местоположении при каждой итерации цикла
                ship.reset()
                monsters.draw(window)
                asteroids.draw(window)
                bullets.draw(window)

                # проверяем, если сейчас босс должен быть на сцене
                if boss_time:
                    cols = sprite.spritecollide(boss, bullets, True) # собираем касания с пулями
                    for col in cols:
                        boss.lifes -= 1 # отнимаем боссу жизни
                    window.blit(font2.render("BOSS: " + str(boss.lifes), 1, (255, 0, 0)), (10, 140)) # обновляем счетчик
                    boss.update()
                    boss.reset()
                    if boss.lifes <= 0: # если у босса кончились жизни
                        boss_time = False 
                        score += 5 
                        boss_comming = score + boss_comming_at # следующий босс появится через "текущие очки" + "через сколько должен появится босс"
                        boss_counter += 1 # счетчик поверженных боссов +1
                        boss.kill() # совсем убиваем его со сцены
                if not boss_time and boss_comming - score <= 0: # если не время босса и "когда должен прийти босс" - "текущие очки" меньше или равно нулю, то пришло время выпускать босса
                    boss_time = True
                    boss = Boss(img_boss, randint(80, win_width - 80), -40, 80, 100, 5) # параметра скорости нет, скорость у боссов - 1
                    #6boss_sound.play() # звук появления босса

                # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
                collides = sprite.groupcollide(monsters, bullets, True, True)
                for c in collides:
                    # этот цикл повторится столько раз, сколько монстров подбито
                    score += 1
                    #destroy_sound.play()
                    monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, uniform(1.5, 3.0)))
                
                # если спрайт коснулся врага уменьшает жизнь
                if sprite.spritecollide(ship, monsters, False):
                    sprite.spritecollide(ship, monsters, True)
                    monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, uniform(1.5, 3.0)))
                    life -= 1
                if sprite.spritecollide(ship, asteroids, False):
                    sprite.spritecollide(ship, asteroids, True)
                    asteroids.add(Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, uniform(1.0, 2.0)))
                    life -= 1
                # проигрыш
                if life == 0 or lost >= max_lost or ship.rect.colliderect(boss): # касание босса - это тоже проигрыш
                    # проиграли, ставим фон и больше не управляем спрайтами.
                    #mixer.music.stop() # останавливаем музыку
                    finish = True
                    make_frame() # отрисовываем фон и счетчики размещая их по центру
                    window.blit(lose, (win_width / 2 - lose.get_width() / 2, 200))
                    window.blit(restart, (win_width / 2 - restart.get_width() / 2, 300))
                    #game_over_sound.play()

                ''' закомментируй если хочешь бесконечную игру '''
                # проверка выигрыша: сколько очков набрали?
                if score >= goal:
                    #mixer.music.stop() # останавливаем музыку
                    finish = True
                    make_frame() # отрисовываем фон и счетчики
                    window.blit(win, (win_width / 2 - win.get_width() / 2, 200))
                    window.blit(restart, (win_width / 2 - restart.get_width() / 2, 300))
                ''' закомментируй если хочешь бесконечную игру '''

                # перезарядка
                if rel_time == True:
                    now_time = timer()  # считываем время
                    if now_time - last_time < reload_time:  # пока не прошло reload_time выводим информацию о перезарядке
                        window.blit(font2.render("Патроны: заряжаем", 1, (255, 0, 0)), (10, 110))
                    else:
                        num_fire = 0   # обнуляем счетчик пуль
                        rel_time = False  # сбрасываем флаг перезарядки
                else:
                    window.blit(font2.render("Патроны: " + str(5 - num_fire), 1, (255, 255, 255)), (10, 110))
                    
                # задаем разный цвет в зависимости от кол-ва жизней
                if life >= 3 and life <= 5:
                    life_color = (0, 150, 0)
                elif life == 2:
                    life_color = (150, 150, 0)
                else:
                    life_color = (150, 0, 0)

                text_life = font1.render(str(life), 1, life_color)
                window.blit(text_life, (750, 10))

                display.update()
            time.delay(50)