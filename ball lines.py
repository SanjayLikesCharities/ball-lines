
"""
This code recreates the game ball lines
This game can be found, e.g., here: http://www.sheppardsoftware.com/braingames/balllines/balllinesAS2.htm
Note that if n (the size of the gameboard) is >=10, then parts of the game might break. (fix this by finding instances of "int(ball_to_move_input[0])" and "int(ball_to_move_input[2])" adjust appropriately)
"""



from random import randint


n = 9                        # size of the gameboard. Assumed to be square
gameboard = [0]*n            # gameboard represented by this array (first row created and initialised to zero)
for i in range(n):
    gameboard[i] = [0]*n     # remaining rows initialised to 0


no_of_colours = 4
no_of_incoming_balls = 3

def initialise_gameboard():
    """
    this function assigns a 'colour' to a few randomly chosen cells within the gameboard
    a colour here is represented by an integer > 0
    it does not yet show the incoming balls
    """
    no_of_initial_balls = 5
    balls_placed = 0             # initialising this counter
    while balls_placed < no_of_initial_balls :
        x = randint(0,8)
        y = randint(0,8)
        if gameboard[x][y] == 0:
            gameboard[x][y] = randint(1,no_of_colours)
            balls_placed +=1
#end of function

initialise_gameboard()

def show_incoming_balls():
    """
    this function shows where the new incoming balls are going to be next turn, and their colour.
    it does this by assigning an imaginary number to the relevant cell in the array
    """

    balls_placed = 0             # initialising this counter
    while balls_placed < no_of_incoming_balls :
        x = randint(0,8)
        y = randint(0,8)
        if gameboard[x][y] == 0:
            gameboard[x][y] = randint(1,no_of_colours)*1j  # python refers to sqrt(-1) as j
            balls_placed +=1

show_incoming_balls()


# I'm now hardcoding the gameboard (and overwriting the randomly assigned stuff from earlier) for debugging/testing purposes
# IMPORTANT TO DELETE THIS OUT if we want this to work properly
gameboard = [[3, 0, 0, 0, 0, 0, 0, 0, 0], [1, 4, 4, 0, 2, 2, 1, 3, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 3, 4, 1, 0, 3, 4, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def print_nicely():
    i = 0
    while i < n:
        print(gameboard[i])
        i += 1

print("Here's the gameboard at the start:")
print_nicely()


# next we ask the user which ball they are going to move
ball_to_move_input = input("Give the x,y co-ordinates of the ball you are going to move, separated by a comma ((0,0) is top left): ")    
print("1st character is "+ ball_to_move_input[0])
print("2nd character is "+ ball_to_move_input[1])
print("3rd character is "+ ball_to_move_input[2])
colour_of_ball_being_moved = gameboard[int(ball_to_move_input[0])][int(ball_to_move_input[2])] # note the colour of the ball moved
print("The colour you've selected is "+ str(colour_of_ball_being_moved))


# TO DO: need to add in verification that someone hasn't entered numbers that are outside of the gameboard
# TO DO: need to add in verification that someone hasn't entered co ordinates of an empty cell (for ball to move)
# TO DO: need to add in verification that the co ordinates entered are for empty cell (for ball destination)

#NOTE I've assumed that n doesn't get any larger than 10 -- if n>10, this code breaks, shouldn't be hard to fix it so that doesn't happen


def flood_fill():

    # these initial_x and initial_y variables are used at the level of overall flood_fill function
    # they refer to the location of the ball being moved
    # there will also be start_x and start_y variables -- they exist within the go_left, go_right, go_up, go_down functions
    initial_x = int(ball_to_move_input[0])
    initial_y = int(ball_to_move_input[2])
    
    
    def go_left(start_x,start_y):
    
        x = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going
        y = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going

        x[0] = start_x
        y[0] = start_y
    
        # when the algorithm stumbles upon an incoming ball (i.e. imaginary ball), the incoming_ball_found variable is updated
        if gameboard[x[0]][y[0]].imag > 0:  # if the cell we're starting at contains an incoming ball (i.e. imaginary ball)
                incoming_ball_found = True  # then set this variable to true
        else:
                incoming_ball_found = False # else set it to false
        
        # this variable will keep track of how far the algorithm has travelled
        # e.g. has it gone all the way to the edge of the board uninterrupted, or did it meet a coloured ball on the way?
        # the start point is included in the count (so it counts all the '-1's that it placed and the imaginary balls encountered
        counter = 0 
        
        for i in range(0, y[0]+1):
            """
            This code just keeps going to the "left" (i.e. the direction of decreasing y)
            It sets everything which is 0 to -1 until it hits a colour (i.e. something greater than 0)
            Incoming balls (i.e. imaginary balls) are left unchanged, and the algorithm continues past them
            """
            if incoming_ball_found == False:        # if there is an incoming/imaginary ball, want to leave it as is (i.e. ignore the next line)
                gameboard[x[i]][y[i]] = -1          # mark the current cell as being within the flood fill region -- this should only happen if it's zero/empty (i.e. if it's an imaginary ball the if statement that we're in means this line won't be seen, and if there's a coloured ball here, then the previous round of the for loop would have spotted it)
                counter +=1                         # increment the counter when a -1 is placed
            if i == y[0]:                           # without this if statement, the code takes the algorithm off the edge of the x[] and y[] arrays. Setting the for loop to stop 1 step earlier doesn't work beacuse then when the ball has to traverse the whole length of the board it doesn't make it all the way
                break
            if gameboard[x[i]][y[i]-1]==0 or gameboard[x[i]][y[i]-1]==-1:          # if the cell immediately to the left is empty
                incoming_ball_found = False         # in case the previous cell contained an imaginary ball, need to set this back to false
                x[i+1] = x[i]                       # move to the "left" (which keeps x constant)
                y[i+1] = y[i]-1                     # move to the "left" (i.e. decreases y by 1)
            elif gameboard[x[i]][y[i]-1].imag > 0:  # if the cell immediately to the left contains an incoming (ie imaginary) ball
                incoming_ball_found = True          # noting that we have found an incoming (i.e. imaginary) ball
                counter +=1                         # increment the counter when an imaginary ball is encountered
                x[i+1] = x[i]                       # move to the "left" (which keeps x constant)
                y[i+1] = y[i]-1                     # move to the "left" (i.e. decreases y by 1)
            else:                                   # if it contains a coloured ball
                incoming_ball_found = False         # this probably isn't necessary (?)
                break                               # stop moving in this direction -- should only happen if there's a coloured ball there (i.e. a number >=1)
        return counter
    
    
    def go_right(start_x,start_y):
        
        x = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going
        y = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going

        x[0] = start_x
        y[0] = start_y
        
        # when the algorithm stumbles upon an incoming ball (i.e. imaginary ball), the incoming_ball_found variable is updated
        if gameboard[x[0]][y[0]].imag > 0:  # if the cell we're starting at contains an incoming ball (i.e. imaginary ball)
                incoming_ball_found = True  # then set this variable to true
        else:
                incoming_ball_found = False # else set it to false
        
        # this will keep track of how far the algorithm has travelled
        # e.g. has it gone all the way to the edge of the board uninterrupted, or did it meet a coloured ball on the way?
        # the start point is included in the count (so it counts all the '-1's that it placed and the imaginary balls encountered
        counter = 0 
        
        for i in range(0, n-y[0]):
            """
            This code just keeps going to the "right" (i.e. the direction of increasing y)
            It sets everything which is 0 to -1 until it hits a colour (i.e. something greater than 0)
            Incoming balls (i.e. imaginary balls) are left unchanged, and the algorithm continues past them
            """
            if incoming_ball_found == False:        # if there is an incoming/imaginary ball, want to leave it as is (i.e. ignore the next line)
                gameboard[x[i]][y[i]] = -1          # mark the current cell as being within the flood fill region -- this should only happen if it's zero/empty
                counter +=1                         # increment the counter when a -1 is placed
            if i == n-y[0]-1:                       # without this if statement, the code evaluates gameboard[x[i]][y[i]+1], but that's off the edge of the board
                break
            if gameboard[x[i]][y[i]+1]==0 or gameboard[x[i]][y[i]+1]==-1:          # if the cell immediately to the right is empty
                incoming_ball_found = False         # in case the previous cell contained an imaginary ball, need to set this back to false
                x[i+1] = x[i]                       # move to the "right" (which keeps x constant)
                y[i+1] = y[i]+1                     # move to the "right" (i.e. increases y by 1)
            elif gameboard[x[i]][y[i]+1].imag > 0:  # if the cell immediately to the right contains an incoming (ie imaginary) ball
                incoming_ball_found = True          # noting that we have found an incoming (i.e. imaginary) ball
                counter +=1                         # increment the counter when an imaginary ball is encountered
                x[i+1] = x[i]                       # move to the "right" (which keeps x constant)
                y[i+1] = y[i]+1                     # move to the "right" (i.e. increases y by 1)
            else:                                   # if it contains a coloured ball
                incoming_ball_found = False         # this probably isn't necessary (?)
                break                               # stop moving in this direction -- should only happen if there's a coloured ball there (i.e. a number >=1)
        return counter
    
    def go_up(start_x,start_y):
    
        x = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going
        y = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going

        x[0] = start_x
        y[0] = start_y
    
        # when the algorithm stumbles upon an incoming ball (i.e. imaginary ball), the incoming_ball_found variable is updated
        if gameboard[x[0]][y[0]].imag > 0:  # if the cell we're starting at contains an incoming ball (i.e. imaginary ball)
                incoming_ball_found = True  # then set this variable to true
        else:
                incoming_ball_found = False # else set it to false
        
        # this will keep track of how far the algorithm has travelled
        # e.g. has it gone all the way to the edge of the board uninterrupted, or did it meet a coloured ball on the way?
        # the start point is included in the count (so it counts all the '-1's that it placed and the imaginary balls encountered
        counter = 0 
        
        for i in range(0, x[0]+1):
            """
            This code just keeps going "up" (i.e. the direction of decreasing x)
            It sets everything which is 0 to -1 until it hits a colour (i.e. something greater than 0)
            Incoming balls (i.e. imaginary balls) are left unchanged, and the algorithm continues past them
            """
            if incoming_ball_found == False:        # if there is an incoming/imaginary ball, want to leave it as is (i.e. ignore the next line)
                gameboard[x[i]][y[i]] = -1          # mark the current cell as being within the flood fill region -- this should only happen if it's zero/empty
                counter +=1                         # increment the counter when a -1 is placed
            if i == x[0]:                           # without this if statement, the code takes the algorithm off the edge of the x[] and y[] arrays. Setting the for loop to stop 1 step earlier doesn't work beacuse then when the ball has to traverse the whole length of the board it doesn't make it all the way
                break 
            if gameboard[x[i]-1][y[i]]==0 or gameboard[x[i]-1][y[i]]==-1:          # if the cell immediately to the left is empty
                incoming_ball_found = False         # in case the previous cell contained an imaginary ball, need to set this back to false
                x[i+1] = x[i]-1                     # move "up" (which decreases x)
                y[i+1] = y[i]                       # move "up" (which keeps y constant)
            elif gameboard[x[i]-1][y[i]].imag > 0:  # if the cell immediately above contains an incoming (ie imaginary) ball
                incoming_ball_found = True          # noting that we have found an incoming (i.e. imaginary) ball
                counter +=1                         # increment the counter when an imaginary ball is encountered
                x[i+1] = x[i]-1                     # move "up" (which decreases x)
                y[i+1] = y[i]                       # move "up" (which keeps y constant)
            else:                                   # if it contains a coloured ball
                incoming_ball_found = False         # this probably isn't necessary (?)
                break                               # stop moving in this direction -- should only happen if there's a coloured ball there (i.e. a number >=1)
        return counter
    
    def go_down(start_x,start_y):
        
        x = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going
        y = [0]*n # creating a variable which will track where on the gameboard the flood fill algorithm is going

        x[0] = start_x
        y[0] = start_y
        
        # when the algorithm stumbles upon an incoming ball (i.e. imaginary ball), the incoming_ball_found variable is updated
        if gameboard[x[0]][y[0]].imag > 0:  # if the cell we're starting at contains an incoming ball (i.e. imaginary ball)
                incoming_ball_found = True  # then set this variable to true
        else:
                incoming_ball_found = False # else set it to false
        
        # this will keep track of how far the algorithm has travelled
        # e.g. has it gone all the way to the edge of the board uninterrupted, or did it meet a coloured ball on the way?
        # the start point is included in the count (so it counts all the '-1's that it placed and the imaginary balls encountered
        counter = 0 
        
        for i in range(0, n-x[0]):
            """
            This code just keeps going "down" (i.e. the direction of increasing x)
            It sets everything which is 0 to -1 until it hits a colour (i.e. something greater than 0)
            Incoming balls (i.e. imaginary balls) are left unchanged, and the algorithm continues past them
            """
            if incoming_ball_found == False:        # if there is an incoming/imaginary ball, want to leave it as is (i.e. ignore the next line)
                gameboard[x[i]][y[i]] = -1          # mark the current cell as being within the flood fill region -- this should only happen if it's zero/empty
                counter +=1                         # increment the counter when a -1 is placed
            if i == n-x[0]-1:                       # without this if statement, the code evaluates gameboard[x[i]+1][y[i]], but that's off the edge of the board
                break
            if gameboard[x[i]+1][y[i]]==0 or gameboard[x[i]+1][y[i]]==-1:          # if the cell immediately below is empty
                incoming_ball_found = False         # in case the previous cell contained an imaginary ball, need to set this back to false
                x[i+1] = x[i]+1                     # move "down" (which increases x by 1)
                y[i+1] = y[i]                       # move "down" (which keeps y constant)
            elif gameboard[x[i]+1][y[i]].imag > 0:  # if the cell immediately below contains an incoming (ie imaginary) ball
                incoming_ball_found = True          # noting that we have found an incoming (i.e. imaginary) ball
                counter +=1                         # increment the counter when an imaginary ball is encountered
                x[i+1] = x[i]+1                     # move "down" (which increases x by 1)
                y[i+1] = y[i]                       # move "down" (which keeps y constant)
            else:                                   # if it contains a coloured ball
                incoming_ball_found = False         # this probably isn't necessary (?)
                break                               # stop moving in this direction -- should only happen if there's a coloured ball there (i.e. a number >=1)
        return counter
    
    
    #this is just a reminder for me for how to do this
    #extent_of_left_branch = [0]*3
    #for i in range(3):
    #    extent_of_left_branch[i] = [0]*7
    #for i in range(3):
    #    for j in range(7):
    #        extent_of_left_branch[i][j] = [0]*5

    #the next section initialises the variables extent_of_left_branch (and similarly for up down and right)
    #these variables are to keep track of how far the flood fill algorithm is supposed to travel
    extent_of_left_branch = [0]*n
    for i in range(n):
        extent_of_left_branch[i] = [0]*n
    for i in range(n):
        for j in range(n):
            extent_of_left_branch[i][j] = [0]*n

    extent_of_right_branch = [0]*n
    for i in range(n):
        extent_of_right_branch[i] = [0]*n
    for i in range(n):
        for j in range(n):
            extent_of_right_branch[i][j] = [0]*n
    
    extent_of_up_branch = [0]*n
    for i in range(n):
        extent_of_up_branch[i] = [0]*n
    for i in range(n):
        for j in range(n):
            extent_of_up_branch[i][j] = [0]*n
    
    extent_of_down_branch = [0]*n
    for i in range(n):
        extent_of_down_branch[i] = [0]*n
    for i in range(n):
        for j in range(n):
            extent_of_down_branch[i][j] = [0]*n
    
    # now we implement the go_left, go_right, etc functions, which start from the initial_x, initial_y starting point and create a "cross" of -1s
    # those functions return the distance they have travelled, so we're storing this in the 0,0,0 spot in the "extent_of_xxx_branch" tensors    
    extent_of_left_branch[0][0][0] = go_left(initial_x,initial_y)
    extent_of_right_branch[0][0][0] = go_right(initial_x,initial_y)
    extent_of_up_branch[0][0][0] = go_up(initial_x,initial_y)
    extent_of_down_branch[0][0][0] = go_down(initial_x,initial_y)
 
    print("Here's the board after creating the initial cross-like shape:")
    print_nicely()
    
 
    # Now we travel down the left branch and go up and go down from each cell on the left branch
    for i in range(1,extent_of_left_branch[0][0][0]):                           # continue until the correct "extent" (i.e. the distance travelled until the code hit a coloured ball or the edge of the board)
        extent_of_left_branch[1][i][0] = go_up(initial_x,initial_y-i)           # as we travel along, apply go_up at each cell along the way; by the time we get to the end of this loop, we've made one "turning"
        extent_of_left_branch[2][i][0] = go_down(initial_x,initial_y-i)         # as we travel along, apply go_down at each cell along the way; by the time we get to the end of this loop, we've made one "turning"
        for j in range(1,extent_of_left_branch[1][i][0]):
            extent_of_left_branch[3][i][j] = go_left(initial_x-j,initial_y-i)   # this is for the second "turning" off the go_up branch
            extent_of_left_branch[4][i][j] = go_right(initial_x-j,initial_y-i)  # this is for the second "turning" off the go_up branch
            for k in range(1,extent_of_left_branch[3][i][j]):
                go_up(initial_x-j,initial_y-i-k)                                # so far have gone left, up, left, now we go up
                go_down(initial_x-j,initial_y-i-k)                              # so far have gone left, up, left, now we go down
            for k in range(1,extent_of_left_branch[4][i][j]):
                go_up(initial_x-j,initial_y-i+k)                                # so far have gone left, up, right, now we go up
                go_down(initial_x-j,initial_y-i+k)                              # so far have gone left, up, right, now we go down
        for j in range(1,extent_of_left_branch[2][i][0]):
            extent_of_left_branch[5][i][j] = go_left(initial_x+j,initial_y-i)   # this is for the second "turning" off the go_down branch
            extent_of_left_branch[6][i][j] = go_right(initial_x+j,initial_y-i)  # this is for the second "turning" off the go_down branch
            for k in range(1,extent_of_left_branch[5][i][j]):
                go_up(initial_x+j,initial_y-i-k)                                # so far have gone left, down, left, now we go up
                go_down(initial_x+j,initial_y-i-k)                              # so far have gone left, down, left, now we go down
            for k in range(1,extent_of_left_branch[6][i][j]):
                go_up(initial_x+j,initial_y-i+k)                                # so far have gone left, down, right, now we go up
                go_down(initial_x+j,initial_y-i+k)                              # so far have gone left, down, right, now we go down    
        

    #this is just for debugging
    print("Here's the board after going along the left branch and going up and down from each part of that branch, and then left and right from there, and then up and down again from those points")
    print_nicely()
    
    #this is just for debugging
    print("And here's the relevant bits of the extent of left branch tensor")
    print("extent_of_left_branch[0][0][0] = "+str(extent_of_left_branch[0][0][0]))
    print("extent_of_left_branch[1][0][0] = "+str(extent_of_left_branch[1][0][0]))
    print("extent_of_left_branch[1][1][0] = "+str(extent_of_left_branch[1][1][0]))
    print("extent_of_left_branch[1][2][0] = "+str(extent_of_left_branch[1][2][0]))
    print("extent_of_left_branch[1][3][0] = "+str(extent_of_left_branch[1][3][0]))
    print("extent_of_left_branch[1][4][0] = "+str(extent_of_left_branch[1][4][0]))
    print("extent_of_left_branch[1][5][0] = "+str(extent_of_left_branch[1][5][0]))
    print("extent_of_left_branch[1][6][0] = "+str(extent_of_left_branch[1][6][0]))
    print("extent_of_left_branch[1][7][0] = "+str(extent_of_left_branch[1][7][0]))
    print("extent_of_left_branch[1][8][0] = "+str(extent_of_left_branch[1][8][0]))
    print("extent_of_left_branch[2][0][0] = "+str(extent_of_left_branch[2][0][0]))
    print("extent_of_left_branch[2][1][0] = "+str(extent_of_left_branch[2][1][0]))
    print("extent_of_left_branch[2][2][0] = "+str(extent_of_left_branch[2][2][0]))
    print("extent_of_left_branch[2][3][0] = "+str(extent_of_left_branch[2][3][0]))
    print("extent_of_left_branch[2][4][0] = "+str(extent_of_left_branch[2][4][0]))
    print("extent_of_left_branch[2][5][0] = "+str(extent_of_left_branch[2][5][0]))
    print("extent_of_left_branch[2][6][0] = "+str(extent_of_left_branch[2][6][0]))
    print("extent_of_left_branch[2][7][0] = "+str(extent_of_left_branch[2][7][0]))
    print("extent_of_left_branch[2][8][0] = "+str(extent_of_left_branch[2][8][0]))
    
        
    
    for i in range(1,extent_of_right_branch[0][0][0]):         
        go_up(initial_x,initial_y+i)
        go_down(initial_x,initial_y+i)
    
    for i in range(1,extent_of_up_branch[0][0][0]):         
        go_left(initial_x-i,initial_y)
        go_right(initial_x-i,initial_y)
    
    for i in range(1,extent_of_down_branch[0][0][0]):         
        go_left(initial_x+i,initial_y)
        go_right(initial_x+i,initial_y)
    
    
# end of flood fill function


flood_fill()
print("Here's the board after applying flood fill:")
print_nicely()



# NEXT LINES OF CODE ARE COMMENTED OUT, BUT SHOULD BE UNCOMMENTED ONCE FLOOD FILL IS WORKING

#ball_destination = input("Give the x,y co-ordinates of the ball's destination, separated by a comma: ")
#gameboard[int(ball_to_move_input[0])][int(ball_to_move_input[2])] = 0 # "lift" the ball off that cell of the gameboard by setting its value to zero

#gameboard[ball_destination[0]][ball_destination[2]] = colour_of_ball_being_moved # "place" the ball in its rightful place

