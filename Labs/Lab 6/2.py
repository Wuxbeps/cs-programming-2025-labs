def calc_profit(a, n):
    if int(a) < 30000:
        return 0.0
    n = int(n)
    if n <= 3:
        rate = 0.03
    elif n <= 6:
        rate = 0.05
    else:
        rate = 0.02
    bonus = (int(a) // 10000) * 0.003
    total_rate = min(rate + bonus, 0.05)
    profit = int(a) * (1 + total_rate) ** n - int(a)
    return round(profit, 2)
a, n = input('Сумма и срок: ').split()
print(calc_profit(a, n))