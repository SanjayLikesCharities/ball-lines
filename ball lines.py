
"""
This code recreates the game ball lines
This game can be found, e.g., here: http://www.sheppardsoftware.com/braingames/balllines/balllinesAS2.htm
Note that if n (the size of the GAMEBOARD) is >=10, then parts of the game might break. (fix this by finding instances of "int(ball_to_move_input[0])" and "int(ball_to_move_input[2])" adjust appropriately)
"""



from random import randint


n = 9                        # size of the GAMEBOARD. Assumed to be square. Assumed to be <10, although could tweak the code to relax that requirement
GAMEBOARD = [0]*n            # GAMEBOARD represented by this array (first row created and initialised to zero)
for i in range(n):
    GAMEBOARD[i] = [0]*n     # remaining rows initialised to 0


NO_OF_COLOURS = 4
NO_OF_INCOMING_BALLS = 3
TARGET_ROW_LENGTH = 5

def initialise_gameboard():
    """
    this function assigns a 'colour' to a few randomly chosen cells within the GAMEBOARD
    a colour here is represented by an integer > 0
    it does not yet show the incoming balls
    """
    no_of_initial_balls = 5
    balls_placed = 0             # initialising this counter
    while balls_placed < no_of_initial_balls :
        x = randint(0,8)
        y = randint(0,8)
        if GAMEBOARD[x][y] == 0:
            GAMEBOARD[x][y] = randint(1,NO_OF_COLOURS)
            balls_placed +=1
#end of function

initialise_gameboard()

INCOMING_BALLS = []



## The idea behind this code is that we only want to continue running the game while there are empty spaces left
## This will probably require a while loop, which I haven't created yet
NO_OF_EMPTY_SPACES_LEFT = 0
for i in range(0,n):
    for j in range(0,n):
        if GAMEBOARD[i][j] == 0:
            NO_OF_EMPTY_SPACES_LEFT += 1




while NO_OF_EMPTY_SPACES_LEFT>0:       # essentially the whole game happens inside this while loop -- i.e. it ends when you run out of space on the board


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
        

        ### use this code for debugging purposes
##        GAMEBOARD[2][2] = 2j
##        GAMEBOARD[5][0] = 4j
##        GAMEBOARD[1][4] = 1j  # this is the one blocking the exit 
##        INCOMING_BALLS = [[2,2],[5,0],[1,4]]
    #end of show_incoming_balls function

    show_incoming_balls()



    def print_nicely():
        i = 0
        while i < n:
            print(GAMEBOARD[i])
            i += 1

    print("Here's the gameboard:")
    print_nicely()



    # next we ask the user which ball they are going to move
    ball_to_move_input = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left, count downwards to get your x value, and count to the right for y): ")    
    colour_of_ball_being_moved = GAMEBOARD[int(ball_to_move_input[0])][int(ball_to_move_input[2])] # note the colour of the ball moved
    print("The colour you've selected is "+ str(colour_of_ball_being_moved))
    while colour_of_ball_being_moved.real == 0:                 # this while loop checks that the user has made sensible choices
        if colour_of_ball_being_moved == 0:                     # if the user has selected a cell where is actually no ball to move
            print("Sorry -- you've selected an empty cell!")    # then inform the user
            ball_to_move_input = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left): ")    # ask the user to choose a different cell
            colour_of_ball_being_moved = GAMEBOARD[int(ball_to_move_input[0])][int(ball_to_move_input[2])] # note the colour of the ball moved
            print("The colour you've selected is "+ str(colour_of_ball_being_moved))
        elif colour_of_ball_being_moved.imag > 0:               # if the user has selected a cell where there is an incoming ball which hasn't arrived yet
            print("Sorry -- this cell contains a ball which hasn't actually arrived on the board yet, so you can't move it")   # then inform the user
            ball_to_move_input = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left): ")    # ask the user to choose a different cell
            colour_of_ball_being_moved = GAMEBOARD[int(ball_to_move_input[0])][int(ball_to_move_input[2])] # note the colour of the ball moved
            print("The colour you've selected is "+ str(colour_of_ball_being_moved))
    #end of while loop        

    ball_destination = input("Give the x,y co-ordinates of the ball's destination, separated by a comma: ")


    # TO DO: need to add in verification that someone hasn't entered numbers that are outside of the GAMEBOARD
    # TO DO: need to add in verification that the co ordinates entered are for empty cell (for ball destination)


    #NOTE -- IMPORTANT ASSUMPTION I've assumed that n doesn't get any larger than 10 -- if n>10, the above code breaks, shouldn't be hard to fix it so that doesn't happen, because it's just the simple fact that I'm assuming it's one digit long


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



    CAN_MOVE = flood_fill(int(ball_to_move_input[0]),int(ball_to_move_input[2]), int(ball_destination[0]), int(ball_destination[2]))

    while CAN_MOVE == False:
        print("Sorry, there is no path between the ball you want to move and that destination")
        ball_destination = input("Give the x,y co-ordinates of the ball's destination, separated by a comma (or type 'new ball' if you want to choose a different ball to move): ")
        if ball_destination.lower() == "new ball":
            ball_to_move_input = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left): ")    
            colour_of_ball_being_moved = GAMEBOARD[int(ball_to_move_input[0])][int(ball_to_move_input[2])] # note the colour of the ball moved
            print("The colour you've selected is "+ str(colour_of_ball_being_moved))
            if colour_of_ball_being_moved == 0:
                print("Warning -- you've selected an empty cell!")
            ball_destination = input("Give the x,y co-ordinates of the ball's destination, separated by a comma: ")    
        CAN_MOVE = flood_fill(int(ball_to_move_input[0]),int(ball_to_move_input[2]), int(ball_destination[0]), int(ball_destination[2]))


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
        GAMEBOARD[int(ball_to_move_input[0])][int(ball_to_move_input[2])] = 0 # "lift" the ball off that cell of the GAMEBOARD by setting its value to zero
        GAMEBOARD[int(ball_destination[0])][int(ball_destination[2])] = colour_of_ball_being_moved # "place" the ball in its rightful place
        # need to tweak this (her's some pseudocode)
        # if long rows eliminated, then go back and give the user the option to move another ball
        # else go on to the make_incoming_Balls_arrive step
        
        make_incoming_balls_arrive()
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
        
        NOTE -- THIS IS CURRENTLY WRONG!
        Wrong because it should accommodate a 6-in-a-row or a 7-in-a-row (etc)
        Also there are some edge cases not working...
        ... e.g. horizontal 5-in-a-row not working if it's right over to the RHS
        FIRST STEP: fix this so edge cases work properly -- DONE
        SECOND STEP: stick a for loop around each existing loop so it checks 9 in a row, then... then 5 DONE
        THIRD STEP: once a 5-in-a-row has disappeared, user should get another move (not sure how to do this)

        """

        # each "long row" (i.e. row of the target length, e.g. each 5-in-a-row) is stored...
        # ... as a 2-tuple where the first element is the "first" position on the gameboard...
        # ... and the second element is a text string indicating the direction, i.e. "h", "v", "dtlbr", "dbltr"...
        # ... for horizontal, vertical, diagonal top left to bottom right, and diagonal bottom left to top right
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
                    while k < length_to_eliminate-1:     # should thsi say -1 at the end?
                        if GAMEBOARD[i][j+k] == GAMEBOARD[i][j+k+1] and GAMEBOARD[i][j+k] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"h"])        
        
            # find all the VERTICAL target length rows
            for j in range(0,n):
                for i in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     # should thsi say -1 at the end?
                        if GAMEBOARD[i+k][j] == GAMEBOARD[i+k+1][j] and GAMEBOARD[i+k][j] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"v"])        
            
            
            # find all the DIAGONAL TOP LEFT TO BOTTOM RIGHT target length rows
            for i in range(0,n-length_to_eliminate+1):
                for j in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     # should thsi say -1 at the end?
                        if GAMEBOARD[i+k][j+k] == GAMEBOARD[i+k+1][j+k+1] and GAMEBOARD[i+k][j+k] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"dtlbr"])        
            
            # find all the DIAGONAL BOTTOM LEFT TO TOP RIGHT target length rows
            for i in range(length_to_eliminate-1,n):
                for j in range(0,n-length_to_eliminate+1):
                    k = 0
                    while k < length_to_eliminate-1:     # should thsi say -1 at the end?
                        if GAMEBOARD[i-k][j+k] == GAMEBOARD[i-k-1][j+k+1] and GAMEBOARD[i-k][j+k] != 0:     # if the current position and then next one along have the same colour ball inside (and if it's not empty -- note that it's only necessary to check that it's non-zero the first time, but the code checks every time anyway)
                            k +=1                    # then move along and check the next one
                        else:
                            break                    # otherwise stop
                    if k == length_to_eliminate - 1:   # i.e. if the previous while loop got all the way through to the target row length    
                        list_of_long_rows.append([[i,j],"dbltr"])        
            
            
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
        
        # end of eliminate long rows function
        
    eliminate_long_rows()    
        
    print("This is a redundant extra print after eliminate_long_rows")
    print_nicely()

    NO_OF_EMPTY_SPACES_LEFT = 0
    for i in range(0,n):
        for j in range(0,n):
            if GAMEBOARD[i][j] == 0:
                NO_OF_EMPTY_SPACES_LEFT += 1
    

