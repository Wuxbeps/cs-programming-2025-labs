units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

def convert(t, to_unit):
    for u in units:
        if u in t:
            seconds = int(t.replace(u, '')) * units[u]
            break
    return f'{seconds / units[to_unit]}{to_unit}'

time, unit = input('Время и единица: ').split()
print(convert(time, unit))