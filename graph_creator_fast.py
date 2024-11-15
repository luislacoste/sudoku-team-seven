import random
import os
import time
import csv

CUADRADO = 9
SUBCUADRO = 3


def medir_tiempo_ejecucion(func, *args, **kwargs):
    inicio = time.time()
    resultado = func(*args, **kwargs)
    fin = time.time()
    tiempo_ejecucion = fin - inicio
    return tiempo_ejecucion, resultado


def get_least_options_cell(tablero):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if tablero[row][col] == 0:
                options = 0
                for num in range(1, CUADRADO + 1):
                    if es_valido(tablero, row, col, num):
                        options += 1
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
                if min_options == 1:
                    return best_cell, min_options
    return best_cell, min_options


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


def initialize_unassigned(board):
    """Initialize the unassigned cells with their candidate lists."""
    unassigned = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = find_candidates(board, row, col)
                unassigned.append((len(candidates), row, col, candidates))
    # Sort by the number of candidates
    unassigned.sort(key=lambda x: x[0])
    return unassigned


def update_unassigned(unassigned, board, row, col):
    """Update the candidates for affected cells after placing or removing a number."""
    updated = []
    for candidates_len, r, c, candidates in unassigned:
        if r == row or c == col or (r // 3 == row // 3 and c // 3 == col // 3):
            # Recalculate candidates for affected cells
            new_candidates = find_candidates(board, r, c)
            updated.append((len(new_candidates), r, c, new_candidates))
        else:
            # Keep original data for unaffected cells
            updated.append((candidates_len, r, c, candidates))
    # Sort updated list by the number of candidates
    updated.sort(key=lambda x: x[0])
    return updated


def branch_and_bound_sudoku(board, unassigned):
    """Solve the Sudoku puzzle using branch and bound."""
    # print_tablero(board)
    if not unassigned:
        return True  # Puzzle solved

    # Pick the cell with the fewest candidates
    _, row, col, candidates = unassigned[0]

    for num in candidates:

        board[row][col] = num  # Make a move
        new_unassigned = update_unassigned(unassigned[1:], board, row, col)
        if branch_and_bound_sudoku(board, new_unassigned):
            return True  # Continue with the solution
        board[row][col] = 0  # Undo the move (backtrack)

    return False  # Trigger backtracking

def es_valido(tablero, row, col, num):
    if tablero[row][col] != 0:
        return False
    if num in tablero[row]:
        return False
    for r in range(CUADRADO):
        if tablero[r][col] == num:
            return False

    start_row = row - row % SUBCUADRO
    start_col = col - col % SUBCUADRO
    for r in range(SUBCUADRO):
        for c in range(SUBCUADRO):
            if tablero[start_row + r][start_col + c] == num:
                return False
    return True


def back_tracking(tablero):
    for fila in range(CUADRADO):
        for columna in range(CUADRADO):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                for num in numeros:
                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if back_tracking(tablero):
                            return True
                        tablero[fila][columna] = 0
                return False
    return True


def eliminar_numeros(tablero, numeros_eliminar):
    casillas = [(i, j) for i in range(CUADRADO) for j in range(CUADRADO)]
    random.shuffle(casillas)
    for i in range(numeros_eliminar):
        fila, columna = casillas[i]
        tablero[fila][columna] = 0
    return tablero


def generate_valid_sudoku(dificultad, algoritmo):
    tablero = [[0] * CUADRADO for _ in range(CUADRADO)]
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)
    numeros_eliminar = 81 - numeros_completos
    if algoritmo == 1:
        back_tracking(tablero)
    
    eliminar_numeros(tablero, numeros_eliminar)
    return tablero


def generate_csv(data_frame):
    with open('data.csv', mode='w') as file:
        writer = csv.writer(file)
        for row in data_frame:
            writer.writerow(row)


def uniTest():
    data_frame = [["Dificultad", "Branch and Bound", "Movimientos BB", "Operaciones BB", "Contador"]]
    for i in range(1, 4):
        for x in range(1, 101):
            tablero = generate_valid_sudoku(i, 1)
            tablero_save = [row[:] for row in tablero]

            movimientos_bt = [0]
            operaciones_bt = [0]
            movimientos_bb = [0]
            operaciones_bb = [0]

            unnasigned = initialize_unassigned(tablero_save)
            time2, _ = medir_tiempo_ejecucion(
                branch_and_bound_sudoku, tablero_save, unnasigned)

            data_frame.append(
                [i, time2,  movimientos_bb[0], operaciones_bb[0], x])
            print(i,x)
            print("---------------------------------")
    generate_csv(data_frame)


if __name__ == '__main__':
    uniTest()
