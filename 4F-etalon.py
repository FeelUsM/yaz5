debug = False
def check(m):
	r = 0
	pmx = -10**9
	pmn = 10**9
	for i in range(n):
		while r<n and x[r] < x[i]+m :
			r+=1
		mx = pmx
		mn = pmn
		if r!=n:
			mx = max(mx, sufmax[r])
			mn = min(mn, sufmin[r])
		if mx-mn < m:
			if debug: print(m, n, mn, mx, True)
			return True
		pmx = prefmax[i]
		pmn = prefmin[i]
	if debug: print(m, False)
	return False

w, h, n = map(int, input().split())
a = []
for i in range(n):
	x,y = map(int,input().split())
	a.append((y,x))
a.sort()
x = []
y = []
for now in a:
	x.append(now[0])
	y.append(now[1])
prefmin = [y[0]]*n
prefmax = [y[0]]*n
sufmin = [y[-1]]*n
sufmax = [y[-1]]*n
for i in range(1,n):
	prefmin[i] = min(prefmin[i-1], y[i])
	prefmax[i] = max(prefmax[i-1], y[i])
for i in range(n-2,-1,-1):
	sufmin[i] = min(sufmin[i+1], y[i])
	sufmax[i] = max(sufmax[i+1], y[i])

if debug:
	print('prefmax',prefmax[0],end=' ')
	for i in range(1,n):
		if prefmax[i-1] < prefmax[i]:
			print(prefmax[i],end=' ')
	print()
	print('prefmin',prefmin[0],end=' ')
	for i in range(1,n):
		if prefmin[i-1] > prefmin[i]:
			print(prefmin[i],end=' ')
	print()
	print('sufmax',end=' ')
	for i in range(1,n):
		if sufmax[i-1] > sufmax[i]:
			print(i-1,end=' ')
	print(n-1)
	print('sufmin',end=' ')
	for i in range(1,n):
		if sufmin[i-1] < sufmin[i]:
			print(i-1,end=' ')
	print(n-1)

if 0:
	check(228)
else:
	l = 0
	r = min(w,h)
	while l<r:
		m = (l+r)//2
		if check(m):
			r = m
		else:
			l = m+1
	print(l)

