
def get_options_for_empty_cells(board):
    options = {}
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                cell_options = [num for num in range(
                    1, CUADRADO + 1) if is_safe(board, row, col, num)]
                options[(row, col)] = cell_options
    return options

def get_least_options_cell(board):
    options = get_options_for_empty_cells(board)
    min_options = CUADRADO + 1
    best_cell = None
    for cell, cell_options in options.items():
        if len(cell_options) < min_options:
            min_options = len(cell_options)
            best_cell = cell
            if min_options == 1:
                return best_cell, min_options
    return best_cell, options


def branch_and_bound_sudoku(board):
    empty_location, options = get_least_options_cell(board)
    if empty_location is None:
        return True  # Si no hay celdas vacías, se encontró una solución

    row, col = empty_location
    cell_options = options[empty_location]

    for num in cell_options:
        if is_safe(board, row, col, num):
            board[row][col] = num

            if branch_and_bound_sudoku(board):
                return True

            board[row][col] = 0

    return False
