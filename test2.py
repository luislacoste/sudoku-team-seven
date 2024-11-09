
row = 7
col = 6
SUBCUADRO = 3   

start_row = row - row % SUBCUADRO
start_col = col - col % SUBCUADRO

print(f"start_row: {start_row}, start_col: {start_col}")
