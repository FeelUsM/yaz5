H,W = map(int,input().split())
desk = []
for i in range(H):
	desk.append(list(map(int,input().split())))

maxx = []
for i in range(H):
	m1 = 0
	im1 = -1
	m2 = 0
	im2 = -1
	for j in range(W):
		if desk[i][j]>m1:
			m2,im2,m1,im1 = m1,im1,desk[i][j],j
		elif desk[i][j]>m2:
			m2,im2 = desk[i][j],j
	maxx.append((m1,im1,m2,im2))
#print(maxx)
jv = -1
iv = -1
rm = 10**10
for j in range(W):
	m1 = 0
	im1 = -1
	m2 = 0
	im2 = -1
	#print(j,'[',end='')
	for i in range(H):
		m = maxx[i][0] if maxx[i][1]!=j else maxx[i][2]
		#print(m,',',end='')
		if m>m1:
			m2,im2,m1,im1 = m1,im1,m,i
		elif m>m2:
			m2,im2 = m,i
	#print(']',m1,im1,m2,im2)
	if m2<rm:
		rm = m2
		jv = j
		iv = im1
		#print('update',rm,jv,iv)
print(iv+1,jv+1)
