def prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
def find_primes(a, b):
    a, b = int(a), int(b)
    if a < 0 or b <= a:
        print('Ошибка!')
        return
    primes = []
    for num in range(a, b):
        if prime(num):
            primes.append(str(num))
    if not primes:
        print('Ошибка!')
        return
    print(' '.join(primes))
x, y = input('Введи числа: ').split()
find_primes(x, y)