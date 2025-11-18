n=int(input('введите число: '))
if (n%10)%2==0 and sum(map(int,str(n)))%3==0: print('делиться на 6')
else: print('не делиться на 6')