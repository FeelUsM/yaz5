Lnums = 10**5+1
nums = [0 for i in range(Lnums)]
N = int(input())
for x in map(int,input().split()):
	nums[x]+=1

m = nums[0]+nums[1]
for i in range(1,Lnums):
	if nums[i]+nums[i-1]>m:
		m = nums[i]+nums[i-1]
print(N-m)

