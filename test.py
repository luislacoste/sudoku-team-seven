import random

# Función para verificar si un número es válido en la posición (fila, columna)
def es_valido(tablero, fila, columna, num):
    # Verificar fila y columna
    for x in range(9):
        if tablero[fila][x] == num or tablero[x][columna] == num:
            return False
    # Verificar el subtablero de 3x3
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (columna // 3)
    for i in range(3):
        for j in range(3):
            if tablero[inicio_fila + i][inicio_col + j] == num:
                return False
    return True

# Función recursiva de Backtracking para llenar el tablero
def llenar_tablero(tablero):
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:
                numeros = list(range(1, 10))
                random.shuffle(numeros)  # Mezcla para mayor variabilidad
                for num in numeros:
                    if es_valido(tablero, fila, columna, num):
                        tablero[fila][columna] = num
                        if llenar_tablero(tablero):
                            return True
                        tablero[fila][columna] = 0
                return False
    return True

# Elimina números aleatoriamente para crear el tablero incompleto
def eliminar_numeros(tablero, vacios=40):
    casillas = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(casillas)
    for i in range(vacios):
        fila, columna = casillas[i]
        tablero[fila][columna] = 0

# Genera un tablero de Sudoku completo y luego le quita números
def generar_sudoku(vacios=40):
    tablero = [[0 for _ in range(9)] for _ in range(9)]
    llenar_tablero(tablero)
    eliminar_numeros(tablero, vacios)
    return tablero

# Imprime el tablero en un formato legible
def imprimir_tablero(tablero):
    for fila in range(9):
        print(" ".join(str(num) if num != 0 else '.' for num in tablero[fila]))

# Genera un tablero de Sudoku y lo imprime
tablero_sudoku = generar_sudoku()
imprimir_tablero(tablero_sudoku)



def is_safe(board, row, col, num):
    # Verifica que la celda no contenga numero
    if board[row][col] != 0:
        return False
    # Verificar fila
    if num in board[row]:
        return False

    # Verificar columna
    for r in range(9):
        if board[r][col] == num:
            return False

    # Verificar subcuadro
    start_row = row - row % 3
    start_col = col - col % 3
    for r in range(3):
        for c in range(3):
            if board[start_row + r][start_col + c] == num:
                return False

    return True


def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Busca una celda vacía
                for num in range(1, 9 + 1):
                    if is_safe(board, row, col, num):
                        board[row][col] = num  # Asigna el número
                        
                        if solve_sudoku(board):
                            return True
                        # Deshace la asignación (backtrack)
                        board[row][col] = 0
                        
                return False
    return True


print(solve_sudoku(tablero_sudoku))

