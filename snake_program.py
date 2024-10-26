import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800,600
FPS = 60

#color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)


#Screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game by Denden")


#Snake
snake_width, snake_height  = 20, 20

#velocity of snake
vel = 2

#default direction
snake_dir = "right"
    
#apple
APPLE_WIDTH, APPLE_HEIGHT = 20, 20
apple_x_pos, apple_y_pos = 50, 40

apple = pygame.Rect(apple_x_pos, apple_y_pos, APPLE_WIDTH, APPLE_HEIGHT)

#Font
font = pygame.font.SysFont("comicsans", 24)

#line 
line = pygame.Rect(0, 35, WIDTH, 2)

def draw_screen(snake_segments, consumed_apple):
    global apple, line
    
    #Draw BG
    WIN.fill(BLACK)  
    
    #draw line
    pygame.draw.rect(WIN, WHITE, line)
    
    #Draw an apple which is an rect              
    pygame.draw.rect(WIN, RED, apple)
    
    
    #Snake THERE IS SOMETHING WRONG HERE
    dup_list = []
    for segment in snake_segments:
        pygame.draw.rect(WIN, GREEN, 
                        (segment[0], segment[1], snake_width, snake_height))
        #Deal when snake ate himself
        if segment in dup_list:
            pygame.quit()
        elif segment not in dup_list:
            dup_list.append(segment)
   
    #Display how many apple is consumed
    text = font.render(("Number of Consumed Apple: " + str(consumed_apple)), 
                       True, WHITE)
    textrect = pygame.Rect(10, 0, 50, 50)
    
    WIN.blit(text, textrect)
    
    pygame.display.update()
    
    
def make_apple():
    apple_x_pos = random.randrange(WIDTH - 20)
    apple_y_pos = random.randrange(36, HEIGHT - 20)
    return apple_x_pos, apple_y_pos 
  

#main
def main():
    global snake_dir
    clock = pygame.time.Clock()
    
    #intial x, y coordinate
    apple.x, apple.y  = make_apple()       
    
    #track how many apple is eaten
    consumed_apple = 0
    
    num_segments = 20 # change this to lengthen the snake body
    snake_segments = [(WIDTH//2, HEIGHT // 2)]
    
    running = True  
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != "down":
                    snake_dir = "up"
                elif event.key == pygame.K_DOWN and snake_dir != "up":
                    snake_dir = "down"
                elif event.key == pygame.K_RIGHT and snake_dir != "left":
                    snake_dir = "right"
                elif event.key == pygame.K_LEFT and snake_dir != "right":
                    snake_dir = "left"
                    
        #Acquire the coordinates of head of snake 
        #which is the first segment
        head_x, head_y = snake_segments[0]
        if snake_dir == "up":
            head_y -= vel
        elif snake_dir == "down":
            head_y += vel
        elif snake_dir == "right":
            head_x += vel
        elif snake_dir == "left":
            head_x -= vel

        # Insert new segment position
        snake_segments.insert(0, (head_x, head_y))
        
        
        #remove last segment so the snake is not infinitely long
        if len(snake_segments) > num_segments:
            snake_segments.pop() #remove the last element in the snake_segments
        
        #Exit if the snake hit the boundary
        if head_x < 1:
            break
        if head_y < line.y:
            break
        if head_x > WIDTH-1:
            break
        if head_y > HEIGHT-1:
            break
            
        #Handle collision
        #make head rect 
        head = pygame.Rect(head_x, head_y, snake_width, snake_height)
        
        if head.colliderect(apple):
            apple.x, apple.y = make_apple()
            consumed_apple += 1
            num_segments = num_segments + consumed_apple
            
        draw_screen(snake_segments, consumed_apple)
           
        clock.tick(FPS)
        
    pygame.quit()
    
if __name__ == "__main__":
    main()