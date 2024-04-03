# 3H
'''
в первом наборе спичек для каждой вычисляем dx dy
и складываем в map, отсортировав точки


по второму набору
	по всем точкам первого набора с той же длиной и ориентацией
		вычисляем перенос, добавляем++, обновляем максимум
'''
def diff(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	dx = x2-x1
	dy = y2-y1
	return dx,dy
def sort_points(p1,p2):
	x1,y1 = p1
	x2,y2 = p2
	dx = x2-x1
	dy = y2-y1
	if dx==0:
		assert dy!=0
		if dy<0:
			return p2,p1
		else:
			return p1,p2
	elif dx>0:
		return p1,p2
	else:
		return p2,p1

from collections import defaultdict
orientations = defaultdict(list)

N = int(input())
for i in range(N):
	x1,y1,x2,y2 = map(int,input().split())
	p1,p2 = sort_points((x1,y1),(x2,y2))
	dx,dy = diff(p1,p2)
	orientations[(dx,dy)].append(p1)

m = 0
incedence = defaultdict(int)

for i in range(N):
	x1,y1,x2,y2 = map(int,input().split())
	p1,p2 = sort_points((x1,y1),(x2,y2))
	dx,dy = diff(p1,p2)
	if (dx,dy) in orientations:
		for p0 in orientations[(dx,dy)]:
			ddx,ddy = diff(p0,p1)
			incedence[(ddx,ddy)]+=1
			m = max(m,incedence[(ddx,ddy)])
print(N-m)
