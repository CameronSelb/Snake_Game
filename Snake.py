from PIL import Image, ImageTk
import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

NUMBER_FRUIT = 2
NUMBER_BOMB = 4

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
#This will create a new window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

#this designs a canvas and adds it to the window, borderwidth = 0 and highlightthickness = 0 gets rid of the border
canvas = tkinter.Canvas(window, bg= "black", width= WINDOW_WIDTH, height= WINDOW_HEIGHT, borderwidth= 0, highlightthickness= 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #Single tile, snake head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
bombs = []
snake_body = [] #multiple snake tiles
food_amount = [food]
velocityX = 0
velocityY = 0
game_over = False
score = 0
time = 200

rot_snake_photo = Image.open("Images/Head.png")
snake_photo = ImageTk.PhotoImage(rot_snake_photo)
apple_photo = tkinter.PhotoImage(file= "Images/Apple.png")
bomb_photo = tkinter.PhotoImage(file= "Images/Bomb.png")

def key_input(e): #e = event
    global velocityX, velocityY, game_over, score, snake_body, food, snake, snake_photo, time, food_amount, bombs
    
    #Restarts the snake game if space bar is pressed
    if game_over:
        if e.keysym == "space":
            snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
            food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
            snake_photo = ImageTk.PhotoImage(rot_snake_photo)
            bombs = []
            snake_body = []
            food_amount = [food]
            velocityX = 0
            velocityY = 0
            game_over = False
            score = 0
            time = 200
        elif e.keysym == 'q':
            exit()
        return
    
    #Checks which direction you are travelling
    if (e.keysym == "w" and velocityY != 1):
       velocityX = 0
       velocityY = -1
       rotated_photo = rot_snake_photo.rotate(180)
       snake_photo = ImageTk.PhotoImage(rotated_photo)
    elif (e.keysym == "s" and velocityY != -1):
        velocityX = 0
        velocityY = 1 
        rotated_photo = rot_snake_photo.rotate(360)
        snake_photo = ImageTk.PhotoImage(rotated_photo)  
    elif (e.keysym == "a" and velocityX != 1):
        velocityX = -1
        velocityY = 0
        rotated_photo = rot_snake_photo.rotate(270)
        snake_photo = ImageTk.PhotoImage(rotated_photo)  
    elif (e.keysym == "d" and velocityX != -1):
        velocityX = 1
        velocityY = 0 
        rotated_photo = rot_snake_photo.rotate(90)
        snake_photo = ImageTk.PhotoImage(rotated_photo)

def random_coords():
    x = random.randint(0, COLS-1) * TILE_SIZE
    y = random.randint(0, ROWS-1) * TILE_SIZE
    return(x, y)

def bomb_activate(score):

    if score % 5 == 0 and score >= 20 and len(bombs) < NUMBER_BOMB:
        w, z = random_coords()
        bombs.append(Tile(w, z)) 
        print(bombs)

    if score % 5 == 0 and score > 20:
        for bomb in bombs:
            invalid = True
            while invalid:
                x, y = random_coords()
                invalid = False
                for tile in snake_body:
                    if tile.x == x and tile.y == y:
                        invalid = True
                        break
                for apple in food_amount:
                    if apple.x == x and apple.y == y:
                        invalid = True
                        break    
            bomb.x = x
            bomb.y = y

def score_change():
    global score, time, food_amount, bombs

    score += 1
    if score % 2 == 0:
        time -= 10
    if time < 100:
        time = 100

    #creates a new food every 10 points
    if score % 10 == 0 and score > 0 and len(food_amount) < NUMBER_FRUIT:
        x, y = random_coords()
        food_amount.append(Tile(x, y))

    bomb_activate(score)   


#Does the collision for the food
def collision(f):
    global snake_body, score

    snake_body.append(Tile(f.x, f.y))
    invalid = True
    while invalid:
        x, y = random_coords()
        invalid = False
        for tile in snake_body:
            if tile.x == x and tile.y == y:
                invalid = True
                break
            for bomb in bombs:
                if bomb.x == x and bomb.y == y:
                    invalid = True
                    break  
    
    score_change()
    return x, y        

def move():
    global snake, food, snake_body, game_over, food_amount, snake_photo

    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return        
    
    #Checks if snake hits bomb
    for bomb in bombs:
        if (snake.x == bomb.x and snake.y == bomb.y):
            snake_photo = tkinter.PhotoImage(file= "Images/Explosion.png")
            game_over = True
            return

    #checks if all the extra foods are not on top of each other
    for i, fo in enumerate(food_amount):
        if (snake.x == fo.x and snake.y == fo.y):
            x, y = collision(fo) 
            
            fo.x = x
            fo.y = y


    #collisions
    if (snake.x == food.x and snake.y == food.y):
        x, y = collision(food)

        food.x = x
        food.y = y    
        

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y   
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y 

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()
    
    canvas.delete("all")

    #draw food
    if len(food_amount) > 0:
        for foods in food_amount:
            canvas.create_image(foods.x + TILE_SIZE/2, foods.y + TILE_SIZE/2, image= apple_photo)      

    #creates the bomb
    if len(bombs) > 0:
        for bomb in bombs:
            canvas.create_image(bomb.x + TILE_SIZE/2, bomb.y + TILE_SIZE/2, image= bomb_photo)

    #creates the snake body
    for tile in snake_body:
        canvas.create_oval(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill= "lime green")

    #draw snake
    #canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill= "lime green") Draws snake head as just a lime square
    canvas.create_image(snake.x + TILE_SIZE/2, snake.y + TILE_SIZE/2, image= snake_photo) #Uses the provided image for snake head

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font= "Arial 20", text= f"Game Over: Score {score}", fill= "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 25, font= "Arial 10", text= "\nPress the SPACEBAR to restart or Q to quit", fill= "white")
    else:
        canvas.create_text(75, 20, font= "Arial 10", text= f"Score: {score} Speed: {time}ms", fill= "white")

    window.after(time, draw) #100ms = 1/10 second, 10 frames/second

draw()


#When you KeyRelease it takes the input from a key that has been pressed and released
window.bind("<KeyRelease>", key_input)
#this will opwn the window in a loop, until it is closed
window.mainloop()