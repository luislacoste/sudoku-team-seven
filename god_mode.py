import heapq

def is_valid_move(board, row, col, num):
    """Check if a number can be placed in a given cell."""
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def find_candidates(board, row, col):
    """Find all valid numbers for a given cell."""
    candidates = []
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            candidates.append(num)
    return candidates

def find_unassigned_cells(board):
    """Find all unassigned cells and prioritize them by the number of candidates."""
    unassigned = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = find_candidates(board, row, col)
                heapq.heappush(unassigned, (len(candidates), row, col, candidates))
    return unassigned

def branch_and_bound_sudoku(board):
    """Solve the Sudoku puzzle using branch and bound."""
    unassigned = find_unassigned_cells(board)
    if not unassigned:
        return True  # Puzzle solved

    _, row, col, candidates = heapq.heappop(unassigned)

    for num in candidates:
        if is_valid_move(board, row, col, num):
            board[row][col] = num  # Make a move
            if branch_and_bound_sudoku(board):
                return True  # Continue with the solution
            board[row][col] = 0  # Undo the move (backtrack)

    return False  # Trigger backtracking

def print_board(board):
    """Print the Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

# Input Sudoku board
tablero = [
    [0, 0, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 6, 7, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0],
    [9, 0, 0, 4, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 0]
]

print("Initial Sudoku Board:")
print_board(tablero)

if branch_and_bound_sudoku(tablero):
    print("\nSolved Sudoku Board:")
    print_board(tablero)
else:
    print("\nNo solution exists.")
