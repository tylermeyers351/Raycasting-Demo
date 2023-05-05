import pygame
import sys
import math

# Global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2 ##960
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE) ##60x60 tiles
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3 # in radians (around 60 degrees)
HALF_FOV = FOV / 2
CASTED_RAYS = 60
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

#Global variables
player_x = (SCREEN_WIDTH / 2) / 2
player_y =(SCREEN_WIDTH / 2) / 2
player_angle = math.pi
forward = True

# Map (8 x 8)
MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '#      #'
    '#   #  #'
    '#   #  #'
    '########'
)

# Initialize pygame, set up window, give title, and setup FPS
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting Demo")
clock = pygame.time.Clock()

# Draw map (left side of screen)
def draw_map():
    for row in range(8):
        for col in range(8):
            square = row * MAP_SIZE + col

            pygame.draw.rect(
                win, #draw on window
                (200, 200, 200) if MAP[square] == '#' else (100, 100, 100), #list comprehension for color
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2) # 
            )
    # Draw player on 2D board
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)

    # Draw player direction
    pygame.draw.line(win, (0,255,0), (player_x,player_y),
                     (player_x - math.sin(player_angle)*50, # Starting coordinates
                      player_y + math.cos(player_angle)*50), # End coordinates
                      3) 
    
    # Draw player FOV
    # Left-most ray cast
    pygame.draw.line(win, (0,255,0), (player_x,player_y),
                     (player_x - math.sin(player_angle - HALF_FOV)*50, # Starting coordinates
                      player_y + math.cos(player_angle - HALF_FOV)*50), # End coordinates
                      3)
    
    # Right_most ray cast
    pygame.draw.line(win, (0,255,0), (player_x,player_y),
                     (player_x - math.sin(player_angle + HALF_FOV)*50, # Starting coordinates
                      player_y + math.cos(player_angle + HALF_FOV)*50), # End coordinates
                      3)

# Raycasting algorithm 😱
def cast_rays():
    # Define left-most angle of FOV
    start_angle = player_angle - HALF_FOV

    # Loop over casted rays
    for ray in range(CASTED_RAYS):
        # Cast a single ray
        for depth in range(MAX_DEPTH):
            # Get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # Convert target X, Y coordinate to map col, row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            # Calculate map square index
            square = row * MAP_SIZE + col

            #
            if MAP[square] == '#':
                pygame.draw.rect(win, (0,255,0), (col*TILE_SIZE,
                                                  row*TILE_SIZE,
                                                  TILE_SIZE-2,
                                                  TILE_SIZE-2))
                # Draw casted ray
                pygame.draw.line(win, (255,255,0), (player_x,player_y),(target_x, target_y), 3)

                # Define shade based on depth
                color = 255 / (1 + depth * depth * 0.0001)

                # Fix fish-eye effect
                depth *= math.cos(player_angle - start_angle)
                
                # Calculate wall height
                wall_height = 21000 / (depth + 0.0001) # Avoid division by 0 error

                # Fix stuck at the wall
                if wall_height > SCREEN_HEIGHT: wall_height = SCREEN_HEIGHT

                # Draw 3D projection (rectangle by rectangle)
                pygame.draw.rect(win, (color,color,color), (
                    SCREEN_HEIGHT + ray * SCALE,
                    (SCREEN_HEIGHT / 2) - wall_height / 2,
                    SCALE,
                    wall_height))

                break

        # Increment angle by a single-step
        start_angle += STEP_ANGLE


# Moving dire

#####################
###               ###
### MAIN GAME LOOP###
###               ###
#####################

while True:
    # Logic to quit out of program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    ### COLLISION DETECTION FOR THE PLAYER (SO HE DOESN'T GO THROUGH WALLS)
    # Convert target X, Y coordinate to map col, row
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    # Calculate map square index
    square = row * MAP_SIZE + col
    # Player hits wall (collision)
    if MAP[square] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    # Update 2D background
    pygame.draw.rect(win, (0,0,0), (0,0,SCREEN_HEIGHT,SCREEN_HEIGHT))

    # Update 3D background
    pygame.draw.rect(win, (100,100,100), (480, SCREEN_HEIGHT/2,SCREEN_HEIGHT,SCREEN_HEIGHT))
    pygame.draw.rect(win, (200,200,200), (480, -SCREEN_HEIGHT/2,SCREEN_HEIGHT,SCREEN_HEIGHT))

    # Draw 2d map
    draw_map()

    # Call raycasting function
    cast_rays()

    # Get user Input
    keys = pygame.key.get_pressed()

    # Handle user input
    if keys[pygame.K_LEFT]: player_angle -= 0.1 #radians
    if keys[pygame.K_RIGHT]: player_angle += 0.1 #radians
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5
        forward = False

    # Set FPS
    clock.tick(30)

    # Get FPS
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    fps_surface = font.render('FPS: ' + fps, False, (255,255,255))
    win.blit(fps_surface, (480, 0))

    # Update display
    pygame.display.flip()