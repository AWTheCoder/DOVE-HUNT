import pygame
import sys  # lets your program interact with the Python system
import random
import math

######## Timer & Systems (A) ######
pygame.init()
pygame.mixer.init()  # turns on pygame's sound system

# Window setup
WIDTH, HEIGHT = 900, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # create game window
pygame.display.set_caption("Dove Hunt")

# Audio Setup
# 1. Loading the sound effects
shoot_sound = pygame.mixer.Sound("sounds/gun_shot.mp3")  # loads a sound effect into memory
hit_sound = pygame.mixer.Sound("sounds/bird_shot.wav")
beep_sound = pygame.mixer.Sound("sounds/beep_sound.wav")

# 2. Loading the background music
pygame.mixer.music.load("sounds/rain_loop.wav")
pygame.mixer.music.play(-1)

# Load backdrop
try:
    backdrop = pygame.image.load("backdrop.png")
    BACKDROP = pygame.transform.scale(backdrop, (WIDTH, HEIGHT))
except pygame.error:
    print("Couldn't find backdrop.")
    sys.exit()

###### Game Logic (G+Y) ######
# Define the missing DOVE variable here and scale it to 60x60
try:
    dove_original = pygame.image.load("dove.png")  # Assumes you have a dove.png image
    DOVE = pygame.transform.scale(dove_original, (90, 90))  # Scales it down so it isn't massive
except pygame.error:
    # Fallback: Creates a white square if the dove is missing
    DOVE = pygame.Surface((60, 60), pygame.SRCALPHA)  # create backup image with transparent background
    DOVE.fill((255, 255, 255))
    print("Couldn't find dove.png, using a white square placeholder.")

clock = pygame.time.Clock()  # helps control how fast your game runs

###### UI & Scoreboard (Z) ######4
# Scoreboard Variables
player1_score = 0
player2_score = 0

# Timer Variables
game_time = 60
start_time = None  # no value assigned yet
last_beep_sound = -1

# Fonts
title_font = pygame.font.SysFont("Arial", 80, bold=True)

# Timer font
font = pygame.font.SysFont("Arial", 50)

# Smaller UI font
ui_font = pygame.font.SysFont("Arial", 28)

# Game States
show_instructions = True
show_difficulty_menu = False
game_over = False
running = True
score_saved = False
night_mode = False
show_leaderboard = False
muted = False

# Difficulty Settings
difficulty = None
DIFFICULTY_SETTINGS = {
    "easy": {
        "dove_speed": 4,
        "spawn_delay": 2000
    },
    "medium": {
        "dove_speed": 7,
        "spawn_delay": 1300
    },
    "hard": {
        "dove_speed": 10,
        "spawn_delay": 800
    }
}

###### Game Logic (G+Y) ######
# Dove Settings
dove_speed = 4
doves = []
spawn_timer = 0
spawn_delay = 2000
HITBOX_SIZE = 60

# Hit Effects
hit_effects = []

FALL_SPEED = 8
FLASH_TIME = 150

# Player Crosshair Settings
crosshair_speed = 7
crosshair_radius = 15

colour_options = [
    ("Red", (255, 50, 50)),
    ("Blue", (50, 150, 255)),
    ("Green", (50, 255, 50)),
    ("Yellow", (255, 255, 0)),
    ("Pink", (255, 100, 255)),
    ("White", (255, 255, 255))
]

p1_colour_index = 0
p2_colour_index = 1

# Player 1 (Red Crosshair)
p1_x, p1_y = 250, HEIGHT // 2
p1_color = colour_options[p1_colour_index][1]

# Player 2 (Blue Crosshair)
p2_x, p2_y = 650, HEIGHT // 2
p2_color = colour_options[p2_colour_index][1]


# Helper function to handle a shot hitting a dove
def check_shot(target_x, target_y, player_name):
    global player1_score, player2_score
    hit = False

    for dove in doves:

        # Smaller hitbox centred inside the 90x90 dove image
        dove_rect = pygame.Rect(
            dove["x"] + (90 - HITBOX_SIZE) // 2,
            dove["y"] + (90 - HITBOX_SIZE) // 2,
            HITBOX_SIZE,
            HITBOX_SIZE
        )

        if dove_rect.collidepoint(target_x, target_y):
            if not dove["hit"]:
                dove["hit"] = True
                dove["hit_time"] = pygame.time.get_ticks()  # return no. of millisecs since game started

                if player_name == "Player 1":
                    player1_score += 1
                    txt_color = p1_color
                elif player_name == "Player 2":
                    player2_score += 1
                    txt_color = p2_color

                # Add a new hit effect to "hit_effects" list when a dove's hit
                hit_effects.append({
                    "x": target_x,
                    "y": target_y,
                    "radius": 5,
                    "life": 15,
                    "color": txt_color
                })

                pygame.mixer.Sound.play(hit_sound)

                print(f"{player_name} Hit a Dove!")
                hit = True
            break


# Main Game Loop
while running:

    def save_score():
        if player1_score > player2_score:
            winner = "Player 1"
        elif player2_score > player1_score:
            winner = "Player 2"
        else:
            winner = "Draw"

        with open("leaderboard.txt", "a") as file:
            file.write(
                f"Player 1: {player1_score} |"
                f"Player 2: {player2_score} |"
                f"Winner: {winner}\n"
            )

    def load_scores():
        try:
            with open("leaderboard.txt", "r") as file:
                return file.readlines()
        except FileNotFoundError:
            return ["No scores yet."]


    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                p1_colour_index = (p1_colour_index + 1) % len(colour_options)
                p1_color = colour_options[p1_colour_index][1]

            if event.key == pygame.K_p:
                p2_colour_index = (p2_colour_index + 1) % len(colour_options)
                p2_color = colour_options[p2_colour_index][1]

            if event.key == pygame.K_m:
                muted = not muted

                if muted:
                    pygame.mixer.music.set_volume(0)
                    shoot_sound.set_volume(0)
                    hit_sound.set_volume(0)
                    beep_sound.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(1.0)
                    shoot_sound.set_volume(1.0)
                    hit_sound.set_volume(1.0)
                    beep_sound.set_volume(1.0)


        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player1_score = 0
                    player2_score = 0
                    game_over = False
                    show_instructions = True
                    show_difficulty_menu = False
                    difficulty = None
                    start_time = None
                    last_beep_sound = -1
                    score_saved = False

        # Start game with ENTER
        if show_instructions:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_instructions = False
                    show_difficulty_menu = True
                if event.key == pygame.K_l:
                    show_leaderboard = True
                    show_instructions = False

        if show_leaderboard:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_leaderboard = False
                    show_instructions = True

        # Difficulty choice inputs
        elif show_difficulty_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "easy"
                elif event.key == pygame.K_2:
                    difficulty = "medium"
                elif event.key == pygame.K_3:
                    difficulty = "hard"

                if difficulty:
                    dove_speed = DIFFICULTY_SETTINGS[difficulty]["dove_speed"]
                    spawn_delay = DIFFICULTY_SETTINGS[difficulty]["spawn_delay"]
                    show_difficulty_menu = False
                    # Start timer ONLY when game begins after selecting level
                    start_time = pygame.time.get_ticks()

        # Shooting inputs from the second loop
        if not show_instructions and not show_difficulty_menu and not show_leaderboard and not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    night_mode = not night_mode

                # Player 1 shoots with SPACE
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(shoot_sound)
                    check_shot(p1_x, p1_y, "Player 1")
                # Player 2 shoots with ENTER
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(shoot_sound)
                    check_shot(p2_x, p2_y, "Player 2")

    # Continuous keyboard input
    keys = pygame.key.get_pressed()

    if not game_over and not show_instructions and not show_difficulty_menu and not show_leaderboard:
        # Player 1 Movement (WASD)
        if keys[pygame.K_a]:
            p1_x -= crosshair_speed
        if keys[pygame.K_d]:
            p1_x += crosshair_speed
        if keys[pygame.K_w]:
            p1_y -= crosshair_speed
        if keys[pygame.K_s]:
            p1_y += crosshair_speed

        # Player 2 Movement (Arrow Keys)
        if keys[pygame.K_LEFT]:
            p2_x -= crosshair_speed
        if keys[pygame.K_RIGHT]:
            p2_x += crosshair_speed
        if keys[pygame.K_UP]:
            p2_y -= crosshair_speed
        if keys[pygame.K_DOWN]:
            p2_y += crosshair_speed

    # Keep crosshairs on screen
    p1_x = max(0, min(p1_x, WIDTH))
    p1_y = max(0, min(p1_y, HEIGHT))

    p2_x = max(0, min(p2_x, WIDTH))
    p2_y = max(0, min(p2_y, HEIGHT))

    # Spawn new doves
    if not show_instructions and not show_difficulty_menu and not show_leaderboard and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - spawn_timer > spawn_delay:
            for i in range(4):  # Spawn 4 doves each time
                doves.append({
                    "x": random.randint(50, WIDTH - 110),
                    "y": HEIGHT + random.randint(0, 150),
                    "hit": False,
                    "hit_time": 0
                })
            spawn_timer = current_time

    # Move doves
    if not show_instructions and not show_difficulty_menu and not show_leaderboard:
        for dove in doves[:]:
            if not dove["hit"]:
                dove["y"] -= dove_speed
                if dove["y"] + 60 < 0:
                    doves.remove(dove)
            else:
                dove["y"] += FALL_SPEED
                if dove["y"] > HEIGHT:
                    doves.remove(dove)

    # UPDATE HIT EFFECTS
    for effect in hit_effects[:]:
        effect["radius"] += 2
        effect["life"] -= 1
        if effect["life"] <= 0:
            hit_effects.remove(effect)

    ###### UI & Scoreboard (Z) ######
    # Drawing Section

    # Draw backdrop
    SCREEN.blit(BACKDROP, (0, 0))
    if night_mode:
        darkness = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        darkness.fill((0, 0, 60, 140))

        SCREEN.blit(darkness, (0, 0))

    # Instructions Screen
    if show_instructions:
        title_y = 150 + int(
            10 * math.sin(
                pygame.time.get_ticks() / 500
            )
        )

        title_shadow = title_font.render(
            "DOVE HUNT",
            True,
            (20, 20, 20)
        )

        title = title_font.render(
            "DOVE HUNT",
            True,
            (255, 215, 0)
        )

        p1 = ui_font.render(
            "Player 1: WASD + SPACE",
            True,
            (255, 255, 255)
        )

        p2 = ui_font.render(
            "Player 2: Arrow Keys + ENTER",
            True,
            (255, 255, 255)
        )
        p1_help = ui_font.render(
            "Q = Change P1 Colour",
            True,
            (255, 255, 0)
        )

        p2_help = ui_font.render(
            "P = Change P2 Colour",
            True,
            (255, 255, 0)
        )

        p1_colour_text = ui_font.render(
            f"P1 Colour: {colour_options[p1_colour_index][0]}",
            True,
            p1_color
        )

        p2_colour_text = ui_font.render(
            f"P2 Colour: {colour_options[p2_colour_index][0]}",
            True,
            p2_color
        )
        leaderboard_text = ui_font.render(
            "Press L for Leaderboard",
            True,
            (255, 215, 0)
        )

        start = ui_font.render(
            "[ENTER] Start Game",
            True,
            (255, 215, 0)
        )

        night_text = ui_font.render(
            f"Press N for Night Mode: {'ON' if night_mode else 'OFF'}",
            True,
            (255, 255, 255)
        )

        mute_text = ui_font.render(
            f"Press M to Mute: {'ON' if muted else 'OFF'}",
            True,
            (255,255,255)
        )

        SCREEN.blit(
            title_shadow,
            (
                WIDTH // 2 - title_shadow.get_width() // 2 + 4,
                title_y + 4
            )
        )

        SCREEN.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                title_y
            )
        )
        # Menu panel
        panel = pygame.Surface((500, 430), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 100))
        SCREEN.blit(panel, (180, 250))

        menu_x = 240

        SCREEN.blit(p1, (menu_x, 280))
        SCREEN.blit(p2, (menu_x, 320))

        SCREEN.blit(p1_help, (menu_x, 380))
        SCREEN.blit(p2_help, (menu_x, 420))

        SCREEN.blit(night_text, (menu_x, 460))
        SCREEN.blit(mute_text, (menu_x, 500))
        SCREEN.blit(leaderboard_text, (menu_x, 540))

        SCREEN.blit(p1_colour_text, (menu_x, 560))
        SCREEN.blit(p2_colour_text, (menu_x, 600))

        SCREEN.blit(start, (menu_x, 650))

    elif show_leaderboard:
        title = title_font.render("LEADERBOARD", True, (255, 215, 0))

        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        scores = load_scores()

        y = 180

        for score in scores[-10:]:
            score_text = ui_font.render(score.strip(), True, (255, 255, 255))

            SCREEN.blit(score_text, (80, y))

            y += 40

        back_text = ui_font.render(
            "ESC = Back",
            True,
            (255, 255, 0)
        )

        SCREEN.blit(
            back_text,
            (
                WIDTH // 2 - back_text.get_width() // 2,
                HEIGHT - 80
            )
        )

    # Difficulty Screen Display Choice
    elif show_difficulty_menu:
        title = title_font.render(
            "SELECT DIFFICULTY",
            True,
            (255, 255, 255)
        )

        easy = ui_font.render(
            "1 - EASY",
            True,
            (0, 255, 0)
        )

        medium = ui_font.render(
            "2 - MEDIUM",
            True,
            (255, 255, 0)
        )

        hard = ui_font.render(
            "3 - HARD",
            True,
            (255, 0, 0)
        )

        SCREEN.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 180)
        )

        SCREEN.blit(easy, (350, 300))
        SCREEN.blit(medium, (350, 360))
        SCREEN.blit(hard, (350, 420))

    else:

        # Timer Default Value
        time_left = 0

        # Timer
        if not game_over:
            # Only compute time if game has started and start_time exists
            if start_time is not None:
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                time_left = max(0, game_time - elapsed_time)

                ###### Timer & Systems (A) ######
                # beep once every second during last 10 seconds
                if 0 < time_left <= 10:
                    if time_left != last_beep_sound:
                        beep_sound.play()
                        last_beep_sound = time_left

                if time_left <= 0:
                    game_over = True
                    doves.clear()
                    if not score_saved:
                        save_score()
                        score_saved = True
        else:
            time_left = 0

        ###### UI & Scoreboard (Z) ######
        # Scoreboard Display
        p1_text = ui_font.render(
            f"Player 1: {player1_score}",
            True,
            (255, 255, 255)
        )

        p2_text = ui_font.render(
            f"Player 2: {player2_score}",
            True,
            (255, 255, 255)
        )

        ###### Timer & Systems (A) ######
        if time_left > 10:
            timer_colour = (255, 255, 255)  # white
        elif time_left > 5:
            timer_colour = (255, 255, 0)  # yellow
        else:
            timer_colour = (255, 0, 0)  # red

        ###### UI & Scoreboard (Z) ######
        timer_text = font.render(
            f"Time: {time_left}",
            True,
            timer_colour
        )

        # Player 1 Score
        SCREEN.blit(p1_text, (20, 20))

        # Player 2 Score
        SCREEN.blit(
            p2_text,
            (WIDTH - p2_text.get_width() - 20, 20)
        )

        # Timer
        SCREEN.blit(
            timer_text,
            (WIDTH // 2 - timer_text.get_width() // 2, 20)
        )

        ###### Timer & Systems (A) ######
        # Game Over Screen
        if game_over:
            if player1_score > player2_score:
                winner = "Player 1 Wins!"
            elif player2_score > player1_score:
                winner = "Player 2 Wins!"
            else:
                winner = "Draw!"

            ###### UI & Scoreboard (Z) ######
            game_over_shadow = title_font.render(
                "GAME OVER",
                True,
                (20, 20, 20)
            )

            game_over_text = title_font.render(
                "GAME OVER",
                True,
                (255, 50, 50)
            )

            winner_text = ui_font.render(
                winner,
                True,
                (255, 215, 0)
            )

            score1_text = ui_font.render(
                f"Player 1 Score: {player1_score}",
                True,
                (255, 255, 255)
            )

            score2_text = ui_font.render(
                f"Player 2 Score: {player2_score}",
                True,
                (255, 255, 255)
            )
            total_hits_text = ui_font.render(
                f"Total Doves Hit: {player1_score + player2_score}",
                True,
                (200, 200, 200)
            )

            ###### Timer & Systems (A) ######
            restart_text = ui_font.render(
                "Press R to Play Again",
                True,
                (255, 255, 0)
            )

            ###### UI & Scoreboard (Z) ######
            panel = pygame.Rect(
                WIDTH // 2 - 250,
                140,
                500,
                430
            )

            pygame.draw.rect(
                SCREEN,
                (25, 25, 25),
                panel,
                border_radius=20
            )

            pygame.draw.rect(
                SCREEN,
                (255, 215, 0),
                panel,
                4,
                border_radius=20
            )

            SCREEN.blit(
                game_over_shadow,
                (
                    WIDTH // 2 - game_over_shadow.get_width() // 2 + 4,
                    184
                )
            )

            SCREEN.blit(
                game_over_text,
                (
                    WIDTH // 2 - game_over_text.get_width() // 2,
                    180
                )
            )

            SCREEN.blit(
                score1_text,
                (
                    WIDTH // 2 - score1_text.get_width() // 2,
                    280
                )
            )

            SCREEN.blit(
                score2_text,
                (
                    WIDTH // 2 - score2_text.get_width() // 2,
                    330
                )
            )

            SCREEN.blit(
                total_hits_text,
                (
                    WIDTH // 2 - total_hits_text.get_width() // 2,
                    380
                )
            )

            SCREEN.blit(
                winner_text,
                (
                    WIDTH // 2 - winner_text.get_width() // 2,
                    410
                )
            )

            SCREEN.blit(
                restart_text,
                (
                    WIDTH // 2 - restart_text.get_width() // 2,
                    500
                )
            )

    ###### Game Logic (G+Y) ######
    # Draw Doves
    if not show_instructions and not show_difficulty_menu and not show_leaderboard:
        for dove in doves:
            if dove["hit"]:
                elapsed = pygame.time.get_ticks() - dove["hit_time"]
                if elapsed < FLASH_TIME:
                    flash = DOVE.copy()
                    red_overlay = pygame.Surface(
                        flash.get_size(),
                        pygame.SRCALPHA
                    )
                    red_overlay.fill((255, 0, 0, 120))
                    flash.blit(red_overlay, (0, 0))
                    SCREEN.blit(
                        flash,
                        (dove["x"], dove["y"])
                    )
                else:
                    SCREEN.blit(
                        DOVE,
                        (dove["x"], dove["y"])
                    )
            else:
                SCREEN.blit(
                    DOVE,
                    (dove["x"], dove["y"])
                )

    # Draw Hit Effects
    for effect in hit_effects:
        pygame.draw.circle(
            SCREEN,
            (255, 255, 0),
            (effect["x"], effect["y"]),
            effect["radius"],
            2
        )

        # --- 3. CREATE AND DRAW THE "+1" TEXT ---
        # Render the "+1" string into an image using the player's stored color
        plus_one_text = ui_font.render("+1", True, effect["color"])

        # Draw the text 20 pixels to the right and 20 pixels up from the hit location
        SCREEN.blit(plus_one_text, (effect["x"] + 20, effect["y"] - 20))

    # Draw Player 1 Crosshair (Red)
    if not show_instructions and not show_difficulty_menu and not show_leaderboard:
        pygame.draw.circle(
            SCREEN,
            p1_color,
            (p1_x, p1_y),
            crosshair_radius,
            2
        )

        pygame.draw.line(
            SCREEN,
            p1_color,
            (p1_x - 25, p1_y),
            (p1_x + 25, p1_y),
            2
        )

        pygame.draw.line(
            SCREEN,
            p1_color,
            (p1_x, p1_y - 25),
            (p1_x, p1_y + 25),
            2
        )

    # Draw Player 2 Crosshair (Blue)
    if not show_instructions and not show_difficulty_menu and not show_leaderboard:
        pygame.draw.circle(
            SCREEN,
            p2_color,
            (p2_x, p2_y),
            crosshair_radius,
            2
        )

        pygame.draw.line(
            SCREEN,
            p2_color,
            (p2_x - 25, p2_y),
            (p2_x + 25, p2_y),
            2
        )

        pygame.draw.line(
            SCREEN,
            p2_color,
            (p2_x, p2_y - 25),
            (p2_x, p2_y + 25),
            2
        )

    ###### Timer & Systems (A) ######
    # Update display
    pygame.display.flip()
    clock.tick(60)  # run game at max of 60 FPS (frames per sec)

pygame.quit()
sys.exit()