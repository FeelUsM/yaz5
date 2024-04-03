N = int(input())
XX = []
YY = []

for i in range(N):
	y,x = map(int,input().split())
	XX.append(x-1)
	YY.append(y-1)

Y = [0 for i in range(N)]
for i in range(N):
	Y[YY[i]]+=1
void_p = 0
while void_p<N and Y[void_p]!=0:
	void_p+=1
over_p = 0
while over_p<N and Y[over_p]<=1:
	over_p+=1
Y_res = 0
while void_p<N and over_p<N:
	Y_res+=abs(void_p-over_p)
	Y[void_p]+=1
	Y[over_p]-=1
	while void_p<N and Y[void_p]!=0:
		void_p+=1
	while over_p<N and Y[over_p]<=1:
		over_p+=1

XS = 0
for i in range(N):
	XS+=XX[i]

XC = round(XS/N)
X_res = 0
for i in range(N):
	X_res+= abs(XX[i]-XC)
#print(XC,X_res)

X_RES = []
for XC in range(N):
	X_res = 0
	for i in range(N):
		X_res+= abs(XX[i]-XC)
	X_RES.append(X_res)
#print(X_RES,min(X_RES))

print(min(X_RES) + Y_res)
