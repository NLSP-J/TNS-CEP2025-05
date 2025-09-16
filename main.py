import pygame as pg
import random  # To generate random positions
import time
import asyncio

pg.init()
clock = pg.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

# Set window size
win_width = 1200
win_height = 400
screen = pg.display.set_mode([win_width, win_height])
pg.display.set_caption('UFO Challenge!')

# Load and scale the background image
background = pg.image.load('./assets/images/spacebg.png')
background = pg.transform.scale(background, (win_width, win_height))  # Scale to fit screen size

# Load and scale player images
player_image = pg.image.load('./assets/images/p1.png') 
player_image = pg.transform.scale(player_image, (40, 40))  # Player image scale
player_pos1 = [win_width / 4, win_height / 2]  # First player's starting position

# Second player images
player_image2 = pg.image.load('./assets/images/p2.png')
player_image2 = pg.transform.scale(player_image2, (40, 40))  # Second player image scale
player_pos2 = [win_width / 1.5, win_height / 2]  # Second player's starting position

# Load and scale the killer image
player_killer = pg.image.load('./assets/images/e1.png')
player_killer = pg.transform.scale(player_killer, (70, 70))  # Killer image scale

# Initialize game state variables
running = True
game_over = False
velocity1 = 0  # First player's velocity
velocity2 = 0  # Second player's velocity
x1, y1 = player_pos1[0], player_pos1[1]
x2, y2 = player_pos2[0], player_pos2[1]

# Variables for the player killers (falling at constant speed)
killer_fall_speed = 5  # Initial constant falling speed for the player killer
killer_on_ground = False  # Whether the killer has hit the ground or not

# Track screen crosses (number of times the players cross the screen from left to right)
cross_count = 0
killers = []  # List to hold all killer positions
killer_fall_speeds = []  # List for each killer's fall speed

# Add initial killer
killers.append([random.randint(0, win_width - 80), -80])  # Add a random killer starting position
killer_fall_speeds.append(killer_fall_speed)

# Score variable
score1 = 0
score2 = 0

# Set up font for score display
font = pg.font.Font(None, 40)

# Main game loop

async def main():

    global running, cross_count, game_over
    global x1, y1, velocity1, score1
    global x2, y2, velocity2, score2

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                # Player 1 controls
                if event.key == pg.K_UP or event.key == pg.K_SPACE:
                    velocity1 = -6  # Set jump velocity for player 1
                if event.key == pg.K_LEFT:
                    x1 -= 8  # Move player 1 left
                if event.key == pg.K_RIGHT:
                    x1 += 8  # Move player 1 right

                # Player 2 controls
                if event.key == pg.K_w:
                    velocity2 = -6  # Set jump velocity for player 2
                if event.key == pg.K_a:
                    x2 -= 8  # Move player 2 left
                if event.key == pg.K_d:
                    x2 += 8  # Move player 2 right

        # Player 1 movement
        x1 += 8  # Move player 1 to the right continuously
        y1 += velocity1  # Apply gravity or jump velocity for player 1

        # Player 2 movement
        x2 += 8  # Move player 2 to the right continuously
        y2 += velocity2  # Apply gravity or jump velocity for player 2

        # Wraparound for player 1 at right edge
        if x1 >= win_width:
            x1 = -40  # Wrap player 1 to the left side of the screen
            cross_count += 1  # Increment cross count when player 1 reaches the right side
            score1 += 1  # Increase score for player 1

        # Wraparound for player 2 at right edge
        if x2 >= win_width:
            x2 = -40  # Wrap player 2 to the left side of the screen
            cross_count += 1  # Increment cross count when player 2 reaches the right side
            score2 += 1  # Increase score for player 2

        # Simulate gravity effect for player 1
        if y1 < win_height - 60 and velocity1 < 6:
            velocity1 += 0.35  # Simulate gravity pulling player 1 down gradually
        elif y1 > win_height - 40:
            velocity1 = 0
            y1 = win_height - 40  # Stop player 1 at the ground level

        # Simulate gravity effect for player 2
        if y2 < win_height - 60 and velocity2 < 6:
            velocity2 += 0.35  # Simulate gravity pulling player 2 down gradually
        elif y2 > win_height - 40:
            velocity2 = 0
            y2 = win_height - 40  # Stop player 2 at the ground level

        # Add a new killer every 10 crosses and increase its fall speed
        if cross_count >= 10:  # For every 10 screen crosses, add a new killer
            killers.append([random.randint(0, win_width - 80), -80])  # Add new killer at a random x position
            killer_fall_speeds.append(killer_fall_speed)  # Initialize fall speed for the new killer
            cross_count = 0  # Reset cross count

        # Simulate the killer's constant falling speed for each killer
        for i in range(len(killers)):
            if killers[i][1] < win_height - 80:  # If the killer hasn't reached the ground yet
                killers[i][1] += killer_fall_speeds[i]  # Move the killer down at its own fall speed

                # Check if the killer hits the ground
                if killers[i][1] >= win_height - 80:  # Stop at the ground level
                    killers[i][1] = win_height - 80  # Position killer on the ground
            else:
                # Reposition the killer at a random x position and top of the screen
                killers[i][0] = random.randint(0, win_width - 80)
                killers[i][1] = -80  # Start the killer from the top again

                # Increase the fall speed of the killers as more are added
                if len(killers) > 1:  # If there are multiple killers, increase their fall speed
                    killer_fall_speeds[i] = min(killer_fall_speeds[i] + 0.2, 15)  # Limit max speed

        # Collision detection between both players and killers
        player1_rect = pg.Rect(x1, y1, 40, 40)  # Player 1's rectangle
        player2_rect = pg.Rect(x2, y2, 40, 40)  # Player 2's rectangle

        # Draw everything
        screen.blit(background, (0, 0))  # Draw the background first
        screen.blit(player_image, (x1, y1))  # Draw player 1
        screen.blit(player_image2, (x2, y2))  # Draw player 2

        # Draw all killers
        for killer_pos in killers:
            screen.blit(player_killer, (killer_pos[0], killer_pos[1]))  # Draw each killer

        for killer_pos in killers:
            killer_rect = pg.Rect(killer_pos[0], killer_pos[1], 80, 80)  # Killer's rectangle
            if player1_rect.colliderect(killer_rect) or player2_rect.colliderect(killer_rect):
                # Display the score and end the game
                score_text = font.render(f"Score: {score1} (Player 1) | {score2} (Player 2)", True, black)
                winner_text = ""
                if score1 > score2:
                    winner_text = font.render("Player 1 Wins!", True, black)
                elif score2 > score1:
                    winner_text = font.render("Player 2 Wins!", True, black)
                else:
                    winner_text = font.render("It's a Tie!", True, black)
                
                screen.blit(score_text, (win_width // 2 - score_text.get_width() // 2, win_height // 2 - 80))  # Display score
                screen.blit(winner_text, (win_width // 2 - winner_text.get_width() // 2, win_height // 2))  # Display winner
                pg.display.update()  # Update the screen
                time.sleep(2)  # Wait for 3 seconds to show the score and winner
                running = False  # End the game loop

        pg.display.update()  # Update the screen with new frame
        clock.tick(60)  # Run the game at 60 FPS
        await asyncio.sleep(0)

    pg.quit()  # Quit the game when done



asyncio.run(main())
