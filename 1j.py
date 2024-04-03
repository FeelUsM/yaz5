'''
y позиция строки
высота строки
список фрагментов
	начало, конец
	free
	img нижняя граница

x позиция в строке
текуший фрагмент

ф-ции:
	вывести слово
	вывести embed
	вывести surr
	вывести float

'''
class AttrDict(dict):
    def __getattr__(self, key):
        if key not in self:
            raise AttributeError() # essential for testing by hasattr
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value
def make_dict(**kwargs):
    return AttrDict(kwargs)

class frag:
	def __init__(self,l,r,typ,bottom=0):
		self.l = l
		self.r = r
		assert typ=='str' or typ=='img'
		self.type = typ
		if typ=='img': assert bottom!=0
		self.bottom = bottom
	def __repr__(self):
		return f'[{self.l} {self.type}{self.bottom if self.type=="img" else ""} {self.r}]'
class screen:
	__slots__ = [
	'W','H','C', # ширина экрана, высота строки, ширина символа
	'y_str', # координата верхней границы строки
	'h_str', # высота текущей строки с учётом embedded картинок
	'frags', # список фрагментов
	'x_str', # позиция курсора в строке
	'i_frag', # № текущего фрагмента
	'last_float', # зажигается в True после вывода floating картинки, и гаснет после вывода всего остального
	'x_float', # координаты правого верхнего угла последней выведенной floating картинки
	'y_float', 
	'void_par', # зажигается в True после начала параграфа, и гаснет после вывода блока
	]
	def trace(self,mes):
		return
		print(mes,end=' ')
		for i in range(len(self.frags)):
			if self.i_frag == i:
				print('*',end='')
			print(self.frags[i],end=' ')
		print()
	def __init__(self,w,h,c):
		self.W = w
		self.H = h
		self.C = c
		self.y_str = 0
		self.h_str = self.H
		self.frags = [frag(0,self.W,'str')]
		self.x_str = 0
		self.i_frag = 0
		self.last_float = False
		self.void_par = True
		self.trace('init')
	def newpar(self):
		self.last_float = False
		b = self.y_str
		if self.x_str!=0 or self.void_par: # излишне. перейдя на новую строку обязательно выведем блок
			b+=self.h_str
		for i in range(len(self.frags)):
			if self.frags[i].type == 'img':
				if self.frags[i].bottom>b:
					b = self.frags[i].bottom
		self.y_str = b
		self.h_str = self.H
		self.frags = [frag(0,self.W,'str')]
		self.x_str = 0
		self.i_frag = 0
		self.void_par = True
		self.trace('\n\nnewpar')
	def newstr(self):
		self.y_str += self.h_str
		self.h_str = self.H
		# освобождаю закончившиеся фрагменты
		for i in range(len(self.frags)):
			if self.frags[i].type=='img':
				if self.frags[i].bottom<=self.y_str:
					self.frags[i].type = 'str'
					self.frags[i].bottom = 0
		# склеиваю строковые фрагменты
		newf = [self.frags[0]]
		for i in range(1,len(self.frags)):
			assert self.frags[i-1].r==self.frags[i].l
		for i in range(1,len(self.frags)):
			if newf[-1].type=='str' and self.frags[i].type=='str':
				newf[-1].r = self.frags[i].r
			else:
				newf.append(self.frags[i])
		self.frags = newf

		self.i_frag = 0
		self.x_str = 0
		self.trace('\nnewstr')
	def outbox(self,w,h,isimg,addspc=True):
		'''
		isimg - выводить ли в output координаты блока
		addspc - добавлять ли пробел, если выводим не в начале фрагмента
		'''
		self.void_par = False
		while True: # если нет подходящей строки - генерируем следующую
			while self.i_frag<len(self.frags): # если нет подходящего фрагмента - ищем следующий
				if self.frags[self.i_frag].type!='str':
					self.i_frag+=1
					continue
				if self.x_str < self.frags[self.i_frag].l:
					self.x_str = self.frags[self.i_frag].l
				if self.frags[self.i_frag].l==self.x_str:
					L = w
				elif addspc:
					L = w + self.C
				else:
					L = w
				r = self.x_str+L
				if r>self.frags[self.i_frag].r: # если не пдходит в текущий фрагмент
					self.i_frag+=1
				else: # подошёёёёл!!!
					if isimg:
						if L!=w:
							print(self.x_str+self.C,self.y_str)
						else:
							print(self.x_str,self.y_str)
					self.x_str+=L
					if h>self.h_str:
						self.h_str = h
					self.trace('outbox')
					return # даже если текущий фрагмент заполнили полностью, остемся в нём
			self.newstr()
	def out_word(self,s):
		self.last_float = False
		self.outbox(self.C*len(s),self.H,False) # не выводить
	def out_img(self,img):
		if img.layout == 'embedded':
			self.last_float = False
			self.outbox(img.width,img.height,True) # выводить
		elif img.layout == 'floating':
			if self.last_float:
				x = self.x_float+img.dx
				y = self.y_float+img.dy
			else:
				x = self.x_str+img.dx
				y = self.y_str+img.dy
			if x<0:
				x = 0
			if x+img.width>self.W:
				x = self.W-img.width
			print(x,y)
			self.last_float = True
			self.x_float = x+img.width
			self.y_float = y
		elif img.layout == 'surrounded':
			self.last_float = False
			self.outbox(img.width,self.H,True,False) # выводим, пробел вначале не ставим, высоту берём минимальную
			fl = self.frags[self.i_frag].l # границы фрагмента
			fr = self.frags[self.i_frag].r
			il = self.x_str - img.width # границы картинки
			ir = self.x_str
			self.frags[self.i_frag].type = 'img' # текущий фрагмент становится картинкой
			self.frags[self.i_frag].bottom = self.y_str + img.height # вычисляем её дно (низ)
			self.frags[self.i_frag].l = il # границы фрагмента = границы картинки
			self.frags[self.i_frag].r = ir
			# если надо, добавляем фрагменты справа
			if ir!=fr:
				self.frags.insert(self.i_frag+1,frag(ir,fr,'str'))
			# и слева
			if il!=fl:
				self.frags.insert(self.i_frag,frag(fl,il,'str'))
				self.i_frag+=1
			self.i_frag+=1 # излишне. outbox() сам найдет следующий фрагмент типа str
			self.trace('surround')
'''
считать параметры
считать строки до пустой
распарсить картинки 
массив строк и картинок
'''
def main():
	with open("input.txt") as fp:
		w,h,c = map(int,fp.readline().split())
		scr = screen(w,h,c)
		while True:
			tokens = []
			while True:
				nstr = fp.readline()
				if len(nstr) == 0: # EOF
					if len(tokens):
						break
					else:
						return
				nstr = nstr.strip()
				if len(nstr) == 0: # end paragraph
					break
				tokens+=nstr.split()
			i = 0
			while i< len(tokens):
				if tokens[i] == '(image':
					img = AttrDict()
					i+=1
					while not tokens[i].endswith(')'):
						k,v = tokens[i].split('=')
						if k!='layout':
							v = int(v)
						img[k]=v
						i+=1
					k,v = tokens[i][:-1].split('=') # [:-1] - обрезаем ')' в конце токена
					if k!='layout':
						v = int(v)
					img[k]=v

					scr.out_img(img)
					i+=1

				else:
					scr.out_word(tokens[i])
					i+=1



			scr.newpar()
main()
