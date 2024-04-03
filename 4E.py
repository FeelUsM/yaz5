from math import floor,ceil
n = int(input())
#for n in range(1,20):
x = (-1+(1+8*n)**0.5)/2
y = floor(x)
d = n -y*(y+1)//2
if d==0:
	d = y
	m=y-1
else:
	m=y
a = d
b = m+2-d
if m%2:
	a,b = b,a
print('/'.join((str(a),str(b))))
