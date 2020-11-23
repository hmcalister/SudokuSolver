def print_board(b):
    """A useful method for debugging, outputing a board of values in a nice way"""
    for i in range(len(b)):
        if i%3==0 and i!=0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(b[i])):
            if j%3==0 and j!=0:
                print(" | ", end="")

            if j==8:
                print(b[i][j])
            else:
                print(str(b[i][j])+" ", end="")
    print()

def find_empty(b):
    """Finds the next entry that is empty in a board. An empty value is denoted by a 0"""
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j]==0:
                return (i,j)
    return None

def solve(b):
    """Solves the board in a recursive manner, using backtracking"""
    #Find the first empty square and work on this
    find = find_empty(b)
    #Check if there is an empty square, if there isn't then we are done!
    if not find:
        return True
    else:
        row, col = find

    #Try every possible value for this empty square
    for i in range(1,10):
        #Check if this value is valid
        if valid(b, i, (row, col)):
            #Try solving the rest of the board with this
            b[row][col]=i
            if solve(b):
                return True
            b[row][col]=0
    #If we have exhausted all possibilites, then this state cannot be correct, go back            
    return False

def valid(b, num, pos):
    """Checks if the number given in num is a valid possibility of position pos in a board b"""
    #Pos takes form of (y,x)
    #check row
    for i in range(len(b[0])):
        if b[pos[0]][i]==num and pos[1]!=i:
            return False
    #check col
    for j in range(len(b)):
        if b[j][pos[1]]==num and pos[0]!=j:
            return False
    #check box
    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3+3):
        for j in range(box_x*3, box_x*3+3):
            if b[i][j]==num and (i,j)!=pos:
                return False

    return True
