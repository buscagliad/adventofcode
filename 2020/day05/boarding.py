def get_row(code):
    row = [0, 127]
    index = 64
    for c in code[:7] :
        if c == 'B' : row[0] = row[0] + index
        elif c == 'F' : row[1] = row[1] - index
        index = index // 2
    if row[0] != row[1] : print("ERROR - rows mismatch " + str(row))
    return row[0]

def get_col(code):
    col = [0, 7]
    index = 4
    for c in code[:3] :
        if c == 'R' : col[0] = col[0] + index
        elif c == 'L' : col[1] = col[1] - index
        index = index // 2
    if col[0] != col[1] : print("ERROR - columns mismatch " + code + " :c: " + c + " :: " + str(col))
    return col[0]



def max_seat_value(fname):
    max_seat_id = 0
    with open(fname) as f:
        for line in f:
            line = line.replace("\n", "")
            gr = get_row(line)
            gc = get_col(line[7:])
            seat_id = gr * 8 + gc
            if seat_id > max_seat_id : max_seat_id = seat_id
            #print(line + " is " + str(gr) + ", " + str(gc) + "  seat id: " + str(seat_id) + "   max seat id: " + str(max_seat_id))
    return max_seat_id

def get_seat_values(fname):
    seat_ids = []
    max_seat_id = 0
    with open(fname) as f:
        for line in f:
            line = line.replace("\n", "")
            gr = get_row(line)
            gc = get_col(line[7:])
            seat_id = gr * 8 + gc
            seat_ids.append(seat_id)
            if seat_id > max_seat_id : max_seat_id = seat_id
            #print(line + " is " + str(gr) + ", " + str(gc) + "  seat id: " + str(seat_id) + "   max seat id: " + str(max_seat_id))
    return seat_ids

ids = get_seat_values('data.txt')
print("Max seat id is: " + str(max(ids)))
ids.sort()
#print(str(ids))

for i in range(len(ids)-1):
    if ids[i+1] - ids[i] == 2 :
        print("My seat id is: " + str(ids[i] + 1))