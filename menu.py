import random

# Tamaño del tablero
CUADRADO = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3


def is_safe(board, row, col, num):
    # Verifica que la celda no contenga numero
    if board[row][col] != 0:
        return False
    # Verificar fila
    if num in board[row]:
        return False

    # Verificar columna
    for r in range(tamaño_tablero):
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
    for i in range(CUADRADO):
        print("Ingrese la fila", i + 1, "del tablero (9 numeros juntos sin repetir)")
        row = list(map(int, input().split()))
        board.append(row)
    return board


def auto_gen_board(dificultad):
    board = [[0] * CUADRADO for _ in range(CUADRADO)]
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)

    # Llenar algunas celdas al azar para iniciar la resolución
    for _ in range(numeros_completos):  # Rellenar entre 16 y 32 celdas
        row = random.randint(0, CUADRADO - 1)
        col = random.randint(0, CUADRADO - 1)
        num = random.randint(1, CUADRADO)
        while not is_safe(board, row, col, num):
            row = random.randint(0, CUADRADO - 1)
            col = random.randint(0, CUADRADO - 1)
            num = random.randint(1, CUADRADO)
        board[row][col] = num
    return board

def generar_tablero(modo, dificultad, algoritmo):
    if modo == 1:
        board = user_gen_board()
        ## Tenemos que resolver de punta a punta el board con algun algo para
        ##  ver si se puede o no resolver
        ##is_board_valid = validate_board(board)
    else:
        if(algoritmo == 1):
            board = auto_gen_board(dificultad)
        else:
            board = auto_gen_board_bt(dificultad)

def main():
    algoritmo = int(input("Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n"))
    while algoritmo != 1 and algoritmo != 2:
        if algoritmo != 1 and algoritmo != 2:
            print("Ingrese una opcion valida")
        algoritmo = int(input("Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n"))
    modo = int(input(
        "Ingrese el modo de juego \n 1. Ingresar Tablero \n 2. Tablero auto-generado \n "))
    while modo != 1 and modo != 2:
        if modo != 1 and modo != 2:
            print("Ingrese una opcion valida")
        modo = int(input(
            "Ingrese el modo de juego \n 1. Ingresar Tablero \n 2. Tablero auto-generado \n "))
    if modo == 1:
        board = generar_tablero(modo, 0)
    if modo == 2:
        dificultad = int(input(
        "Ingrese la dificultad del Sudoku \n 1. Facil \n 2. Medio \n 3. Dificil \n"))
        while dificultad != 1 and dificultad != 2 and dificultad != 3:
            if dificultad != 1 and dificultad != 2 and dificultad != 3:
                print("Ingrese una opcion valida")
            dificultad = int(input(
                "Ingrese la dificultad del Sudoku \n 1. Facil \n 2. Medio \n 3. Dificil \n"))
        board = generar_tablero(modo, dificultad, algoritmo)
    resolucion = int(input(
        "Ingrese el metodo de resolucion \n 1. Resolver manual \n 2. Resolver automatico (AI) \n"))
    while resolucion != 1 and resolucion != 2:
        if resolucion != 1 and resolucion != 2:
            print("Ingrese una opcion valida")
        resolucion = int(input(
            "Ingrese el metodo de resolucion \n 1. Resolver manual \n 2. Resolver automatico (AI) \n"))
    if resolucion == 1:
        print("Resolver manual")
    else:
        resolver_auto_bt(board)
        resolver_auto_bb(board)

if __name__ == '__main__':
    main()
