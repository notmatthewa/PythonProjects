# Snake in Python using Arrays
# V 1.0
# Created by Matt Anderson 10/19/2018
import threading
from threading import Thread
from multiprocessing import Process
from os import system, name 
import operator
import time
import sys
import keyboard
import random

# These arrays store the default stage. Changing these will change the background/walls
# Due to the way I wrote the code, Adding a character in this string will cause the 'points' 
# to no longer spawn there. Filling the board without any spaces will most likely cause an error 
# on the collection of the first point.
reset = [ 
    " -------------------",
    "|                   |",
    "|                   |",
    "|                   |",
    "|                   |",
    "|                   |",
    "|                   |",
    "|                   |",
    " -------------------"
    ]

# This is what the user sees when the game is ended.
# This is completely just for looks. Changing this will not affect the game in any way.
gameOver = [
    " --------------------------------------",
    "|              GAME  OVER              |",
    "|          THANKS FOR PLAYING!         |",
    "|                                      |",
    "|               q: QUIT                |",
    "|             r: RESTART               |",
    "|                                      |",
    "|     CREATED BY: MATTHEW ANDERSON     |",
    " --------------------------------------"
]

# Variable to store all the info of the game. The following are all of the settings
# ["HeadDisplayCharacter", "FacingDirection", "IsGameOver", "BodyDisplayCharacter", ["StartingPointX, StartingPointY"]]
setup = ["♥", [0, -1], False, "♦", [10, 2]]

# The ArrayList containing all the locations of the starting snake in [x, y] coordinates
snake = [[10, 4], [10, 5], [10, 6]]

# These are just the resets so that if one of the default array lists is changed, we have a backup
defaultSetup = setup.copy()
defaultSnake = snake.copy()

# clears the screen
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

# The main loop of the game. Once started, it runs until the "quit()" function is called
def MainLoop(threadname):
    
    # Declare that snake and setup are global variables and not local
    global snake
    global setup

    while True:
        # More variables
        hasTail = False
        matrix = reset.copy()
        clear()
        openSpaces = []
        
        # Add the point to the screen depending on location
        pointsList = list(matrix[setup[4][1]])
        pointsList[setup[4][0]] = "."
        matrix[setup[4][1]] = "".join(pointsList)

        # Generates a list of open spaces or empty " " characters in the matrix
        for e in range(1, len(matrix) - 1):
            y = matrix[e]
            for c in range(1, len(y) - 1):
                x = list(y)[c]
                if x == " ":
                    openSpaces += [[c, e]]
        
        # If the location of the snake's head is equal to the location of the point
        # hasTail tells the game to append a new tail section to the end of the snake
        if snake[0] == setup[4]:
            hasTail = True
            setup[4] = openSpaces[random.randint(0, len(openSpaces) - 1)]
        
        # Generates the new snake
        snake2 = [[snake[0][0] + setup[1][0], snake[0][1] + setup[1][1]]] + snake
        
        # If the snake has not colelcted a point, remove the last body block
        if not hasTail:
            
            snake2 = snake2[0:-1]
        snake = snake2

        # Run through every single body location of the snake
        for i in range(0, len(snake)):
            line = snake[i][1]
            col = snake[i][0]
            test = list(matrix[line])
            
            # Draw the body character or head character to the line
            if i == 0:
                test[col] = setup[0]
            else:
                test[col] = setup[3]
            
            # Join the line back together
            matrix[line] = "".join(test) 
            test = list(matrix[-1])

            # Just drawing the coordinates to the screen
            try:
                test[-5] = list(str(snake[0][0]))[1]
            except Exception:
                1
            
            # Drawing Coordinates
            test[-6] = list(str(snake[0][0]))[0]

            # Drawig Coordinates
            try:
                test[-2] = list(str(snake[0][1]))[1]
            except Exception:
                1
            test[-3] = list(str(snake[0][1]))[0]
            matrix[-1] = "".join(test)
            
            # Test for collisions using hard coded coordinates.
            # Might be better to test for character collision instead, however The game is a set size
            collide = False
            for y in range(0, len(snake)):
                if not y == i:
                    if snake[y] == snake[i]:
                        collide = True
            if snake[0][1] <= 0 or snake[0][1] >= 8 or snake[0][0] >= 20 or snake[0][0] <= 0 or collide == True:
                clear()
                print("\n".join(gameOver))
                setup[2] = True
                sys.exit()
        print("\n".join(matrix))

        # Delay the game being drawn
        time.sleep(0.4)

# This is the second loop of the game
# Ran in a different thread
# Excutes commands in the background and quicker than the main loop  
def SecondLoop(threadname):
    
    #Get Globals
    global setup
    global snake
    global defaultSetup
    global defaultSnake

    #Detect keyboard inputs to change directions
    while True:
        time.sleep(0.05)
        if keyboard.is_pressed('down'):
            setup[1] = [0, 1]
        if keyboard.is_pressed('up'):
            setup[1] = [0, -1]
        if keyboard.is_pressed('right'):
            setup[1] = [1, 0]
        if keyboard.is_pressed('left'):
            setup[1] = [-1, 0]

        # Detect keyboard inputs when the game is over to execute commands based on menu selection
        if keyboard.is_pressed('q') and setup[2]:
            sys.exit()
        if keyboard.is_pressed('r') and setup[2]:
            setup = defaultSetup.copy()
            snake = defaultSnake.copy()
            clear()

            #Restarts the main loop
            thread1 = Thread( target=MainLoop, args=("Thread-1",) )
            thread1.start()

# Used to multithread the code. Each loop running on it's own thread
if __name__ == '__main__':
    thread1 = Thread( target=MainLoop, args=("Thread-1",) )
    thread2 = Thread( target=SecondLoop, args=("Thread-2",) )

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()