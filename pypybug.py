# считываю w,h
sq_w,sq_h,nnn = map(int,input().split())

# считываю yto_x
yto_x = []
for i in range(nnn):
	x,y = map(int,input().split())
	yto_x.append((x,y))

# сортирую по y
yto_x.sort(key=lambda p: p[1])

# склеиваю одинаковые y и получаю yto_xmm
class Line:
	__slots__ = ['y','xmin','xmax']
	def __init__(self,x,y):
		self.y = y
		self.xmin = x
		self.xmax = x
	def update(self,x):
		self.xmin = min(self.xmin,x)
		self.xmax = max(self.xmax,x)
	def __repr__(self):
		return repr((self.y,self.xmin,self.xmax))
yto_xmm = [Line(*yto_x[0])]
for i in range(1,nnn):
	x,y = yto_x[i]
	if y == yto_xmm[-1].y:
		yto_xmm[-1].update(x)
	else:
		yto_xmm.append(Line(x,y))

# составляю массив индексов максимумов x по убыванию
max_decrease = []
#print(1)
for i in range(len(yto_xmm)):
	print(i,len(max_decrease))
	while max_decrease and yto_xmm[i].xmax >= yto_xmm[max_decrease[-1]].xmax:
		max_decrease.pop()
	max_decrease.append(i)
print(2)
