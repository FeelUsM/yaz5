from collections import defaultdict
letters = defaultdict(int)
s = input()
for c in s:
	letters[c]+=1
letters2 = defaultdict(int)
s = input()
for c in s:
	letters2[c]+=1
print('YES' if letters==letters2 else 'NO')