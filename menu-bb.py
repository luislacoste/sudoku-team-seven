import random
import os
import time


# Tamaño del tablero
CUADRADO = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3


def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for row in board:
        print(" ".join(f"\033[92m{num}\033[0m" if num !=
              0 else '.' for num in row))
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
                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if auto_gen_board_bb(tablero):  # Se fija si puede generar el tablero con lo que va poniendo
                            return tablero
                        tablero[fila][columna] = 0
                return False
    return tablero


# ESTE VA A SER USADO PARA EL USER INPUT
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
    board = [[0] * CUADRADO for _ in range(CUADRADO)]
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)
    numeros_eliminar = 81 - numeros_completos

    if modo == 1:
        board = user_gen_board(dificultad, algo)
        # Tenemos que resolver de punta a punta el board con algun algo para
        # ver si se puede o no resolver
        is_board_valid = validate_board(board)
    else:
        if algo == 1:
            board = auto_gen_board_bb(dificultad)
        else:
            board = auto_gen_board_bb(board) # auto_gen_board retornaba un booleano si se pudo generar el tablero o no, cambiado para que retorne el tablero
        # board = auto_gen_board_bt(dificultad)
        eliminar_numeros(board, numeros_eliminar)
    return board



def get_empty_location(board):
    # Busca una celda vacía en el tablero
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
                options = sum(1 for num in range(1, CUADRADO + 1) if is_safe(board, row, col, num)) # Verificar funcionamiento de esta funcion (Decide la celda con menos opciones)
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
        if is_safe(board, row, col, num):
            board[row][col] = num  # Asignar número
            print_board(board)  # Mostrar intento

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound_sudoku(board):
                return True
            
            # Deshacer la asignación (backtrack)
            board[row][col] = 0
            print_board(board)  # Mostrar retroceso

    return False



def main():
    # algoritmo 1 = backtracking 2 = branch and bound
    algo = 2
    # modo = int(input(
    #     "Ingrese el modo de juego \n 1. Ingresar Tablero \n 2. Tablero auto-generado \n "))
    modo = 2
    # dificultad = int(input(
    # "Ingrese la dificultad del Sudoku \n 1. Facil \n 2. Medio \n 3. Dificil \n"))
    dificultad = 1
    board = generar_tablero(modo, dificultad, algo)
    # print_board(board)
    branch_and_bound_sudoku(board)


    # resolucion = int(input(
    #     "Ingrese el metodo de resolucion \n 1. Resolver manual \n 2. Resolver automatico (AI) \n"))
    # # if resolucion == 1:
    # #     print("Resolver manual")
    # else:
    #     resolver_auto_bt(board)
    #     resolver_auto_bb(board)


if __name__ == '__main__':
    main()
