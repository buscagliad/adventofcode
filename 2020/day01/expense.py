def sum2(arr, sval):
    for e1 in arr:
        for e2 in arr:
            if e1 + e2 == sval:
                print("e1: " + str(e1)+ "  e2: " + str(e2) + "  Product: " + str(e1*e2))
                return

def sum3(arr, sval):
    for e1 in arr:
        for e2 in arr:
            for e3 in arr:
                if e1 + e2 + e3 == sval:
                    print("e1: " + str(e1)+ "  e2: " + str(e2) + "  e3: " + str(e3) + "  Product: " + str(e1*e2*e3))
                    return

with open('data.txt') as f:
    expenses = []
    for line in f:
        expenses.append(int(line))

sum2(expenses, 2020)
sum3(expenses, 2020)