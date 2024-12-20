import random
import os
import time

# Tamaño del tablero
CUADRADO = 9

# Tamaño de cada subcuadro
SUBCUADRO = 3

movimientos = 0


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

    return tiempo_ejecucion


def print_tablero(tablero):
    time.sleep(0.03)  # Pausar para visualizar el progreso

    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for i in range(len(tablero)):
        if i % 3 == 0 and i != 0:
            print("------------------------")  # Separación de subcuadros

        for j in range(len(tablero[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")  # Separación de subcuadros en columnas
            if j == 8:
                print(f"\033[92m{tablero[i][j]}\033[0m")  # Fin de la fila
            else:
                # print(str(tablero[i][j]) + " ", end="")  # Imprime el número con un espacio
                print(f"\033[92m{tablero[i][j]}\033[0m", end=" ")


# # Falta comentarios
# def get_least_options_cell(tablero):
#     min_options = CUADRADO + 1
#     best_cell = None
#     for row in range(CUADRADO):
#         for col in range(CUADRADO):
#             if tablero[row][col] == 0:
#                 options = 0
#                 for num in range(1, CUADRADO + 1):
#                     if es_valido(tablero, row, col, num):
#                         options += 1
#                 if options < min_options:
#                     min_options = options
#                     best_cell = (row, col)
#     return best_cell, min_options


def get_least_options_cell(tablero):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if tablero[row][col] == 0:
                options = sum(1 for num in range(1, CUADRADO + 1) if es_valido(tablero, row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
                # Poda: si encontramos una celda con solo una opción, la seleccionamos inmediatamente
                if min_options == 1:
                    return best_cell, min_options
    return best_cell, min_options


# def get_least_options_cell(tablero, rows_options, cols_options, subgrids_options):
#     min_options = CUADRADO + 1
#     best_cell = None
#     for row in range(CUADRADO):
#         for col in range(CUADRADO):
#             if tablero[row][col] == 0:
#                 # Intersect the sets to find available numbers for this cell
#                 options = rows_options[row] & cols_options[col] & subgrids_options[(
#                     row // 3, col // 3)]
#                 num_options = len(options)

#                 if num_options < min_options:
#                     min_options = num_options
#                     best_cell = (row, col)

#                 # Early exit if we find a cell with only one option
#                 if min_options == 1:
#                     break
#     return best_cell, min_options


def branch_and_bound(tablero, movimientos=[0]):

    # all_numbers = set(range(1, CUADRADO + 1))
    # rows_options = [all_numbers.copy() for _ in range(CUADRADO)]
    # cols_options = [all_numbers.copy() for _ in range(CUADRADO)]
    # subgrids_options = {(i, j): all_numbers.copy()
    #                     for i in range(3) for j in range(3)}

    # # Initialize by removing numbers already present in the board from options sets
    # for row in range(CUADRADO):
    #     for col in range(CUADRADO):
    #         num = tablero[row][col]
    #         if num != 0:
    #             rows_options[row].discard(num)
    #             cols_options[col].discard(num)
    #             subgrids_options[(row // 3, col // 3)].discard(num)

    # empty_location, min_options = get_least_options_cell(
    #     tablero, rows_options, cols_options, subgrids_options)

    empty_location, min_options = get_least_options_cell(tablero)
    if empty_location is None:
        return True  # Si no hay celdas vacías, se encontró una solución

    if min_options == 0:
        return False

    row, col = empty_location

    # Intentar números del 1 al 9
    for num in range(1, CUADRADO + 1):

        if es_valido(tablero, row, col, num):
            tablero[row][col] = num
            movimientos[0] += 1

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound(tablero, movimientos):
                return True

            # Deshacer la asignación (backtrack)
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
def back_tracking(tablero, generando=False, movimientos=[0]):

    for fila in range(CUADRADO):
        for columna in range(CUADRADO):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                if generando:
                    random.shuffle(numeros)
                for num in numeros:
                    movimientos[0] += 1  # Incrementamos el contador

                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if back_tracking(tablero, generando, movimientos):
                            return tablero
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
    # Generar tablero vacío lista de listas
    tablero = [[0] * CUADRADO for _ in range(CUADRADO)]

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
        back_tracking(tablero, True)
    else:
        # Tablero generado con branch and bound
        branch_and_bound(tablero)

    # Eliminar números para generar tablero con dificultad
    eliminar_numeros(tablero, numeros_eliminar)
    return tablero


def generate_csv(data_frame):
    import csv
    with open('data.csv', mode='w') as file:
        writer = csv.writer(file)
        for row in data_frame:
            writer.writerow(row)


def uniTest():
    data_frame = [["Dificultad", "Backtracking", "Branch and Bound",
                   "Porcentaje BT", "Movimientos BT", "Movimientos BB", "Operaciones BB", "Contador"]]
    # 1 = Backtracking
    # 2 = Branch and Bound
    for i in range(1, 4):
        for x in range(1, 101):
            tablero = generate_valid_sudoku(i, 1)
            tablero_save = [row[:] for row in tablero]
            movimientos_bt = [0]
            moviemientos_bb = [0]
            operaciones_bb = [0]
            time1 = medir_tiempo_ejecucion(
                back_tracking, tablero, False, movimientos_bt)
            time2 = medir_tiempo_ejecucion(
                branch_and_bound, tablero_save, moviemientos_bb)

            if time1 < time2:
                porcentaje = ((time2 - time1) / time2) * 100
                # print("---------------------------------")
                # print(f"El tablero que demoro menos fue: Backtracking")
                # print(f"Fue un {porcentaje}% mas rapido")
                # print("---------------------------------")
            else:
                porcentaje = ((time1 - time2) / time1) * 100
                print("---------------------------------")
                print("El tablero que demoro menos fue: Branch and Bound")
                print(f"Fue un {porcentaje}% mas rapido")
                print("---------------------------------")
            data_frame.append(
                [i, time1, time2, ((time2 - time1) / time2) * 100, movimientos_bt, moviemientos_bb,operaciones_bb, x])
            print("---------------------------------")
    generate_csv(data_frame)


if __name__ == '__main__':
    uniTest()
