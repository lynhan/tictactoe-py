# math.py

def num_to_coords(num):
    row = (num-1) // 3
    col = (num-1) % 3
    return row, col

def coords_to_num(row, col):
    num = row*3 + col + 1
    return num
