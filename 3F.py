ddd = [set() for x in range(101)]
for d in input().split():
	for l in range(1,len(d)):
		if d[:l] in ddd[l]:
			break
	else:
		ddd[len(d)].add(d)
#print(ddd)

for w in input().split():
	for l in range(1,min(101,len(w))):
		#print(w[:l],ddd[l])
		if w[:l] in ddd[l]:
			print(w[:l],end=' ')
			break
	else:
		print(w,end=' ')
print()
