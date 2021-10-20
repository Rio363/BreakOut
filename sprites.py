import pygame as pg
from settings import *
import random


class Player(pg.sprite.Sprite):
    def __init__(self, game_obj):
        super().__init__(game_obj.all_sprites)
        self.game_obj = game_obj
        self.image = game_obj.player_imgs[0]
        self.rect = self.image.get_rect(midbottom=[WIDTH / 2, HEIGHT - 40])
        self.speedx = 0

        self.lives = 3
        self.anim_lst = game_obj.player_imgs
        self.anim_wait_time = 100
        self.anim_last_update = 0
        self.frame = 0

        # Collectables Vars...
        self.safety_line_active = False
        self.safety_line_start_time = 0
        self.safety_line_wait_time = 5000

        self.is_big = False
        self.become_bigger_time = 0
        self.size_change_time = 5000
        ########
        self.is_small = False
        self.become_smaller_time = 0

    def update(self):
        self.movement()
        self.animate()
        now = pg.time.get_ticks()

        if self.safety_line_active:
            self.draw_safety_line()
            if now - self.safety_line_start_time > self.safety_line_wait_time:
                self.stop_safety_line()

        if self.is_big:
            if now - self.become_bigger_time > self.size_change_time:
                self.back_to_normal_size()
        if self.is_small:
            if now - self.become_smaller_time > self.size_change_time:
                self.back_to_normal_size()

    def movement(self):
        self.rect.centerx += self.speedx
        self.speedx = 0
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.move_left()
        if keys[pg.K_RIGHT]:
            self.move_right()

    def move_right(self):
        if self.rect.right < WIDTH:
            self.speedx = 20

    def move_left(self):
        if self.rect.left > 0:
            # self.rect.x -= self.speedx
            self.speedx = -20

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.anim_last_update > self.anim_wait_time:
            self.anim_last_update = now
            self.frame = (self.frame + 1) % len(self.anim_lst)
            old_center = self.rect.center
            self.image = self.anim_lst[self.frame]
            self.rect = self.image.get_rect(center=old_center)

    # Collectables....
    def start_safety_line(self):
        self.safety_line_active = True
        self.safety_line_start_time = pg.time.get_ticks()

    def stop_safety_line(self):
        self.safety_line_active = False

    def draw_safety_line(self):
        pg.draw.rect(self.game_obj.screen, GREEN, [0, HEIGHT - 30, WIDTH, 20])

    #########
    def multi_ball(self):
        for _ in range(3):
            b = Ball(self.game_obj)
            b.rect.midbottom = self.rect.midtop

    #########
    def back_to_normal_size(self):
        self.is_big = self.is_small = False
        self.anim_lst = self.game_obj.player_imgs

    def become_bigger(self):
        if self.is_small:
            self.back_to_normal_size()
        self.is_big = True
        self.become_bigger_time = pg.time.get_ticks()
        self.anim_lst = self.game_obj.player_imgs_big

    def become_smaller(self):
        if self.is_big:
            self.back_to_normal_size()
        self.is_small = True
        self.become_smaller_time = pg.time.get_ticks()
        self.anim_lst = self.game_obj.player_imgs_small


class Brick(pg.sprite.Sprite):
    def __init__(self, game_obj, pos_x, pos_y):
        super().__init__(game_obj.all_sprites, game_obj.bricks)
        self.image = random.choice(game_obj.brick_images)
        self.rect = self.image.get_rect(topleft=[pos_x, pos_y])


class Ball(pg.sprite.Sprite):
    def __init__(self, game_obj):
        super().__init__(game_obj.all_sprites, game_obj.balls)
        self.image_orig = game_obj.ball_img
        self.game_obj = game_obj
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect(topleft=[WIDTH / 2, HEIGHT / 2])

        self.speedx = random.choice([-10, 10])
        self.speedy = random.choice([-7, -4])

        self.last_rot_time = 0
        self.rot_wait_time = 25
        self.rot_speed = 10
        self.rot_angle = 0

    def update(self):
        self.movement()
        self.rotate() # Barely makes any difference -_-

    def movement(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH - 10 # so It would never stick to sides
            self.speedx *= -1
        elif self.rect.left < 0:
            self.rect.left = 10
            self.speedx *= -1
        if self.rect.top < 50: # 50 is the space over the bricks defined in breakout.py initialize_bricks()
            self.rect.top = 60
            self.speedy *= -1

        # Kill ball if safety_line is not active or bounce
        if self.game_obj.player.safety_line_active:
            if self.rect.bottom + 20 >= HEIGHT:  # 20 == safety_line height
                self.rect.bottom = HEIGHT - 30
                self.speedy *= -1
        else:
            if self.rect.top > HEIGHT:
                self.kill()
    
    def rotate(self):
        now = pg.time.get_ticks()

        if now - self.last_rot_time > self.rot_wait_time:
            self.last_rot_time = now
            self.rot_angle = (self.rot_angle + self.rot_speed) % 360
            old_center = self.rect.center
            self.image = pg.transform.rotate(self.image_orig, self.rot_angle)
            self.rect = self.image.get_rect(center=old_center)

class Collectable(pg.sprite.Sprite):
    def __init__(self, game_obj, brick_obj):
        super().__init__(game_obj.all_sprites, game_obj.collectables)
        self.game_obj = game_obj
        brick_rect = brick_obj.rect
        self.collectable_type = random.choice(COLLECTABLE_TYPES)

        if self.collectable_type == "safety_line":
            self.image = game_obj.safety_line_img
        elif self.collectable_type == "multi_ball":
            self.image = game_obj.multi_ball_img
        elif self.collectable_type == "become_bigger":
            self.image = game_obj.bigger_img
        elif self.collectable_type == "become_smaller":
            self.image = game_obj.smaller_img
        else:
            self.image = pg.Surface([20, 20])
            self.image.fill(GREEN)

        self.rect = self.image.get_rect(center=brick_rect.center)
        self.speedy = random.randint(3, 6)

    def movement(self):
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.kill()

    def update(self):
        self.movement()


class SpriteSheet(pg.sprite.Sprite):
    def __init__(self, file_path):
        super().__init__()
        self.sprite_sheet = pg.image.load(file_path).convert()

    def get_sprite(self, x, y, w, h):
        img = pg.Surface([w, h])
        img.set_colorkey(BLACK)
        img.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return pg.transform.scale(img, (w // 2, h // 2))


class Rock(pg.sprite.Sprite):
    def __init__(self, game_obj, brick_obj):
        super().__init__(game_obj.all_sprites, game_obj.rocks)
        self.game_obj = game_obj
        self.image_orig = pg.Surface([5, 15])
        self.image = self.image_orig.copy()
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.top = brick_obj.rect.top
        self.rect.centerx = brick_obj.rect.centerx

        self.speedy = 5

        self.last_rot_time = 0
        self.rot_wait_time = 20
        self.rot_angle = 0
        self.rot_speed = 10

    def update(self):
        self.rotate()

        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

    def rotate(self):
        now = pg.time.get_ticks()

        if now - self.last_rot_time > self.rot_wait_time:
            self.last_rot_time = now
            self.rot_angle = (self.rot_angle + self.rot_speed) % 360
            old_center = self.rect.center
            self.image = pg.transform.rotate(self.image_orig, self.rot_angle)
            self.image.fill(RED)
            self.rect = self.image.get_rect(center=old_center)

class Explosion(pg.sprite.Sprite):
    def __init__(self, game_obj, expl_obj):
        super().__init__(game_obj.all_sprites, game_obj.explosions)
        self.game_obj = game_obj

        self.anim_wait_time = 100
        self.last_update_time = pg.time.get_ticks()
        self.frame = 0

        self.expl_lst = game_obj.player_expl_lst
        if isinstance(expl_obj, Brick):
            self.expl_lst = game_obj.brick_expl_lst
            self.anim_wait_time = random.randint(25, 125)


        self.image = self.expl_lst[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = expl_obj.rect.center

        

    def update(self):
        now = pg.time.get_ticks()

        try:
            if now - self.last_update_time > self.anim_wait_time:
                self.last_update_time = now
                self.frame += 1
                old_center = self.rect.center
                self.image = self.expl_lst[self.frame]
                self.rect = self.image.get_rect(center=old_center)
        except IndexError:
            self.kill()
