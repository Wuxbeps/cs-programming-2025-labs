print("Введите число от 1 до 9")
a = int(input())
for i in range(0, 10):
    print(f'{a} * {i + 1} = {a * (i + 1)}')