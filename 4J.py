debug = True

from math import sqrt

class AttrDict(dict):
	def __getattr__(self, key):
		if key not in self:
			raise AttributeError(key) # essential for testing by hasattr
		return self[key]
	def __setattr__(self, key, value):
		self[key] = value
	def __repr__(self):
		return 'mkdict('+', '.join(k+'='+(f'{v:.4}' if type(v) is float else repr(v)) for k,v in self.items())+')' 
		# если встретиться ключ, который не является строкой, то будет исключение
def make_dict(**kwargs):
	return AttrDict(kwargs)

N,V = input().split()
N = int(N)
Dens = float(V)

best_H = 0

Pools = []

leftx,lefty = map(float,input().split())
most_left = leftx

def fill_pool(pool,V):
	# заполняет бассейн, обновляет best_H
	if debug: print('fill_pool',V)
	assert pool.type=='pool'
	lvls = pool.lvls
	while len(lvls)>=2 and V>0.:
		a = lvls[0].maxl
		b = lvls[1].minl
		assert b>a
		hmax = lvls[1].h-lvls[0].h
		k = hmax/(b-a)
		dh = -a*k+sqrt(a*a*k*k + 2*V*k)
		global filledV
		if dh>=hmax:
			dV = (a+b)*hmax/2 
			filledV+=dV
			V-= dV
			if debug: print('fill',lvls[0],lvls[1],dV)
			del lvls[0]
		else:
			b = a+dh/k
			filledV+=(a+b)*dh/2
			assert V-(a+b)*dh/2 < 0.00000001 , V-(a+b)*dh/2
			a+=dh/k
			p = lvls[0].h
			q = lvls[0].minl
			r = lvls[0].maxl
			lvls[0].h+=dh
			lvls[0].minl = lvls[0].maxl = a
			if debug: print('fill partial',[p,q,r],lvls[0],V)
			V=0.
	global best_H
	best_H = max(best_H,pool.lvls[0].h-pool.bottom)
	return V
def extend_to(stok,L):
	for lvl in stok.lvls:
		lvl.minl+=L
		lvl.maxl+=L
def merge_toto(bot,top):
	# объединяет два подряд идущих стока
	# верхний расширить нижним и соединить
	# обновить bottom
	# объединить объёмы
	extend_to(top,bot.lvls[-1].maxl)
	top.lvls[0].minl = bot.lvls[-1].minl
	bot.lvls.pop()
	bot.lvls+=top.lvls
	bot.bottom = min(bot.bottom,top.bottom)
	bot.overvol += top.overvol
	return bot
def make_pool(lr,rl):
	llvls = lr.lvls
	rlvls = rl.lvls
	assert llvls[0].h==rlvls[0].h , (llvls[0].h,rlvls[0].h)
	h0 = llvls[0].h
	lminl = llvls[0].minl
	lmaxl = llvls[0].maxl
	rminl = rlvls[0].minl
	rmaxl = rlvls[0].maxl
	del llvls[0]
	del rlvls[0]
	reslvls = [make_dict(h=h0,minl=lminl+rminl,maxl=lmaxl+rmaxl)]
	while len(llvls) and len(rlvls):
		#print(h0,lminl,lmaxl,rminl,rmaxl)
		if llvls[0].h<rlvls[0].h:
			h1 = llvls[0].h
			h2 = rlvls[0].h
			a = rmaxl
			b = rlvls[0].minl
			assert b>a
			l = a+ (b-a)*(h1-h0)/(h2-h0)
			h0 = h1
			lminl = llvls[0].minl
			lmaxl = llvls[0].maxl
			rminl = l
			rmaxl = l
			reslvls.append(make_dict(h=h1,minl=lminl+l,maxl=lmaxl+l))
			del llvls[0]
		else:
			h1 = rlvls[0].h
			h2 = llvls[0].h
			a = lmaxl
			b = llvls[0].minl
			assert b>a
			l = a+ (b-a)*(h1-h0)/(h2-h0)
			h0 = h1
			lminl = l
			lmaxl = l
			rminl = rlvls[0].minl
			rmaxl = rlvls[0].maxl
			reslvls.append(make_dict(h=h1,minl=rminl+l,maxl=rmaxl+l))
			del rlvls[0]
	#print('h0=',h0,lminl,lmaxl,rminl,rmaxl)
	#print(f'{reslvls=}')
	assert len(llvls) or len(rlvls)
	if len(rlvls):
		extend_to(rl,-rmaxl)
		rlvls.insert(0,make_dict(h=h0,minl=0.,maxl=0.))
		lr.lvls = reslvls
		lr.type = 'pool'
	else:
		extend_to(lr,-lmaxl)
		llvls.insert(0,make_dict(h=h0,minl=0.,maxl=0.))
		rl.lvls = reslvls
		rl.type = 'pool'
	return lr,rl

if debug:
	print()
	print('add zero section',leftx,lefty)
i=0
watchdog = 0
droppedV = 0.
filledV = 0.
while True:
	if debug:
		print(':::::::')
		print('outer cycle',len(Pools))
		#for pool in Pools:
		#	print(pool)
	if i<N:
		rightx,righty = map(float,input().split())
		most_right = rightx
		assert rightx>leftx
		curlen = rightx-leftx
		curV = curlen*Dens
		droppedV += curV
		#print('adding',i,curlen)
		if righty<lefty: # decrease
			Pools.append(make_dict(
				type='toright',
				lvls=[make_dict(h=righty,minl=0.,maxl=0.),make_dict(h=lefty,minl=curlen,maxl=curlen)],
				overvol=curV,
				bottom=righty
				))
		else: # increase
			Pools.append(make_dict(
				type='toleft',
				lvls=[make_dict(h=lefty,minl=0.,maxl=0.),make_dict(h=righty,minl=curlen,maxl=curlen)],
				overvol=curV,
				bottom=lefty
				))
		leftx,lefty = rightx,righty
		i+=1
		if debug:
			print('add one section',leftx,lefty)
	else:
		pool = Pools.pop()
		if pool.type=='toright':
			#print(':::::::')
			if debug: print('do to right wall')
			pool.type='pool'
			V = pool.overvol
			# уровни остаются теми же
			pool.overvol = 0.
			V = fill_pool(pool,V) # 
			if V>0.:
				if debug: print('do wall (pool) to right')
				pool.type = 'toleft'
				pool.overvol = V
			Pools.append(pool)
			watchdog+=1
			if watchdog>10:
				raise Exception()
		else:
			#print(':::::::')
			Pools.append(pool)
			break

	while True:
		if debug:
			print('inner cycle',len(Pools))
			#for pool in Pools:
			#	print(pool)

		assert len(Pools)!=0
		assert sum(pool.lvls[-1].maxl for pool in Pools) - (most_right - most_left)<0.000000001
		assert droppedV-filledV-sum(pool.overvol for pool in Pools) < 0.00000001
		pool = Pools.pop()

		if len(Pools)==0:
			if pool.type=='toright':
				if debug: print('do wall to right')
				Pools.append(pool)
			else: # toleft
				if debug: print('do wall to left')
				pool.type='pool'
				V = pool.overvol
				# уровни остаются теми же
				pool.overvol = 0.
				V = fill_pool(pool,V) # 
				if V>0.:
					if i<N:
						if debug: print('do wall (pool) to right')
						pool.type = 'toright'
						pool.overvol = V
					else:
						pool.type = 'pool'
						pool.overvol = 0
						best_H += V/(most_right - most_left)
				Pools.append(pool)
			break # 
		else:
			if pool.type=='toright':
				if Pools[-1].type=='toright':
					if debug: print('do merge right right')
					Pools[-1] = merge_toto(pool,Pools[-1]) # нижний, верхний
				else:
					if debug: print('do right push back')
					Pools.append(pool)
				break
			else:
				two = pool
				one = Pools.pop()
				if one.type=='toleft':
					if debug: print('do merge left left')
					Pools.append(merge_toto(one,two))
				elif one.type=='pool': # pool-toleft
					V = fill_pool(one,two.overvol)
					two.overvol = 0.
					if V==0.:
						if debug: print('do (fill)pool left')
						Pools.append(one)
						Pools.append(two)
						break
					else:
						if debug: print('do (fill pool) left')
						extend_to(two,one.lvls[-1].maxl)
						two.overvol = V
						two.bottom = min(one.bottom,two.bottom)
						one.bottom = min(one.bottom,two.bottom)
						Pools.append(two)
				elif one.type=='toright': # toright-toleft
					if debug: print('do (make pool)')
					V = one.overvol+two.overvol
					one,two = make_pool(one,two) # overvol==0 in both
					#if debug:
					#	print(f'{one=}')
					#	print(f'{two=}')
					if two.type=='pool': # toright-pool
						V = fill_pool(two,V)
						if V==0.:
							if debug: print('do toright (fill)pool')
							one.overvol = 0.
							two.overvol = 0.
							Pools.append(one)
							Pools.append(two)
						else:
							if debug: print('do toright (fill pool)')
							extend_to(one,two.lvls[-1].maxl)
							one.overvol = V
							one.bottom = min(one.bottom,two.bottom)
							two.bottom = min(one.bottom,two.bottom)
							Pools.append(one)
							#if debug:
							#	for pool in Pools:
							#		print(pool)
							#	print()
						break
					else: # pool-toleft
						if debug: print('do pool toleft')
						one.overvol = 0.
						two.overvol = V
						Pools.append(one)
						Pools.append(two)
				else:
					assert False

if debug:
	print(':::::::')
	print('final:')
	for pool in Pools:
		print(pool)

print(best_H)