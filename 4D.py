debug = False

def arrstat(arr):
	return sum(arr)+len(arr) , max(arr)

total_width,ll,rl = map(int,input().split()) # left/right lenght
la = list(map(int,input().split())) # left/right array
ra = list(map(int,input().split()))
lv,lmal = arrstat(la) # left/right volume
rv,rmal = arrstat(ra) # left/right max length

def calc_h(arr,width):
	#global lmal,rmal
	minover = max(lmal,rmal)
	minunder = minover
	pos = 0
	line = 1
	for word in arr:
		if pos+word>width:
			assert pos!=0
			minover = min(minover,pos+word-width) # на сколько надо сдвинуть границу вправо, чтобы следующее слово туда поместилось 
			minunder = min(minunder,width-pos+1+1) # на сколько надо сдвинуть границу влево, чтобы предыдущее слово здесь НЕ поместилось
			line+=1
			pos = word+1
		else:
			pos+= word+1
	minunder = min(minunder,width-pos+1+1)
	return (line if pos!=0 else line-1),minover,minunder

TOTAL_HEIGHT = -1
LEFT_STEP = 0
RIGHT_STEP = 0
def check(vp):
	if debug: print('check',vp)
	global TOTAL_HEIGHT,LEFT_STEP,RIGHT_STEP
	lh,mlr,mll = calc_h(la,vp)
	rh,mrl,mrr = calc_h(ra,total_width-vp)
	hhh = max(lh,rh)
	TOTAL_HEIGHT = hhh if TOTAL_HEIGHT==-1 else min(hhh,TOTAL_HEIGHT)
	LEFT_STEP = min(mll,mrl)
	RIGHT_STEP = min(mlr,mrr)
	if debug: print(lh,mlr,mll,' - ',rh,mrl,mrr)
	return lh-rh # >0 go to right, <0 go to left

def center_bound(first,last,check):
	if debug: print(first,last)
	if check(first)<0:
		return first,1
	if check(last-1)>0:
		return last,2
	count = last - first
	c=2
	while count > min(LEFT_STEP,RIGHT_STEP)-1:
		step = count // 2
		it = first+step; 
		tmp = check(it)
		c+=1
		if debug: print(it,tmp,end=' ')
		if tmp>0 :
			if debug: print('<')
			first = it+1
			count -= (step + 1) 
		elif tmp==0:
			if debug: print('==')
			return it,c
		else:
			if debug: print('>')
			count = step
	return first,c

start = round(total_width*lv/(lv+rv))
start = min(max(start,lmal),total_width-rmal)
if debug:
	print(lmal,start,total_width-rmal)
zz = center_bound(lmal,total_width-rmal+1,check)
if debug:
	print(zz,TOTAL_HEIGHT,LEFT_STEP,RIGHT_STEP)
print(TOTAL_HEIGHT)

if debug:
	print()
	for vp in range(lmal,lmal+10):
		print(vp,calc_h(la,vp))
	print()
	for vp in range(rmal,rmal+10):
		print(vp,calc_h(ra,vp))