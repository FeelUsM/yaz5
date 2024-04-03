debug = 1
if debug:
	import time
	start_time = time.time()
'''
считываю w,h
считываю yto_x
сортирую по y
склеиваю одинаковые y и получаю yto_xmm
составляю массив индексов максимумов x по убыванию
составляю массив индексов минимумов x по возрастанию
'''
# считываю w,h
sq_w,sq_h,nnn = map(int,input().split())

# считываю yto_x
yto_x = []
for i in range(nnn):
	x,y = map(int,input().split())
	yto_x.append((x,y))

# сортирую по y
if debug: print('yto_x unsorted=',time.time() - start_time)
yto_x.sort(key=lambda p: p[1])
if debug: print('yto_x=',len(yto_x),time.time() - start_time)

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
if debug: print('yto_xmm=',len(yto_xmm),time.time() - start_time)

# составляю массив индексов максимумов x по убыванию
max_decrease = []
tail = 0
for i in range(len(yto_xmm)):
	while tail-1>=0 and yto_xmm[i].xmax >= yto_xmm[max_decrease[tail-1]].xmax:
		tail-=1
	if tail==len(max_decrease):
		max_decrease.append(i)
	else:
		max_decrease[tail] = i
	tail+=1
del max_decrease[tail:]
if debug: print(f'{max_decrease=}',time.time() - start_time)
# составляю массив индексов минимумов x по возрастанию
min_increase = []
tail = 0
for i in range(len(yto_xmm)):
	while tail-1>=0 and yto_xmm[i].xmin <= yto_xmm[min_increase[tail-1]].xmin:
		tail-=1
	min_increase.append(i)
	if tail==len(min_increase):
		min_increase.append(i)
	else:
		min_increase[tail] = i
	tail+=1
del min_increase[tail:]
if debug: print(f'{min_increase=}',time.time() - start_time)

def mymax(a,b):
	if a==None and b==None:
		return None
	elif a==None:
		return b
	elif b==None:
		return a
	else:
		return max(a,b)
def mymin(a,b):
	if a==None and b==None:
		return None
	elif a==None:
		return b
	elif b==None:
		return a
	else:
		return min(a,b)
def lower_bound(first,last,check):
	#print(first,last)
	count = last - first
	while count > 0:
		step = count // 3
		it = first+step; 
		#if debug : print(it,arr(it),end=' ')
		if check(it) < 0 :
			#if debug : print('<')
			first = it+1
			count -= (step + 1) 
		else:
			#if debug : print('>=')
			count = step
	return first
'''
check(wr)
	нахожу правую границу бинарным поиском
	для каждого окна
		вычисляю максимум/минимум слева и справа
		по этим знаениям ищу min(ширины)
			и если она <wr
				return True
	шаг сдвига окна:
		чтобы вошла правая - только так может уменьшиться ширина
'''
def check(wr): # width of road
	# инициализируюсь левой точкой
	left_ind = 0 # индекс первой точки внутри
	left_y = yto_xmm[0].y
	left_max = None
	left_min = None

	right_y = left_y+wr
	right_ind = lower_bound(0,len(yto_xmm),lambda p: yto_xmm[p].y-right_y) # индекс первой точки снаружи
	right_maxind = lower_bound(0,len(max_decrease),lambda p: yto_xmm[max_decrease[p]].y-right_y)
	right_minind = lower_bound(0,len(min_increase),lambda p: yto_xmm[min_increase[p]].y-right_y)
	def right_max():
		return yto_xmm[max_decrease[right_maxind]].xmax if right_maxind<len(max_decrease) else None
	def right_min():
		return yto_xmm[min_increase[right_minind]].xmin if right_minind<len(min_increase) else None

	if debug>1: print(f'left: {left_y} {left_ind} {left_min} {left_max} right: {right_y} {right_ind} {right_minind} {right_min()} {right_maxind} {right_max()}')
	if left_max!=None and left_max - left_min+1 > wr: # здесь это никогда не сработает
		assert False
		return -1
	ma = mymax(left_max,right_max())
	mi = mymin(left_min,right_min())
	if ma==None: 
		if debug: print(wr,'слева и справа нет точек, return True',time.time() - start_time)
		return 0 # слева и справа нет точек
	found_wr = ma - mi+1
	if found_wr<=wr:
		if debug: print(wr,'общая разность меньше требуемой, return True',time.time() - start_time)
		return 0

	# двигаюсь по правым точкам
	while right_ind<len(yto_xmm):
		right_y = yto_xmm[right_ind].y+1
		left_y = right_y - wr
		while yto_xmm[left_ind].y<left_y:
			left_max = mymax(left_max,yto_xmm[left_ind].xmax)
			left_min = mymin(left_min,yto_xmm[left_ind].xmin)
			left_ind+=1
		if max_decrease[right_maxind]==right_ind:
			right_maxind+=1
		if min_increase[right_minind]==right_ind:
			right_minind+=1

		if debug>1: print(f'left: {left_y} {left_ind} {left_min} {left_max} right: {right_y} {right_ind+1} {right_minind} {right_min()} {right_maxind} {right_max()}')
		if left_max!=None and left_max - left_min+1 > wr: # здесь всегда left_max!=None
			if debug: print(wr,'слева превышение, return False',time.time() - start_time)
			return -1
		ma = mymax(left_max,right_max())
		mi = mymin(left_min,right_min())
		if ma==None: # здесь это никогда не сработает
			assert False
			return 0 # слева и справа нет точек
		found_wr = ma - mi+1
		if found_wr<=wr:
			if debug: print(wr,'общая разность меньше требуемой, return True',time.time() - start_time)
			return 0

		right_ind+=1
	assert False # а я не знаю как сюда попасть

#print(1700,check(1700))
#if debug:
#	for wr in range(1,min(sq_h,sq_w)+1):
#		check(wr)
if debug: print(yto_xmm[-1].y-yto_xmm[0].y+1,sq_h,sq_w)
print(lower_bound(1,min(yto_xmm[-1].y-yto_xmm[0].y+1,sq_h,sq_w)+1,check))