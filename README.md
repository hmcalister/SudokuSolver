# SudokuSolver
A GUI based Sudoku Solving program

main.py is the GUI base of the program, handling the user inputs into the squares and drawing everything onto the screen. The GUI is built using pygame.

solver.py is the solving algorithms for the sodoku. The basis of this is backtracking: taking a board state and trying every each combination sequentially until a solution is found, and when an invalid move is made the next number is tried. The solver finds the next empty square in the board, tries a value then repeats. Because of the fixed size of the board, python can handle this algorithm well and can solve valid boards in less than a second.

Click into a square and type a number to enter it. Backspace deletes a number from a square. Press "S" to solve the board, or "C" to clear all squares.

# TODO
Currently, the GUI doesn't have buttons for solve or clear, which would be very useful and intuitive.
It would be nice if using the arrow keys could navigate around the board, rather than having to click into each square. This would require a new data structure to track active squares which could be bad practice.
The solving algorithm can hang if an implied invalid state is entered. For example, 
```
0 0 0  | 0 0 0  | 0 0 1
0 0 0  | 0 0 0  | 0 0 2
0 0 0  | 0 0 0  | 0 0 3
- - - - - - - - - - - - - 
0 0 0  | 0 0 0  | 0 0 4
0 0 0  | 0 0 0  | 0 0 5
0 0 0  | 0 0 0  | 0 0 6
- - - - - - - - - - - - - 
0 0 0  | 0 0 0  | 0 0 7
0 0 0  | 0 0 0  | 0 0 8
9 8 7  | 6 5 4  | 3 2 0
```
this implies the last square needs to be a 9 and a 1. Because the solving algorithm cannot validate either number, it will fail eventually. But in order to fail it needs to try every possible state of the board before that square. i.e. it will try approximately 9^81 states before finally declaring this state invalid. That's a little beyond my computation power, so instead I am considering just adding a timer that alerts the user if a state is taking too long to compute. Because valid states take less than a second to compute, this would be an easy way to differentiate between valid and invalid states.
