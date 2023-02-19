import pygame
from sys import exit
from random import randint, choice


# CONSTANTS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
MIN_Y_SPAWN = 100
MAX_Y_SPAWN = SCREEN_HEIGHT - 30
MAX_Y_MOVEMENT = 10
BALL_WIDTH = 10
BALL_HEIGHT = 10
VELOCITY = 5
BALL_SPAWN_INTERVAL = 2000


class Player(pygame.sprite.Sprite):
    def __init__(self, player_number):
        super().__init__()

        self.image = pygame.image.load("assets/graphics/player.jpg").convert()
        if player_number == 1:
            self.rect = self.image.get_rect(midleft=(0, SCREEN_HEIGHT//2))
        elif player_number == 2:
            self.rect = self.image.get_rect(midright=(SCREEN_WIDTH, SCREEN_HEIGHT//2))


class Ball(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()

        self.direction = direction

        self.image = pygame.image.load("assets/graphics/ball.jpg")
        self.image = pygame.transform.scale(self.image, (BALL_WIDTH, BALL_HEIGHT))
        self.image.fill("Yellow")
        self.rect = self.image.get_rect(center=(400, randint(MIN_Y_SPAWN, MAX_Y_SPAWN)))

        self.collide_sound = pygame.mixer.Sound("assets/audio/beep.mp3")
        self.collide_sound.set_volume(0.5)

    def movement(self):  # makes the ball go right or left depending on given direction
        if self.direction == "r":
            self.rect.x += VELOCITY
        if self.direction == "l":
            self.rect.x -= VELOCITY

    def collide(self):
        global player1_score, player2_score

        if pygame.sprite.spritecollide(self, player1, False):
            player1_score += 1
            self.collide_sound.play()
            self.direction = "r"
        if pygame.sprite.spritecollide(self, player2, False):
            player2_score += 1
            self.collide_sound.play()
            self.direction = "l"

    def out_of_screen(self) -> bool:
        if self.rect.right < -BALL_WIDTH or self.rect.left > SCREEN_WIDTH+BALL_WIDTH:
            return True
        return False

    def update(self):
        self.movement()
        self.collide()

        if self.out_of_screen():
            self.kill()


# Functions
def check_user_input(user_key_input):
    global game_active, player1_score, player2_score, start_time, player1, player2, ball_group, select_sound

    if not game_active and user_key_input == pygame.K_SPACE:
        select_sound.play()

        player1_score = 0
        player2_score = 0

        player1.sprite.rect.y = SCREEN_HEIGHT // 2
        player2.sprite.rect.y = SCREEN_HEIGHT // 2

        start_time = pygame.time.get_ticks()

        ball_group.empty()
        ball_group.add(Ball(direction=choice(["r", "l"])))

        game_active = True

    if game_active:
        # if user_key_input == pygame.K_s and player1.sprite.rect.top > MAX_Y_MOVEMENT:
        #     player1.sprite.rect.y -= MAX_Y_MOVEMENT
        # if user_key_input == pygame.K_x and player1.sprite.rect.bottom < SCREEN_HEIGHT-MAX_Y_MOVEMENT:
        #     player1.sprite.rect.y += MAX_Y_MOVEMENT
        # if user_key_input == pygame.K_j and player2.sprite.rect.top > MAX_Y_MOVEMENT:
        #     player2.sprite.rect.y -= MAX_Y_MOVEMENT
        # if user_key_input == pygame.K_n and player2.sprite.rect.bottom < SCREEN_HEIGHT-MAX_Y_MOVEMENT:
        #     player2.sprite.rect.y += MAX_Y_MOVEMENT
        if user_key_input == pygame.K_ESCAPE:
            select_sound.play()
            game_active = False
            ball_group.empty()


def display_time_scores():
    current_time = (pygame.time.get_ticks() - start_time)//1000
    time_surf = text_font.render(f"Time: {current_time}/30s", False, "White")
    time_rect = time_surf.get_rect(center=(SCREEN_WIDTH//2, 50))
    screen.blit(time_surf, time_rect)

    player1_score_surf = text_font.render(f"{player1_score}", False, "Blue")
    player1_score_rect = time_surf.get_rect(center=(200, 50))
    screen.blit(player1_score_surf, player1_score_rect)

    player2_score_surf = text_font.render(f"{player2_score}", False, "Red")
    player2_score_rect = time_surf.get_rect(center=(SCREEN_WIDTH-60, 50))
    screen.blit(player2_score_surf, player2_score_rect)

    return current_time


def display_winner():
    if player1_score > player2_score:
        winner = "Player 1"
    elif player2_score > player1_score:
        winner = "Player 2"
    else:
        winner = "No one"
    winner_surf = text_font.render(f"Winner: {winner}", False, "Gold")
    winner_rect = winner_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(winner_surf, winner_rect)


# Setup
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Pong but weird")
clock = pygame.time.Clock()
start_time = 0
first_time_on_menu = True
text_font = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)
game_active = False

# Audio
select_sound = pygame.mixer.Sound("assets/audio/select.mp3")
select_sound.set_volume(1)

# Scores
player1_score = 0
player2_score = 0

# Surfaces
menu_1 = pygame.image.load("assets/graphics/menu_1.png").convert()
menu_1 = pygame.transform.scale(menu_1, (800, 500))
menu_2 = pygame.image.load("assets/graphics/menu_2.png").convert()
menu_2 = pygame.transform.scale(menu_2, (800, 500))
menu = [menu_1, menu_2]
menu_index = 0

# Groups
player1 = pygame.sprite.GroupSingle()
player1.add(Player(player_number=1))

player2 = pygame.sprite.GroupSingle()
player2.add(Player(player_number=2))

ball_group = pygame.sprite.Group()

# Timers
ball_timer = pygame.USEREVENT
pygame.time.set_timer(ball_timer, BALL_SPAWN_INTERVAL)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            check_user_input(event.key)

        if game_active:
            if event.type == ball_timer:
                ball_group.add(Ball(direction=choice(["r", "l"])))

    if game_active:
        first_time_on_menu = False
        time = display_time_scores()
        if time >= 30:
            game_active = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and player1.sprite.rect.bottom > MIN_Y_SPAWN:
            player1.sprite.rect.y -= MAX_Y_MOVEMENT
        if keys[pygame.K_x] and player1.sprite.rect.top < MAX_Y_SPAWN:
            player1.sprite.rect.y += MAX_Y_MOVEMENT
        if keys[pygame.K_j] and player2.sprite.rect.bottom > MIN_Y_SPAWN:
            player2.sprite.rect.y -= MAX_Y_MOVEMENT
        if keys[pygame.K_n] and player2.sprite.rect.top < MAX_Y_SPAWN:
            player2.sprite.rect.y += MAX_Y_MOVEMENT

        # Background
        screen.fill("Black")

        # Players
        player1.draw(screen)
        player1.update()
        player2.draw(screen)
        player2.update()

        # Balls
        ball_group.draw(screen)
        ball_group.update()

        # Display time and scores
        display_time_scores()

    else:
        menu_index += 0.04
        if menu_index >= len(menu):
            menu_index = 0
        screen.blit(menu[int(menu_index)], (0, 0))

        if not first_time_on_menu:
            display_winner()

    pygame.display.update()
    clock.tick(60)
