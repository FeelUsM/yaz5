N = int(input())
arr = sorted(map(int,input().split()))
K = int(input())

def lower_bound(arr,value):
	first = 0
	last = len(arr)
	count = last - first
	while count > 0:
		step = count // 2
		it = first+step; 
		if arr[it] < value :
			first = it+1
			count -= (step + 1) 
		else:
			count = step
	return first

def upper_bound(arr, value):
	first = 0
	last = len(arr)
	count = last-first
	while count > 0:
		step = count // 2; 
		it = first+step
		if arr[it] <= value:
			first = it+1;
			count -= (step + 1)
		else:
			count = step
	return first

for i in range(K):
	L,R = map(int,input().split())
	print(upper_bound(arr,R)-lower_bound(arr,L),end=' ')
print()