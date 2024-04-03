


# 3J
from collections import defaultdict
N,K = map(int,input().split())

timing = False
debug = False
if timing:
	import time
	start_time = time.time()


class AttrDict(dict):
    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key) # essential for testing by hasattr
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value
def make_dict(**kwargs):
    return AttrDict(kwargs)

machs = [make_dict(
	start_freq=1, # самый редкий freq in need_frag_byfreq
	need_frag_byfreq={1:{j for j in range(K)}}, # need_frag
	total_need=K,
	rate_other=[0 for j in range(N)],
	time_full=-1
) for i in range(N)]
machs[0].need_frag_byfreq={}
machs[0].total_need=0
machs[0].start_freq=-1
machs[0].time_full=0
# Перед каждым таймслотом для каждой части обновления определяется, на скольких устройствах сети скачана эта часть.
total_frags = [{0} for i in range(K)] # фрагмент -> список машин

generation = 0
while True:
	generation+=1
	back_requests = defaultdict(list)

	dev_byfrag = {}

	for im in range(1,N): # Каждое устройство 
		if machs[im].start_freq==-1:
			continue
		#mi = 10000000
		imi = min(machs[im].need_frag_byfreq[machs[im].start_freq])
		#for inf in machs[im].need_frag_byfreq[machs[im].start_freq]: # выбирает отсутствующую на нем часть обновления
		#	if len(total_frags[inf])<mi: # , которая встречается в сети реже всего.
		#		mi = len(total_frags[inf])
		#		imi = inf
		#	# Если таких частей несколько, то выбирается отсутствующая на устройстве часть обновления с наименьшим номером.
		#	elif len(total_frags[inf])==mi and inf<imi: 
		#		imi = inf

		if imi in dev_byfrag:
			ima = dev_byfrag[imi]
		else:
	 		#После этого устройство делает запрос выбранной части обновления у одного из устройств,
			ma = 0
			ima = 0
			for inm in total_frags[imi]: # на котором такая часть обновления уже скачана.
				# Если таких устройств несколько — выбирается устройство, на котором скачано наименьшее количество частей обновления.
				if machs[inm].total_need>ma:
					ma = machs[inm].total_need
					ima = inm
				# Если и таких устройств оказалось несколько — выбирается устройство с минимальным номером.
				elif machs[inm].total_need==ma and inm<ima:
					ima = inm
			assert ima!=-1 and ima!=im
			dev_byfrag[imi] = ima
		back_requests[ima].append((im,imi)) # у машины ima запрашивает фрагмент imi машина im

	if len(back_requests)==0:
		break

	if debug:
		pass
		print(generation,dict(back_requests)) # sum(len(x) for k,x in back_requests.items()),len(back_requests))

	#selfs = set()
	#После того, как все запросы отправлены, каждое устройство выбирает, чей запрос удовлетворить.
	for ifrom,li in back_requests.items():
		selm = -1
		self = -1
		maxrate = -1
		maxneed = 1000000000
		pito = -1
		for ito,inf in li:
			#print(ifrom,ito,inf,"ifrom,ito,inf",machs[ifrom].rate_other)
			assert ito>pito # Если и таких запросов несколько, то среди них выбирается устройство с наименьшим номером. 
			pito = ito
			# Устройство A удовлетворяет тот запрос, который поступил от наиболее ценного для A устройства.
			if machs[ifrom].rate_other[ito]>maxrate:
				selm = ito
				self = inf
				maxrate = machs[ifrom].rate_other[ito]
				maxneed = machs[ito].total_need
			# Если на устройство A пришло несколько запросов от одинаково ценных устройств,
			# то удовлетворяется запрос того устройства, на котором меньше всего скачанных частей обновления.
			elif machs[ifrom].rate_other[ito]==maxrate and machs[ito].total_need>maxneed: # или у кого поменьше скачано
				selm = ito
				self = inf
				#maxrate = machs[ifrom].rate_other[ito]
				maxneed = machs[ito].total_need
		back_requests[ifrom] = (selm,self)
		#assert self not in machs[ifrom].need_frag_byfreq[machs[ifrom].start_freq]
		#assert self not in selfs
		#selfs.add(self)

	for ifrom,(ito,inf) in back_requests.items():
		#machs[ito].need_frag_byfreq[machs[ito].start_freq].remove(inf) # скачиваем
		start = machs[ito].start_freq # сколько раз встречается inf
		for im in range(N): # по всем машинам
			if machs[im].start_freq!=-1: # которые не завершены
				if start in machs[im].need_frag_byfreq:
					if inf in machs[im].need_frag_byfreq[start]: # если там требуется inf
						machs[im].need_frag_byfreq[start].remove(inf)
						if len(machs[im].need_frag_byfreq[start])==0:
							del machs[im].need_frag_byfreq[start]
							if start==machs[im].start_freq:
								if im!=ito:
									machs[im].start_freq+=1
								else:
									if len(machs[im].need_frag_byfreq)==0:
										machs[ito].time_full = generation # отмечаем время завершения скачивания
										machs[ito].start_freq=-1
									else:
										machs[ito].start_freq = min(machs[im].need_frag_byfreq)
						if im!=ito:
							if start+1 not in machs[im].need_frag_byfreq:
								machs[im].need_frag_byfreq[start+1] = set()
							machs[im].need_frag_byfreq[start+1].add(inf)


		total_frags[inf].add(ito)
		# Ценность устройства B(from) для устройства A(to) определяется как количество частей обновления, ранее полученных устройством A(to) от устройства B(from).
		machs[ito].rate_other[ifrom]+=1
		machs[ito].total_need-=1
			

	if debug:
		pass
		print(generation,len(dict(back_requests)))
		print(dict(back_requests))
		for i in range(N):
			def has(im,inf):
				if machs[im].start_freq==-1:
					return True
				for k,q in machs[i].need_frag_byfreq.items():
					if inf in q:
						return False
				return True
			print(i,' '.join(['*' if has(i,j) else ' ' for j in range(K)]),machs[i].total_need,machs[i].rate_other,machs[im].start_freq,machs[i].need_frag_byfreq)
		print(' ',' '.join(str(len(total_frags[q])) for q in range(K)))
		print()

for im in range(1,N):
	print(machs[im].time_full,end=' ')
print()
if timing:
	print(K*(N-1)/generation,'stop',time.time() - start_time)
