h=int(input('введите число: '))
def f(n):
    d=2
    while n%d!=0:
        d+=1
    return d==n
if f(h)==True:
    print(f'{h}-простое число')
else:
    print(f'{h}-составное число')