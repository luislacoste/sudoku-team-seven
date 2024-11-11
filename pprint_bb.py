
import random
import os
import time


# Tamaño del tablero
CUADRADO = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3



def print_board(board, options=None):
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for i, row in enumerate(board):
        for j, num in enumerate(row):
            if num != 0:
                print(f"\033[92m{num}\033[0m", end=" ")
            else:
                cell_options = options.get((i, j), []) if options else []
                print(f"({','.join(map(str, cell_options))})", end=" ")
        print()
    time.sleep(0.07)  # Pausar para visualizar el progreso


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
            print_board(board, options)

            if branch_and_bound_sudoku(board):
                return True

            board[row][col] = 0
            print_board(board, options)


    return False


def is_safe(board, row, col, num):
    # Verifica que la celda no contenga numero
    if board[row][col] != 0:
        return False
    # Verificar fila
    if num in board[row]:
        return False
    # Verificar columna
    for r in range(CUADRADO):
        if board[r][col] == num:
            return False

    # Verificar subcuadro
    start_row = row - row % SUBCUADRO
    start_col = col - col % SUBCUADRO
    for r in range(SUBCUADRO):
        for c in range(SUBCUADRO):
            if board[start_row + r][start_col + c] == num:
                return False
    return True


if __name__ == "__main__":
    tablero = [[9, 0, 0, 6, 0, 0, 2, 0, 8], [0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [6, 8, 0, 0, 0, 0, 0, 0, 0], [
        0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 7, 3], [7, 5, 9, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 5]]
    branch_and_bound_sudoku(tablero)
