import random


# facil <= 7
# medio = a 5
# Tamaño del tablero
TAB_N = 9
# Tamaño de cada subcuadro (2x4 en este caso)
SUB_TAB_N = 3


def print_board(tabla):
    for row in tabla:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


def is_safe(tabla, row, col, num):
    # Verificar fila
    if num in tabla[row]:
        return False

    # Verificar columna
    for r in range(TAB_N):
        if tabla[r][col] == num:
            return False

    # Verificar subcuadro
    start_row = row - row % SUB_TAB_N
    start_col = col - col % SUB_TAB_N
    for r in range(SUB_TAB_N):
        for c in range(SUB_TAB_N):
            if tabla[start_row + r][start_col + c] == num:
                return False

    return True


def solve_sudoku(tabla):
    for row in range(TAB_N):
        for col in range(TAB_N):
            if tabla[row][col] == 0:  # Busca una celda vacía
                for num in range(1, TAB_N + 1):
                    if is_safe(tabla, row, col, num):
                        tabla[row][col] = num  # Asigna el número
                        if solve_sudoku(tabla):
                            return True
                        # Deshace la asignación (backtrack)
                        tabla[row][col] = 0
                return False
    return True


def generar_random(tabla):
    # Llenar algunas celdas al azar para iniciar la resolución
    for _ in range(random.randint(16, 32)):  # Rellenar entre 16 y 32 celdas
        row = random.randint(0, TAB_N - 1)
        col = random.randint(0, TAB_N - 1)
        num = random.randint(1, TAB_N)
        while not is_safe(tabla, row, col, num):
            row = random.randint(0, TAB_N - 1)
            col = random.randint(0, TAB_N - 1)
            num = random.randint(1, TAB_N)
        tabla[row][col] = num
    return tabla


def generar_custom(tabla):
    # dejamos al usuario gelejir 10 celdas a rellenar aleatoriamente
    for _ in range(10):
        row = random.randint(0, TAB_N - 1)
        col = random.randint(0, TAB_N - 1)
        num = int(input("Ingrese el número: "))
        while num <= 1 or num > 9:
            num = int(input("Ingrese el número: "))

        tabla[row][col] = num

    return tabla


def generate_sudoku(generar_metodo):
    tabla = [[0] * TAB_N for _ in range(TAB_N)]

    if generar_metodo == 1:

        # Generar un tablero de Sudoku
        tabla = generar_random(tabla)
    elif generar_metodo == 2:
        # Generar un tablero de Sudoku
        tabla = generar_custom(tabla)

    return tabla


def generar_tablero():
    return [[0] * TAB_N for _ in range(TAB_N)]



def main():

    ## @TODO arreglar esta logica de mierda de validacion
    dificultad = 0
    while dificultad != 1 and dificultad != 2 and dificultad != 3:
        dificultad = int(
            input("Ingrese la dificultad del sudoku \n 1: Facil\n 2: Medio\n 3: Dificil: "))
        
    if dificultad == 1:
        tablero = generar_tablero()
    elif dificultad == 2:
        tablero = generar_tablero()
    elif dificultad == 3:
        tablero = generar_tablero()

    generar_metodo = 0
    while generar_metodo != 1 and generar_metodo != 2:
        generar_metodo = int(input(
            "Ingrese el método de generación de tablero de Sudoku (1: Aleatorio, 2: Personalizado): "))

    sudoku_board = generate_sudoku(generar_metodo)
    print("Tablero de Sudoku inicial:")
    print_board(sudoku_board)

    if solve_sudoku(sudoku_board):
        print("\nTablero de Sudoku resuelto:")
        print_board(sudoku_board)
    else:
        print("No se pudo resolver el Sudoku.")


if __name__ == "__main__":
    main()
