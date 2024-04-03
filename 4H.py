debug = 0

from math import ceil,floor

N = int(input())
arr = []
for i in range(N):
	v,p = map(int,input().split())
	arr.append([i,v,p])

arr.sort(key=lambda x: x[1], reverse = True)

def next_stage(p):
	x = arr[p][1]
	while p<N and arr[p][1]==x:
		p+=1
	return p
def next_stage_bribe(p):
	x = arr[p][1]
	mbr = arr[p][2]
	imbr = p
	while p<N and arr[p][1]==x:
		if arr[p][2]!=-1 and (mbr==-1 or arr[p][2]<mbr):
			mbr = arr[p][2]
			imbr = p
		p+=1
	return mbr,imbr,p


current_start = 0
current_end = 0
cut_start = 0
cut_end = next_stage(0)
cutlevel = arr[0][1]
cutsumm = 0

best_ibribe = 0
best_cost = -1
best_level = 0
best_auxcut = 0
def update(ibr,cost,cutlevel,aux):
	# кому, сколько, до скольких обрезаем остальных, и доп.обрез
	# всех обрезаем до cutlevel, из них (доп.обрез) обрезаем до cutlevel-1
	# ibr-у добавляем cost-arr[ibr][2]
	global best_ibribe, best_cost, best_level, best_auxcut
	if best_cost==-1 or cost<best_cost:
		best_ibribe = ibr
		best_cost = cost
		best_level = cutlevel
		best_auxcut = aux
def minlevel(p):
	return 0 if p==N else arr[p][1]
def printall(mes=''):
	print(f'{mes}:\n {best_ibribe=} {best_cost=} {best_level=} {best_auxcut=}')
	print('ind','i','v0','v1','br','cost',sep='\t')
	sv0 = 0
	sv1 = 0
	for i in range(N):
		ind,v0,br = arr[i]
		if best_cost!=-1:
			if i==best_ibribe:
				v1 = v0+best_cost-br
				cost = best_cost
			else:
				if i<best_auxcut:
					assert best_level-1<v0, (ind,i,v0,br)
					v1 = best_level-1
				else:
					v1 = min(v0,best_level)
				cost = ''
		else:
			v1 = v0
			cost = ''
		print(ind,i,v0,v1,br,cost,sep='\t')
		sv0+=v0
		sv1+=v1
	print(sv0,sv1)
	assert sv0==sv1

if debug: printall('start')

while current_end!=N:
	current_start = current_end
	bribe,i_bribe,current_end = next_stage_bribe(current_end)
	if debug>1: 
		print()
		print(f'next stage {current_start}-{current_end} {i_bribe=} :{bribe=} ({cutlevel=} {cutsumm=})')
	if bribe==-1: # нам нужен хотябы один взяточник
		if debug>1: print('взяточников не обнаружено')
		continue
	if i_bribe!=current_end-1: # перемещаем его в конец текущей стадии
		# чтобы придальнейшей обрезке auxcut его не задело
		if debug>1: print('меняем',i_bribe,current_end-1)
		arr[current_end-1],arr[i_bribe] = arr[i_bribe],arr[current_end-1]
		i_bribe = current_end-1
	if current_end==1: # если есть -единственный- максимум
		if debug>1: print('-единственный- максимум')
		update(0,bribe,cutlevel,0)
		continue
	while True: # двигаем cut_stage
		assert cut_end<=current_end
		# макс.доп.обрез === cut_end-1
		if arr[current_start][1]+cutsumm+cut_end-1 > cutlevel: 
			# если нам хватило макс.доп.обреза
			auxcut = cutlevel+1-(arr[current_start][1]+cutsumm)
			if auxcut==-1: auxcut = 0
			assert 0<=auxcut and auxcut<cut_end
			update(i_bribe,bribe+cutsumm+auxcut,cutlevel,auxcut)
			break
		elif arr[current_start][1]+cutsumm+cut_end-1+(cutlevel-minlevel(cut_end))*cut_end > minlevel(cut_end)+1:
			# нам хватило высоты ступеньки
			assert cut_end!=current_end
			y1 = cutlevel
			y2 = arr[current_start][1]+cutsumm+cut_end-1
			x = floor((y1-y2)/(cut_end+1))+1
			#print(f'{y1=} {y2=} {x=}')
			if cutlevel-x > minlevel(cut_end):
				cutsumm+= x*cut_end
				cutlevel-= x
				#print(f'({cutlevel=} {cutsumm=})')

				auxcut = cutlevel+1-(arr[current_start][1]+cutsumm)
				if auxcut==-1: auxcut = 0
				assert 0<=auxcut and auxcut<cut_end , auxcut
				update(i_bribe,bribe+cutsumm+auxcut,cutlevel,auxcut)
				break
		# обрезаем ступеньку полностью и переходим к следующей
		x = cutlevel-minlevel(cut_end)
		cutsumm+= x*cut_end
		cutlevel-= x
		cut_start = cut_end
		cut_end = next_stage(cut_end)
		# continue
	# вычислили, сколько надо обрезать, кому добавить, переходим к следующей ступеньке
	if debug>1: 
		print()
		printall(f'{cut_end=} {current_end=}')
if debug: printall('final')


assert best_cost!=-1
for i in range(N):
	ind,v0,br = arr[i]
	if i==best_ibribe:
		v1 = v0+best_cost-br
	else:
		if i<best_auxcut:
			assert best_level-1<v0, (ind,i,v0,br)
			v1 = best_level-1
		else:
			v1 = min(v0,best_level)
	arr[i][1] = v1
best_ibribe = arr[best_ibribe][0]
arr.sort(key=lambda x: x[0])

print(best_cost)
print(best_ibribe+1)
print(' '.join(str(arr[i][1]) for i in range(N)))
