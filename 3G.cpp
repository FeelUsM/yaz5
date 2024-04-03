#include <iostream>
#include <unordered_set>
using namespace std;

struct hash_pair {
    template <class T1, class T2>
    size_t operator()(const pair<T1, T2>& p) const
    {
        auto hash1 = hash<T1>{}(p.first);
        auto hash2 = hash<T2>{}(p.second);
		return (hash1<<1) ^ hash2;              
    }
};

typedef pair<int,int> Point; 

	pair<bool,pair<Point,Point>> 
orto(Point p1, Point p2) {
	int x1 = p1.first;
	int y1 = p1.second;
	int x2 = p2.first;
	int y2 = p2.second;
	int dx = x2-x1;
	int dy = y2-y1;
	if((dx%2 + dy%2)%2) {
		return make_pair(false,make_pair(make_pair(0,0),make_pair(0,0)));
	}
	Point r1 = make_pair(x1+(dx-dy)/2, y1+(dy+dx)/2);
	Point r2 = make_pair(x1+(dx+dy)/2, y1+(dy-dx)/2);
	return make_pair(true,make_pair(r1,r2));
}

int main(int argc, char * argv[]) {
	int N;
	cin >> N ;

	unordered_set<Point, hash_pair> processed;
	for(int i =0; i<N; i++) {
		int x,y;
		cin>>x>>y;
		processed.insert(make_pair(x,y));
	}

	unordered_set<Point, hash_pair> wanted;
	int answer = N==1 ? 3 : 2;

	int I;
	auto pcur = processed.begin();
	for(pcur = processed.begin(), I=0; pcur!=processed.end(); pcur++, I++) {
		//cout << pcur->first << ' ' << pcur->second<<endl;
		if(wanted.find(*pcur)!=wanted.end()) { // if cur in wanted:
			answer = 0;
		}
		if(answer==0) continue;
		int j;
		auto pproc = processed.begin();
		for(pproc = processed.begin(), j=0; j!=I; pproc++, j++) {
			if(answer==0) break;
			auto bp3p4 = orto(*pcur,*pproc);
			bool b = bp3p4.first;
			if(not b)
				continue;
			auto p3p4 = bp3p4.second;
			Point p3 = p3p4.first;
			Point p4 = p3p4.second;
			bool p3p = processed.find(p3)!=processed.end(); // p3p = p3 in processed
			bool p4p = processed.find(p4)!=processed.end(); // p4p = p4 in processed
			if(p3p) {
				answer = 1;
				if(p4p) {
					answer = 0;
					break;
				}
				else
					wanted.insert(p4);
			}
			if(p4p) {
				answer = 1;
				if(p3p) {
					answer = 0;
					break;
				}
				else
					wanted.insert(p3);
			}
		}
	}

	cout << answer << endl;
	if(answer==1) {
		auto pp = wanted.begin();
		cout << pp->first <<" "<< pp->second <<endl;
	}
	else if(answer==2) {
		bool stop = false;
		int I;
		auto p1 = processed.begin();
		for(p1 = processed.begin(), I=0; p1!=processed.end(); p1++, I++) {
			if(stop) break;
			int j;
			auto p2 = processed.begin();
			for(p2 = processed.begin(), j=0; j!=I; p2++, j++) {
				if(stop) break;
				if(I==j) break;
				auto bp3p4 = orto(*p1,*p2);
				bool b = bp3p4.first;
				if(not b)
					continue;
				auto p3p4 = bp3p4.second;
				Point p3 = p3p4.first;
				Point p4 = p3p4.second;
				cout << p3.first <<" "<< p3.second <<endl;
				cout << p4.first <<" "<< p4.second <<endl;
				stop = true;
			}
		}
	}
	else if(answer ==3) {
		auto p = processed.begin();
		int x = p->first;
		int y = p->second;
		cout << x <<" "<< y+1 <<endl;
		cout << x+1 <<" "<< y <<endl;
		cout << x+1 <<" "<< y+1 <<endl;
		
	}
}