debug = True
def issquare(i,j,k):
	return sums[i][j] - sums[i-k][j] - sums[i][j-k] + sums[i-k][j-k] == k**2

def check(k):
	for i in range(1, n-2*k+1):
		for j in range(1, m-2*k+1):
			if issquare(i,j+k,k) and \
			   issquare(i+k,j,k) and \
			   issquare(i+k,j+k,k) and \
			   issquare(i+k,j+2*k,k) and \
			   issquare(i+2*k,j+k,k):
				return True
	return False

n,m = map(int, input().split())
sums = [[0]*(m+1)]
if debug:
	arr = ['.'*(m+1)]
for i in range(1,n+1):
	sums.append([0]*(m+1))
	s = '.'+input()
	if debug:
		arr.append(s)
	for j in range(1,m+1):
		sums[i][j] = sums[i-1][j] + sums[i][j-1] - sums[i-1][j-1]
		if s[j]=='#':
			sums[i][j]+=1
if debug:
	for i in range(n+1):
		for j in range(m+1):
			print(f'{sums[i][j]:2}',end=' ')
		print()

	# 0   0   0   0   0   0   0   0   0   0   0   0   0
	# 0   0.  0.  0.  1#  2#  2.  3#  4#  5#  5.  5.  5.
	# 0   0.  0.  0.  2#  4#  4.  6#  8# 10# 10. 10. 10.
	# 0   0.  1#  2#  5#  8#  9# 12# 15# 18# 18. 18. 18.
	# 0   0.  2#  4#  8# 12# 14# 18# 22# 26# 27# 28# 29#
	# 0   0.  2.  4.  9# 14# 17# 22# 27# 32# 34# 36# 38#
	# 0   0.  2.  4. 10# 16# 20# 26# 32# 38# 41# 44# 47#
	# 0   0.  2.  4. 10. 16. 20. 27# 34# 41# 44. 47. 50.
	# 0   0.  2.  4. 10. 16. 20. 28# 36# 44# 47. 50. 53.
	# 0   0.  2.  4. 10. 16. 20. 29# 38# 47# 50. 53. 56.

	def getsums(ii,jj):
		s = 0
		for i in range(ii+1):
			for j in range(jj+1):
				if arr[i][j]=='#':
					s+=1
		return s
	print()
	for i in range(n+1):
		for j in range(m+1):
			print(f'{getsums(i,j):2}',end=' ')
		print()


l=1
r=n
while l<r:
	mid = (l+r+1)//2
	if check(mid):
		l = mid
	else:
		r = mid-1
print(l)

