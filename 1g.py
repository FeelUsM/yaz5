def name(weekday):
    if weekday == 0:
        return "Sunday"
    if weekday == 1:
        return "Monday"
    if weekday == 2:
        return "Tuesday"
    if weekday == 3:
        return "Wednesday"
    if weekday == 4:
        return "Thursday"
    if weekday == 5:
        return "Friday"
    if weekday == 6:
        return "Saturday"

def main(N,Y,hds,j1):
    from datetime import datetime
    import locale
    #locale.setlocale(locale.LC_ALL, 'C')
    hs = [0,0,0,0,0,0,0]
    for i in range(N):
        hs[int(datetime.strptime(hds[i]+' '+Y,'%d %B %Y').strftime('%w'))]+=1
    assert datetime.strptime('1 January '+Y,'%d %B %Y').strftime('%A') == j1.strip()

    for i in range(int(datetime.strptime('1 January '+Y,'%d %B %Y').strftime('%w')),7):
        hs[i]-=1
    for i in range(0,int(datetime.strptime('31 December '+Y,'%d %B %Y').strftime('%w'))+1):
        hs[i]-=1

    mi = hs[0]
    ma = hs[0]
    imi = 0
    ima = 0
    for i in range(7):
        if hs[i]<mi:
            mi = hs[i]
            imi = i
        if hs[i]>ma:
            ma = hs[i]
            ima = i
    return (imi,ima)

N  = int(input())
Y = input()
hds = []
for i in range(N):
    hds.append(input())
j1 = input()

imi,ima = main(N,Y,hds,j1)
print(name(imi),name(ima))