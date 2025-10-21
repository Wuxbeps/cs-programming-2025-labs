print('Введите слово')
t = input()
a = ''
for i in range(len(t)):
    a += t[i] +f'{i+1}'
print(a)