# 3G
timing = False
if timing:
	import time
	start_time = time.time()

def orto(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	dx = x2-x1
	dy = y2-y1
	if (dx%2 + dy%2)%2:
		return None,None
	r1 = (x1+(dx-dy)//2, y1+(dy+dx)//2)
	r2 = (x1+(dx+dy)//2, y1+(dy-dx)//2)
	return r1,r2

def main():
	N = int(input())
	processed = {tuple(map(int,input().split()))}
	wanted = set()
	answer = 3 if N==1 else 2

	for I in range(1,N):
		processed.add(tuple(map(int,input().split())))

	for I,cur in enumerate(processed):
		if cur in wanted:
			answer = 0
		if answer==0: continue
		for j,proc in enumerate(processed):
			if j==I:
				break
			if answer==0: break
			p3,p4 = orto(cur,proc)
			#print(cur,proc,p3,p4)
			if p3==None:
				continue
			p3p = p3 in processed
			p4p = p4 in processed
			if p3p:
				answer = 1
				if p4p:
					answer = 0
					break
				else:
					wanted.add(p4)
			if p4p:
				answer = 1
				if p3p:
					answer = 0
					break
				else:
					wanted.add(p3)

	print(answer)
	if answer==1:
		print(*next(iter(wanted)))
	elif answer==2:
		stop = False
		for I,p1 in enumerate(processed):
			if stop: break
			for j,p2 in enumerate(processed):
				if stop: break
				if j==I:
					break
				p3,p4 = orto(p1,p2)
				if p3!=None:
					print(*p3)
					print(*p4)
					stop = True
	elif answer==3:
		x,y = next(iter(processed))
		print(x,y+1)
		print(x+1,y)
		print(x+1,y+1)
main()
if timing:
	print('stop',time.time() - start_time)

#exit(0)
