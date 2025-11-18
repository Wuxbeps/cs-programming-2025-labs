a=input()
if len(a)<9:
    print('слишком мало символов')
elif not any(i.isupper() for i in a):
  print('пароль ненадежный: отсутствуют заглавные буквы латиницы')
elif not any(i.islower() for i in a):
    print('пароль ненадежный: отсутствуют строчные буквы латиницы')
elif not any(char in '0123456789' for char  in a):
    print('пароль ненадежный:отсутствуют числа')
elif not any (char in '!@#$%^&*()_-+|~' for char  in a):
    print('пароль ненадежный: отсутствуют специальные символы')
else:
    print('пароль надежный')