import random
import time
import os

# Tamaño del tablero
tamaño_tablero = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for row in board:
        print(" ".join(f"\033[92m{num}\033[0m" if num != 0 else '.' for num in row))
    time.sleep(0.03)  # Pausar para visualizar el progreso

def is_safe(board, row, col, num):
    # Verifica que la celda no contenga número
    if board[row][col] != 0:
        return False
    # Verificar fila
    if num in board[row]:
        return False

    # Verificar columna
    if num in [board[r][col] for r in range(tamaño_tablero)]:
        return False

    # Verificar subcuadro
    start_row = row - row % SUBCUADRO
    start_col = col - col % SUBCUADRO
    for r in range(SUBCUADRO):
        for c in range(SUBCUADRO):
            if board[start_row + r][start_col + c] == num:
                return False

    return True

def get_empty_location(board):
    # Busca una celda vacía en el tablero
    for row in range(tamaño_tablero):
        for col in range(tamaño_tablero):
            if board[row][col] == 0:
                return row, col
    return None

def branch_and_bound_sudoku(board):
    empty_location = get_empty_location(board)
    if empty_location is None:
        return True  # Si no hay celdas vacías, se encontró una solución

    row, col = empty_location

    # Intentar números del 1 al 9
    for num in range(1, tamaño_tablero + 1):
        if is_safe(board, row, col, num):
            board[row][col] = num  # Asignar número
            print_board(board)  # Mostrar intento

            # Recursivamente llamar a la función para el siguiente paso
            if branch_and_bound_sudoku(board):
                return True
            
            # Deshacer la asignación (backtrack)
            board[row][col] = 0
            print_board(board)  # Mostrar retroceso

    return False

def generate_sudoku(dificultad):
    board = [[0] * tamaño_tablero for _ in range(tamaño_tablero)]
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)
    
    # Llenar algunas celdas al azar para iniciar la resolución
    for _ in range(numeros_completos):
        row = random.randint(0, tamaño_tablero - 1)
        col = random.randint(0, tamaño_tablero - 1)
        num = random.randint(1, tamaño_tablero)
        while not is_safe(board, row, col, num):
            row = random.randint(0, tamaño_tablero - 1)
            col = random.randint(0, tamaño_tablero - 1)
            num = random.randint(1, tamaño_tablero)
        board[row][col] = num

    return board

def main():
    dificultad = 3  # Puedes cambiar la dificultad si lo deseas
    # Generar y resolver un tablero de Sudoku
    sudoku_board = [[0, 0, 0, 3, 0, 0, 2, 0, 0], 
                    [0, 0, 0, 0, 0, 8, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 7], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 7, 2, 0, 1, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 9, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 4, 0, 7, 0]]
    
    print("Tablero de Sudoku inicial:")
    print_board(sudoku_board)

    if branch_and_bound_sudoku(sudoku_board):
        print("\nTablero de Sudoku resuelto:")
        print_board(sudoku_board)
    else:
        print("No se pudo resolver el Sudoku.")

if __name__ == "__main__":
    main()
