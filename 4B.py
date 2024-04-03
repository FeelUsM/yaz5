timing = False
debug = False
if timing:
	import time
	

N = int(input())
def arr(k):
	return (k+1)*(k+2)*(k+3)//6-k-2 if k!=0 else 0

def lower_bound(first,last,arr,value):
	#print(first,last)
	count = last - first
	while count > 0:
		step = count // 2
		it = first+step; 
		if debug : print(it,arr(it),end=' ')
		if arr(it) < value :
			if debug : print('<')
			first = it+1
			count -= (step + 1) 
		else:
			if debug : print('>=')
			count = step
	return first
def upper_bound(first,last,arr, value):
	#print(first,last)
	count = last-first
	while count > 0:
		step = count // 2; 
		it = first+step
		#print(it,arr(it),end=' ')
		if arr(it) <= value:
			#print('<=')
			first = it+1;
			count -= (step + 1)
		else:
			#print('>')
			count = step
	return first
from math import floor,ceil

#for j in range(18):
#print(j,arr(j))
if timing : start_time = time.time()
i=N
a = floor(i**(1/3))
b = 2*a+10
r = lower_bound(a,b,arr,i+1)-1
#print(j,a,r/a,b/r)
print(r)
if timing : print(time.time() - start_time)
#print()
#print(upper_bound(floor(N**(1/3)),ceil(N**(1/2))+1,arr,N))
#0 0
#1 1
#2 6
#3 15
#4 29
#5 49
#6 76
#7 111
#8 155
#9 209
#10 274
#11 351
#12 441
#13 545
#14 664
#15 799
#16 951
#17 1121