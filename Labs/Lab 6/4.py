def add_mats(n, a, b):
    n = int(n)
    if n <= 2:
        return "Ошибка!"
    res = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(a[i][j]) + int(b[i][j]))
        res.append(row)
    return res
data = input('Введите N: ').split()
n = data[0]
m1 = []
m2 = []
for _ in range(int(n)):
    m1.append(input().split())
for _ in range(int(n)):
    m2.append(input().split())
ans = add_mats(n, m1, m2)
if ans == "Ошибка!":
    print("Ошибка!")
else:
    for row in ans:
        print(" ".join(map(str, row)))