import os
import time

# Tamaño del tablero
CUADRADO = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for row in board:
        print(" ".join(f"\033[92m{num}\033[0m" if num != 0 else '.' for num in row))
    time.sleep(0.03)  # Pausar para visualizar el progreso

def es_valido(tablero, fila, columna, num):
    # Verificar fila y columna
    for x in range(CUADRADO):
        if tablero[fila][x] == num or tablero[x][columna] == num:
            return False
    # Verificar el subtablero de 3x3
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (columna // 3)
    for i in range(SUBCUADRO):
        for j in range(SUBCUADRO):
            if tablero[inicio_fila + i][inicio_col + j] == num:
                return False
    return True

def get_empty_location(board):
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                return row, col
    return None

def get_least_options_cell(board):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                options = sum(1 for num in range(1, CUADRADO + 1) if es_valido(board, row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
    return best_cell

def branch_and_bound_sudoku(board):
    empty_location = get_least_options_cell(board)
    if empty_location is None:
        return True  # Si no hay celdas vacías, se encontró una solución

    row, col = empty_location

    # Intentar números del 1 al 9
    for num in range(1, CUADRADO + 1):
        if es_valido(board, row, col, num):
            board[row][col] = num  # Asignar número
            print_board(board)  # Mostrar intento

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound_sudoku(board):
                return True
            
            # Deshacer la asignación (backtrack)
            board[row][col] = 0
            print_board(board)  # Mostrar retroceso

    return False

# Ejemplo de uso
tablero = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

branch_and_bound_sudoku(tablero)
print_board(tablero)
