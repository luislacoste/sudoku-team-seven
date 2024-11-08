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
    time.sleep(0.3)  # Pausar para visualizar el progreso


def eliminar_numeros(tablero, numeros_eliminar):
    casillas = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(casillas)
    for i in range(numeros_eliminar):
        fila, columna = casillas[i]
        tablero[fila][columna] = 0
    return tablero


def auto_gen_board_bb(tablero):
    for fila in range(CUADRADO):
        for columna in range(CUADRADO):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                random.shuffle(numeros)  # Mezcla para mayor variabilidad
                for num in numeros:
                    if is_safe(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if auto_gen_board_bb(tablero):
                            return tablero
                        tablero[fila][columna] = 0
                return False
    return tablero


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


def user_gen_board():
    board = []
    for _ in range(CUADRADO):
        row = list(map(int, input().split()))
        board.append(row)
    return board


def generar_tablero(modo, dificultad, algo):
    # Generar tablero vacío lista de listas
    board = [[0] * CUADRADO for _ in range(CUADRADO)]
    
    # Definir cantidad de números a completar
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)
    numeros_eliminar = 81 - numeros_completos

    
    if modo == 1:
        # Usuario rellena el tablero
        board = user_gen_board()
    else:
        if algo == 1:
            # Tablero generado con backtracking
            board = auto_gen_board_bt(board)
        else:
            # Tablero generado con branch and bound
            board = auto_gen_board_bb(board)
        # Eliminar números para generar tablero con dificultad
        eliminar_numeros(board, numeros_eliminar)
    return board


def get_options_for_empty_cells(board):
    options = {}
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                cell_options = [num for num in range(1, CUADRADO + 1) if is_safe(board, row, col, num)]
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
            print_board(board, options)  # Mostrar intento con opciones

            if branch_and_bound_sudoku(board):
                return True
            
            board[row][col] = 0
            print_board(board, options)  # Mostrar retroceso con opciones

    return False


def main():
    algo = 2
    modo = 2
    dificultad = 1
    board = generar_tablero(modo, dificultad, algo)
    print_board(board)
    branch_and_bound_sudoku(board)


if __name__ == '__main__':
    main()
