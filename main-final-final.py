import random
import os
import time

# Tamaño del tablero
CUADRADO = 9

# Tamaño de cada subcuadro
SUBCUADRO = 3


def medir_tiempo_ejecucion(func, *args, **kwargs):
    # Captura el tiempo antes de ejecutar la función
    inicio = time.time()

    # Ejecuta la función con los argumentos proporcionados
    resultado = func(*args, **kwargs)

    # Captura el tiempo después de ejecutar la función
    fin = time.time()

    # Calcula el tiempo de ejecución
    tiempo_ejecucion = fin - inicio

    print(f"{func.__name__}: {tiempo_ejecucion:.6f} segundos")

    return resultado


def print_board(board):
    time.sleep(0.3)  # Pausar para visualizar el progreso

    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("------------------------")  # Separación de subcuadros

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")  # Separación de subcuadros en columnas
            if j == 8:
                print(f"\033[92m{board[i][j]}\033[0m")  # Fin de la fila
            else:
                # print(str(board[i][j]) + " ", end="")  # Imprime el número con un espacio
                print(f"\033[92m{board[i][j]}\033[0m", end=" ")


# Falta comentarios
def get_least_options_cell(board):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                options = sum(1 for num in range(1, CUADRADO + 1)
                              if es_valido(board, row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
    return best_cell, min_options


def branch_and_bound(tablero, generando=False):
    empty_location, min_options = get_least_options_cell(tablero)
    if empty_location is None:
        return True  # Si no hay celdas vacías, se encontró una solución

    # min_options == 0:, significa que hay al menos una celda que no puede ser llenada
    # con ningún número válido, lo que implica que el tablero en su estado actual
    # no puede llevar a una solución válida. Por lo tanto, la función retorna
    # False para indicar que esta rama del algoritmo de búsqueda no puede conducir
    # a una solución válida y debe ser descartada.
    if min_options == 0:
        return False

    row, col = empty_location

    # Intentar números del 1 al 9
    for num in range(1, CUADRADO + 1):
        if es_valido(tablero, row, col, num):
            # if generando == False: print_board(tablero)
            tablero[row][col] = num

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound(tablero, generando):
                return True

            # Deshacer la asignación (backtrack)
            tablero[row][col] = 0
            # if generando == False: print_board(tablero)

    return False


def es_valido(board, row, col, num):
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


# Falta comentarios
def back_tracking(tablero):
    for fila in range(CUADRADO):
        # print_board(tablero)
        for columna in range(CUADRADO):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                for num in numeros:
                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if back_tracking(tablero):
                            return tablero
                        tablero[fila][columna] = 0
                return False
    return True


def eliminar_numeros(tablero, numeros_eliminar):
    casillas = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(casillas)
    for i in range(numeros_eliminar):
        fila, columna = casillas[i]
        tablero[fila][columna] = 0
    return tablero


def generate_valid_sudoku(dificultad, algoritmo):
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

    # Crea el tablero con el algoritmo elegido
    if algoritmo == 1:
        # Tablero generado con backtracking
        back_tracking(board)
    else:
        # Tablero generado con branch and bound
        branch_and_bound(board, generando=True)

    # Eliminar números para generar tablero con dificultad
    eliminar_numeros(board, numeros_eliminar)
    return board


def valid_input(prompt, valid_choices):
    while True:
        try:
            choice = int(input(prompt))
            if choice not in valid_choices:
                raise ValueError("Opción no válida.")
            return choice
        except ValueError:
            print("Error, elige bien las opciones!")


def uniTest():
    algoritmo = 1
    dificultad = 3
    modo = 2

    # Genera un tablero válido con solución garantizada
    # board = generate_valid_sudoku(dificultad, algoritmo)
    board = medir_tiempo_ejecucion(
        generate_valid_sudoku, dificultad, algoritmo)

    if modo == 1:
        print('resolvelo vos capo')
    else:
        # Resuelve el Sudoku con el algoritmo seleccionado
        if algoritmo == 1:
            # medir_tiempo_ejecucion(back_tracking(board))
            medir_tiempo_ejecucion(back_tracking, board)
        else:
            # Implementar algoritmo Branch and Bound si es necesario
            # medir_tiempo_ejecucion(branch_and_bound(board))
            medir_tiempo_ejecucion(branch_and_bound, board)
        # print_board(board)
    quit()


def main():
    uniTest()  # Para no volvernos locos
    algoritmo = valid_input(
        "Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n", [1, 2])

    dificultad = valid_input(
        "Ingrese la dificultad del Sudoku \n 1. Fácil \n 2. Medio \n 3. Difícil \n", [1, 2, 3])

    # Genera un tablero válido con solución garantizada
    board = generate_valid_sudoku(dificultad, algoritmo)
    # print_board(board)

    modo = valid_input(
        "Ingrese el modo de reseolver el juego \n 1. Manual \n 2. Automatico AI \n", [1, 2])

    if modo == 1:
        print('resolvelo vos capo')
    else:
        # Resuelve el Sudoku con el algoritmo seleccionado
        if algoritmo == 1:
            back_tracking(board)
        else:
            # Implementar algoritmo Branch and Bound si es necesario
            branch_and_bound(board)
        print_board(board)


if __name__ == '__main__':
    main()
