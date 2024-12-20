import random
import os
import time
import pprint_bb
# Tamaño del tablero
CUADRADO = 9

# Tamaño de cada subcuadro
SUBCUADRO = 3

CONTADOR = [0]


def print_tablero(tablero, borrar_pantalla=True):
    time.sleep(0.07)  # Pausar para visualizar el progreso
    if borrar_pantalla:
        os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla

    # Imprimir el contador en la esquina superior derecha
    if CONTADOR[0] > 0:
        print(f"Contador de movimientos: {CONTADOR[0]}\n")

    for i in range(len(tablero)):
        if i % 3 == 0 and i != 0:
            print("------------------------")  # Separación de subcuadros

        for j in range(len(tablero[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")  # Separación de subcuadros en columnas

            # Aplicar color verde si el número no es cero
            if tablero[i][j] != 0:
                print(f"\033[92m{tablero[i][j]}\033[0m",
                      end=" " if j != 8 else "\n")
            else:
                print("0", end=" " if j != 8 else "\n")


def resuelve_manual(tablero):
    termino = True
    while termino:
        print_tablero(tablero, False)
        fila = int(input("Ingrese la fila: ")) - 1
        columna = int(input("Ingrese la columna: ")) - 1

        # Verifica que las coordenadas estén dentro de los límites y que la casilla esté vacía (0).
        if fila < 0 or fila >= CUADRADO or columna < 0 or columna >= CUADRADO or tablero[fila][columna] != 0:
            print("Movimiento inválido, intente de nuevo.")
            continue

        numero = int(input("Ingrese el número: "))
        if es_valido(tablero, fila, columna, numero):
            tablero[fila][columna] = numero
        else:
            print("Movimiento inválido, intente de nuevo.")
        if all(all(num != 0 for num in row) for row in tablero):
            print_tablero(tablero)
            print("¡Felicidades! Has resuelto el Sudoku.")
            termino = False


def get_least_options_cell(tablero):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            # Recorre cada celda del tablero para encontrar una vacía (con valor 0).
            if tablero[row][col] == 0:
                # Cuenta las opciones válidas para esta celda.
                options = sum(1 for num in range(1, CUADRADO + 1)
                              if es_valido(tablero, row, col, num))

                # Si esta celda tiene menos opciones, actualiza el número mínimo y la celda.
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)

                # Poda: si encontramos una celda con solo una opción, la seleccionamos inmediatamente
                if min_options == 1:
                    return best_cell, min_options

    return best_cell, min_options


def branch_and_bound(tablero):
    CONTADOR[0] += 1
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


# Verifica si el número es válido en la posición dada, sin violar las reglas de Sudoku.
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
        CONTADOR[0] += 1
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
            
def generate_manual():
    while True:
        tablero = [[0 for i in range(9)] for j in range(9)]
        print("Ingrese el tablero de Sudoku, si desea dejar una casilla vacía, ingrese 0")
        for i in range(9):
            fila = input(f"Ingrese la fila {i + 1}: ")
            if len(fila) != 9:
                print("Error, la fila debe tener 9 elementos")
                return generate_manual()
            for j in range(9):
                try:
                    tablero[i][j] = int(fila[j])
                except ValueError:
                    print("Error, ingrese solo números")
                    return generate_manual()
        tablero_copia = [row[:] for row in tablero]
        if(back_tracking(tablero_copia, True)):
            return tablero
        else:
            print("Tablero inválido, intente de nuevo")

def main():
    generacion = valid_input(
        "Ingrese el modo de generación del Sudoku \n 1. Generación aleatoria \n 2. Generación manual \n", [1, 2])
    
    if(generacion == 1):
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
            tablero_copia = [row[:] for row in tablero]
        else:
            # Genera un tablero válido con solución garantizada
            tablero = generate_valid_sudoku(dificultad)
    else:
        tablero = generate_manual()
        dificultad = 1

    os.system('clear' if os.name == 'posix' else 'cls')
    print("---Tablero a resolver--- \n")
    print_tablero(tablero, False)
    print("\n")
    if dificultad != 4:
        modo = valid_input(
            "Ingrese el modo de resolver el juego \n 1. Manual \n 2. Automatico AI \n", [1, 2])
        if modo == 1:
            resuelve_manual(tablero)
            return
        algoritmo = valid_input(
            "Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n", [1, 2])
    else:
        if bt_o_bb == 1:
            input("Presione enter para resolver con Branch & Bound")
            tiempo_inicio = time.time()
            branch_and_bound(tablero_copia)
            tiempo_final = time.time()
            print(f"Tiempo de resolucion con Branch & Bound: {
                  tiempo_final - tiempo_inicio}")
            input("Presione enter para resolver con Backtracking")
        else:
            input("Presione enter para resolver con Backtracking")
            tiempo_inicio = time.time()
            back_tracking(tablero_copia)
            tiempo_final = time.time()
            print(f"Tiempo de resolucion con Backtracking: {
                  tiempo_final - tiempo_inicio}")
            input("Presione enter para resolver con Branch & Bound")
        CONTADOR[0] = 0
        algoritmo = bt_o_bb
        modo = 2

    # Resuelve el Sudoku con el algoritmo seleccionado
    if algoritmo == 1:
        back_tracking(tablero)
    else:
        como_imprimir = valid_input(
            "Ingrese como quiere ver el tablero \n 1. Normal \n 2. Avanzado \n", [1, 2])
        # Implementar algoritmo Branch and Bound si es necesario
        if como_imprimir == 1:
            branch_and_bound(tablero)
        else:
            pprint_bb.branch_and_bound_sudoku(tablero)
    print_tablero(tablero)


if __name__ == '__main__':
    while True:
        main()
        if input("¿Desea jugar de nuevo? (s/n): ").lower() != 's':
            break
        os.system('clear' if os.name == 'posix' else 'cls')
