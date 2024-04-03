N = int(input())
n = int(input())
every_like = set(input().split())
for i in range(1,N):
	n = int(input())
	every_like &= set(input().split())
print(len(every_like))
print(' '.join(sorted(every_like)))