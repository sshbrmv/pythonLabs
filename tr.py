import copy

def reader(filename):
    with open(filename, 'r') as file:
        return [list(map(int, line.split())) for line in file]

k = int(input("Введите число k: "))
n = int(input("Введите число n: "))

A = reader('matrix1.txt')

print("Матрица A:")
for row in A:
    print(row)

F = copy.deepcopy(A)
AT = [[0]*n for _ in range(n)]

for i in range(n):
    for j in range(n):
        AT[j][i] = A[i][j]

print("Транспонированная матрица A (AT):")
for row in AT:
    print(row)

count_polozh = 0
count_otric = 0

for i in range(n):
    for j in range(n):
        if i < j and (j+1) % 2 == 0 and F[i][j] > 0:
            count_polozh += 1

for i in range(n):
    for j in range(n):
        if i > j and (j+1) % 2 != 0 and F[i][j] < 0:
            count_otric += 1

if count_polozh > count_otric:
    for i in range(n):
        for j in range(i+1, n):
            if i > j:
                continue
            if i < j and j > i:
                F[i][j], F[j][i] = F[j][i], F[i][j]
else:
    for i in range(n):
        for j in range(i+1, n):
            F[i][j], F[n-1-j][i] = F[n-1-j][i], F[i][j]

print("Матрица F после замены областей:")
for row in F:
    print(row)

A_B = [[A[i][j] + F[i][j] for j in range(n)] for i in range(n)]
Fk = [[F[i][j] * k for j in range(n)] for i in range(n)]

print("Матрица (F + A):")
for row in A_B:
    print(row)

print(f"Матрица F, умноженная на число {k}:")
for row in Fk:
    print(row)

U = [[0]*n for _ in range(n)]

for i in range(n):
    for j in range(n):
        s = 0
        for m in range(n):
            s += A_B[i][m] * AT[m][j]
        U[i][j] = s

print("Матрица (F + A) * AT:")
for row in U:
    print(row)

K = [[U[i][j] - Fk[i][j] for j in range(n)] for i in range(n)]

print("Результат выражения (F + A)*AT - k*F:")
for row in K:
    print(row)
