Ntests = int(input())
for itest in range(Ntests):
	L = int(input())
	arr = list(map(int,input().split()))
	res = []
	i = 0
	while i<L:
		start = i
		m = arr[i]
		i+=1
		while i<start+m and i<L:
			x = arr[i]
			i+=1
			if x<i-start:
				i-=1
				res.append(i-start)
				break
			elif x<m:
				m = x
		else:
			res.append(min(m,L-start))
	print(len(res))
	print(*res)
