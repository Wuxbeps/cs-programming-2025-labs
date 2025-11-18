year=int(input('введите год: '))
if year%4==0:
    if year%100!=0 or year%400==0:
        print("високосный год")
    else:
        print("не високосный год")
else:
    print("не високосный год")