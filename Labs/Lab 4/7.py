w=input('Введите три числа: ')
x,y,z=map(int,w.split())
mn=100
if x<mn and x<y and x<z: print(x)
if y<mn and y<x and y<z: print(y)
if z<mn and z<y and z<x: print(z)