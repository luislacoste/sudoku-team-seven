import random


# Tamaño del tablero
TAB_N = 9
# Tamaño de cada subcuadro (2x4 en este caso)
SUB_TAB_N = 3


def print_board(tabla):
    for row in tabla:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


def is_safe(tabla, row, col, num):
    # Verifica si la celda ya está ocupada
    if tabla[row][col] != 0:
        return False

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
                # Si no se puede colocar ningún número, imprime la posición
                print(f"No se puede resolver en la posición ({row}, {col})")
                return False
    return True



def generar_random(tabla, celdas):
    # Llenar algunas celdas al azar para iniciar la resolución
    for _ in range(celdas):
        row = random.randint(0, TAB_N - 1)
        col = random.randint(0, TAB_N - 1)
        num = random.randint(1, TAB_N)
        while not is_safe(tabla, row, col, num):
            row = random.randint(0, TAB_N - 1)
            col = random.randint(0, TAB_N - 1)
            num = random.randint(1, TAB_N)
        tabla[row][col] = num
    return tabla


def generar_tablero(dificultad):
  tabla = [[0] * TAB_N for _ in range(TAB_N)]
  if dificultad == 1:
      celdas = random.randint(35, 50)
  elif dificultad == 2:
      celdas = random.randint(22, 34)
  elif dificultad == 3:
      celdas = random.randint(10, 21)
  
  
  
  # llena x cantidad de celdas
  tabla = generar_random(tabla, celdas)

  print(tabla)
  return tabla


def main():
    # @TODO arreglar esta logica de mierda de validacion
    dificultad = 1
    # while dificultad != 1 and dificultad != 2 and dificultad != 3:
    #     dificultad = int(
    #         input("Ingrese la dificultad del sudoku \n 1: Facil\n 2: Medio\n 3: Dificil \n "))

    tablero = generar_tablero(dificultad)

    
    # generar_metodo = 0
    # while generar_metodo != 1 and generar_metodo != 2:
    #     generar_metodo = int(input(
    #         "Ingrese el método de generación de tablero de Sudoku (1: Aleatorio, 2: Personalizado): "))

    # sudoku_board = generate_sudoku(generar_metodo)
    print("Tablero de Sudoku inicial:")
    print_board(tablero)

    if solve_sudoku(tablero):
        print("\nTablero de Sudoku resuelto:")
        print_board(tablero)
    else:
        print("No se pudo resolver el Sudoku.")


if __name__ == "__main__":
    main()
