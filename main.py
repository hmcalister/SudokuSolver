import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import solver
pygame.init()

class SudokuSquare:
    """An object for each square in the sudoku grid.
        Handles the drawing of squares, as wells as active/inactive squares
        Also handles user input of numbers into squares."""

    #defining some useful class variables. Mainly for easy changes later
    COLOR_INACTIVE = pygame.Color(200,200,200)
    COLOR_ACTIVE = pygame.Color(150,150,150)
    FONT_COLOR = pygame.Color(0,0,0)
    FONT = pygame.font.Font(None, 32)
    
    def __init__(self, x, y, size, screen):
        """x,y gives position of sudoku square top left corner
            size gives length of one side of sodoku square
            screen is the pygame surface to draw onto"""
        self.size=size
        self.rect = pygame.Rect(x, y, size, size)
        self.color = SudokuSquare.COLOR_INACTIVE
        self.screen = screen
        self.text = ''
        self.txt_surface = SudokuSquare.FONT.render(self.text, True, self.color)
        self.active = False
        self.draw()

    def handle_event(self, event):
        """Passes a pygame event to the square, checking if this square is active and if it should respond to it"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = SudokuSquare.COLOR_ACTIVE if self.active else SudokuSquare.COLOR_INACTIVE
            #Update the box
            self.draw()
            
        if event.type == pygame.KEYDOWN:
            #Check if box is active, only type if is active
            if self.active:
                #Allow for deletion
                if event.key == pygame.K_BACKSPACE:
                    self.text = ''
                else:
                    #Ensure input is a digit 1-9 and replace the text
                    char = event.unicode
                    if char.isdigit() and char!='0':
                        self.text = char
                    
                # Re-render the text.
                self.txt_surface = SudokuSquare.FONT.render(self.text, True, SudokuSquare.FONT_COLOR)
                self.draw()
                
    def draw(self):
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect)
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+2*self.size//5, self.rect.y+self.size//3))

    def set_digit(self, num):
        """Update the digit to be displayed in this square"""
        if num==0: num=''
        self.text = str(num)
        self.txt_surface = SudokuSquare.FONT.render(self.text, True, SudokuSquare.FONT_COLOR)
        self.draw()

    def get_digit(self):
        """Return the digit currently in the square, zero if blank"""
        if self.text=='': return 0
        return int(self.text)

    def clear_digit(self):
        """Clear the digit currently held in the square, making text blank"""
        self.text = ''
        self.txt_surface = SudokuSquare.FONT.render(self.text, True, SudokuSquare.FONT_COLOR)
        self.draw()
        
def solve_board(board):
    """board is the 2D array of SudokuSquare objects.
        Get the values of the board currently, and solve the board state
        Then, update the board and display the solved state"""
    #Get the board values into a 2D array
    values = list()
    for y in range(9):
        values.append([])
        for x in range(9):
            values[y].append(board[y][x].get_digit())

    #Better check the user has a valid board state to start with...
    for y in range(9):
        for x in range(9):
            if values[y][x]!=0:
               if not solver.valid(values, values[y][x], (y,x)):
                   #We have an invalid board state, do not solve
                   print("Invalid state!")
                   return False
    #solver.print_board(values)
    solver.solve(values)
    #solver.print_board(values)
    #Update the values in the GUI
    for y in range(9):
        for x in range(9):
            board[y][x].set_digit(values[y][x])

def main():
    #set a title
    pygame.display.set_caption("Sudoku Solver")
     
    # create a display that is square of a set size
    screenSize = 450
    squareSize = screenSize//9            
    screen = pygame.display.set_mode((screenSize,screenSize))

    #Create the sudoku squares, and orgainse them into a 2D array
    #This 2D array is addressed by y first, then x !!!
    sudokuSquares = list()
    for y in range(9):
        sudokuSquares.append([])
        for x in range(9):
            sudokuSquares[y].append(SudokuSquare(x*squareSize, y*squareSize, squareSize, screen))

    #Create the lines we need to seperate the squares
    #Lines have form of (startPos, endPos, width)
    LINE_COLOR = pygame.Color(0,0,0)
    lines = list()
    for x in range(1,9):
        lines.append(((x*squareSize, 0), (x*squareSize, screenSize), 1 if x%3 else 3))
    for y in range(1,9):
        lines.append(((0, y*squareSize), (screenSize, y*squareSize), 1 if y%3 else 3))

        
    # main loop
    running = True
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            #If exit button is clicked, exit the game
            if event.type == pygame.QUIT:
                running=False
            #Give the event to the squares
            for y in range(9):
                for x in range(9):
                    sudokuSquares[y][x].handle_event(event)
            #Redraw the lines                    
            for line in lines:
                pygame.draw.line(screen, LINE_COLOR, line[0], line[1], line[2])
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    values = list()
                    for y in range(9):
                        values.append([])
                        for x in range(9):
                            values[y].append(sudokuSquares[y][x].get_digit())
                    solver.print_board(values)
                if event.key == pygame.K_s:
                    solve_board(sudokuSquares)
                if event.key == pygame.K_c:
                    for y in range(9):
                        for x in range(9):
                            sudokuSquares[y][x].clear_digit()
            pygame.display.update()
     
     
if __name__=="__main__":
    print("""Welcome to the Sudoku Solver!\n
Click in a square to activate it, then type a number in to load that square.\n
When you have loaded all the numbers you have, press 's' to solve the sodoku.\n
At any time, press 'c' to clear the grid!""")
    main()
    pygame.quit()
