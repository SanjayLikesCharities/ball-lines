
"""
This code recreates the game ball lines
This game can be found, e.g., here: http://www.sheppardsoftware.com/braingames/balllines/balllinesAS2.htm
Note that if n (the size of the GAMEBOARD) is >=10, then parts of the game might break. (fix this by finding instances of "int(BALL_TO_MOVE_INPUT[0])" and "int(BALL_TO_MOVE_INPUT[2])" adjust appropriately)
(one minor oddity: in the scenario where an incoming ball is going to arrive in the spot which would complete a 5-in-a-row...
... but the incoming ball is of a different colour from the others in the 5-in-a-row....
... and then the user completes the 5-in-a-row by moving a ball...
... then the eliminate_long_rows function will also delete out the incoming ball...
... whereas the original version on the website will leave the incoming ball there.)
"""


import numpy as np 

from random import randint
from random import random


n = 9                        # size of the GAMEBOARD. Assumed to be square. Assumed to be <10, although could tweak the code to relax that requirement
GAMEBOARD = [0]*n            # GAMEBOARD represented by this array (first row created and initialised to zero)
for i in range(n):
    GAMEBOARD[i] = [0]*n     # remaining rows initialised to 0


NO_OF_COLOURS = 4
NO_OF_INCOMING_BALLS = 5
TARGET_ROW_LENGTH = 5
SCORE = 0
#TARGET_SCORE = 1000          # used to use target score as a mechanism to decide when the game ends -- instead i'll use a count of the number of turns
MAX_NO_OF_TURNS = 100          # 

"""
For machine learning purposes, we need to keep a record of what happened over the course of the game...
... I'm doing this by storing it in a single vector/array called GAME_RECORD.
GAME_RECORD stores the state of the GAMEBOARD at each point when new balls are about to arrive on the board.
We do this by simply listing out each of the 81 cells of the board in order and adding them to GAME_RECORD in order
I've also created WEIGHTS1, which is a matrix to apply to the GAME_RECORD vector.
"""
GAME_RECORD = [0+0j]*((MAX_NO_OF_TURNS+2)*n*n)
GAME_RECORD_POSITION = 0
WEIGHTS1 = []


def update_game_record():
    
    global GAME_RECORD_POSITION
    
    for i in range(0,n):
        for k in range(0,n):
            GAME_RECORD[GAME_RECORD_POSITION] = GAMEBOARD[i][k] + 0j
            GAME_RECORD_POSITION += 1
    
#end of function

NO_OF_HIDDEN_NEURONS = 10







def initialise_gameboard():
    """
    this function assigns a 'colour' to a few randomly chosen cells within the GAMEBOARD
    a colour here is represented by an integer > 0
    it does not yet show the incoming balls
    """
    no_of_initial_balls = 4
    balls_placed = 0             # initialising this counter
        
    while balls_placed < no_of_initial_balls :
        x = randint(0,n-1)
        y = randint(0,n-1)
        if GAMEBOARD[x][y] == 0:
            GAMEBOARD[x][y] = randint(1,NO_OF_COLOURS)
            balls_placed +=1

    update_game_record()
    
#end of function

initialise_gameboard()


"""
This section of code was here for machine learning purposes,
but it seems to be slowing down the code,
so I'm commenting it out


def initialise_weights():
    
    global WEIGHTS1
    
    WEIGHTS1 = [0]*NO_OF_HIDDEN_NEURONS            
    for i in range(NO_OF_HIDDEN_NEURONS):
        WEIGHTS1[i] = [0]*((MAX_NO_OF_TURNS+2)*n*n)       # this is aligned with the length of the GAME_RECORD vector

    for i in range(0,NO_OF_HIDDEN_NEURONS):
        for j in range(0,(MAX_NO_OF_TURNS+2)*n*n):
            WEIGHTS1[i][j] = random()                     # this creates a matrix of size NO_OF_HIDDEN_NEURONS  by (MAX_NO_OF_TURNS+2)*n*n (or maybe that should be the other way round) which is populated with randomly generated weighting factors

#end of function

initialise_weights()

INTERIM_VECTOR = []

WEIGHTS1 = np.array(WEIGHTS1)
GAME_RECORD = np.array(GAME_RECORD)
INTERIM_VECTOR = np.array(INTERIM_VECTOR)

print("Here's the interim vector")
INTERIM_VECTOR = WEIGHTS1 @ GAME_RECORD
print(INTERIM_VECTOR)

"""

INCOMING_BALLS = []



## The idea behind this code is that we only want to continue running the game while there are empty spaces left
## This is for the while loop within which the bulk of the game occurs
NO_OF_EMPTY_SPACES_LEFT = 0
for i in range(0,n):
    for j in range(0,n):
        if GAMEBOARD[i][j] == 0:
            NO_OF_EMPTY_SPACES_LEFT += 1


print("WELCOME TO SANJAY'S VERSION OF BALL LINES")
GAME_METHOD = input("If you (the user) would like to play, type 'user'; if you would like the bot to play, type 'bot': ")
GAME_METHOD = GAME_METHOD.casefold()           # this changes the text to lower case (e.g. if someone enters "Bot" instead of "bot" the code will be forgiving)
while GAME_METHOD != "user" and GAME_METHOD != "bot":
    print("sorry, I didn't recognise your response, please try again")
    GAME_METHOD = input("If you (the user) would like to play, type 'user'; if you would like the bot to play, type 'bot': ")



NO_OF_TURNS = 0

while NO_OF_EMPTY_SPACES_LEFT>1:       # essentially the whole game happens inside this big while loop -- i.e. it ends when you run out of space on the board


    # I'm now hardcoding the GAMEBOARD (and overwriting the randomly assigned stuff from earlier) for debugging/testing purposes
    # IMPORTANT TO DELETE OR COMMENT THIS OUT if we want this to work properly
    # GAMEBOARD = [[3, 0, 0, 0, 0, 0, 0, 3, 0], [1, 4, 4, 0, 2, 2, 1, 3, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 3, 4, 1, 3, 3, 4, 2], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 1, 2, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 0]]
    # GAMEBOARD = [[0, 0, 0, 0, 0, 4, 0, 0, 2], [4, 0, 0, 0, 0, 0, 1, 0, 2], [4, 0, 0, 0, 0, 0, 0, 3, 0], [4, 2, 2, 0, 0, 0, 0, 0, 0], [4, 0, 2, 0, 3, 0, 0, 0, 1], [0, 0, 2, 3, 3, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 4, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 0, 3, 0, 0, 4]]
    # GAMEBOARD = [[0, 0, 0, 4, 1, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 4, 0, 4, 3, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 4, 1, 0, 0, 0], [4, 0, 0, 0, 0, 0, 1, 0, 0], [0, 3, 0, 0, 0, 0, 3, 1, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0]]

    def show_incoming_balls():
        """
        this function shows where the new incoming balls are going to be next turn, and their colour.
        it does this by assigning an imaginary number to the relevant cell in the array
        """
        global INCOMING_BALLS
        
        
        balls_placed = 0             # initialising this counter
        while balls_placed < min(NO_OF_INCOMING_BALLS, NO_OF_EMPTY_SPACES_LEFT) :            # Introducing the cap of No of Empty Spaces Left means that if the board is nearly full then we only add as many new balls as there is space for
            x = randint(0,n-1)                                 # generates a random integer between 0 and n-1 incl
            y = randint(0,n-1)                                 # generates a random integer between 0 and n-1 incl
            if GAMEBOARD[x][y] == 0:                           # checking that it's empty means we don't put an incoming ball where there is already a ball or where there is already an incoming ball expected
                GAMEBOARD[x][y] = randint(1,NO_OF_COLOURS)*1j  # python refers to sqrt(-1) as j
                INCOMING_BALLS.append([x,y])                   # This is keeping track of which cells contain the incoming balls, so when it comes to making them arrive they will be easy to find
                balls_placed +=1


        update_game_record()

        ### use this code for debugging purposes
##        GAMEBOARD[2][2] = 2j
##        GAMEBOARD[5][0] = 4j
##        GAMEBOARD[1][4] = 1j  # this is the one blocking the exit 
##        INCOMING_BALLS = [[2,2],[5,0],[1,4]]
    #end of show_incoming_balls function

    if NO_OF_TURNS == 0:             # variable initialisation only needed the first time round (thereafter the value is set towards the end of the while loop)
        NO_OF_ROWS_ELIMINATED = 0    # need to set this to zero at the start so that the next if statement can call the show_incoming_balls function
    if NO_OF_ROWS_ELIMINATED == 0:
        show_incoming_balls() # calling the function



    def print_nicely():
        print("This is the GAMEBOARD!!!!!!!!!!")
        i = 0
        while i < n:
            print(GAMEBOARD[i])
            i += 1
        print("Score:"+str(SCORE))


    print("Here's the gameboard:")
    print_nicely()


    # just initialising/"declaring" a few global variables which are about to used in the ask for ball to move and destination function
    BALL_TO_MOVE_INPUT = ""
    COLOUR_OF_BALL_BEING_MOVED = 0
    BALL_DESTINATION = ""
    
    def ask_for_ball_to_move_and_destination():
        """
        # this function asks the user which ball they want to move and where the ball should go
        # it also includes various checks on the sensibleness of what the user has inputted
        """
        # TO DO: need to add in verification that someone hasn't entered numbers that are outside of the GAMEBOARD
        # TO DO: need to add in verification that the co ordinates entered are for empty cell (for ball destination) -- note that flood fill takes care of this, so this isn't that important


        #NOTE -- IMPORTANT ASSUMPTION I've assumed that n doesn't get any larger than 10 -- if n>10, the above code breaks, shouldn't be hard to fix it so that doesn't happen, because it's just the simple fact that I'm assuming it's one digit long



        BALL_TO_MOVE_INPUT = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma (- enter just three characters | (0,0) is top left, count downwards to get your x value, and count to the right for y, so 8,0 would be the bottom left corner, and 8,8 would be the bottom right corner): ")    
        COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved
        print("The colour you've selected is "+ str(COLOUR_OF_BALL_BEING_MOVED))
        while COLOUR_OF_BALL_BEING_MOVED.real == 0:                 # this while loop checks that the user has made sensible choices
            if COLOUR_OF_BALL_BEING_MOVED == 0:                     # if the user has selected a cell where is actually no ball to move
                print("Sorry!!! -- you've selected an empty cell!")    # then inform the user
                BALL_TO_MOVE_INPUT = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left): ")    # ask the user to choose a different cell
                COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved
                print("The colour you've selected is "+ str(COLOUR_OF_BALL_BEING_MOVED))
            elif COLOUR_OF_BALL_BEING_MOVED.imag > 0:               # if the user has selected a cell where there is an incoming ball which hasn't arrived yet
                print("Sorry!!! -- this cell contains a ball which hasn't actually arrived on the board yet, so you can't move it")   # then inform the user
                BALL_TO_MOVE_INPUT = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left): ")    # ask the user to choose a different cell
                COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved
                print("The colour you've selected is "+ str(COLOUR_OF_BALL_BEING_MOVED))
        #end of while loop        

        BALL_DESTINATION = input("Give the x,y co-ordinates of the ball's destination, separated by a comma: ")
        


        return [BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION]

    # end of ask for ball to move and destination function

    def ball_to_move_and_destination_bot_random():
        """
        I created this function by taking a copy of ask_for_ball_to_move_and_destination
        I then updated it to automatically generate the BALL_TO_MOVE_INPUT variable and the BALL_DESTINATION variable
        At first it generates these at random
        """
        

        x = randint(0,n-1)
        y = randint(0,n-1)
        BALL_TO_MOVE_INPUT = str(x)+","+str(y)
        COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved
        while COLOUR_OF_BALL_BEING_MOVED.real == 0:                 # this while loop checks that the user has made sensible choices
            x = randint(0,n-1)
            y = randint(0,n-1)
            BALL_TO_MOVE_INPUT = str(x)+","+str(y)
            COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved        
        #end of while loop        

        x = randint(0,n-1)
        y = randint(0,n-1)
        BALL_DESTINATION = str(x)+","+str(y)
        colour_of_ball_destination = GAMEBOARD[int(BALL_DESTINATION[0])][int(BALL_DESTINATION[2])]  # I don't think this variable exists already, but we need to take note of this colour to check it is sensible. Looks like a local variable is fine for this, I don't think it will be needed outside of this function
        while colour_of_ball_destination.real > 0:                 # this while loop checks that the ball is going to an empty (or imaginary) cell
            x = randint(0,n-1)
            y = randint(0,n-1)
            BALL_DESTINATION = str(x)+","+str(y)
            colour_of_ball_destination = GAMEBOARD[int(BALL_DESTINATION[0])][int(BALL_DESTINATION[2])]
        #end of while loop
            
            
        
        print("ball to move input from RANDOM BOT = "+BALL_TO_MOVE_INPUT)
        print("colour of ball being moved from RANDOM BOT = "+str(COLOUR_OF_BALL_BEING_MOVED))
        print("ball destination from RANDOM BOT = "+BALL_DESTINATION)
        
        return [BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION]

    # end of function


    
    
    def identify_partial_long_rows():
        """
        Runs through all possible 5-in-a-row combinations (I say 5 -- could be any number)
        Identifies all the instances of a 5-in-a-row which are partially complete (i.e. they have 2 out of the 5, or 3 out of the 5, etc)
        
        """
    

        # each "long row" (i.e. row of the target length, e.g. each 5-in-a-row) is stored...
        # ... as a 3-tuple where the first element is the "first" position on the gameboard...
        # ... and the second element is a text string indicating the direction, i.e. "h", "v", "dtlbr", "dbltr"...
        # ... for horizontal, vertical, diagonal top left to bottom right, and diagonal bottom left to top right...
        # ... and the third element indicates the length of the row (is it a 5-in-a-row, or a 6-in-a-row, whatever)
        list_of_partial_long_rows = []
        colour = 0
        colour_counter = 0
        partial_row_length = 0
        temp_partial_row = []
        global TARGET_ROW_LENGTH   # i.e. if the game is to create 5 in a rows, then this number will be 5
        global NO_OF_COLOURS
        
        
        if TARGET_ROW_LENGTH > n:
            print("Error! The parameters have been set up wrong -- TARGET_ROW_LENGTH shouldn't be any larger than the size of the gameboard (n)")
                    
    
        # find all the HORIZONTAL partial target length rows
        for i in range(0,n):
            for j in range(0,n-TARGET_ROW_LENGTH+1):
                for colour in range(1,NO_OF_COLOURS+1):
                    # what the algorithm should do here is keep on looking until it finds "colour"
                    # the moment it finds "colour", look out for the possibility that...
                    # ...each cell from there until the next instance of "colour" consists only of zeros
                    for k in range(0,TARGET_ROW_LENGTH):
                        if GAMEBOARD[i][j+k] == colour:
                            temp_partial_row.append([i,j+k])
                            colour_counter += 1
                        
                    this_is_a_partial_row = False                     # setting this to false here means that if the number of colours in the block of 5 is <or= 1, then the row won't get added to the list of partial long rows
                    
                    if colour_counter > 1:                            # if there's more than 1 of that colour within the block of 5 cells being considered
                        this_is_a_partial_row = True                  # this variable is now going to be true unless we find an offending colour within the block of 5
                        imaginary_counter = 0
                        for k in range(0,TARGET_ROW_LENGTH):
                            if GAMEBOARD[i][j+k].real > 0 and GAMEBOARD[i][j+k] != colour:        # if we hit something within the block of 5 cells is neither empty nor is the desired colour...
                                this_is_a_partial_row = False                                     # ... then we don't count it as a partial row
                            if GAMEBOARD[i][j+k].imag > 0 and GAMEBOARD[i][j+k].imag != colour:   # the point of this is that if there are two or more incoming balls of the wrong colour, then we are screwed and can't make a 5-in-a-row
                                imaginary_counter +=1
                            if imaginary_counter >1:
                                this_is_a_partial_row = False
                            
                            
                        if this_is_a_partial_row:
                            list_of_partial_long_rows.append([i,j,temp_partial_row,"h",colour_counter,colour])        
                    
                    temp_partial_row=[]
                    colour_counter = 0
                    
    
        # find all the VERTICAL partial target length rows
        for j in range(0,n):
            for i in range(0,n-TARGET_ROW_LENGTH+1):
                for colour in range(1,NO_OF_COLOURS+1):
                    # what the algorithm should do here is keep on looking until it finds "colour"
                    # the moment it finds "colour", look out for the possibility that...
                    # ...each cell from there until the next instance of "colour" consists only of zeros
                    for k in range(0,TARGET_ROW_LENGTH):
                        if GAMEBOARD[i+k][j] == colour:
                            temp_partial_row.append([i+k,j])
                            colour_counter += 1
                        
                    this_is_a_partial_row = False                     # setting this to false here means that if the number of colours in the block of 5 is <or= 1, then the row won't get added to the list of partial long rows
                    
                    if colour_counter > 1:                            # if there's more than 1 of that colour within the block of 5 cells being considered
                        this_is_a_partial_row = True                  # this variable is now going to be true unless we find an offending colour within the block of 5
                        imaginary_counter = 0
                        for k in range(0,TARGET_ROW_LENGTH):
                            if GAMEBOARD[i+k][j].real > 0 and GAMEBOARD[i+k][j] != colour:        # if we hit something within the block of 5 cells is neither empty nor is the desired colour...
                                this_is_a_partial_row = False                                     # ... then we don't count it as a partial row
                            if GAMEBOARD[i+k][j].imag > 0 and GAMEBOARD[i+k][j].imag != colour:   # the point of this is that if there are two or more incoming balls of the wrong colour, then we are screwed and can't make a 5-in-a-row
                                imaginary_counter +=1
                            if imaginary_counter >1:
                                this_is_a_partial_row = False
                            
                            
                        if this_is_a_partial_row:
                            list_of_partial_long_rows.append([i,j,temp_partial_row,"v",colour_counter,colour])        
                    
                    temp_partial_row=[]
                    colour_counter = 0
                    
    
        # find all the DIAGONAL TOP LEFT TO BOTTOM RIGHT partial target length rows
        for i in range(0,n-TARGET_ROW_LENGTH+1):
            for j in range(0,n-TARGET_ROW_LENGTH+1):
                for colour in range(1,NO_OF_COLOURS+1):
                    # what the algorithm should do here is keep on looking until it finds "colour"
                    # the moment it finds "colour", look out for the possibility that...
                    # ...each cell from there until the next instance of "colour" consists only of zeros
                    for k in range(0,TARGET_ROW_LENGTH):
                        if GAMEBOARD[i+k][j+k] == colour:
                            temp_partial_row.append([i+k,j+k])
                            colour_counter += 1
                        
                    this_is_a_partial_row = False                     # setting this to false here means that if the number of colours in the block of 5 is <or= 1, then the row won't get added to the list of partial long rows
                    
                    if colour_counter > 1:                            # if there's more than 1 of that colour within the block of 5 cells being considered
                        this_is_a_partial_row = True                  # this variable is now going to be true unless we find an offending colour within the block of 5
                        imaginary_counter = 0
                        for k in range(0,TARGET_ROW_LENGTH):
                            if GAMEBOARD[i+k][j+k].real > 0 and GAMEBOARD[i+k][j+k] != colour:        # if we hit something within the block of 5 cells is neither empty nor is the desired colour...
                                this_is_a_partial_row = False                                     # ... then we don't count it as a partial row
                            if GAMEBOARD[i+k][j+k].imag > 0 and GAMEBOARD[i+k][j+k].imag != colour:   # the point of this is that if there are two or more incoming balls of the wrong colour, then we are screwed and can't make a 5-in-a-row
                                imaginary_counter +=1
                            if imaginary_counter >1:
                                this_is_a_partial_row = False
                            
                            
                        if this_is_a_partial_row:
                            list_of_partial_long_rows.append([i,j,temp_partial_row,"dtlbr",colour_counter,colour])        
                    
                    temp_partial_row=[]
                    colour_counter = 0
               
                               
        # find all the DIAGONAL BOTTOM LEFT TO TOP RIGHT partial target length rows
        for i in range(TARGET_ROW_LENGTH-1,n):
            for j in range(0,n-TARGET_ROW_LENGTH+1):
                for colour in range(1,NO_OF_COLOURS+1):
                    # what the algorithm should do here is keep on looking until it finds "colour"
                    # the moment it finds "colour", look out for the possibility that...
                    # ...each cell from there until the next instance of "colour" consists only of zeros
                    for k in range(0,TARGET_ROW_LENGTH):
                        if GAMEBOARD[i-k][j+k] == colour:
                            temp_partial_row.append([i-k,j+k])
                            colour_counter += 1
                        
                    this_is_a_partial_row = False                     # setting this to false here means that if the number of colours in the block of 5 is <or= 1, then the row won't get added to the list of partial long rows
                    
                    if colour_counter > 1:                            # if there's more than 1 of that colour within the block of 5 cells being considered
                        this_is_a_partial_row = True                  # this variable is now going to be true unless we find an offending colour within the block of 5
                        imaginary_counter = 0
                        for k in range(0,TARGET_ROW_LENGTH):
                            if GAMEBOARD[i-k][j+k].real > 0 and GAMEBOARD[i-k][j+k] != colour:        # if we hit something within the block of 5 cells is neither empty nor is the desired colour...
                                this_is_a_partial_row = False                                     # ... then we don't count it as a partial row
                            if GAMEBOARD[i-k][j+k].imag > 0 and GAMEBOARD[i-k][j+k].imag != colour:   # the point of this is that if there are two or more incoming balls of the wrong colour, then we are screwed and can't make a 5-in-a-row
                                imaginary_counter +=1
                            if imaginary_counter >1:
                                this_is_a_partial_row = False
                            
                            
                        if this_is_a_partial_row:
                            list_of_partial_long_rows.append([i,j,temp_partial_row,"dbltr",colour_counter,colour])        
                    
                    temp_partial_row=[]
                    colour_counter = 0
                    
    
        print("List of partial long rows using format [i,j,temp_partial_row,direction,colour_counter,colour]") # this is just here for debugging purposes
        for i in range(0,len(list_of_partial_long_rows)):
            print(list_of_partial_long_rows[i])              # this is just here for debugging purposes
        
        
        return list_of_partial_long_rows   
        
        # end of identify partial long rows function
    
    
    def identify_cells_with_colour(colour):
        """
        This code runs through the whole gameboard and puts all the cells with the chosen colour into a list
        and the function returns that list
        """
        
        cells_with_colour=[]
        
        for i in range(n):
            for j in range(n):
                if GAMEBOARD[i][j] == colour:
                    cells_with_colour.append([i,j])
        
        return cells_with_colour
        # end of identify_cells_with_colour(colour) function
    
    
    def ball_to_move_and_destination_bot(bot_method):
        """
        If bot_method == "normal", this bot works by
        (1) identifying all the partial long rows
        (2a) if there are none, then just pick a random ball and move it
        (2b) if there is at least one, pick one of those partial long rows at random
        (3) picking another ball of the same colour at random (which isn't in the partial long row) and send it into that partial long row
                
        If bot_method == "shuffle", this bot works by
        (1) identifying all the partial long rows
        (2a) if there are none, then just pick a random ball and move it
        (2b) if there is at least one, pick one of those partial long rows at random
        (3) pick a ball from within that partial long row and move it to another spot within the same partial long row (i.e. shuffle it)
        Note that the shuffle method is only expected to be used in situations where scenario (2a) (no partial long rows) won't apply
                
        """
        
        BALL_TO_MOVE_INPUT = "0,0"    # There were error messages complaining that this hadn't been assigned, so it's assigned now
        COLOUR_OF_BALL_BEING_MOVED = 0
        BALL_DESTINATION = "0,0"
        global TEMP
        
        list_of_partial_long_rows = identify_partial_long_rows()   # this calls the identify partial long rows function, which runs through the gameboard and identifies the "partial long rows" i.e. instances of 2 or 3 or 4 out of a possible 5 in a row
        
        if list_of_partial_long_rows == []:
            TEMP = ball_to_move_and_destination_bot_random()              # if there are no partial long rows, just choose a ball at random and move it to a random spot
            BALL_TO_MOVE_INPUT = TEMP[0]                           # this function returns these variables: BALL_TO_MOVE_INPUT, COLOUR_OF_BALL_BEING_MOVED, BALL_DESTINATION; so need to enter the output of the random bot into these variables so that it's available outside of this function
            COLOUR_OF_BALL_BEING_MOVED = TEMP[1]                   # this function returns these variables: BALL_TO_MOVE_INPUT, COLOUR_OF_BALL_BEING_MOVED, BALL_DESTINATION; so need to enter the output of the random bot into these variables so that it's available outside of this function
            BALL_DESTINATION = TEMP[2]                             # this function returns these variables: BALL_TO_MOVE_INPUT, COLOUR_OF_BALL_BEING_MOVED, BALL_DESTINATION; so need to enter the output of the random bot into these variables so that it's available outside of this function
        else:
            partial_long_row_targeted = randint(0,len(list_of_partial_long_rows)-1)           # choose a partial long row to target -- this is chosen at random
            colour_of_targeted_row = list_of_partial_long_rows[partial_long_row_targeted][5]  # assign the colour of that targeted partial long row to this variable colour_of_targeted_row
            cells_with_targeted_colour = identify_cells_with_colour(colour_of_targeted_row)   # uses the identify_cells_with_colour function to run through the gameboard and create a list of all the cells which have the same colour as the colour of the targeted row
            
            
            row_start_i = list_of_partial_long_rows[partial_long_row_targeted][0]  # just using this variable as a slightly shorter variable name to represent the i value of the start of this partial long row
            row_start_j = list_of_partial_long_rows[partial_long_row_targeted][1]  # just using this variable as a slightly shorter variable name to represent the j value of the start of this partial long row
            partial_row_direction = list_of_partial_long_rows[partial_long_row_targeted][3]  # this will be h,v, dtlbr or dtrbl
            temp_possible_destinations = []   # this will indicate which cells out of the 5 in a row are possible destinations
            temp_occupied_positions = []      # this will indicate which cells out of the 5 in a row already have a ball in them
            
            # The next section populates the temp_occupied_positions and temp_possible_destinations lists. We need to have very similar code repeated 4 times for each of the 4 directions
            
            # for HORIZONTAL: this bit of code runs through each of the cells in the selected 5-in-a-row and if it's empty (including if a ball is about to arrive) it puts it into temp_possible_destinations, and if it contains a ball, then that cell is stored in temp_occupied_positions
            if partial_row_direction == "h":
                for k in range(0,TARGET_ROW_LENGTH):
                    if GAMEBOARD[row_start_i][row_start_j+k].real == 0:
                        temp_possible_destinations.append([row_start_i,row_start_j+k])
                    elif GAMEBOARD[row_start_i][row_start_j+k] == colour_of_targeted_row:
                        temp_occupied_positions.append([row_start_i,row_start_j+k])
            
            # for VERTICAL: this bit of code runs through each of the cells in the selected 5-in-a-row and if it's empty (including if a ball is about to arrive) it puts it into temp_possible_destinations, and if it contains a ball, then that cell is stored in temp_occupied_positions
            if partial_row_direction == "v":
                for k in range(0,TARGET_ROW_LENGTH):
                    if GAMEBOARD[row_start_i+k][row_start_j].real == 0:
                        temp_possible_destinations.append([row_start_i+k,row_start_j])
                    elif GAMEBOARD[row_start_i+k][row_start_j] == colour_of_targeted_row:
                        temp_occupied_positions.append([row_start_i+k,row_start_j])
                        
            # for DIAGONAL TLBR: this bit of code runs through each of the cells in the selected 5-in-a-row and if it's empty (including if a ball is about to arrive) it puts it into temp_possible_destinations, and if it contains a ball, then that cell is stored in temp_occupied_positions
            if partial_row_direction == "dtlbr":     # diagonal top left to bottom right
                for k in range(0,TARGET_ROW_LENGTH):
                    if GAMEBOARD[row_start_i+k][row_start_j+k].real == 0:
                        temp_possible_destinations.append([row_start_i+k,row_start_j+k])
                    elif GAMEBOARD[row_start_i+k][row_start_j+k] == colour_of_targeted_row:
                        temp_occupied_positions.append([row_start_i+k,row_start_j+k])
            
            # for DIAGONAL BLTR: this bit of code runs through each of the cells in the selected 5-in-a-row and if it's empty (including if a ball is about to arrive) it puts it into temp_possible_destinations, and if it contains a ball, then that cell is stored in temp_occupied_positions
            if partial_row_direction == "dbltr":     # diagonal bottom left to top right
                for k in range(0,TARGET_ROW_LENGTH):
                    if GAMEBOARD[row_start_i-k][row_start_j+k].real == 0:
                        temp_possible_destinations.append([row_start_i-k,row_start_j+k])
                    elif GAMEBOARD[row_start_i-k][row_start_j+k] == colour_of_targeted_row:
                        temp_occupied_positions.append([row_start_i-k,row_start_j+k])
            
            
            
            # This section of code chooses the ball to be moved
            
            if len(cells_with_targeted_colour) == len(temp_occupied_positions):    # this is just to tackle an edge case: if there are no balls of the same colour as a partial long row (apart from the ones *in* the partial long row)
                print("The only balls have the desired colour are the ones in the partial long row, so I'm just calling the random bot here")
                TEMP = ball_to_move_and_destination_bot_random()                          # then just pick something at random (this is not the best solution, could try to improve this later)
    
            elif bot_method == "normal":
                # This section of code selects a ball by looking in the cells_with_targeted_colour list and choosing one which isn't in the targeted partial long row
                temp_ball_to_move = cells_with_targeted_colour[randint(0,len(cells_with_targeted_colour)-1)]   # randomly selects one of the sets of co-ordinates in the list cells_with_targeted_colour
                x = temp_ball_to_move[0]
                y = temp_ball_to_move[1]
                while [x,y] in temp_occupied_positions:                 # this while loop checks that the randomly chosen cell isn't in the partial long row
                    temp_ball_to_move = cells_with_targeted_colour[randint(0,len(cells_with_targeted_colour)-1)]
                    x = temp_ball_to_move[0]
                    y = temp_ball_to_move[1]
                #end of while loop                    
                BALL_TO_MOVE_INPUT = str(x)+","+str(y)
                COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved
                
                # This section of code chooses the destination
                position_in_long_row = randint(0,len(temp_possible_destinations)-1)  # this position_in_long_row variable is a randomly chosen position in the partial 5-in-a-row. I'll use it to select the ball destination
                x = temp_possible_destinations[position_in_long_row][0]
                y = temp_possible_destinations[position_in_long_row][1]
                BALL_DESTINATION = str(x)+","+str(y)
            elif bot_method == "shuffle":
                # This section of code chooses the destination as a random position in the chosen partial long row
                position_in_long_row = randint(0,len(temp_possible_destinations)-1)  # this position_in_long_row variable is a randomly chosen position in the partial 5-in-a-row. I'll use it to select the ball destination
                x = temp_possible_destinations[position_in_long_row][0]
                y = temp_possible_destinations[position_in_long_row][1]
                BALL_DESTINATION = str(x)+","+str(y)
                
                
                # This section of code chooses the ball to move
                # The ball to move is chosen as any ball adjacent (left, right, up, down) to the destination which has the right colour
                ball_to_move_found_yet = False                       # initialising this; the variable is here to tell us whether the shuffle method has found the ball to move yet
                if x > 0:                                            # if we're not right up at the top edge
                    if GAMEBOARD[x-1][y] == colour_of_targeted_row:  # if the ball immediately above the destination has the correct colour (note this probably means it's in the partial long row)
                        BALL_TO_MOVE_INPUT = str(x-1)+","+str(y)     # then move it to the destination
                        ball_to_move_found_yet = True                # and set this variable so we know whether we're done yet
                if x < n-1:                                          # if we're not right down at the bottom edge
                    if GAMEBOARD[x+1][y] == colour_of_targeted_row:  # if the ball immediately above the destination has the correct colour (note this probably means it's in the partial long row)
                        BALL_TO_MOVE_INPUT = str(x+1)+","+str(y)     # then move it to the destination
                        ball_to_move_found_yet = True                # and set this variable so we know whether we're done yet
                if y > 0:                                            # if we're not right over at the left edge
                    if GAMEBOARD[x][y-1] == colour_of_targeted_row:  # if the ball immediately to the left of the destination has the correct colour (note this probably means it's in the partial long row)
                        BALL_TO_MOVE_INPUT = str(x)+","+str(y-1)     # then move it to the destination
                        ball_to_move_found_yet = True                # and set this variable so we know whether we're done yet
                if y < n-1:                                          # if we're not right over at the right edge
                    if GAMEBOARD[x][y+1] == colour_of_targeted_row:  # if the ball immediately to the right of the destination has the correct colour (note this probably means it's in the partial long row)
                        BALL_TO_MOVE_INPUT = str(x)+","+str(y+1)     # then move it to the destination
                        ball_to_move_found_yet = True                # and set this variable so we know whether we're done yet
            
                if ball_to_move_found_yet == False:                  # if we've gone through all those four and none of them has had the right colour yet
                    if y > 0:                                        # then as long we're not right over the at the left-hand edge
                        if GAMEBOARD[x][y-1].real > 0:               # check that the cell immediately to the left contains a ball
                            BALL_TO_MOVE_INPUT = str(x)+","+str(y-1) # and if it does just take the ball immediately to the left of the chosen destination, whatever colour it is
                            ball_to_move_found_yet = True            # and set this variable so we know whether we're done yet
                    else:                                            # and if we are over at the left-hand edge
                        if GAMEBOARD[x][y+1].real > 0:               # check that the cell immediately to the right contains a ball
                            BALL_TO_MOVE_INPUT = str(x)+","+str(y+1) # and if it does just take the ball immediately to the right of the chosen destination, whatever colour it is
                            ball_to_move_found_yet = True            # and set this variable so we know whether we're done yet
                # note that we're mostly expecting to use the shuffle method in scenarios where the board is densely packed
                # however in case it's not densely packed, the backup plan is to use the random bot again
                if ball_to_move_found_yet == False:                  # if we've gone through all those four and none of them has had the right colour yet
                    TEMP = ball_to_move_and_destination_bot_random() # just choose a ball at random and move it to a random spot
                    BALL_TO_MOVE_INPUT = TEMP[0]                     # this function returns these variables: BALL_TO_MOVE_INPUT, COLOUR_OF_BALL_BEING_MOVED, BALL_DESTINATION; so need to enter the output of the random bot into these variables so that it's available outside of this function
                    COLOUR_OF_BALL_BEING_MOVED = TEMP[1]             # this function returns these variables: BALL_TO_MOVE_INPUT, COLOUR_OF_BALL_BEING_MOVED, BALL_DESTINATION; so need to enter the output of the random bot into these variables so that it's available outside of this function
                    BALL_DESTINATION = TEMP[2]                       # this function returns these variables: BALL_TO_MOVE_INPUT, COLOUR_OF_BALL_BEING_MOVED, BALL_DESTINATION; so need to enter the output of the random bot into these variables so that it's available outside of this function        
                
                COLOUR_OF_BALL_BEING_MOVED = GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] # note the colour of the ball moved
                
                
        
        if list_of_partial_long_rows == []:
            print("there are no partial long rows, so this is the random bot")
        else:
            print("partial long row targeted start at "+str(row_start_i)+","+str(row_start_j)+" and has direction "+str(partial_row_direction))
        print("ball to move input from bot = "+BALL_TO_MOVE_INPUT)
        print("colour of ball being moved from bot = "+str(COLOUR_OF_BALL_BEING_MOVED))
        print("ball destination from bot = "+BALL_DESTINATION)
            
        return [BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION]

    # end of ball_to_move_and_destination_bot() function

    
    
    TEMP = ["-",0,"-"]  # initialising this variable, which is here to capture the outputs of the ask_for_ball_to_move_and_dest function (notes: I first tried to treat those outputs (BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION) as global variables and use them outside fo the function, but that didn't work -- the code seemed to simply treat those variables as local, and so outside of the function they were back to being the empty string.
    
    if GAME_METHOD == "user":
        TEMP = ask_for_ball_to_move_and_destination() # this calls the function and stores BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION into the TEMP variable
    elif GAME_METHOD == "bot":
        TEMP = ball_to_move_and_destination_bot("normal") # this calls the function and stores BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION into the TEMP variable
    else:
        print("error: something's gone wrong, the GAME_METHOD variable doesn't seem to be right")
    
    
    BALL_TO_MOVE_INPUT = TEMP[0]
    COLOUR_OF_BALL_BEING_MOVED = TEMP[1]
    BALL_DESTINATION = TEMP[2]

    def flood_fill(initial_x, initial_y, destination_x, destination_y):

        # these initial_x and initial_y variables are used at the level of overall flood_fill function
        # they refer to the location of the ball being moved
        
        reachable_cells = []
        
        # the start point is included as a "reachable cell"
        reachable_cells.append([initial_x,initial_y])

        def check_neighbours(position):
            
            x = position[0]
            y = position[1]
            
            # CHECK TO THE LEFT
            if y>0:                                       # check first that we're not already at the leftmost edge of the board
                if(GAMEBOARD[x][y-1]==0 or GAMEBOARD[x][y-1].imag > 0):                 # if the cell to the left of the current position is empty
                    if(not [x,y-1] in reachable_cells):   # if the cell to the left of the current position is not already captured in the reachable_cells list
                        reachable_cells.append([x,y-1])   # then add it to the end of the reachable_cells list
            # CHCEK TO THE RIGHT
            if y<n-1:                                     # check first that we're not already at the rightmost edge of the board
                if(GAMEBOARD[x][y+1]==0 or GAMEBOARD[x][y+1].imag > 0):                 # if the cell to the right of the current position is empty
                    if(not [x,y+1] in reachable_cells):   # if the cell to the right of the current position is not already captured in the reachable_cells list
                        reachable_cells.append([x,y+1])   # then add it to the end of the reachable_cells list
            
            # CHECK ABOVE
            if x>0:                                       # check first that we're not already at the top of the board
                if(GAMEBOARD[x-1][y]==0 or GAMEBOARD[x-1][y].imag > 0):                 # if the cell above the current position is empty
                    if(not [x-1,y] in reachable_cells):   # if the cell above the current position is not already captured in the reachable_cells list
                        reachable_cells.append([x-1,y])   # then add it to the end of the reachable_cells list
            
            # CHECK BELOW
            if x<n-1:                                     # check first that we're not already at the bottom of the board
                if(GAMEBOARD[x+1][y]==0 or GAMEBOARD[x+1][y].imag > 0):                 # if the cell below the current position is empty
                    if(not [x+1,y] in reachable_cells):   # if the cell below the current position is not already captured in the reachable_cells list
                        reachable_cells.append([x+1,y])   # then add it to the end of the reachable_cells list

        
        #end of check_neighbours
        
        
        i = 0
        while i < len(reachable_cells):           # this makes sense because if the index is as big as the number of cells marked as reachable, it means that we've covered all the cells we can
            check_neighbours(reachable_cells[i])
            i += 1
        
        
        ### populating the reachable cells with a -1 can be useful for debugging -- just to see what's going on
##        for i in range(1,len(reachable_cells)):
##            GAMEBOARD[reachable_cells[i][0]][reachable_cells[i][1]] = -1
##        print("This is the gameboard as printed from within the floodfill subroutine")
##        print_nicely()
        
        return [destination_x, destination_y] in reachable_cells
        
        
    # end of flood fill function



    CAN_MOVE = flood_fill(int(BALL_TO_MOVE_INPUT[0]),int(BALL_TO_MOVE_INPUT[2]), int(BALL_DESTINATION[0]), int(BALL_DESTINATION[2])) # this line checks hwether there is a path from the ball to move to the destination. it uses the flood fill method to do this
    can_move_attempts_counter = 0     # this is to keep track of how many times someone has tried to move a ball but it's not worked because there's no path (a bot could get stuck in a loop trying it if there's no partial long row with another ball that can reach it
    
    while CAN_MOVE == False:
        print("Sorry!!! There is no path between the ball you want to move and that destination")
        
        TEMP = [0,0,0]  # initialising this variable, which is here to capture the outputs of the ask_for_ball_to_move_and_dest function (notes: I first tried to treat those outputs (BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION) as global variables and use them outside fo the function, but that didn't work -- the code seemed to simply treat those variables as local, and so outside of the function they were back to being the empty string.    
        if GAME_METHOD == "user":
            TEMP = ask_for_ball_to_move_and_destination() # this calls the function and stores BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION into the TEMP variable
        elif GAME_METHOD == "bot":
            TEMP = ball_to_move_and_destination_bot("normal") # this calls the function and stores BALL_TO_MOVE_INPUT,COLOUR_OF_BALL_BEING_MOVED,BALL_DESTINATION into the TEMP variable
        else:
            print("error: something's gone wrong, the GAME_METHOD variable doesn't seem to be right")
        
        BALL_TO_MOVE_INPUT = TEMP[0]
        COLOUR_OF_BALL_BEING_MOVED = TEMP[1]
        BALL_DESTINATION = TEMP[2]
        
        can_move_attempts_counter += 1
        if can_move_attempts_counter >= 50:
            print("There's been 50 attempts to move a ball from one spot to another without success, so a random move is going to be made now")
            TEMP = ball_to_move_and_destination_bot_random() # included this to avoid infinite loops
            BALL_TO_MOVE_INPUT = TEMP[0]
            COLOUR_OF_BALL_BEING_MOVED = TEMP[1]
            BALL_DESTINATION = TEMP[2]
            
            if can_move_attempts_counter >= 70:
                print("There's been 70 attempts to move a ball from one spot to another without success, so a shuffle-within-a-partial-long-row move is going to be made now")
                TEMP = ball_to_move_and_destination_bot("shuffle")
                BALL_TO_MOVE_INPUT = TEMP[0]
                COLOUR_OF_BALL_BEING_MOVED = TEMP[1]
                BALL_DESTINATION = TEMP[2]
        
        CAN_MOVE = flood_fill(int(BALL_TO_MOVE_INPUT[0]),int(BALL_TO_MOVE_INPUT[2]), int(BALL_DESTINATION[0]), int(BALL_DESTINATION[2]))
        
        
        
        #end of the "can_move" whileloop
        
        
    def make_incoming_balls_arrive():
        global INCOMING_BALLS
        for i in range(0,len(INCOMING_BALLS)):
            if not GAMEBOARD[INCOMING_BALLS[i][0]][INCOMING_BALLS[i][1]].imag == 0:                             # check that this is actually imaginary, if it isn't, it probably means that the user opted to move a ball to a spot where an incoming ball was expected
                GAMEBOARD[INCOMING_BALLS[i][0]][INCOMING_BALLS[i][1]] = int(GAMEBOARD[INCOMING_BALLS[i][0]][INCOMING_BALLS[i][1]].imag)     # This takes the imaginary part and converts it to an integer. I also tried multiplying by -1j, but then it treated it as a complex number, which looked ugly
                
        
        INCOMING_BALLS = []      # empty out this list ready for next time
        
        # the next bit is a belt-and-braces check -- hoepfully shouldn't be needed
        imaginary_balls_left = False
        for i in range(0,n):
            for j in range(0,n):
                if not GAMEBOARD[i][j].imag == 0:
                    imaginary_balls_left = True
        if imaginary_balls_left:
            print("Error! Apparently there are still incoming balls left, even though we're supposed to have made them all real now. Something funny is going on, investigate!")
            print_nicely()
        # this last section of code was a belt-and-braces check
    # end of make_incoming_balls_arrive function



    if CAN_MOVE:
        GAMEBOARD[int(BALL_TO_MOVE_INPUT[0])][int(BALL_TO_MOVE_INPUT[2])] = 0 # "lift" the ball off that cell of the GAMEBOARD by setting its value to zero
        GAMEBOARD[int(BALL_DESTINATION[0])][int(BALL_DESTINATION[2])] = COLOUR_OF_BALL_BEING_MOVED # "place" the ball in its rightful place
        # need to tweak this (her's some pseudocode)
        # if long rows eliminated, then go back and give the user the option to move another ball
        # else go on to the make_incoming_Balls_arrive step
        
    else:
        print("This message should never be seen. If you're seeing this, something funny is happening with the logic around the CAN_MOVE variable, so try to debug that.")


        
    # need to create something here to check if there's a row to delete, and then delete it
    
    # PSEUDO CODE FOR VARIANT 1
    
        # FOR I,J IN GAMEBOARD
            # IF GAMEBOARD[I][J] > 0
                # PUT THAT POSITION INTO A LIST OF NONZERO POSITIONS IN GAMEBOARD, MAKE SURE IT ONLY CAPTURES REAL BALLS, NOT IMAGINARY/INCOMING ONES
                
        # FOR EACH POSITION IN LIST OF NONZERO POSITIONS
            #CHECK EACH OF THE 8 ADJACENT POSITIONS CONTAINS A BALL OF THE SAME COLOUR, AND IF IT DOES...
                # ... THEN ADD IT TO A NEW ARRAY FOR 2-IN-A-ROW, CREATING A 2-TUPLE FOR EACH CONNECTED PAIR OF THE SAME COLOUR
                # POSSIBLY NEED TO KEEP TRACK OF THE DIRECTION OF THE CONNECTEDNESS, I GUESS? (i.E. IS IT HORIZONTAL, VERITCAL, OR DIAGONAL ONE WAY OR DIAGONAL THE OTHER WAY?)
        
        # FOR EACH 2-TUPLE IN LIST OF CONNECTED 2-TUPLES
            # CHECK IF IT'S PART OF A 3-IN-A-ROW, AND IF SO ADD IT TO A LIST OF CONNECTED 3-TUPLES
        
        # SIMILARLY FOR 4 IN A ROW AND 5 IN A ROW

    
    # PSEUDO CODE FOR VARIANT 2

        ## CHECK THE HORIZONTALS
        # FOR I IN RANGE(0,N):
            # FOR J IN RANGE (0,N-TARGET_ROW_LENGTH):
                # K = 0
                # WHILE K < TARGET_ROW_LENGTH: (OR SHOULD THIS SAY -1 AT THE END??)
                    # IF GAMEBOARD[I][J+K] == GAMEBOARD[I][J+K+1]
                        # K += 1
                    # ELSE
                        # BREAK
                # IF K == TARGET_ROW_LENGTH - 1 (OR SOME OTHER TEST OF WHETHER WE GOT THROUGH ALL 5 WITHOUT BREAKING THE WHILE LOOP)
                    # THEN CREATE A 5-TUPLE OF THE POSITIONS OF EACH OF THE 5 BALLS IN THE SUCCESSFUL ROW (WE TAKE A RECORD OF EACH ROW OF 5 NOW AND DELETE THEM LATER BECAUSE IF THERE WAS A SINGLE BALL WHICH CAUSED 2 5-IN-A-ROWS TO APPEAR AT ONCE, THEN BOTH OF THEM SHOULD DISAPPEAR)
        
        ## SIMILAR CHECKS FOR VERTICALS, AND THEN FOR TOPLEFT TO BOTTOM RIGHT DIAGONALS AND THE OTHER DIAGONALS
    
    # ADVANTAGE OF VARIANT 2 IS THAT THE TARGET ROW LENGTH OF 5 BECOMES AN EASY TO TWEAK VARIABLE
    
    
    def eliminate_long_rows():
        """
        Runs through all possible 5-in-a-row combinations (I say 5 -- could be any number)
        Stores a list of those which contain balls all of the same colour
        Goes through the list and sets those to zero (empty)
        This is also where the SCORE is updated
        """
    
        global SCORE

        # each "long row" (i.e. row of the target length, e.g. each 5-in-a-row) is stored...
        # ... as a 3-tuple where the first element is the "first" position on the gameboard...
        # ... and the second element is a text string indicating the direction, i.e. "h", "v", "dtlbr", "dbltr"...
        # ... for horizontal, vertical, diagonal top left to bottom right, and diagonal bottom left to top right...
        # ... and the third element indicates the length of the row (is it a 5-in-a-row, or a 6-in-a-row, whatever)
        list_of_long_rows = []          
        global TARGET_ROW_LENGTH
        length_to_eliminate = n # length_to_eliminate tracks what length of row we are eliminating -- so we'll start off by eliminating n-in-a-row (ie 9-in-a-row) and then work our way down
        
        if TARGET_ROW_LENGTH > n:
            print("Error! The parameters have been set up wrong -- TARGET_ROW_LENGTH shouldn't be any larger than the size of the gameboard (n)")
        
        while length_to_eliminate >= TARGET_ROW_LENGTH:      # the purpose of this while loop is to start off by eliminating the longest possible row and then work our way down
            
            # find all the HORIZONTAL target length rows
            for i in range(0,n):
                for j in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     
                        if GAMEBOARD[i][j+k] == GAMEBOARD[i][j+k+1] and GAMEBOARD[i][j+k] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"h",length_to_eliminate])        
        
            # find all the VERTICAL target length rows
            for j in range(0,n):
                for i in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     
                        if GAMEBOARD[i+k][j] == GAMEBOARD[i+k+1][j] and GAMEBOARD[i+k][j] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"v",length_to_eliminate])        
            
            
            # find all the DIAGONAL TOP LEFT TO BOTTOM RIGHT target length rows
            for i in range(0,n-length_to_eliminate+1):
                for j in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     
                        if GAMEBOARD[i+k][j+k] == GAMEBOARD[i+k+1][j+k+1] and GAMEBOARD[i+k][j+k] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"dtlbr",length_to_eliminate])        
            
            # find all the DIAGONAL BOTTOM LEFT TO TOP RIGHT target length rows
            for i in range(length_to_eliminate-1,n):
                for j in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     
                        if GAMEBOARD[i-k][j+k] == GAMEBOARD[i-k-1][j+k+1] and GAMEBOARD[i-k][j+k] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"dbltr",length_to_eliminate])        
            
            
            # now we go through and eliminate each of the 5-in-a-rows (or whatever length it is)
            for i in range(0,len(list_of_long_rows)):
                
                if list_of_long_rows[i][1] == "h":
                    for j in range(0,length_to_eliminate):
                        GAMEBOARD[list_of_long_rows[i][0][0]][list_of_long_rows[i][0][1]+j] = 0
                    
                elif list_of_long_rows[i][1] == "v":
                    for j in range(0,length_to_eliminate):
                        GAMEBOARD[list_of_long_rows[i][0][0]+j][list_of_long_rows[i][0][1]] = 0
                    
                elif list_of_long_rows[i][1] == "dtlbr":
                    for j in range(0,length_to_eliminate):
                        GAMEBOARD[list_of_long_rows[i][0][0]+j][list_of_long_rows[i][0][1]+j] = 0
                    
                elif list_of_long_rows[i][1] == "dbltr":
                    for j in range(0,length_to_eliminate):
                        GAMEBOARD[list_of_long_rows[i][0][0]-j][list_of_long_rows[i][0][1]+j] = 0
            
        
            length_to_eliminate = length_to_eliminate - 1
            #end of while loop
        
        for i in range(0,len(list_of_long_rows)):
            SCORE = SCORE + list_of_long_rows[i][2]*100   # this runs through everything in the list of "long rows" (i.e. lines long enough to be eliminated) and adds up the length of each, multiplied by 100
        
        return len(list_of_long_rows)
        # end of eliminate long rows function
    
    
    NO_OF_ROWS_ELIMINATED = 0 # initialising this variable, which will track whether we eliminated a row
    NO_OF_ROWS_ELIMINATED = eliminate_long_rows() # this calls the function, and sets the variable to the number of long rows eliminated. This will be used in the make_incoming_balls_real bit -- this shouldn't be called if one or more long rows have been eliminated
    
    
    if NO_OF_ROWS_ELIMINATED == 0:
        make_incoming_balls_arrive()
        eliminate_long_rows()        # we call this again, just to catch the scenario where an incoming ball happens to fall in the end of a 4-in-a-row
    
    print("This is an extra print after the imaginary balls have been made real and after eliminate_long_rows")
    print_nicely()

### The below applies if we're aiming for a target score, however I'm switching to a max number of turns instead
##    if SCORE >= TARGET_SCORE:
##        break
    
    if NO_OF_TURNS == MAX_NO_OF_TURNS:
        break

    
    NO_OF_EMPTY_SPACES_LEFT = 0
    for i in range(0,n):
        for j in range(0,n):
            if GAMEBOARD[i][j] == 0:
                NO_OF_EMPTY_SPACES_LEFT += 1
    
    if NO_OF_EMPTY_SPACES_LEFT == 1:
        print("GAME OVER!!! The gameboard has filled up and the game is over.")
##        print("This is what GAME_RECORD looks like")
##        print(GAME_RECORD)
        print("GAME_RECORD Array length = "+str(len(GAME_RECORD)))

    NO_OF_TURNS +=1
# end of big while loop


### The below applies if we're aiming for a target score, however I'm switching to a max number of turns instead
##if SCORE >= TARGET_SCORE:
##    print("Congratulations, you've won!")
##    print("This is what GAME_RECORD looks like")
##    print(GAME_RECORD)
##    print("Array length = "+str(len(GAME_RECORD)))
    
if NO_OF_EMPTY_SPACES_LEFT > 1:
    print("Congratulations, you've not been defeated!")
    print("Your score is "+str(SCORE))
##    print("This is what GAME_RECORD looks like")
##    print(GAME_RECORD)
    print("GAME_RECORD array length = "+str(len(GAME_RECORD)))


