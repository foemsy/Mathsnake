import pygame
import sys
import random 
import math

# pygame setup
screen_width = 1024
screen_height = 768
pygame.display.set_caption('Mathsnake')

pygame.init()

green = (0, 255, 0) # specify what is green
blue = (0, 0, 128) # specify what is blue
white = (255, 255, 255)
black = (0, 0, 0)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
color = (255,0,0) # snake colour
game_running = False # Main menu makes this true.

#Range of integers used for maths question
global range1, range2
range1 = 1
range2 = 9

global score # score gained by eating correct fruit. Global variable so it can be used in menu loop to display after the player has lost.
score = 0

# Snake Speed
xvelocity = 0
yvelocity = 0
speed = 0

snake_segments = [] # snake body is a list of coordinates.


# Position of all entities
x = 200 # Position of snake
y = 200 # IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!! Y- coordinates are inverted: y-5 is up, y+5 is down. 
width = 18 # Dimensions of snake. measured from bottom left
height = 18
#initial fruit positions
global incorrectfruit1x, incorrectfruit1y, incorrectfruit2x, incorrectfruit2y, correctfruitx, correctfruity # Global variables for fruit positions
incorrectfruit1x = random.randint(50, screen_width - 50) # fruits will not be at the edge of screen to make them easier to eat
incorrectfruit1y = random.randint(50, screen_height - 50)
incorrectfruit2x = random.randint(50, screen_width - 50)
incorrectfruit2y = random.randint(50, screen_height - 50)
correctfruitx = random.randint(50, screen_width - 50)
correctfruity = random.randint(50, screen_height - 50)


print(f" incorrectfruit1 position: {incorrectfruit1x}, {incorrectfruit1y}")
title_font = pygame.font.SysFont("arial", 64) # Title and button font for the main menu
button_font = pygame.font.SysFont("arial", 32)
menu_running = True # Menu Loop
while menu_running: # Main Menu
  # Define a function to draw a button with text
  def draw_button(x, y, width, height, color, text, text_color):
    # Draw a rectangle with the given color
    pygame.draw.rect(screen, color, (x, y, width, height))
    # Render the text with the given font and color
    text_surface = button_font.render(text, True, text_color)
    # Get the size and position of the text surface
    text_rect = text_surface.get_rect()
    # Center the text surface inside the button
    text_rect.center = (x + width // 2, y + height // 2)
    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect)

  # Define the position and size of the play button
  play_x = screen_width // 2 - 100
  play_y = screen_height // 2 - 50
  play_width = 200
  play_height = 100



  # Define a function to handle events
  def handle_events():
    global menu_running, game_running # Use the global variables menu_running and game_running
    # Loop through the events in the event queue
    for event in pygame.event.get():
      # If the user clicks the close button, quit the program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      # If the user clicks the mouse button
      if event.type == pygame.MOUSEBUTTONDOWN:
        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Check if the mouse position is inside the play button
        global incorrectfruit1x, incorrectfruit1y, incorrectfruit2x, incorrectfruit2y
        if play_x <= mouse_x <= play_x + play_width and play_y <= mouse_y <= play_y + play_height:
          if (x >= incorrectfruit1x-50 and x <= incorrectfruit1x+50) and (y >= incorrectfruit1y-50 and y <= incorrectfruit1y+50):#if fruit 1 spawns near snake
            print("Fruit spawned too close to snake! changing now...")
            incorrectfruit1x = random.randint(50, screen_width - 50) 
            incorrectfruit1y = random.randint(50, screen_height - 50)
          if (x >= incorrectfruit2x-50 and x <= incorrectfruit2x+50) and (y >= incorrectfruit2y-50 and y <= incorrectfruit2y+50): #if fruit 2 spawns near snake
            print("Fruit spawned too close to snake! changing now...")
            incorrectfruit2x = random.randint(50, screen_width - 50) 
            incorrectfruit2y = random.randint(50, screen_height - 50)

          # Set the menu_running variable to False
          menu_running = False
          # Set the game_running variable to True
          game_running = True
          # Print a message to the console
          print("Running the game...")

  # Define a function to update the screen
  def update_screen():
    # Fill the screen with blue
    screen.fill(black)
    # Render the title text with the title font and white color
    title_text = title_font.render("Mathsnake", True, white)
    # Get the size and position of the title text
    title_rect = title_text.get_rect()
    # Center the title text at the top of the screen
    title_rect.center = (screen_width // 2, 100)
    # Blit the title text onto the screen
    screen.blit(title_text, title_rect)
    # Draw the play button with green color and "Play" text
    draw_button(play_x, play_y, play_width, play_height, green, "Play", black)
    # Update the display
    pygame.display.update()

  # Call the handle_events function
  handle_events()

  # Call the update_screen function
  update_screen()

  # Tick the clock at 60 frames per second
  clock.tick(60)

correctfruiteaten = False # Initial conditions of fruit for game loop: it is placed in a random place, and it is not eaten.
fruit = pygame.draw.rect(screen, "red", (random.randint(0, screen_width), random.randint(0, screen_height), 40, 40)) 


def ymovement(y, yvelocity): # defining vertical/horizontal motion
  y -= yvelocity
  return y
def xmovement(x, xvelocity):
  x += xvelocity
  return x

font = pygame.font.Font(None, 36)




# Function to create a new math question
def new_math_question():
  global range1, range2
  num1 = random.randint(range1, range2)
  num2 = random.randint(range1, range2)
  question = f'{num1} + {num2} = ?'
  return question, num1 + num2

# Function to handle snake growth
def grow_snake(snake, x, y):
  global snake_segments
  growth = 20
  for times in range(growth):
    snake_segments.append(pygame.Rect(x, y, width, height))
  return snake_segments


# Function to draw fruits. Text also inside them
def draw_fruits():
  global incorrectfruit1x, incorrectfruit1y, incorrectfruit2x, incorrectfruit2y, correctfruitx, correctfruity,incorrectfruit1, incorrectfruit2, correctfruit, snake_segments #calling the assigned global variables from earlier and assigning additional new ones
  incorrectfruit1 = pygame.draw.rect(screen, color, (incorrectfruit1x, incorrectfruit1y, 18, 18))
  incorrectfruit2 = pygame.draw.rect(screen, color, (incorrectfruit2x, incorrectfruit2y, 18, 18))
  correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))
  
  if (incorrectfruit1x >= incorrectfruit2x-35 and incorrectfruit1x <= incorrectfruit2x + 35) and (incorrectfruit1y >= incorrectfruit2y-35 and incorrectfruit1y <= incorrectfruit2y+35):
    print("Fruit1 and fruit2 are too close! attempting to change now :-)")
    # re-roll random positions if two fruits are too close to each other
    incorrectfruit1x = random.randint(50, screen_width - 50) 
    incorrectfruit1y = random.randint(50, screen_height - 50)
    
    incorrectfruit1 = pygame.draw.rect(screen, color, (incorrectfruit1x, incorrectfruit1y, 18, 18))
    incorrectfruit2 = pygame.draw.rect(screen, color, (incorrectfruit2x, incorrectfruit2y, 18, 18))
    
    correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))
    
  elif (correctfruitx >= incorrectfruit1x -35  and correctfruitx <= incorrectfruit1x +35) and (correctfruity >= incorrectfruit1y-35 and correctfruity <= incorrectfruit1y+35): 
  # if the fruit is in the same position as the incorrect fruit 1, re-roll the position of the correct fruit
    print("Fruits detected in same position OMG!! attempting to change now :-)")
    
    correctfruitx = random.randint(50, screen_width - 50)
    correctfruity = random.randint(50,screen_height - 50)
    correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))
    
    incorrectfruit1 = pygame.draw.rect(screen, color, (incorrectfruit1x, incorrectfruit1y, 18, 18))
    incorrectfruit2 = pygame.draw.rect(screen, color, (incorrectfruit2x, incorrectfruit2y, 18, 18))
    
    correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))

  elif (correctfruitx >= incorrectfruit2x -35  and correctfruitx <= incorrectfruit2x +35) and (correctfruity >= incorrectfruit2y-35 and correctfruity <= incorrectfruit2y+35): # if the fruit is in the same position as the incorrect fruit 2, re-roll the position of the correct fruit
    print("Fruits detected in same position OMG!! attempting to change now :-)")

    correctfruitx = random.randint(50, screen_width - 50)
    correctfruity = random.randint(50,screen_height - 50)
    correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))
  
    incorrectfruit1 = pygame.draw.rect(screen, color, (incorrectfruit1x, incorrectfruit1y, 18, 18))
    incorrectfruit2 = pygame.draw.rect(screen, color, (incorrectfruit2x, incorrectfruit2y, 18, 18))
  
    correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))

  

        

global randint1, randint2 # global variables for the deviation from the correct answer
randint1 = random.randint(1, 3)
randint2 = random.randint(1, 3)

def draw_fruits_text():
  global randint1, randint2
  font = pygame.font.Font(None, 28)
  #fruit texts
  correctfruit_text = font.render(str(answer), True, (white))
  textrect = correctfruit_text.get_rect(center = (correctfruitx +7 , correctfruity + 9)) #tectrect for correct fruit
  
  incorrectfruit1_text = font.render(str(answer + randint1),True, white)
  tectrect2 = incorrectfruit1_text.get_rect(center = (incorrectfruit1x+9 , incorrectfruit1y + 9))# used 9 for each fruit to place text in centre of fruit (1/2 of 18 = 9)
  
  incorrectfruit2_text = font.render(str(answer - randint2),True, white)
  textrect3 = incorrectfruit2_text.get_rect(center = (incorrectfruit2x+9 , incorrectfruit2y + 9))
  
  screen.blit(correctfruit_text, textrect)
  screen.blit(incorrectfruit1_text, tectrect2)
  screen.blit(incorrectfruit2_text, textrect3)


  

  


# Function to render the question on the screen. includes the fruits and their answers
def draw_math_question(question):
  text = font.render(question, True, (white))
  text_rect = text.get_rect(center= (screen_width/2, screen_height/8))
  
  draw_fruits()
  draw_fruits_text()
  
  screen.blit(text, text_rect)
  pygame.display.flip()
  
question, answer = new_math_question()  # Get a new question. Question is the f-string from def new_math_question , answer is num1 + num2. If correct answer is chosen then run new_math_question() again.

def display_score():
  global score
  score_text = font.render(f"Score: {score}", True, (white))
  score_rect = score_text.get_rect(topleft=(10, 10))
  
  screen.blit(score_text, score_rect)





while game_running: # game loop
  keys = pygame.key.get_pressed() #needed to register key presses
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get(): # anything in here executes ONLY when an event happens: Key presses, cursor movement within the window.
    if event.type == pygame.QUIT:
      sys.exit()
    
  if yvelocity != (speed): 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: # if down or s key is pressed, move down constantly
        yvelocity = -(speed)
        xvelocity = 0
  if yvelocity != -(speed):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      yvelocity = speed
      xvelocity = 0
      
  if xvelocity != (speed): 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      yvelocity = 0
      xvelocity = -(speed)

  if xvelocity != -(speed):
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      yvelocity = 0
      xvelocity = speed
        
  y = ymovement(y,yvelocity)
  x = xmovement(x,xvelocity)

  
  # Game gets increasingly difficult as the snake grows.
  if score == 0:
    range1 = 1
    range2 = 9
    speed = 3 # Speed up once snake grows
  if score == 10:
    range1 = 5
    range2 = 13 # Number range widens as snake grows
    speed = 4
  if score == 25:
    range1 = 10
    range2 = 18
    speed = 5
  if score == 35:
    range1 = 15
    range2 = 25
    speed = 6
  if score == 45:
    range1 = 30
    range2 = 70
    speed = 8
  if score == 55:
    range1 = 50
    range2 = 100
    speed = 10
  if score == 65:
    range1 = 70
    range2 = 120
    speed = 12
  if score == 80:
    range1 = 100
    range2 = 150
    speed = 16
  if score == 100:
    range1 = 200
    range2 = 1000
    speed = 20

                             
  if x >= screen_width-18 or x <= 0 or y >= screen_height-18 or y <= 0: # because snake hitbox. if snake hits the edge of the screen, game ends.
    x = 200
    y = 200
    
    xvelocity = 0 # reset xvelocity and yvelocity when player loses. Ensures snake doesnt move offscreen
    yvelocity = 0
    
    snake_segments = [] #reset snake segment
    
    global previous_score
    previous_score = score
    score = 0 
    
    print(f"Your score was {previous_score}")
    
    print(f"Debug: score is now {score}")
    
    game_running = False
    menu_running = True
    
    print("You lost!")
  
    # fill the screen with a color to wipe away anything from last frame
  screen.fill(black)
  
  
    # -----------------RENDER GAME HERE------------------------
  snake = pygame.draw.rect(screen, color, (x,y,width,height)) #displays snake
  # Draw the snake segments on the screen
  for segment in snake_segments:
      pygame.draw.rect(screen, color, segment)
    
  for i in range(len(snake_segments) - 1, 0, -1):
    snake_segments[i].x = snake_segments[i - 1].x
    snake_segments[i].y = snake_segments[i - 1].y
    
  if len(snake_segments) > 0:
    snake_segments[0].x = x
    snake_segments[0].y = y
    
  display_score()
  
  draw_math_question(question) # displays math question, including fruits
  for segment in snake_segments[1:]:  # Start from index 1 to avoid checking collision with the head itself
    if x == segment.x and y == segment.y:  # Check if head collides with any segment
      print("Snake collided with itself! Game Over")
      snake_segments = []  # Reset the snake segments
      x = 200
      y = 200
      
      xvelocity = 0
      yvelocity = 0
      
      game_running = False
      menu_running = True
      
      previous_score = score
      score = 0
      
      print(f"Your score was {previous_score}")
 
  #Check for collision with fruits (fruit eaten)
  if pygame.Rect.colliderect(snake, incorrectfruit1) or pygame.Rect.colliderect(snake, incorrectfruit2):
    print("collision with incorrectfruit detected")
    snake_segments = []
    x = 200
    y = 200
    
    xvelocity = 0 # reset xvelocity and yvelocity when player loses. Ensures snake doesnt move offscreen
    yvelocity = 0
    
    game_running = False
    menu_running = True
    
    print("You lost!")
    
    previous_score = score #Store the previous score before losing the game
    score = 0
    
    print(f"Your score was {previous_score}")
    print(f"Debug: score is now {score}")
    
  

  
  elif pygame.Rect.colliderect(snake, correctfruit):
    print("collision with correctfruit detected")
    score = score + 1
    snake = grow_snake(snake, x, y)  # Grow the snake body
    
    incorrectfruit1x = random.randint(50, screen_width - 50) 
    incorrectfruit1y = random.randint(50, screen_height - 50)
    
    incorrectfruit2x = random.randint(50, screen_width - 50)
    incorrectfruit2y = random.randint(50, screen_height - 50)
    
    correctfruitx = random.randint(50, screen_width - 50)
    correctfruity = random.randint(50, screen_height - 50)
    question, answer = new_math_question()

    
    if (x >= incorrectfruit1x-50 and x <= incorrectfruit1x+50) and (y >= incorrectfruit1y-50 and y <= incorrectfruit1y+50):#if fruit 1 spawns near snake
      print("Fruit spawned too close to snake! changing now...")
      incorrectfruit1x = random.randint(50, screen_width - 50) 
      incorrectfruit1y = random.randint(50, screen_height - 50)


    
    if (x >= incorrectfruit2x-50 and x <= incorrectfruit2x+50) and (y >= incorrectfruit2y-50 and y <= incorrectfruit2y+50): #if fruit 2 spawns near snake
      print("Fruit spawned too close to snake! changing now...")
      incorrectfruit2x = random.randint(50, screen_width - 50) 
      incorrectfruit2y = random.randint(50, screen_height - 50)

      incorrectfruit1 = pygame.draw.rect(screen, color, (incorrectfruit1x, incorrectfruit1y, 18, 18))
      incorrectfruit2 = pygame.draw.rect(screen, color, (incorrectfruit2x, incorrectfruit2y, 18, 18))
      
      correctfruit = pygame.draw.rect(screen, color, (correctfruitx, correctfruity, 18, 18))
      
      incorrectfruit1x = random.randint(50, screen_width - 50) 
      incorrectfruit1y = random.randint(50, screen_height - 50)
    print("score: " + str(score))


    


  while menu_running: # Main Menu loop. modified to display the last played score.
    # Define a function to draw a button with text
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(str(score), True, (white))
    textrect = score_text.get_rect(center = (screen_width/2 , screen_height/2 + 80)) #display previous score
    screen.blit(score_text, textrect)



    
    def draw_button(x, y, width, height, color, text, text_color):
      # Draw a rectangle with the given color
      pygame.draw.rect(screen, color, (x, y, width, height))
      # Render the text with the given font and color
      text_surface = button_font.render(text, True, text_color)
      # Get the size and position of the text surface
      text_rect = text_surface.get_rect()
      # Center the text surface inside the button
      text_rect.center = (x + width // 2, y + height // 2)
      # Blit the text surface onto the screen
      screen.blit(text_surface, text_rect)

    # Define the position and size of the play button
    play_x = screen_width // 2 - 100
    play_y = screen_height // 2 - 50
    play_width = 200
    play_height = 100



    # Define a function to handle events
    def handle_events():
      global menu_running, game_running # Use the global variables menu_running and game_running
      # Loop through the events in the event queue
      for event in pygame.event.get():
        # If the user clicks the close button, quit the program
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        # If the user clicks the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
          # Get the mouse position
          mouse_x, mouse_y = pygame.mouse.get_pos()
          # Check if the mouse position is inside the play button
          if play_x <= mouse_x <= play_x + play_width and play_y <= mouse_y <= play_y + play_height:
            global incorrectfruit1x, incorrectfruit1y, incorrectfruit2x, incorrectfruit2y
            # Set the menu_running variable to False
            menu_running = False
            # Set the game_running variable to True
            game_running = True
            # Print a message to the console
            print("Running the game...")
          if (x >= incorrectfruit1x-50 and x <= incorrectfruit1x+50) and (y >= incorrectfruit1y-50 and y <= incorrectfruit1y+50):#if fruit 1 spawns near snake
            print("Fruit spawned too close to snake! changing now...")
            incorrectfruit1x = random.randint(50, screen_width - 50) 
            incorrectfruit1y = random.randint(50, screen_height - 50)
          if (x >= incorrectfruit2x-50 and x <= incorrectfruit2x+50) and (y >= incorrectfruit2y-50 and y <= incorrectfruit2y+50): #if fruit 2 spawns near snake
            print("Fruit spawned too close to snake! changing now...")
            incorrectfruit2x = random.randint(50, screen_width - 50) 
            incorrectfruit2y = random.randint(50, screen_height - 50)

    # Define a function to update the screen
    def update_screen():
      # Fill the screen with blue
      screen.fill(black)
      # Render the title text with the title font and white color
      title_text = title_font.render("Score: " + str(previous_score), True, white)
      # Get the size and position of the title text
      title_rect = title_text.get_rect()
      # Center the title text at the top of the screen
      title_rect.center = (screen_width // 2, 100)
      # Blit the title text onto the screen
      screen.blit(title_text, title_rect)
      # Draw the play button with green color and "Play" text
      draw_button(play_x, play_y, play_width, play_height, green, "Play again", black)
      # Update the display
      pygame.display.update()

    # Call the handle_events function
    handle_events()

    # Call the update_screen function
    update_screen()

    # Tick the clock at 60 frames per second
    clock.tick(60)


    # Define the position and size of the play button
    play_x = screen_width // 2 - 100
    play_y = screen_height // 2 - 50
    play_width = 200
    play_height = 100
                                                                                     
  
    # flip() the display to put your work on screen
  pygame.display.flip()

  clock.tick(60)  # limits FPS to 60. SHOULD be playable at 60fps but testing required
sys.exit()
  
