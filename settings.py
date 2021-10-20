WIDTH, HEIGHT = 900, 675
FPS = 60
TITLE = "BreakOut"
FONT_NAME = "Arial"
SPRITESHEET_NAME = "Breakout_Tile_Free.png"
PLAYER_EXPL_SPRITESHEET_NAME = "player_expolision_spriteSheet.png"
BRICK_EXPL_SPRITESHEET_NAME = "brick_expolision_spriteSheet.png"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game Vars...
PLAYER_W, PLAYER_H = 100, 20
BRICK_W, BRICK_H = (63, 20)
BALL_SIZE = 20
COLLECTABLE_TYPES = ["multi_ball", "safety_line", 
					"become_bigger", "become_smaller",
                     ] 
# "glue_ball" "slower" "faster" "player_gun"
# glue-ball makes the ball stick to player
COLLECTABLE_SIZE = (80, 25)
COLLECTABLE_SPAWN_PCT = 0.1
ROCK_DROP_PCT = 0.5
