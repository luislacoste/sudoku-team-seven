import time


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



def back_tracking():
    # Función para verificar si un número es válido en una posición específica
    def es_valido(sudoku, fila, col, num):
        # Verificar la fila
        if num in sudoku[fila]:
            return False

        # Verificar la columna
        for i in range(9):
            if sudoku[i][col] == num:
                return False

        # Verificar el subcuadrado 3x3
        inicio_fila = (fila // 3) * 3
        inicio_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if sudoku[inicio_fila + i][inicio_col + j] == num:
                    return False

        return True

    # Función de búsqueda en profundidad para resolver el Sudoku


    def resolver_sudoku(sudoku):
        # Encontrar una celda vacía
        for fila in range(9):
            for col in range(9):
                if sudoku[fila][col] == 0:
                    # Probar con los números del 1 al 9
                    for num in range(1, 10):
                        time.sleep(1)
                        if es_valido(sudoku, fila, col, num):
                            # Colocar el número en la celda
                            sudoku[fila][col] = num

                            # Llamada recursiva para continuar con la siguiente celda
                            if resolver_sudoku(sudoku):
                                return True

                            # Si no es solución, deshacer el cambio (backtracking)
                            sudoku[fila][col] = 0

                    return False  # Si ningún número es válido, regresar False

        return True  # Si se completó todo el Sudoku, regresar True


    # Ejemplo de Sudoku a resolver
    sudokuInicial = [[0, 8, 0, 0, 0, 1, 0, 0, 4], [0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 6], [
        7, 0, 0, 0, 0, 0, 1, 0, 5], [0, 0, 0, 0, 0, 0, 2, 9, 0], [0, 0, 0, 0, 0, 3, 0, 5, 0], [5, 0, 0, 0, 0, 0, 0, 7, 0], [3, 0, 1, 0, 0, 8, 0, 2, 9]]
    tablero_save2 = [row[:] for row in sudokuInicial]
    # Resolver el Sudoku y mostrar el resultado 
    if resolver_sudoku(sudokuInicial):
        for fila in sudokuInicial:
            print(fila)
    else:
        print("No se encontró una solución.")

print("Backtracking")
medir_tiempo_ejecucion(back_tracking)
print("Branch and Bound")
