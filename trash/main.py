import random

# Tamaño del tablero
tamaño_tablero = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3


def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


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


def solve_sudoku(board):
    for row in range(tamaño_tablero):
        for col in range(tamaño_tablero):
            if board[row][col] == 0:  # Busca una celda vacía
                for num in range(1, tamaño_tablero + 1):
                    if is_safe(board, row, col, num):
                        board[row][col] = num  # Asigna el número
                        if solve_sudoku(board):
                            return True
                        # Deshace la asignación (backtrack)
                        board[row][col] = 0
                return False
    return True


def generate_sudoku(dificultad):
    board = [[0] * tamaño_tablero for _ in range(tamaño_tablero)]
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)
    # Llenar algunas celdas al azar para iniciar la resolución
    for _ in range(numeros_completos):  # Rellenar entre 16 y 32 celdas
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
  dificultad = int(input("Ingrese la dificultad del Sudoku \n 1. Facil \n 2. Medio \n 3. Dificil \n"))
  # Generar y resolver un tablero de Sudoku
  sudoku_board = generate_sudoku(dificultad)
  print("Tablero de Sudoku inicial:")
  print(sudoku_board)
  # print_board(sudoku_board)

  if solve_sudoku(sudoku_board):
      print("\nTablero de Sudoku resuelto:")
      print_board(sudoku_board)
  else:
      print("No se pudo resolver el Sudoku.")


if __name__ == "__main__":
    main()