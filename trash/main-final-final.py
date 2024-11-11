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

    return resultado


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


# Falta comentarios
def get_least_options_cell(tablero):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if tablero[row][col] == 0:
                options = sum(1 for num in range(1, CUADRADO + 1)
                              if es_valido(tablero, row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
    return best_cell, min_options


def branch_and_bound(tablero, generando=False):
    # if generando == False: print_tablero(tablero)
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
            tablero[row][col] = num

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound(tablero, generando):
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

    # if generando == False: print_tablero(tablero)

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
        back_tracking(tablero, generando=True)
    else:
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
    algoritmo = 1
    dificultad = 3
    modo = 2

    # Genera un tablero válido con solución garantizada
    # tablero = generate_valid_sudoku(dificultad, algoritmo)
    # print('BT')
    # tablero = medir_tiempo_ejecucion(
    #     generate_valid_sudoku, dificultad, algoritmo)
    

    # print('BB')
    # # algoritmo = 2
    # tablero = medir_tiempo_ejecucion(
    #     generate_valid_sudoku, dificultad, algoritmo)
    
    # tablero = [[4, 2, 0, 9, 0, 3, 8, 0, 6], [9, 1, 0, 0, 8, 0, 2, 0, 4], [6, 0, 3, 0, 5, 0, 0, 0, 9], [0, 7, 1, 0, 4, 0, 6, 9, 0], [
    # 3, 0, 9, 0, 2, 6, 0, 8, 5], [0, 0, 0, 0, 9, 0, 3, 0, 0], [0, 9, 0, 0, 6, 0, 4, 0, 0], [1, 0, 0, 0, 0, 9, 5, 0, 0], [7, 0, 4, 5, 0, 8, 0, 0, 0]]
    # print('BT')
    # medir_tiempo_ejecucion(back_tracking, tablero)
    
    # tablero = [[4, 2, 0, 9, 0, 3, 8, 0, 6], [9, 1, 0, 0, 8, 0, 2, 0, 4], [6, 0, 3, 0, 5, 0, 0, 0, 9], [0, 7, 1, 0, 4, 0, 6, 9, 0], [
    #     3, 0, 9, 0, 2, 6, 0, 8, 5], [0, 0, 0, 0, 9, 0, 3, 0, 0], [0, 9, 0, 0, 6, 0, 4, 0, 0], [1, 0, 0, 0, 0, 9, 5, 0, 0], [7, 0, 4, 5, 0, 8, 0, 0, 0]]
    # print('BB')
    # medir_tiempo_ejecucion(branch_and_bound, tablero)
    
    # print('---------------------------------')

    # tablero = [[0, 3, 5, 0, 0, 2, 0, 0, 9], [0, 4, 0, 8, 3, 0, 0, 0, 2], [7, 0, 0, 0, 0, 9, 0, 1, 6], [0, 9, 0, 1, 0, 7, 2, 3, 8], [
    #     0, 0, 7, 0, 8, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 5, 0, 7], [0, 0, 0, 4, 0, 5, 0, 7, 3], [0, 0, 1, 7, 0, 3, 9, 2, 4], [4, 7, 3, 0, 0, 8, 0, 6, 0]]
    # print('BT')
    # medir_tiempo_ejecucion(back_tracking, tablero)
    
    # tablero = [[0, 3, 5, 0, 0, 2, 0, 0, 9], [0, 4, 0, 8, 3, 0, 0, 0, 2], [7, 0, 0, 0, 0, 9, 0, 1, 6], [0, 9, 0, 1, 0, 7, 2, 3, 8], [
    #     0, 0, 7, 0, 8, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 5, 0, 7], [0, 0, 0, 4, 0, 5, 0, 7, 3], [0, 0, 1, 7, 0, 3, 9, 2, 4], [4, 7, 3, 0, 0, 8, 0, 6, 0]]
    # print('BB')
    # medir_tiempo_ejecucion(branch_and_bound, tablero)
    # print('---------------------------------')
    
    # tablero = [[0, 2, 0, 5, 3, 0, 0, 8, 4], [0, 0, 3, 6, 0, 9, 2, 0, 0], [0, 0, 0, 0, 2, 7, 0, 0, 3], [0, 0, 0, 0, 2, 7, 0, 0, 3], [0, 0, 0, 0, 0, 6, 0, 0, 0], [
    #     0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 4, 8, 0, 0, 0, 1, 0, 6], [4, 5, 0, 0, 0, 0, 3, 0, 8], [9, 8, 0, 0, 0, 0, 0, 6, 1], [7, 0, 0, 0, 0, 5, 4, 0, 9]]
    # print('BT')
    # medir_tiempo_ejecucion(back_tracking, tablero)
    
    # tablero = [[0, 2, 0, 5, 3, 0, 0, 8, 4], [0, 0, 3, 6, 0, 9, 2, 0, 0], [0, 0, 0, 0, 2, 7, 0, 0, 3], [0, 0, 0, 0, 2, 7, 0, 0, 3], [0, 0, 0, 0, 0, 6, 0, 0, 0], [
    #     0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 4, 8, 0, 0, 0, 1, 0, 6], [4, 5, 0, 0, 0, 0, 3, 0, 8], [9, 8, 0, 0, 0, 0, 0, 6, 1], [7, 0, 0, 0, 0, 5, 4, 0, 9]]
    # print('BB')
    # medir_tiempo_ejecucion(branch_and_bound, tablero)
    # print('---------------------------------')
    
    # tablero = [[0, 8, 0, 0, 0, 3, 2, 0, 0], [4, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 7, 2, 4, 0, 0, 1, 0], [9, 0, 0, 4, 1, 0, 8, 0, 0], [
    #     0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 9], [3, 0, 0, 8, 9, 0, 1, 0, 0], [0, 6, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0]]
    # print('BT')
    # medir_tiempo_ejecucion(back_tracking, tablero)
    
    # tablero = [[0, 8, 0, 0, 0, 3, 2, 0, 0], [4, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 7, 2, 4, 0, 0, 1, 0], [9, 0, 0, 4, 1, 0, 8, 0, 0], [
    #     0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 9], [3, 0, 0, 8, 9, 0, 1, 0, 0], [0, 6, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0]]
    # print('BB')
    # medir_tiempo_ejecucion(branch_and_bound, tablero)
    # print('---------------------------------')

    # tablero = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 9, 0, 0, 6, 0], [0, 0, 4, 0, 0, 5, 0, 0, 2], [0, 0, 2, 0, 0, 8, 0, 0, 1], [7, 3, 0, 0, 0, 0, 0, 0, 0],
    #            [1, 0, 0, 0, 0, 9, 3, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 3], [0, 0, 9, 0, 4, 0, 0, 0, 5], [0, 4, 7, 0, 6, 0, 2, 0, 0]]
    # print('BT')
    # medir_tiempo_ejecucion(back_tracking, tablero)
    
    # tablero = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 9, 0, 0, 6, 0], [0, 0, 4, 0, 0, 5, 0, 0, 2], [0, 0, 2, 0, 0, 8, 0, 0, 1], [7, 3, 0, 0, 0, 0, 0, 0, 0],
    #            [1, 0, 0, 0, 0, 9, 3, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 3], [0, 0, 9, 0, 4, 0, 0, 0, 5], [0, 4, 7, 0, 6, 0, 2, 0, 0]]
    # print('BB')
    # medir_tiempo_ejecucion(branch_and_bound, tablero)

    print('---------------------------------')
    print('RANDOM')
    # tablero = generate_valid_sudoku(dificultad, algoritmo)
    
    # tablero = [[9, 0, 0, 6, 0, 0, 2, 0, 8], [0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [6, 8, 0, 0, 0, 0, 0, 0, 0], [
    #     0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 7, 3], [7, 5, 9, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 5]]
    
    tablero = [[0, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 6, 7, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [
        0, 0, 7, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0], [9, 0, 0, 4, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0]] 
    tablero_save = [row[:] for row in tablero]
    tablero_save2 = [row[:] for row in tablero]
    print(tablero_save2)
    print('---------------------------------')

    print('BT')
    movimientos = [0]  # Iniciar contador en una lista

    medir_tiempo_ejecucion(back_tracking, tablero, movimientos=movimientos)
    print("Número de movimientos:", movimientos[0])

    print('BB')
    medir_tiempo_ejecucion(branch_and_bound, tablero_save)
    

    

    quit()


def main():
    uniTest()  # Para no volvernos locos
    algoritmo = valid_input(
        "Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n", [1, 2])

    dificultad = valid_input(
        "Ingrese la dificultad del Sudoku \n 1. Fácil \n 2. Medio \n 3. Difícil \n", [1, 2, 3])

    # Genera un tablero válido con solución garantizada
    tablero = generate_valid_sudoku(dificultad, algoritmo)
    # print_tablero(tablero)

    modo = valid_input(
        "Ingrese el modo de reseolver el juego \n 1. Manual \n 2. Automatico AI \n", [1, 2])

    if modo == 1:
        print('resolvelo vos capo')
    else:
        # Resuelve el Sudoku con el algoritmo seleccionado
        if algoritmo == 1:
            back_tracking(tablero)
        else:
            # Implementar algoritmo Branch and Bound si es necesario
            branch_and_bound(tablero)
        print_tablero(tablero)


if __name__ == '__main__':
    main()
