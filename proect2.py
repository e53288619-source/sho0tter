from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x , size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self,  player_image, player_x, player_y, size_x, size_y, x_speed, hp):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = x_speed
        self.hp = hp
    def update(self):
        self.rect.x +=self.x_speed
    def fire(self):
        bullet = Bullet('pula.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.y_speed = y_speed
    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y >= win_height:
            global cnt
            cnt += 1
            self.rect.y = 0
            self.rect.x = randint(0,600)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.y_speed = y_speed
    def update(self):
        self.rect.y -= self.y_speed
        if self.rect.y <= 0:
            self.kill()
class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.y_speed = y_speed
    def update(self):
        self.rect.y += self.y_speed
        if self.rect.y >= win_height:
            self.rect.y = 0

# 1.Класс Пуля. Двигается вертикально вверх. Создать объект нужно при определенных условиях.
# 2.Пули должны в группе
# 3.Пуля связано. Ее появление должно быть относительно игрока

pibble = Player('pibble.png', 350 , 400 , 50, 50, 0, 3)
asteroid = Asteroid('ast.png', randint(0, 600) ,100 ,100, 100 , 1)
asteroid2 = Asteroid('ast.png', randint(0, 600) ,100 ,100, 100 , 1)
asteroid3 = Asteroid('ast.png', randint(0, 600) ,100 ,100, 100 , 1)
healf = GameSprite('healf.png', randint(0, 600),randint(200, 400), 100, 100)

cnt = 0
score = 0
asteroiD = sprite.Group()
enemies = sprite.Group()
bullets = sprite.Group()

asteroiD.add(asteroid)
asteroiD.add(asteroid2)
asteroiD.add(asteroid3)


init()

mixer.init()
mixer.music.load('fon.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.3)

bullet_flew = mixer.Sound('bullet.ogg')
bullet_flew.set_volume(0.3)

for i in range(5):
    enemy = Enemy('enemy.png', randint(0, 600) ,100 ,100, 100 , randint(2,5))
    enemies.add(enemy)

win_width = 800
win_height = 600
display.set_caption("стрелялки")
window = display.set_mode((win_width, win_height))

img = image.load('nebo.png')
img = transform.scale(img, (800, 600))

run = True
clock = time.Clock()
finish = False

while run:
    for e in event.get():
        if e.type ==QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_a:
                pibble.x_speed = -5
            if e.key == K_d:
                pibble.x_speed = 5
            if e.key == K_SPACE:
                bullet_flew.play()
                pibble.fire()

        elif e.type == KEYUP:
            if e.key == K_a:
                pibble.x_speed = 0
            if e.key == K_d:
                pibble.x_speed = 0
    if not finish:
        window.blit(img, (0, 0))
        pibble.draw_sprite()
        pibble.update()
        enemies.draw(window)
        enemies.update()
        asteroiD.draw(window)
        asteroiD.update()
        healf.draw_sprite()
        healf.update()
        bullets.draw(window)
        bullets.update()
        font_lose = font.SysFont('verdana', 24)
        text = font_lose.render(str(cnt) + ' счетчик нло', True, (255, 0, 0))
        window.blit(text,(10, 400))
        text = font_lose.render(str(score) + ' счетчик сбитых нло', True, (255, 0, 0))
        window.blit(text,(10, 350))
        text = font_lose.render(str(pibble.hp) + '-здоровье', True, (255, 0, 0))
        window.blit(text,(10, 300))

        collides = sprite.groupcollide(bullets, enemies, True, True)
        for c in collides:
            score += 1
            enemy =Enemy('enemy.png', randint(0, 600), 100, 100, 100, randint(1, 3))
            enemies.add(enemy)

            
        if sprite.spritecollide(pibble, enemies, True):
            if pibble.hp > 1:
                pibble.hp -= 1
                print('корабль уничтожен')
                enemy = Enemy('enemy.png', randint(0, 600), 100, 100, 100, randint(1, 3))
                enemies.add(enemy)
            else:
                pibble.hp -= 1
                finish = True
                text = font_lose.render('вы проиграли', True, (255, 0, 0))
                window.blit(text, (300, 200))


        if sprite.spritecollide(pibble, asteroiD, False):
            finish = True
            text = font_lose.render('вы проиграли', True, (255, 0, 0))
            window.blit(text, (300, 200))


        if sprite.spritecollide(healf, bullets, True):
            pibble.hp += 1
            healf.rect.x = randint(0, 600)
            healf.rect.y= randint(200, 400)



    display.update()
    clock.tick(60)
