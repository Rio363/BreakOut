from sprites import *
from os import path
import math


class Game:
    def __init__(self):
        self.running = True
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.font_file = pg.font.match_font(FONT_NAME)

        img_dir = path.join(path.dirname(__file__), "img")

        self.sprite_sheet = SpriteSheet(path.join(img_dir, SPRITESHEET_NAME))
        self.ball_img = pg.transform.scale(self.sprite_sheet.get_sprite(1403, 652, 64, 64), (BALL_SIZE, BALL_SIZE))
        self.player_imgs = [
            self.sprite_sheet.get_sprite(1158, 462, 243, 64),
            self.sprite_sheet.get_sprite(1158, 528, 243, 64),
            self.sprite_sheet.get_sprite(1158, 594, 243, 64),
        ]
        self.player_imgs = [pg.transform.scale(img, (PLAYER_W, PLAYER_H)) for img in self.player_imgs]
        self.player_imgs_big = [pg.transform.scale(img, (int(PLAYER_W * 2), PLAYER_H + 10)) for img in self.player_imgs]
        self.player_imgs_small = [pg.transform.scale(img, (int(PLAYER_W / 1.5), PLAYER_H)) for img in self.player_imgs]
        self.brick_images = [self.sprite_sheet.get_sprite(772, 390, 384, 128),
                             self.sprite_sheet.get_sprite(0, 130, 384, 128),
                             self.sprite_sheet.get_sprite(0, 390, 384, 128),
                             self.sprite_sheet.get_sprite(772, 260, 384, 128),
                             self.sprite_sheet.get_sprite(772, 0, 384, 128),
                             self.sprite_sheet.get_sprite(386, 650, 384, 128),
                             self.sprite_sheet.get_sprite(386, 390, 384, 128),
                             self.sprite_sheet.get_sprite(386, 130, 384, 128),
                             self.sprite_sheet.get_sprite(772, 520, 384, 128),
                             self.sprite_sheet.get_sprite(386, 780, 384, 128),
        ]
        self.brick_images = [pg.transform.scale(img, (BRICK_W, BRICK_H)) for img in self.brick_images]

        # Collectables...
        self.safety_line_img = pg.transform.scale(self.sprite_sheet.get_sprite(1158, 330, 243, 64),
                                                  COLLECTABLE_SIZE)  # safeline Collectable
        self.multi_ball_img = pg.transform.scale(self.sprite_sheet.get_sprite(594, 910, 243, 64),
                                                 COLLECTABLE_SIZE)  # multiball Collectable
        self.bigger_img = pg.transform.scale(self.sprite_sheet.get_sprite(1158, 264, 243, 64),
                                             COLLECTABLE_SIZE)  # Bigger Collectable
        self.smaller_img = pg.transform.scale(self.sprite_sheet.get_sprite(1158, 198, 243, 64),
                                              COLLECTABLE_SIZE)  # smaller Collectable
        self.heart_img = pg.transform.scale(self.sprite_sheet.get_sprite(1637, 652, 64, 58), (64 / 2.5, 58 / 2.5))

        self.player_expl_sprite_sheet = SpriteSheet(path.join(img_dir, PLAYER_EXPL_SPRITESHEET_NAME))
        self.player_expl_lst = [
            self.player_expl_sprite_sheet.get_sprite(1, 1, 192, 192),
            self.player_expl_sprite_sheet.get_sprite(195, 1, 152, 150),
            self.player_expl_sprite_sheet.get_sprite(195, 153, 190,190),
            self.player_expl_sprite_sheet.get_sprite(387, 1, 284, 284),
            self.player_expl_sprite_sheet.get_sprite(673, 1, 120, 124),
            self.player_expl_sprite_sheet.get_sprite(673, 127, 133, 134),
            self.player_expl_sprite_sheet.get_sprite(1, 263, 138, 140),
            self.player_expl_sprite_sheet.get_sprite(387, 287, 143, 144),
        ]
        self.player_expl_lst = [pg.transform.scale(img, (img.get_rect().w, img.get_rect().h)) for img in self.player_expl_lst]

        self.brick_expl_sprite_sheet = SpriteSheet(path.join(img_dir, BRICK_EXPL_SPRITESHEET_NAME))
        self.brick_expl_lst = [
            self.brick_expl_sprite_sheet.get_sprite(1, 1, 192, 192),
            self.brick_expl_sprite_sheet.get_sprite(195, 1, 152, 150),
            self.brick_expl_sprite_sheet.get_sprite(195, 153, 82, 91),
            self.brick_expl_sprite_sheet.get_sprite(279, 153, 92, 102),
            self.brick_expl_sprite_sheet.get_sprite(1, 257, 120, 124),
            self.brick_expl_sprite_sheet.get_sprite(123, 257, 133, 134),
            self.brick_expl_sprite_sheet.get_sprite(258, 257, 138, 140),
            self.brick_expl_sprite_sheet.get_sprite(349, 1, 143, 144),
            self.brick_expl_sprite_sheet.get_sprite(398, 147, 149, 151)
        ]
        self.brick_expl_lst = [pg.transform.scale(img, (img.get_rect().w, img.get_rect().h)) for img in self.brick_expl_lst]


    def new(self):
        self.score = 0

        self.all_sprites = pg.sprite.Group()
        self.bricks = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.collectables = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.explosions = pg.sprite.Group()        

        self.initialize_bricks()
        Ball(self)

        # for i in range(2):
        #     Ball(self)

        self.player = Player(self)

        self.run()

    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.update()
            # self.auto_pilot()

    def update(self):
        self.events()
        self.all_sprites.update()
        self.draw()
        self.collide_manager()

        # GameOver Checks...
        if len(self.balls) <= 0:
            self.player.lives -= 1
            Ball(self)
            self.player.back_to_normal_size()

        if self.player.lives <= 0:
            self.playing = False

        # Winning Checks...
        if len(self.bricks) <= 0:
            self.playing = False

    def initialize_bricks(self):
        brick_x = 10
        brick_y = 50
        x_gap = 5 + BRICK_W
        y_gap = 5 + BRICK_H
        columns = 13
        rows = 8

        c = 0
        for i in range(columns * rows):
            if i in [29, 30, 42, 43] or i in [34, 35, 47, 48]:
                pass
            else:
                Brick(self, brick_x + (x_gap * (c)), brick_y)

            c += 1
            if c == columns:
                c = 0
                brick_y += y_gap

    def collide_manager(self):
        self.ball_collider()
        self.pow_collector()
        self.rock_collider()

    def ball_collider(self):
        dist = 20

        # Ball/Player
        hits = pg.sprite.spritecollide(self.player, self.balls, False)
        if hits:
            for ball in hits:
                ball.rect.bottom = self.player.rect.top

                # player&ball moving right
                if self.player.speedx > 0 and ball.speedx > 0:
                    ball.speedx *= 1.5
                    print("1")
                    if ball.speedx > 15:
                        ball.speedx = 15
                # player&ball moving left
                elif self.player.speedx < 0 and ball.speedx < 0:
                    ball.speedx *= 1.5
                    print("2")
                    if ball.speedx < -15:
                        ball.speedx = -15

                # player moving right & ball moving left
                elif self.player.speedx > 0 and ball.speedx < 0:
                    print("3")
                    ball.speedx *= -1

                # player moving left & ball moving right
                elif self.player.speedx < 0 and ball.speedx > 0:
                    print("4")
                    ball.speedx *= -1

                ball.speedy *= -1

        # Ball/Bricks...
        for ball in self.balls:
            hits = pg.sprite.spritecollide(ball, self.bricks, True)
            if hits:
                for hit in hits:
                    self.score += 31

                    ball_rect = ball.rect

                    # Ball top hits brick bottom...
                    if abs(ball_rect.top - hit.rect.bottom) < dist and ball.speedy <= 0:
                        ball.speedy *= -1
                    # Ball bottom hits brick top...
                    if abs(ball_rect.bottom - hit.rect.top) < dist and ball.speedy >= 0:
                        ball.speedy *= -1
                    # Ball left hits brick right...
                    if abs(ball_rect.left - hit.rect.right) < dist and ball.speedx <= 0:
                        ball.speedx *= -1
                    # Ball right hits brick left...
                    if abs(ball_rect.right - hit.rect.left) < dist and ball.speedx >= 0:
                        ball.speedx *= -1

                    # Drop a collectable...
                    if random.random() < COLLECTABLE_SPAWN_PCT:
                        Collectable(self, hit)

                    # Drop Rock...
                    if random.random() > ROCK_DROP_PCT:
                        Rock(self, hit)

                    Explosion(self, hit)

    def pow_collector(self):
        hits = pg.sprite.spritecollide(self.player, self.collectables, True)
        if hits:
            for hit in hits:
                if hit.collectable_type == "safety_line":
                    self.player.start_safety_line()
                elif hit.collectable_type == "multi_ball":
                    self.player.multi_ball()
                elif hit.collectable_type == "become_bigger":
                    self.player.become_bigger()
                elif hit.collectable_type == "become_smaller":
                    self.player.become_smaller()

    def rock_collider(self):
        hits = pg.sprite.spritecollide(self.player, self.rocks, True)
        if hits:
            hit = hits[0]
            self.player.lives -= 1
            Explosion(self, hit)
            hit.rect.x = WIDTH - 30
            hit.rect.y = 20
            Explosion(self, hit)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
                self.playing = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player.start_safety_line()
            #     if event.key == pg.K_UP:
            #         self.player.multi_ball()
            #     if event.key == pg.K_SPACE:
            #         for i in self.balls:
            #             i.speedx = 0
            #             i.speedy = 0

    def draw(self):
        pg.display.flip()
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_lives_score()

    def draw_text(self, txt, pos_x, pos_y, color=WHITE, size=18):
        font = pg.font.Font(self.font_file, size)
        font_surf = font.render(txt, True, color)
        font_rect = font_surf.get_rect(center=[pos_x, pos_y])
        self.screen.blit(font_surf, font_rect)

    def draw_lives_score(self):
        self.draw_text(f"Score: {self.score}", 65, 25, size=22)
        self.screen.blit(self.heart_img, (WIDTH - self.heart_img.get_rect().w - 10, 15))
        self.draw_text("x", WIDTH - self.heart_img.get_rect().w - 20, 25)
        self.draw_text(str(self.player.lives), WIDTH - self.heart_img.get_rect().w - 35, 25)

    # Auto-pilot function that follows balls based on distance
    # def auto_pilot(self):
    #     closest = list(self.balls)[0]
    #     for ball in self.balls:
    #         if ball.speedy > 0:
    #             if self.find_distance(self.player, closest) > self.find_distance(self.player, ball):
    #                 closest = ball
        # if self.player.rect.centerx < closest.rect.centerx:
        #     self.player.move_right()

        # if self.player.rect.centerx > closest.rect.centerx:
        #     self.player.move_left()

    # Auto-pilot function than follows the lowest ball
    def auto_pilot(self):
        # Follow balls if the safe_line isn't active
        # Follow Collectables if safe_line active
        
        if not self.player.safety_line_active:
            lowest = list(self.balls)[0]
            for ball in self.balls:
                if ball.speedy > 0:  # Make sure the lowest is going down..
                    if ball.rect.y > lowest.rect.y:
                        lowest = ball

            if self.player.rect.centerx + 10 < lowest.rect.centerx:
                self.player.move_right()

            if self.player.rect.centerx - 10 > lowest.rect.centerx:
                self.player.move_left()
        else:
            if len(self.collectables):
                for c in self.collectables:
                    lowest = list(self.collectables)[0]

                    if c.rect.y > lowest.rect.y:
                        lowest = c
                    if self.player.rect.centerx < lowest.rect.centerx:
                        self.player.move_right()
                    if self.player.rect.centerx > lowest.rect.centerx:
                        self.player.move_left()


    def find_distance(self, obj_1, obj_2):
        obj_1 = obj_1.rect
        obj_2 = obj_2.rect

        dist = math.sqrt((obj_1.x - obj_2.x) ** 2 + (obj_1.y - obj_2.y) ** 2)
        return dist

    def show_splash_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("BreakOut Game", WIDTH / 2, HEIGHT / 4, size=35)
        self.draw_text("Arrow keys to move right and left", WIDTH / 2, HEIGHT / 2, size=20)
        self.draw_text("Press Enter to Start", WIDTH / 2, HEIGHT - HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key_press()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("BreakOut Game", WIDTH / 2, HEIGHT / 4, size=38)
        self.draw_text("Game Over", WIDTH / 2, HEIGHT / 2, size=35)
        self.draw_text("Press Enter to play again", WIDTH / 2, HEIGHT - HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key_press()

    def wait_for_key_press(self):
        waiting = True

        while waiting:
            self.clock.tick(10)

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RETURN:
                        waiting = False


if __name__ == "__main__":
    g = Game()
    g.show_splash_screen()
    while g.running:
        g.new()
        if g.running:
            g.show_game_over_screen()
