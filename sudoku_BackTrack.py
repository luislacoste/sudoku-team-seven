import random
import os

# Tamaño del tablero
tamaño_tablero = 9
# Tamaño de cada subcuadro
SUBCUADRO = 3

def print_board(board):
    """Imprime el tablero de Sudoku con formato adecuado."""
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("------------------------")  # Separación de subcuadros
        
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")  # Separación de subcuadros en columnas
            if j == 8:
                print(board[i][j])  # Fin de la fila
            else:
                print(str(board[i][j]) + " ", end="")  # Imprime el número con un espacio

def find_empty_position(board):
    """Encuentra la siguiente posición vacía en el tablero con la menor cantidad de valores posibles."""
    empty_positions = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                possible_values = get_possible_values(board, i, j)
                empty_positions.append((i, j, len(possible_values)))  # Guardamos la cantidad de valores posibles
    # Si hay celdas vacías, devuelve la que tiene menos valores posibles
    if empty_positions:
        return min(empty_positions, key=lambda x: x[2])[:2]  # Devuelve (fila, columna)
    return None


def get_possible_values(board, row, col):
    """Devuelve una lista de valores válidos posibles para una celda."""
    possible_values = set(range(1, 10))

    # Verificar fila
    possible_values -= set(board[row])

    # Verificar columna
    possible_values -= {board[i][col] for i in range(9)}

    # Verificar subcuadro 3x3
    cube_x = col // 3
    cube_y = row // 3
    for i in range(cube_y * 3, cube_y * 3 + 3):
        for j in range(cube_x * 3, cube_x * 3 + 3):
            if board[i][j] != 0:
                possible_values.discard(board[i][j])

    return possible_values

def is_Valid(board, position, number):
    """Verifica si se puede colocar un número en la posición indicada."""
    row, col = position
    possible_values = get_possible_values(board, row, col)
    return number in possible_values

def solve_board(board):
    """Resuelve el Sudoku usando backtracking con optimización."""
    print_board(board)
    print("------------------------")
    empty_position = find_empty_position(board)

    # Caso base: si no hay posiciones vacías, el Sudoku está resuelto
    if not empty_position:
        return True
    else:
        row, col = empty_position

    # Obtener los valores posibles para la posición actual
    possible_values = list(get_possible_values(board, row, col))
    
    # Intentar los números de menor a mayor en la celda
    for i in possible_values:
        if is_Valid(board, (row, col), i):
            board[row][col] = i

            # Intentar resolver el resto del tablero con backtracking
            if solve_board(board):
                return True
            board[row][col] = 0  # Si no se puede, retroceder y probar otro número

    return False  # No se puede resolver este tablero

def generate_sudoku(dificultad):
    """Genera un Sudoku con un número aleatorio de celdas llenas dependiendo de la dificultad."""
    board = [[0] * tamaño_tablero for _ in range(tamaño_tablero)]
    if dificultad == 1:
        numeros_completos = random.randint(35, 50)
    elif dificultad == 2:
        numeros_completos = random.randint(22, 34)
    elif dificultad == 3:
        numeros_completos = random.randint(10, 21)
    else:
        raise ValueError("Dificultad inválida.")  # Asegura que la dificultad sea válida
    # Llenar algunas celdas al azar para iniciar la resolución
    for _ in range(numeros_completos):  # Rellenar entre 16 y 32 celdas
        row = random.randint(0, tamaño_tablero - 1)
        col = random.randint(0, tamaño_tablero - 1)
        num = random.randint(1, tamaño_tablero)
        while not is_Valid(board, (row, col), num):
            row = random.randint(0, tamaño_tablero - 1)
            col = random.randint(0, tamaño_tablero - 1)
            num = random.randint(1, tamaño_tablero)
        board[row][col] = num

    return board

def generate_valid_sudoku(dificultad):
    """Genera un Sudoku válido con solución garantizada."""
    while True:
        board = generate_sudoku(dificultad)
        # Intenta resolver el tablero generado
        copy_board = [row[:] for row in board]  # Copia del tablero para no modificar el original
        if solve_board(copy_board):
            return board
        else:
            # Si no se puede resolver, genera otro tablero
            continue

def valid_input(prompt, valid_choices):
    """Función para solicitar una opción al usuario y validar que esté dentro de las opciones válidas."""
    while True:
        try:
            choice = int(input(prompt))
            if choice not in valid_choices:
                raise ValueError("Opción no válida.")
            return choice
        except ValueError:
            print("Error, elige bien las opciones!")

def user_gen_board():
    """Genera un tablero ingresado manualmente por el usuario."""
    board = []
    for i in range(tamaño_tablero):
        print(f"Ingrese la fila {i + 1} del tablero (9 números entre 1 y 9, 0 para vacíos):")
        while True:
            try:
                row = list(map(int, input().split()))
                if len(row) != tamaño_tablero or any(num < 0 or num > 9 for num in row):
                    raise ValueError("Debe ingresar exactamente 9 números entre 0 y 9.")
                board.append(row)
                break
            except ValueError as e:
                print(f"Entrada no válida. {e}")
                print("Error, elige bien las opciones!")  # Mostrar el mensaje en caso de error
    return board

def main():
    """Función principal que gestiona el flujo del juego."""
    algoritmo = valid_input("Ingrese el algoritmo a utilizar \n 1. Backtracking \n 2. Branch and Bound \n", [1, 2])
    
    modo = valid_input("Ingrese el modo de juego \n 1. Ingresar Tablero \n 2. Tablero auto-generado \n", [1, 2])

    if modo == 1:
        board = user_gen_board()
    else:
        dificultad = valid_input("Ingrese la dificultad del Sudoku \n 1. Fácil \n 2. Medio \n 3. Difícil \n", [1, 2, 3])
        board = generate_valid_sudoku(dificultad)  # Genera un tablero válido con solución garantizada

    # Resuelve el Sudoku con el algoritmo seleccionado
    print("Resolviendo el Sudoku automáticamente...")
    if algoritmo == 1:
        if solve_board(board):
            print("¡Sudoku resuelto!")
        else:
            print("No se pudo resolver el Sudoku.")
    else:
        # Implementar algoritmo Branch and Bound si es necesario
        print("Algoritmo Branch and Bound aún no implementado.")
    
if __name__ == '__main__':
    main()
