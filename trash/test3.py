import cupy as cp
import time


def is_valid(tablero, row, col, num):
    for i in range(9):
        if tablero[row, i] == num or tablero[i, col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[start_row + i, start_col + j] == num:
                return False

    return True


def back_tracking(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i, j] == 0:
                for num in range(1, 10):
                    if is_valid(tablero, i, j, num):
                        tablero[i, j] = num
                        if back_tracking(tablero):
                            return True
                        tablero[i, j] = 0
                return False
    return True


def main():
    tablero = cp.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 9, 0, 0, 6, 0],
                        [0, 0, 4, 0, 0, 5, 0, 0, 2],
                        [0, 0, 2, 0, 0, 8, 0, 0, 1],
                        [7, 3, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 9, 3, 0, 0],
                        [0, 0, 0, 0, 7, 0, 0, 0, 3],
                        [0, 0, 9, 0, 4, 0, 0, 0, 5],
                        [0, 4, 7, 0, 6, 0, 2, 0, 0]])

    print("Backtracking usando GPU")
    start_time_bt = time.time()
    back_tracking(tablero)
    end_time_bt = time.time()
    print(f"Tiempo de ejecución: {end_time_bt - start_time_bt} segundos")

    print("Tablero resuelto:")
    print(cp.asnumpy(tablero))


if __name__ == '__main__':
    main()
