import string
def pal_check(s):
    s = s.lower()
    for p in string.punctuation:
        s = s.replace(p, '')
    s = s.replace(' ', '')
    return 'Да' if s == s[::-1] else 'Нет'
text = input('Введите текст: ')
print(pal_check(text))