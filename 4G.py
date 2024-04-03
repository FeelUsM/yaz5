debug = False
H,W = map(int,input().split())
F = []
M = 1
for y in range(H):
	S = input().strip()
	L = []
	F.append(L)
	for x in range(W):
		if S[x]=='.':
			L.append(0)
		elif S[x]=='#':
			if x==0 or y==0:
				L.append(1)
			else:
				L.append(min(F[y][x-1],F[y-1][x-1],F[y-1][x])+1)
				M = max(M,F[y][x])
		else:
			assert False
M = min(M,W//3,H//3)
if debug:
	for y in range(H):
		print(*map(str,F[y]))
	print(M)

def check(size):
	for y in range(H-3*size+1):
		yc = y+2*size-1
		for x in range(W-3*size+1):
			xc = x + 2*size-1
			if F[yc][xc]>=size and F[yc-size][xc]>=size and F[yc+size][xc]>=size and F[yc][xc-size]>=size and F[yc][xc+size]>=size :
				return 0 # True
	return 1 # False

def upper_bound(first,last, check):
	count = last-first
	while count > 0:
		step = count // 2; 
		it = first+step
		if check(it) <= 0:
			first = it+1;
			count -= (step + 1)
		else:
			count = step
	return first

print(upper_bound(1,M+1,check)-1)