from pygame import *
from random import *
font.init()
font = font.Font(None, 50)

window = display.set_mode((900, 600))
display.set_caption("Космо шутер")
background = transform.scale(image.load("galaxy.jpg"), (900, 600))

game = True
finish = False
ms_chuma = 0
hlebalo = 0
timer = 15
is_ready_shoot = True

class GameSprite(sprite.Sprite):
    def __init__(self, file_name, speed, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(file_name), (w, h))    
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE]:
            self.fire()
    def fire(self):
        global is_ready_shoot
        global timer
        if is_ready_shoot:
            bullet = Bullet("bullet.png", 5, self.rect.centerx, self.rect.top, 10, 3)
            bullets.add(bullet)
            is_ready_shoot = False
            timer = 15

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global hlebalo
        if self.rect.y >= 650:
            self.rect.y = 0
            self.rect.x = randint(75, 825)
            self.speed = randint(1, 3)
            hlebalo = hlebalo + 1

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
clock = time.Clock()
FPS = 60

players = Player("space_ship.png", 7, 425, 500, 60, 100)
monster1 = Enemy("ufo.png", 2, 100, 0, 100, 60)
monster2 = Enemy("ufo.png", 1.5, 250, 0, 100, 60)
monster3 = Enemy("ufo.png", 3, 400, 0, 100, 60)
monster4 = Enemy("ufo.png", 2, 600, 0, 100, 60)
monster5 = Enemy("ufo.png", 1.5, 750, 0, 100, 60)
asteroid1 = Enemy("asteroid.png", 2, 300, 0, 80, 80)
asteroid2 = Enemy("asteroid.png", 3, 500, 0, 80, 80)

monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
bullets = sprite.Group()

while game:
    win = font.render("YOU WIN!", True, (240, 242, 242))
    lose = font.render("YOU LOSE!", True, (240, 242, 242))
    schet = font.render("Счёт:" + str(ms_chuma), True, (240, 242, 242))
    propusk = font.render("Пропущено:" + str(hlebalo), True, (240, 242, 242))
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.blit(background, (0, 0))
        window.blit(schet, (10, 30))
        window.blit(propusk, (10, 60))
        players.reset()
        players.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        list_sprites = sprite.groupcollide(asteroids, bullets, True, True)

        if timer <= 0:
            is_ready_shoot = True
        else:
            timer -= 1
        for i in sprites_list:
            ms_chuma = ms_chuma + 1
            monster = Enemy("ufo.png", randint(1, 3), randint(75, 825), 0, 100, 60)
            monsters.add(monster)
        for i in list_sprites:
            asteroid = Enemy("asteroid.png", randint(1, 3), randint(75, 825), 0, 80, 80)
            asteroids.add(asteroid)
        if ms_chuma == 30:
            window.blit(win, (425, 300))
            finish = True
        if hlebalo >= 10:
            window.blit(lose, (425, 300))
            finish = True
        
        display.update()
        clock.tick(FPS)