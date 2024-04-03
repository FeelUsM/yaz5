timing = True
debug = True
if timing:
	import time
if timing : start_time = time.time()

def lower_bound(first,last,l,value):
	if debug: print(first,last)
	global summs
	if summs[first+l]-summs[first] > value:
		return first,0
	if summs[last-1+l]-summs[last-1] < value:
		return last,0
	count = last - first
	c=0
	while count > 0:
		c+=1
		step = count // 2
		it = first+step; 
		if debug: print(it,summs[it+l]-summs[it] , value,end=' ')
		if summs[it+l]-summs[it] < value :
			if debug: print('<')
			first = it+1
			count -= (step + 1) 
		elif summs[it+l]-summs[it] == value:
			if debug: print('==')
			return it,c
		else:
			if debug: print('>')
			count = step
	return first,c

n,m = map(int,input().split())
arr = list(map(int,input().split()))
summs = [0 for i in range(n+1)]
for i in range(n):
	summs[i+1] = summs[i]+arr[i]
if timing : print('in',time.time() - start_time)

ans = [0 for i in range(m)]
sc = 0
stat = [0 for i in range(20)]
for i in range(m):
	l,s = map(int,input().split())
	a,ca = lower_bound(0,len(summs)-l,l,s)
	#b,cb = upper_bound(0,len(summs)-l,l,s)
	stat[ca]+=1
	sc+=ca
	#sc+=cb
	if a+l>=n+1 or summs[a+l]-summs[a] != s:
		ans[i] = str(-1)
	else:
		ans[i] = str(a+1)
if timing : print('calc',time.time() - start_time)		
print('\n'.join(ans))
print(sc/m,m,stat)
if timing : print('out',time.time() - start_time)