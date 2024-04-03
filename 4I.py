debug = 1

from math import *

def diff(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	return x2-x1, y2-y1
def sq_dist(p1,p2):
	dx,dy = diff(p1,p2)
	return dx**2 + dy**2
if debug>2: 
	print(f'{sq_dist((0.,0.),(3.,4.))=}')

def c_rel_c(c1,r1,c2,r2):
	sqd = sq_dist(c1,c2)
	if sqd<=(r2-r1)**2:
		if r2>r1:
			return '1in2'
		else:
			return '2in1'
	if sqd>(r2+r1)**2:
		return 'out'
	return 'inter'
if debug>2:
	print(f'{c_rel_c((0.,0.),2.,(0.,1.),0.5)=}')
	print(f'{c_rel_c((0.,0.),2.,(0.,1.),3. )=}')
	print(f'{c_rel_c((0.,0.),2.,(0.,1.),2. )=}')
	print(f'{c_rel_c((0.,0.),2.,(5.,0.),1. )=}')
def intersections(c1,r1,c2,r2):
	x1,y1 = c1
	x2,y2 = c2
	d = sqrt(sq_dist(c1,c2))
	a = (r1**2-r2**2+d**2)/2/d
	h = sqrt(r1**2-a**2)
	x0 = x1 + a * (x2 - x1) / d
	y0 = y1 + a * (y2 - y1) / d
	x3 = x0 + h * (y2 - y1) / d
	y3 = y0 - h * (x2 - x1) / d
	x4 = x0 - h * (y2 - y1) / d
	y4 = y0 + h * (x2 - x1) / d
	return (x3,y3),(x4,y4)
if debug>2:
	print(f'{intersections((0.,0.),2.,( 0., 1.),2. )=}')
	print(f'{intersections((0.,0.),2.,( 0.,-1.),2. )=}')
	print(f'{intersections((0.,0.),2.,( 1., 0.),2. )=}')
	print(f'{intersections((0.,0.),2.,(-1., 0.),2. )=}')
	print(f'{intersections((0.,0.),1.,( 1., 1.),1. )=}')

class Circle:
	__slots__ = ['c','v','r','rel','cd']
	def __init__(self,c,v):
		self.c = c
		self.v = v
	def __repr__(self):
		return repr((self.c,self.v))
	def cr(self):
		return self.c, self.r

D,N = input().split()
D = float(D)
N = int(N)
circs = []
M = 1e20
for i in range(N):
	x,y,v = map(float,input().split())
	M = min(M,(sqrt(x**2+y**2)+D+0.1)/v)
	circs.append(Circle((x,y),v))
if debug: print(f'{M=} {D=}')

def p_in_D(p):
	return p[1]>=0 and p[0]**2+p[1]**2<=D**2
def c_rel_D(c1,r1):
	rel = c_rel_c(c1,r1,(0.,0.),D)
	if rel=='out':
		return 'out',[]
	if rel=='1in2':
		if c1[1]-r1>=0:
			return 'СinD',[]
		elif c1[1]+r1<=0:
			return 'out',[]
		else:
			x1 = c1[0] + sqrt(r1**2-c1[1]**2)
			x2 = c1[0] - sqrt(r1**2-c1[1]**2)
			return 'inter',[(x1,0.),(x2,0.)]
	if rel=='2in1':
		return 'DinC',[]
	assert rel=='inter'
	p1,p2 = intersections(c1,r1,(0.,0.),D)
	if p1[1]>=0 and p2[1]>=0:
		if c1[1]-r1>0:
			return 'inter',[p1,p2]
		else:
			x1 = c1[0] + sqrt(r1**2-c1[1]**2)
			x2 = c1[0] - sqrt(r1**2-c1[1]**2)
			return 'inter',[p1,p2,(x1,0.),(x2,0.)]
	elif p1[1]<0 and p2[1]<0:
		if c1[1]+r1<=0:
			return 'out',[]
		else:
			x1 = c1[0] + sqrt(r1**2-c1[1]**2)
			x2 = c1[0] - sqrt(r1**2-c1[1]**2)
			if abs(x1)>D and abs(x2)>D:
				return 'DinC',[]
			assert abs(x1)<=D and abs(x2)<=D
			return 'inter',[(x1,0.),(x2,0.)]
	else:
		x1 = c1[0] + sqrt(r1**2-c1[1]**2)
		x2 = c1[0] - sqrt(r1**2-c1[1]**2)
		if abs(x1)<D:
			assert abs(x2)>=D
			x = x1
		else:
			assert abs(x2)<D
			x = x2
		if p1[1]>=0:
			return 'inter' , [p1 , (x,0.)]
		assert p2[1]>=0
		return 'inter' , [p2 , (x,0.)]
if debug>2:
	print(f'{c_rel_D((0.,12.),1.)=}')
	print(f'{c_rel_D((0., 8.),1.)=}')
	print(f'{c_rel_D((0.,-8.),1.)=}')
	print(f'{c_rel_D((0., 0.),1.)=}')
	print(f'{c_rel_D((0., 0.),11.)=}')
	print(f'{c_rel_D((0., 5.),6.)=}')
	print(f'{c_rel_D((0., 9.),2.)=}')
	print(f'{c_rel_D((0.,-9.),2.)=}')
	print(f'{c_rel_D((0., 5.),12.)=}')
	print(f'{c_rel_D((0.,-5.),6.)=}')
	print(f'{c_rel_D((-10.,0.),2.)=}')

if debug: print(circs)

FREE = (0.,0.)
def check(T):
	if debug: print('check',T)
	global FREE
	Disopen = True
	for ic1 in range(N):
		circs[ic1].r = circs[ic1].v*T
		circs[ic1].rel,circs[ic1].cd = c_rel_D(*circs[ic1].cr())
		if circs[ic1].rel=='DinC':
			if debug: print(ic1,circs[ic1].r,'covers all D, return False')
			return 1 # накрывает полностью, нет свободного места
		elif circs[ic1].rel!='out':
			Disopen = False
	if Disopen:
		if debug: print('D ни с кем не пересекается, return True')
		FREE = (0.,0.)
		return 0

	for ic1 in range(N):
		c1,r1 = circs[ic1].cr()
		c1relD = circs[ic1].rel
		if c1relD=='out':
			if debug: print(ic1,r1,'is out D')
			continue
		else:
			if debug: print(ic1,r1,': checking')
		# c1,r1 пересекается (как круг) с D, но накрывает его не полностью, т.е. CinD или inter
		# причем найдется по крайней мере один такой круг
		c1isopen = True
		for ic2 in range(N):
			if ic2==ic1 or circs[ic2].rel=='out':
				continue
			c2,r2 = circs[ic2].cr()
			rel12 = c_rel_c(c1,r1,c2,r2)
			if rel12=='2in1' or rel12=='out':
				#if debug: print(' ',ic2,r2,'is inside or outside ',ic1,r1)
				continue
			if rel12=='1in2':
				c1isopen = False
				if debug: print(' ',ic2,r2,'covers',ic1,r1)
				break
			cross1,cross2 = intersections(c1,r1,c2,r2)
			both_outside = True
			if p_in_D(cross1):
				both_outside = False
				c1isopen = False
				if debug: print('  check intersection',cross1,ic1,r1,ic2,r2)
				for ic3 in range(N): # точка должна оказаться снаружи всех остальных кругов
					if ic3==ic1 or ic3==ic2 or circs[ic3].rel=='out':
						continue
					c3,r3 = circs[ic3].cr()
					if sq_dist(c3,cross1)<r3**2:
						if debug: print('    intersection in',ic3,r3)
						break # пересечение покрывается другим кругом
				else:
					if debug: print('    intersection is free, return True')
					FREE = cross1
					return 0
			if p_in_D(cross2):
				both_outside = False
				c1isopen = False
				if debug: print('  check intersection',cross2,ic1,r1,ic2,r2)
				for ic3 in range(N): # точка должна оказаться снаружи всех остальных кругов
					if ic3==ic1 or ic3==ic2 or circs[ic3].rel=='out':
						continue
					c3,r3 = circs[ic3].cr()
					if sq_dist(c3,cross2)<r3**2:
						if debug: print('    intersection in',ic3,r3)
						break # пересечение покрывается другим кругом
				else:
					if debug: print('    intersection is free, return True')
					FREE = cross2
					return 0
			if both_outside:
				out_points = []
				for p in circs[ic1].cd:
					if sq_dist(p,c2)>=r2**2:
						out_points.append(p)
				circs[ic1].cd = out_points
				if len(out_points)==0:
					c1isopen = False
					break
		if c1isopen:
			if c1relD=='CinD':
				if debug: print(' ',ic1,r1,'is totally free, return True')
				FREE = (c1[0],c1[1]+r1)
			else:
				if debug: print(' ',ic1,r1,'intersects only D, return True')
				assert c1relD=='inter'
				FREE = circs[ic1].cd[0]
			return 0
	if debug: print('все пересечения покрываются или находятся вне D, return False')
	return 1


def upper_bound(first,last, check):
	count = last-first
	while count > 0.000001:
		step = count / 2; 
		it = first+step
		if check(it) <= 0:
			first = it;
			count = step
		else:
			count = step
	return first

#if debug:
#	print(check(2.3378),FREE)
#	(x,y),v = circs[2]
#	print(f'{c_rel_D((x,y),v*2.3378)=}')
print(upper_bound(0.0001,M, check)-0.0000001)
print(FREE[0],FREE[1])
