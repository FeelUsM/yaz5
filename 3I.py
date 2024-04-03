def split_lastnum(s):
	l = len(s.split()[-1])
	return (s[:-l].strip(),int(s[-l:]))

class AttrDict(dict):
    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key) # essential for testing by hasattr
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value
def make_dict(**kwargs):
    return AttrDict(kwargs)

teams = {
	# num_games
	# num_doals
	# num_first
}
players = {
	# team
	# num_goals
	# num_first
	# timing = list[90]: num_goals
}


try:
	while (s := input()) !='' :
		if s.startswith("Total goals for "): # team
			team = s[len("Total goals for "):]
			print(teams[team].num_goals if team in teams else 0) # team
		elif s.startswith("Mean goals per game for "):
			team = s[len("Mean goals per game for "):]
			print(teams[team].num_goals/teams[team].num_games)#else garantee
		elif s.startswith("Total goals by "): # name
			name = s[len("Total goals by "):]
			print(players[name].num_goals if name in players else 0)
		elif s.startswith("Mean goals per game by "): # name
			name = s[len("Mean goals per game by "):]
			print(players[name].num_goals/teams[players[name].team].num_games)#else garantee
		elif s.startswith("Goals on minute "): # minute by name
			s = s[len("Goals on minute "):]
			m,name = s.split(' by ')
			m = int(m)
			print(players[name].timing[m-1] if name in players else 0)
		elif s.startswith("Goals on first "): # minute minutes by name
			s = s[len("Goals on first "):]
			m,name = s.split(' minutes by ')
			m = int(m)
			print(sum(players[name].timing[:m]) if name in players else 0)
		elif s.startswith("Goals on last "): # minute minutes by name
			s = s[len("Goals on last "):]
			m,name = s.split(' minutes by ')
			m = int(m)
			print(sum(players[name].timing[-m:]) if name in players else 0)
		elif s.startswith("Score opens by "): # team or name
			name = s[len("Score opens by "):]
			if name in teams:
				print(teams[name].num_first)
			elif name in players:
				print(players[name].num_first)
			else:
				print(0)
		else:
			team1,s = s.split('-')
			team1 = team1.strip()
			s,n2 = s.split(':')
			n2 = int(n2)
			team2,n1 = split_lastnum(s)

			if team1 not in teams:
				teams[team1] = make_dict(num_games=1, num_goals=n1, num_first=0)
			else:
				teams[team1].num_games+=1
				teams[team1].num_goals+=n1
			if team2 not in teams:
				teams[team2] = make_dict(num_games=1, num_goals=n2, num_first=0)
			else:
				teams[team2].num_games+=1
				teams[team2].num_goals+=n2

			time1 = None
			name1 = None
			for i in range(n1):
				name,t = split_lastnum(input()[:-1])
				if name not in players:
					players[name] = make_dict(team=team1, num_goals=1, num_first=0, timing=[0 for j in range(90)])
				else:
					assert players[name].team == team1
					players[name].num_goals+=1
				players[name].timing[t-1]+=1
				if i==0:
					time1 = t
					name1 = name
			time2 = None
			name2 = None
			for i in range(n2):
				name,t = split_lastnum(input()[:-1])
				if name not in players:
					players[name] = make_dict(team=team2, num_goals=1, num_first=0, timing=[0 for j in range(90)])
				else:
					assert players[name].team == team2
					players[name].num_goals+=1
				players[name].timing[t-1]+=1
				if i==0:
					time2 = t
					name2 = name
			if time1!=None and (time2!=None and time1<time2 or time2==None):
				teams[team1].num_first+=1
				players[name1].num_first+=1
			elif time2!=None and (time1!=None and time2<time1 or time1==None):
				teams[team2].num_first+=1
				players[name2].num_first+=1
			else:
				assert n1==0 and n2==0

			#print(teams)
			#print(players)
except EOFError as e:
	#print('end')
	pass