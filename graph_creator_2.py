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


def print_tablero(tablero):
    time.sleep(0.03)
    os.system('clear' if os.name == 'posix' else 'cls')
    for i in range(len(tablero)):
        if i % 3 == 0 and i != 0:
            print("------------------------")
        for j in range(len(tablero[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(f"\033[92m{tablero[i][j]}\033[0m")
            else:
                print(f"\033[92m{tablero[i][j]}\033[0m", end=" ")


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


def branch_and_bound(tablero):
    empty_location, min_options = get_least_options_cell(tablero)
    if empty_location is None:
        return True
    if min_options == 0:
        return False

    row, col = empty_location
    for num in range(1, CUADRADO + 1):
        if es_valido(tablero, row, col, num):
            tablero[row][col] = num
            if branch_and_bound(tablero):
                return True
            tablero[row][col] = 0
    return False


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
        back_tracking(tablero, True)
    else:
        branch_and_bound(tablero)
    eliminar_numeros(tablero, numeros_eliminar)
    return tablero


def generate_csv(data_frame):
    with open('data.csv', mode='w') as file:
        writer = csv.writer(file)
        for row in data_frame:
            writer.writerow(row)


def uniTest():
    data_frame = [["Dificultad", "Backtracking", "Branch and Bound",
                   "Porcentaje BT", "Movimientos BT", "Movimientos BB", "Operaciones BT", "Operaciones BB", "Contador"]]
    for i in range(1, 4):
        for x in range(1, 101):
            tablero = generate_valid_sudoku(i, 1)
            tablero_save = [row[:] for row in tablero]

            movimientos_bt = [0]
            operaciones_bt = [0]
            movimientos_bb = [0]
            operaciones_bb = [0]

            time1, _ = medir_tiempo_ejecucion(
                back_tracking, tablero, False, movimientos_bt, operaciones_bt)
            time2, _ = medir_tiempo_ejecucion(
                branch_and_bound, tablero_save, movimientos_bb, operaciones_bb)

            porcentaje_bt = ((time2 - time1) / time2) * 100 if time2 else 0
            data_frame.append(
                [i, time1, time2, porcentaje_bt, movimientos_bt[0], movimientos_bb[0], operaciones_bt[0], operaciones_bb[0], x])
            print(i,x)
            print("---------------------------------")
    generate_csv(data_frame)


if __name__ == '__main__':
    uniTest()
