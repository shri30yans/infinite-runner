import pygame

pygame.init()
screen = pygame.display.set_mode((1000,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()


floor_y_axis = 300

# Background
sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# Score
def display_score():
    test_font = pygame.font.Font('font/Robot Crush Italic.otf',20)
    score = int(pygame.time.get_ticks()//100)-start_time
    score_surface = test_font.render(f"Score: {score}",False,"Black")
    score_rect = score_surface.get_rect(center = (900,30))
    screen.blit(score_surface,score_rect)
    return score


# Obstacle
obstacle_surface = pygame.image.load('graphics/obstacle/obstacle1.png').convert_alpha()
obstacle_rect = obstacle_surface.get_rect(bottomright = (1200,floor_y_axis)) # Create a rectangle around the image

# Player
player_surface = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,floor_y_axis)) # Create a rectangle around the image

player_stand = pygame.image.load('graphics/player.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand,(150,150))
player_stand_scaled_rect = player_stand_scaled.get_rect(center = (500,200)) # Create a rectangle around the image

player_gravity = 0

test_font = pygame.font.Font('font/Robot Crush Italic.otf',50)

game_name_surface = test_font.render(f"infinte Runner",False,"Black")
game_name_rect = game_name_surface.get_rect(center = (500,50))

score = 0
game_active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    if player_rect.bottom == floor_y_axis: # player is on the floor, jump
                        player_gravity = -25
                else:
                    # player lost, start again
                    obstacle_rect.left = 1200 # bring obstacle to original position
                    start_time = int(pygame.time.get_ticks()//100) 
                    game_active = True
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,floor_y_axis))

        # Obstacles
        obstacle_rect.left -=5 # obstacle doesn't continue beyond screen bounds
        if obstacle_rect.left <= 0: 
            obstacle_rect.left = 1200
        screen.blit(obstacle_surface,obstacle_rect)

        #Player
        player_gravity +=2
        player_rect.y += player_gravity
        if player_rect.bottom > floor_y_axis: 
            player_rect.bottom = 300 # create a floor
        screen.blit(player_surface,player_rect)

        # collision between rectangles
        if player_rect.colliderect(obstacle_rect):
            game_active = False

        score = display_score()
    else:
        screen.fill((175, 238, 238))
        screen.blit(player_stand_scaled,player_stand_scaled_rect)
        screen.blit(game_name_surface,game_name_rect)
        if score == 0:
            game_message_surface = test_font.render(f"Press Space to run.",False,"Black")
        else:
            game_message_surface = test_font.render(f"Your score: {score}",False,"Black")
        game_message_rect = game_message_surface.get_rect(center = (500,350))
        screen.blit(game_message_surface,game_message_rect)



    pygame.display.update() 
    clock.tick(60) # set maximum framerate 
