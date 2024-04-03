class Arr:
	def __init__(self,arr):
		self.arr = arr
	def __getitem__(self,p):
		return self.arr[p[0]][p[1]]
	def __setitem__(self,p,v):
		self.arr[p[0]][p[1]] = v
	def getline(self,i):
		return self.arr[i]
	def size(self):
		return (len(self.arr),len(self.arr[0]))
class RArr:
	def __init__(self,arr):
		self.arr = arr
	def __getitem__(self,p):
		return arr[p[1]][p[0]]
	def __setitem__(self,p,v):
		arr[p[1]][p[0]] = v
	def getline(self,n):
		return [self.arr[i][n] for i in range(len(self.arr))]
	def size(self):
		return (len(self.arr[0]),len(self.arr))
def scan(arr):
	h,w = arr.size()
	curline = ['.' for i in range(w)]
	res = []
	for i in range(h):
		t = arr.getline(i)
		if t!=curline:
			res.append(i)
			curline = t
	if curline != ['.' for i in range(w)]:
		res.append(h)

	return res
def paint(arr,a,b,c,d):
	out = []
	for i in range(0,a):
		out.append(arr.getline(i))
	for i in range(a,b):
		out.append(list(map(lambda x: x.replace('#', 'a'), arr.getline(i))))
	for i in range(b,c):
		out.append(arr.getline(i))
	for i in range(c,d):
		out.append(list(map(lambda x: x.replace('#', 'b'), arr.getline(i))))
	for i in range(d,arr.size()[0]):
		out.append(arr.getline(i))
	return out
def pprint(arr):
	for i in range(arr.size()[0]):
		print(''.join(arr.getline(i)))
def out(pict,a,b,c,d):
	pict = paint(Arr(pict),a,b,c,d)
	pprint(Arr(pict))
def rout(pict,a,b,c,d):
	pict = paint(RArr(pict),a,b,c,d)
	pprint(RArr(pict))

def main(W,H,pict):
	y_stages = scan(Arr(pict))
	x_stages = scan(RArr(pict))
	#print(y_stages,x_stages)
	if len(x_stages)>4 or len(y_stages)>4 or len(x_stages)==0 or len(y_stages)==0 :
		print('NO')
		return
	if len(y_stages)==4 and '#' not in Arr(pict).getline(y_stages[1]):
		if len(scan(RArr([Arr(pict).getline(y_stages[0])])))!=2 or len(scan(RArr([Arr(pict).getline(y_stages[2])])))!=2:

			print('NO')
		else:
			print('YES')
			out(pict,*y_stages)
		return
	if len(x_stages)==4 and '#' not in RArr(pict).getline(x_stages[1]):
		if len(scan(RArr([RArr(pict).getline(x_stages[0])])))!=2 or len(scan(RArr([RArr(pict).getline(x_stages[2])])))!=2:
			print('NO')
		else:
			print('YES')
			rout(pict,*x_stages)
		return
	if len(y_stages)==4 and len(x_stages)==4:
		print('NO')
		return
	if len(y_stages)==4 and len(x_stages)==3:
		print('YES')
		rout(pict,x_stages[0],x_stages[1],x_stages[1],x_stages[2])
		return
	if len(y_stages)==3 and len(x_stages)==4:
		print('YES')
		out(pict,y_stages[0],y_stages[1],y_stages[1],y_stages[2])
		return
	if len(y_stages)==3 and len(x_stages)==3:
		print('YES')
		out(pict,y_stages[0],y_stages[1],y_stages[1],y_stages[2])
		return
	if len(x_stages)==2 and len(y_stages)==2:
		if x_stages[1]-x_stages[0]>1 and y_stages[1]-y_stages[0]>1:
			print('YES')
			out(pict,y_stages[0],y_stages[0]+1,y_stages[0]+1,y_stages[1])
			return
		if x_stages[1]-x_stages[0]==1 and y_stages[1]-y_stages[0]>1:
			print('YES')
			out(pict,y_stages[0],y_stages[0]+1,y_stages[0]+1,y_stages[1])
			return
		if x_stages[1]-x_stages[0]>1 and y_stages[1]-y_stages[0]==1:
			print('YES')
			rout(pict,x_stages[0],x_stages[0]+1,x_stages[0]+1,x_stages[1])
			return
		print('NO')
		return
	assert False

H,W = map(int,input().split())
pict = []
for i in range(H):
	pict.append(list(input()))
main(W,H,pict)