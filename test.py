import time
import os

CONTADOR = [0]  # Contador de movimientos


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


def is_valid_move(board, row, col, num):
    """Check if a number can be placed in a given cell."""
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def find_candidates(board, row, col):
    """Find all valid numbers for a given cell."""
    candidates = []
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            candidates.append(num)
    return candidates


def initialize_unassigned(board):
    """Initialize the unassigned cells with their candidate lists."""
    unassigned = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = find_candidates(board, row, col)
                unassigned.append((len(candidates), row, col, candidates))
    # Sort by the number of candidates
    unassigned.sort(key=lambda x: x[0])
    return unassigned


def update_unassigned(unassigned, board, row, col):
    """Update the candidates for affected cells after placing or removing a number."""
    updated = []
    for candidates_len, r, c, candidates in unassigned:
        if r == row or c == col or (r // 3 == row // 3 and c // 3 == col // 3):
            # Recalculate candidates for affected cells
            new_candidates = find_candidates(board, r, c)
            updated.append((len(new_candidates), r, c, new_candidates))
        else:
            # Keep original data for unaffected cells
            updated.append((candidates_len, r, c, candidates))
    # Sort updated list by the number of candidates
    updated.sort(key=lambda x: x[0])
    return updated


def branch_and_bound_sudoku(board, unassigned):
    """Solve the Sudoku puzzle using branch and bound."""
    # print_tablero(board)
    if not unassigned:
        return True  # Puzzle solved

    # Pick the cell with the fewest candidates
    _, row, col, candidates = unassigned[0]

    for num in candidates:

        board[row][col] = num  # Make a move
        new_unassigned = update_unassigned(unassigned[1:], board, row, col)
        if branch_and_bound_sudoku(board, new_unassigned):
            return True  # Continue with the solution
        board[row][col] = 0  # Undo the move (backtrack)

    return False  # Trigger backtracking


tablero = [[9, 0, 0, 6, 0, 0, 2, 0, 8], [0, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [6, 8, 0, 0, 0, 0, 0, 0, 0], [
    0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 7, 3], [7, 5, 9, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 5]]

start_time = time.time()
unnasigned = initialize_unassigned(tablero)


if branch_and_bound_sudoku(tablero, unnasigned):
    print("\n--- %s seconds ---" % (time.time() - start_time))
    # print("\nSolved Sudoku Board:")
    # print_tablero(tablero, borrar_pantalla=False)
else:
    print("\nNo solution exists.")
