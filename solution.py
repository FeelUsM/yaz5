import numpy as np

# я закономерность буду называть центральностью

# чтобы получить центральность необходимо в некоторой строке изменить один бит
# если строка x отличается от строки y одним битом, то изменением этого бита в строке x центральность получить невозможно
# центральность будем обозначать строкой, состоящей из '.', '0', '1' (точки и биты)
# при изменении любого бита (0<->1) в центральности мы должны получить паттерн (на строку), присутствующий в матрице
# если из строки x можно добраться в строку y изменив биты k,l, а строки x,y отличаются битами k,l,m_i, то биты m_i отсутствуют в центральности

# все множества не превышают 100 элементов, поэтому будем их хранить в целых числах как битовые множества

# матрица расстояний показывает, какие биты надо изменить, чтобы одна строка превратилась в другую
# в каждой строке пытемся изменить каждый бит
# найденные центральности складываем в общее множество
# далее алгоритм:
# 
# строку-бит задали (рассматриваем столбец в матрице расстояний, соответствующий данной строке. Он состоит из множеств)
# выбираем строки, в которых этот бит присутствует
#   в каждом множестве исключаем этот бит
# 
# среди выбранных
#   если есть пустые множества - конец (в эту строку можно добраться изменив только один бит)
#   если есть множества из одного элемента - фиксируем их (в эти строки можно добраться единственным способом)
#   из выбранных строк исключаем те, в которых присутствуют фиксированные элементы (они точно не равны центральности)
#   если строк не осталось - yield (найденные центральности складываем в общее множество)
# 
#   объединяем все множества выбранных строк
#   + подсчитываем, сколько раз встречается каждый элемент, и перебираем от меньшего к большему
#   по каждому элементу из этого множества
#       выбранные строки разбиваем на текущие (те, в которых присутствуют этот элемент (они точно не равны центральности)), и дальнейшие (для дальнейшего анализа)
#       если все текущие строки ранее обрабатывались - continue
#       пересекаем текущие строки
#       фиксируем этот элемент, а остальные элементы из пересечения добавляем в исключённые (точно должны отсутствовать в центральности)
#       из дальнейших множеств удаляем исключённые

#       если есть пустые множества - конец (в эту строку можно добраться изменив только один бит)
#       если есть множества из одного элемента - фиксируем их (в эти строки можно добраться единственным способом)
#       из выбранных строк исключаем те, в которых присутствуют фиксированные элементы (они точно не равны центральности)

#       если дальнейших строк не осталось - yield (найденные центральности складываем в общее множество)
#       по каждой из текущих строк, которые раньше не обрабатывали
#           остальные элементы из этой строки добавляем в исключённые (точно должны отсутствовать в центральности)
#           из дальнейших множеств удаляем исключённые
# 
#           если есть пустые множества - конец (в эту строку можно добраться изменив только один бит)
#           если есть множества из одного элемента - фиксируем их (в эти строки можно добраться единственным способом)
#           из выбранных строк исключаем те, в которых присутствуют выбранные элементы (они точно не равны центральности)
# 
#           если строк не осталось - yield (найденные центральности складываем в общее множество)
#           -> объединяем все множества выбранных строк (рекурсия)
#       из выбранных строк исключаем этот элемент (он полностью обработан)
#       если есть пустые строки - конец
# 
# + в алгоритм добавляем опитимизации, чтобы он не пытался добраться из текущей строки в ранее полностью рассмотренные
# ответ - размер общего множества центральностей + количество постоянных столбцов (которые мы в самом начале исключили)

from inspect import getframeinfo, stack

def thisline(message):
    caller = getframeinfo(stack()[1][0])
    return caller.lineno

def bits(x,l):
    s = ''
    for i in range(l):
        s+= '1' if (2**i)&x else '0'
    return s
def sets(x):
    se = set()
    i=0
    q=1
    while q<=x:
        if q&x:
            se.add(i)
        i+=1
        q<<=1
    return ''.join(str(i) for i in sorted(list(se)))
0.5 # статистику считать но не печатать
d_stat = 1 # 1 статистика
1.5 # только добавления
d_main = 2 # 2 основное
2.5 # + ускорения (пропуски)
d_dbg = 3 # 3 отладка
debug = 0
def printmat(m):
    ml = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            ml = max(ml,len(sets(m[i][j])))
    f = '{:'+str(ml)+'}'
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(f.format(sets(m[i][j])),end=' ')
        print()
def print_sets(sets,depth=0,mes=None):
    if mes!=None:
        print('    '*depth,mes)
    union = 0
    for s in sets:
        union|= s
    se = set()
    i=0
    q=1
    while q<=union:
        if q&union:
            se.add(i)
        i+=1
        q<<=1
    se = sorted(list(se))
    for s,n in sets.items():
        print('    '*depth,f'|{n:2})',end=' ')
        for i in se:
            print(i if (2**i)&s else ' ' if i<10 else '  ',end=' ')
        print()


def pc(fixed,center,W):
    fixed = bits(fixed,W)
    center = bits(center,W)
    s = ''
    for i in range(len(fixed)):
        s+= '.' if fixed[i]=='0' else center[i]
    return s
def number_of_patterns(matrix1: np.ndarray) -> int:
    # одинаковые строки убираем сразу
    # постоянные столбцы обрабатываем отдельно и убираем
    if debug>=d_main: print('start')
    if debug>=d_main: print(matrix1)
    cnt = 0
    W = len(matrix1[0])
    H = len(matrix1)
    # ищем постоянные столбцы
    matrix = [[] for i in range(H)]
    for i in range(W):
        if (matrix1[:,i]==1).all() or (matrix1[:,i]==0).all():
            cnt+=1
        else:
            for j in range(H):
                matrix[j].append(matrix1[j,i])
    W-=cnt
    if debug>=d_main: print('постоянных столбцов: ',cnt)
    
    # преобразовываем в биты
    for i in range(H):
        q=1
        line = 0
        for j in range(W):
            if matrix[i][j]:
                line|=q
            q<<=1
        matrix[i] = line
    all1 = 2**(W+1)-1

    # удаляем повторы
    matrix.sort()
    for i in range(H-2,-1,-1):
        if matrix[i]==matrix[i+1]:
            del matrix[i+1]
            H-=1
    if debug>=d_main: 
        print('подготовили матрицу',H,W,'--',thisline())
        for x in matrix:
            print(bits(x,W))

    dist = []
    for i in range(H):
        dist.append([])
        for j in range(H):
            dist[i].append(matrix[i]^matrix[j])
    if debug>=d_stat+0.5: 
        print('матрица расстояний')
        printmat(dist)
    def count(x):
        q = 1
        cnt = 0
        while q<=x:
            if q&x:
                cnt+=1
            q<<=1
        return cnt
    centrals = set()
    maxdepth = 0
    falsecnt = 0
    for ln in range(H):
        if debug>=d_stat+0.5: print('---------',ln,'--------','//',len(centrals),falsecnt)
        for bn in range(W):
            bit = 2**bn
            # строку-бит задали

            # выбираем строки, в которых этот бит присутствует
            cont = False
            fixed = 0
            for i in range(H):
                if dist[ln][i]&bit:
                    # в каждом множестве исключаем этот бит
                    tmp = dist[ln][i]^bit
                    # среди выбранных:
                    # если есть пустые множества - конец
                    if tmp==0:
                        if debug>=d_main+0.5: print(bn,'->',f'>>> {ln} void','--',thisline())
                        cont = True
                        break
                    # если есть множества из одного элемента - фиксируем их
                    if count(tmp)==1:
                        if i<=ln: # в предыдущие строки нам не нужно попадать
                            if debug>=d_main+0.5: print(bn,'->',f'>>> {i} already done','--',thisline())
                            cont = True
                            break
                        fixed|=tmp
            if cont:
                continue

            # из выбранных строк исключаем те, в которых присутствуют фиксированные элементы
            cur = {}
            for i in range(H):
                if dist[ln][i]&bit and dist[ln][i]&fixed==0:
                    v = dist[ln][i]^bit
                    cur[v] = i # еще ничего не вычеркнул => все строки разные
            if debug>=d_stat+0.5: print(bn,'->',sets(fixed),'//',len(centrals),falsecnt)

            #если строк не осталось - yield
            if len(cur)==0:
                fixed |= bit
                center = (matrix[ln]^bit)&fixed
                if debug>=0.5: 
                    boo = (fixed,center) in centrals
                    if boo: falsecnt+=1
                centrals.add((fixed,center))

                if debug>=d_stat+0.5:
                    print('+',pc(fixed,center,W),f'[{len(centrals)}]',end=' ')
                    if boo: print('!!!',falsecnt)
                    else:   print()
                continue

            excluded = all1
            def perebor(sel,fixed,excluded,depth):
                if debug>=0.5: nonlocal falsecnt
                if debug>=0.5: nonlocal maxdepth
                if debug>=0.5: maxdepth = max(maxdepth,depth)
                if debug>=d_main: print('    '*depth,f'fixed={sets(fixed)}, excluded={sets(all1^excluded)}','--',thisline())
                
                # объединяем все множества выбранных строк
                union = 0
                for v in sel:
                    union |= v

#   + подсчитываем, сколько раз встречается каждый элемент, и перебираем от меньшего к большему

                # по каждому элементу из этого множества
                q = 1
                while q<=union:
                    if q&union:
                        if debug>=d_main: print_sets(sel,depth,f'sel: bit {sets(q)} -- {thisline()}')
                        # выбранные строки разбиваем на текущие (те, в которых присутствуют этот элемент (они точно не равны центральности)), и дальнейшие (для дальнейшего анализа)
                        cur = {}
                        intersect = -1
                        cont = True
                        partial_done = False
                        for s,n, in sel.items():
                            if q&s:
                                cur[s] = n
                                # если все текущие строки ранее обрабатывались - continue
                                if n>ln:
                                    cont = False
                                else:
                                    partial_done = True
                                # пересекаем текущие строки
                                if intersect==-1:
                                    intersect = s
                                else:
                                    intersect &= s
                        if cont:
                            if debug>=d_main+0.5: print('    '*depth,sets(q),'->','>>> all already done','--',thisline())
                    #
                        if not cont:
                            # фиксируем этот элемент, а остальные элементы из пересечения добавляем в исключённые (точно должны отсутствовать в центральности)
                            fixed2 = fixed|q
                            excluded2 = excluded&(all1^intersect^q)
                            if debug>=d_dbg: print('    '*depth,f'fixed2={sets(fixed2)}, excluded2={sets(all1^excluded2)}','--',thisline())
                            if debug>=d_dbg: print_sets(cur,depth,f'cur: -- {thisline()}')
                    #
                            # из дальнейших множеств удаляем исключённые
                            fur = {}
                            cont = False
                            if debug>=d_main: sledstv = 0
                            for s,n, in sel.items():
                                if q&s==0:
                                    v = s&excluded2
                                    # если есть пустые множества - конец (в эту строку можно добраться изменив только один бит)
                                    if v==0:
                                        if debug>=d_main+0.5: print('    '*depth,sets(q),'->',f'>>> {n} void','--',thisline())
                                        cont = True
                                        break
                                    if v in fur:
                                        fur[v] = max(fur[v],n)
                                    else:
                                        fur[v] = n
                        if not cont:
                            # из выбранных строк исключаем те, в которых присутствуют фиксированные элементы (они точно не равны центральности)
                            fur = {s:n for s,n in fur.items() if s&fixed2==0}
                            if debug>=d_dbg: print_sets(fur,depth,f'fur: -- {thisline()}')
                    #
                            if debug>=d_main: print('    '*depth,sets(q),'->',sets(sledstv),'X',sets(intersect^q),'//',len(centrals),falsecnt,'--',thisline())
                            # если дальнейших строк не осталось - yield (найденные центральности складываем в общее множество)
                            if len(fur)==0:
                                if not partial_done:
                                    fixed2 |= bit
                                    center = (matrix[ln]^bit)&fixed2
                                    if debug>=0.5: 
                                        boo = (fixed2,center) in centrals
                                        if boo: falsecnt+=1
                                    centrals.add((fixed2,center))
                                    if debug>=d_stat+0.5:
                                        print('    '*maxdepth,'+',pc(fixed2,center,W),f'[{len(centrals)}]',end=' ')
                                        if boo: print('!!!',falsecnt)
                                        else:   print()
                                else:
                                    if debug>=d_main+0.5: print('    '*maxdepth,f'+ >>>','--',thisline())
                                cont = True
                    #
                        if not cont:
                            # по каждой из выбранных строк, в которой присутствует этот элемент
                            for v,k in cur.items():
                                if k>ln: # в предыдущие строки нам не нужно попадать
                                    # остальные элементы из этой строки добавляем в исключённые (точно должны отсутствовать в центральности)
                                    excluded3 = excluded2&(all1^v^q)
                                    if debug>=d_main and v==intersect: print('    '*depth,' ','частное равно общему','--',thisline())
                    #
                                    cont = False
                                    fixed3 = fixed2
                                    for v2,k2 in fur.items():
                                        # из множеств удаляем вычеркнутые
                                        t = v2&excluded3
                                        # если есть пустые множества - конец
                                        if t==0:
                                            if debug>=d_main+0.5: print('    '*depth,sets(q),f'({k})','->',sets(t),f'>>> {k2} void','--',thisline())
                                            cont = True
                                            break
                                        # если есть множества из одного элемента - фиксируем их
                                        if count(t)==1:
                                            if k2<=ln: # в предыдущие строки нам не нужно попадать
                                                if debug>=d_main+0.5: print('    '*depth,sets(q),f'({k})','->',sets(t),f'>>> {k2} already done','--',thisline())
                                                cont = True
                                                break
                                            fixed3|=t
                                    if cont:
                                        continue
                                    if debug>=d_dbg: print('    '*depth,' ',f'fixed3={sets(fixed3)}, excluded3={sets(all1^excluded3)}','--',thisline())
                    #                                    
                                    #из выбранных строк исключаем те, в которых присутствуют выбранные элементы
                                    cur2 = {}
                                    for v2,k2 in fur.items():
                                        if v2&excluded3&fixed3==0:
                                            if v2 in cur2:
                                                cur2[v2] = max(cur2[v2],k2)
                                            else:
                                                cur2[v2] = k2
                                    if debug>=d_dbg: print_sets(cur2,depth,f'cur2: -- {thisline()}')
                    #
                                    if debug>=d_main: print('    '*depth,' ',sets(q),f'({k})','->',sets(fixed3^fixed2),'X',sets(excluded3^excluded2),'//',len(centrals),falsecnt,'--',thisline())
                                    # если строк не осталось - yield
                                    if len(cur2)==0:
                                        fixed3 |= bit
                                        center = (matrix[ln]^bit)&fixed3
                                        if debug>=0.5: 
                                            boo = (fixed3,center) in centrals
                                            if boo: falsecnt+=1
                                        centrals.add((fixed3,center))
                                        if debug>=d_stat+0.5:
                                            print('    '*maxdepth,' ','+',pc(fixed3,center,W),f'[{len(centrals)}]',end=' ')
                                            if boo: print('!!!',falsecnt)
                                            else:   print()
                                        continue
                                    #-> объединяем все множества выбранных строк
                                    perebor(cur2,fixed3,excluded3,depth+1)
                                else:
                                    if debug>=d_main+0.5: print('    '*depth,sets(q),f'({k})','->','>>> already done','--',thisline())
                    #
                        # из выбранных строк исключаем этот элемент (он полностью обработан)
                        sel2 = {}
                        cont = False
                        for v,k in sel.items():
                            t = v&(all1^q)
                            # если есть пустые строки - конец
                            if t==0:
                                if debug>=d_main+0.5: print('    '*depth,f'>>> deletion {sets(q)} make {k} void','--',thisline())
                                cont = True
                                break
                            if t in sel2:
                                sel2[t] = max(sel2[t],k)
                            else:
                                sel2[t] = k
                        if cont:
                            q<<=1
                            return
                        sel = sel2
                    q<<=1
            perebor(cur,fixed,excluded,1)
    if debug>=d_stat: print('maxdepth:',maxdepth)
    if debug>=d_stat: print('falsecnt:',falsecnt)
    if debug>=0.5: return (cnt + len(centrals),falsecnt,centrals)
    return cnt + len(centrals)

