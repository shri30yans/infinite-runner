import pygame
from random import randint 

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


def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.left -=5 
            
            # Obstacle is removed from the list, once it reaches screen bounds
            if obstacle_rect.left <= 0: 
                obstacle_rect_list.remove(obstacle_rect)
            screen.blit(obstacle_surface,obstacle_rect)

            # If collision takes place, return immediately
            game_active = collisions(obstacle_rect)
            if not(game_active):
                return game_active
        else:
            # If no collisions take place between any obstacle
            return True
    else:
        return True



def collisions(obstacle_rect):
    game_active = True
    # collision between rectangles
    if player_rect.colliderect(obstacle_rect):
        game_active = False
    
    return game_active


# Obstacle
obstacle_surface = pygame.image.load('graphics/obstacle/obstacle1.png').convert_alpha()
obstacle_rect = obstacle_surface.get_rect(bottomright = (1200,floor_y_axis)) # Create a rectangle around the image
obstacle_rect_list = []
# Player
player_surface = pygame.image.load('graphics/player.png').convert_alpha()

# Temp 
player_surface = pygame.transform.scale(player_surface,(40,40))


player_rect = player_surface.get_rect(midbottom = (80,floor_y_axis)) # Create a rectangle around the image

player_stand = pygame.image.load('graphics/player.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand,(150,150))
player_stand_scaled_rect = player_stand_scaled.get_rect(center = (500,200)) # Create a rectangle around the image


# Obstacle Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

test_font = pygame.font.Font('font/Robot Crush Italic.otf',50)

game_name_surface = test_font.render(f"infinte Runner",False,"Black")
game_name_rect = game_name_surface.get_rect(center = (500,50))


score = 0
player_gravity = 0
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
                    # Player lost and space is clicked. Start again.
                    obstacle_rect_list = [] 
                    start_time = int(pygame.time.get_ticks()//100) 
                    game_active = True

        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(obstacle_surface.get_rect(bottomright = (randint(1300,1500),floor_y_axis)))
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,floor_y_axis))

        # # Obstacle movement
        game_active = obstacle_movement(obstacle_rect_list)

        #Player
        player_gravity +=2
        player_rect.y += player_gravity
        if player_rect.bottom > floor_y_axis: 
            player_rect.bottom = 300 # create a floor
        screen.blit(player_surface,player_rect)

        score = display_score()
    else:
        # Start screen 
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
