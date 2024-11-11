import random
import os
import time

# Tamaño del tablero
CUADRADO = 9

# Tamaño de cada subcuadro
SUBCUADRO = 3

movimientos = 0

def print_tablero(tablero, borrar_pantalla=True):
    time.sleep(0.07)  # Pausar para visualizar el progreso
    if borrar_pantalla:
        os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    
    for i in range(len(tablero)):
        if i % 3 == 0 and i != 0:
            print("------------------------")  # Separación de subcuadros

        for j in range(len(tablero[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")  # Separación de subcuadros en columnas

            # Apply green color if the number is not zero, otherwise print normally
            if tablero[i][j] != 0:
                print(f"\033[92m{tablero[i][j]}\033[0m", end=" " if j != 8 else "\n")
            else:
                print("0", end=" " if j != 8 else "\n")



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

def branch_and_bound(tablero):
    print_tablero(tablero)
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

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound(tablero):
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


def back_tracking(tablero, generando=False):
    if not generando:
        print_tablero(tablero)
        
    for fila in range(CUADRADO):
        for columna in range(CUADRADO):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                if generando:
                    random.shuffle(numeros)
                for num in numeros:
                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if back_tracking(tablero, generando):
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


def generate_valid_sudoku(dificultad):
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

    # Tablero generado con backtracking
    back_tracking(tablero, True)

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
            
            

def main():
    dificultad = valid_input(
        "Ingrese la dificultad del Sudoku \n 1. Fácil \n 2. Medio \n 3. Difícil \n 4. Ejemplos \n", [1, 2, 3, 4])


    if dificultad == 4:
        bt_o_bb = valid_input(
            "Ingrese el ejemplo complejo que quiera ver \n 1. Backtracking \n 2. Branch & Bound \n", [1, 2])
        if bt_o_bb == 1:
            tablero = [[0, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 6, 7, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [
                0, 0, 7, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0], [9, 0, 0, 4, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0]]
        else:
            tablero = [[9, 0, 0, 6, 0, 0, 2, 0, 8], [0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [6, 8, 0, 0, 0, 0, 0, 0, 0], [
                0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 7, 3], [7, 5, 9, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 5]]
    else:
        # Genera un tablero válido con solución garantizada
        tablero = generate_valid_sudoku(dificultad)
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Tablero a resolver:")
    print_tablero(tablero, False)
    
    if dificultad != 4:
        algoritmo = valid_input(
            "Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n", [1, 2])

        modo = valid_input(
            "Ingrese el modo de reseolver el juego \n 1. Manual \n 2. Automatico AI \n", [1, 2])
    else:
        algoritmo = bt_o_bb
        modo = 2

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
