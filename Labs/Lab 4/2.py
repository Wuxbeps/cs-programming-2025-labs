print('Введите номер месяца')
a = int(input())

if a in [12, 1, 2]:
    print("Это зима")
elif a in [3, 4, 5]:
    print("Это весна")
elif a in [6, 7, 8]:
    print("Это лето")
elif a in [9, 10, 11]:
    print("Это осень")
else:
    print("Ошибка: такого месяца нет")