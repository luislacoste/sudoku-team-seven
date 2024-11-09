def es_valido(board, row, col, num):
    # Verifica que la celda no contenga numero
    if board[row][col] != 0:
        return False
    # Verificar fila
    if num in board[row]:
        return False
    # Verificar columna
    for r in range(CUADRADO):
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

def print_board(board):
    for row in board:
        print(row)
    print()
    
CUADRADO = 9    




def get_least_options_cell(board):
    min_options = CUADRADO + 1
    best_cell = None
    for row in range(CUADRADO):
        for col in range(CUADRADO):
            if board[row][col] == 0:
                options = sum(1 for num in range(1, CUADRADO + 1) if es_valido(board, row, col, num))
                if options < min_options:
                    min_options = options
                    best_cell = (row, col)
    return best_cell, min_options


def branch_and_bound(tablero, generando=False):
    empty_location, min_options = get_least_options_cell(tablero)
    if empty_location is None:
        return True
    
    if min_options == 0:
        return False

    row, col = empty_location
    for num in range(1, CUADRADO + 1):
        if es_valido(tablero, row, col, num):
            if generando == False:
                print_board(tablero)
            tablero[row][col] = num

            if branch_and_bound(tablero, generando):
                return True

            tablero[row][col] = 0
            if generando == False:
                print_board(tablero)

    return False
