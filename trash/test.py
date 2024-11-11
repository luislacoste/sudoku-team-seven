import random
import os
import time
import heapq

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


def get_least_options_cell(board):
    heap = []
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                options = sum(1 for num in range(1, CUADRADO + 1)
                              if es_valido(board, row, col, num))
                # Push (options, (row, col)) to the heap
                heapq.heappush(heap, (options, (row, col)))

    # Pop the least option cell
    if heap:
        return heapq.heappop(heap)[1], heap[0][0]
    return None, None


def branch_and_bound(tablero, generando=False):
    # Find the next cell with the least options
    empty_location, min_options = get_least_options_cell(tablero)

    # If no empty cells are found, solution is found
    if empty_location is None:
        return True

    # If there are no valid options for this cell, return False (pruning)
    if min_options == 0:
        return False

    row, col = empty_location

    # Try numbers from 1 to 9
    for num in range(1, CUADRADO + 1):
        if es_valido(tablero, row, col, num):
            tablero[row][col] = num

            # Recursive call to fill the next cell
            if branch_and_bound(tablero, generando):
                return True

            # Backtrack if no solution is found
            tablero[row][col] = 0

    return False


def es_valido(tablero, row, col, num):
    # Verifica que la celda no contenga numero
    if tablero[row][col] != 0:
        return False
    # Verificar fila
    if num in tablero[row]:
        return False
    # Verificar columna
    for r in range(CUADRADO):
        if tablero[r][col] == num:
            return False

    # Verificar subcuadro
    start_row = row - row % SUBCUADRO
    start_col = col - col % SUBCUADRO
    for r in range(SUBCUADRO):
        for c in range(SUBCUADRO):
            if tablero[start_row + r][start_col + c] == num:
                return False
    return True


# Falta comentarios
def back_tracking(tablero, generando=False):
    for fila in range(CUADRADO):
        for columna in range(CUADRADO):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                for num in numeros:

                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if back_tracking(tablero, generando):
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


def generate_valid_sudoku_bt():
    # Generar tablero vacío lista de listas
    tablero = [[0] * CUADRADO for _ in range(CUADRADO)]

    numeros_eliminar = 11

    back_tracking(tablero, generando=True)

    # Eliminar números para generar tablero con dificultad
    eliminar_numeros(tablero, numeros_eliminar)
    print(tablero)
    return tablero


def generate_valid_sudoku_bb():
    # Generar tablero vacío lista de listas
    tablero = [[0] * CUADRADO for _ in range(CUADRADO)]

    numeros_eliminar = 71

    # Tablero generado con branch and bound
    branch_and_bound(tablero, generando=True)

    # Eliminar números para generar tablero con dificultad
    eliminar_numeros(tablero, numeros_eliminar)
    return tablero


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

    # Genera un tablero válido con solución garantizada
    # tablero = generate_valid_sudoku(dificultad, algoritmo)
    print('BT')
    tablero = medir_tiempo_ejecucion(
        generate_valid_sudoku_bt)

    print('BB')
    tablero = medir_tiempo_ejecucion(
        generate_valid_sudoku_bb)

    print('---------------------------------')

    tablero = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 9, 0, 0, 6, 0],
               [0, 0, 4, 0, 0, 5, 0, 0, 2],
               [0, 0, 2, 0, 0, 8, 0, 0, 1],
               [7, 3, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 9, 3, 0, 0],
               [0, 0, 0, 0, 7, 0, 0, 0, 3],
               [0, 0, 9, 0, 4, 0, 0, 0, 5],
               [0, 4, 7, 0, 6, 0, 2, 0, 0]]
    print('BT')
    # Resuelve el Sudoku con el algoritmo seleccionado
    # if algoritmo == 1:
    # medir_tiempo_ejecucion(back_tracking(tablero))
    medir_tiempo_ejecucion(back_tracking, tablero)


    tablero = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 9, 0, 0, 6, 0],
            [0, 0, 4, 0, 0, 5, 0, 0, 2],
            [0, 0, 2, 0, 0, 8, 0, 0, 1],
            [7, 3, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 9, 3, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 3],
            [0, 0, 9, 0, 4, 0, 0, 0, 5],
            [0, 4, 7, 0, 6, 0, 2, 0, 0]]
    print('BB')
    # else:
    # Implementar algoritmo Branch and Bound si es necesario
    # medir_tiempo_ejecucion(branch_and_bound(tablero))
    medir_tiempo_ejecucion(branch_and_bound, tablero)
    # print_tablero(tablero)
    quit()


def main():
    uniTest()  # Para no volvernos locos


if __name__ == '__main__':
    main()
