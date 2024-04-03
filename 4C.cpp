#include <iostream>
#include <vector>
#include <string>
using namespace std;
#define debug false

vector<long> summs;
long lower_bound(long first, long last, long l, long value) {
	if(debug) cout<<first<<" "<<last<<endl;
	if(summs[first+l]-summs[first] > value)
		return first;
	if(summs[last-1+l]-summs[last-1] < value)
		return last;
	long count = last - first;
	while(count>0) {
		long step = count/2;
		long it = first+step;
		if(debug) cout<<it<<" "<<summs[it+l]-summs[it]<<" "<<value;
		if(summs[it+l]-summs[it] < value) {
			if(debug) cout<<"<"<<endl;
			first = it+1;
			count -= (step + 1);
		}
		else if(summs[it+l]-summs[it] == value) {
			if(debug) cout<<"=="<<endl;
			return it;
		}
		else {
			if(debug) cout<<">"<<endl;
			count = step;
		}
	}
	return first;
}

int main() {
	int n,m;
	cin >> n >> m;
	//vector<long> arr(n);
	summs.reserve(n+1);
	summs.push_back(0);
	for(int i=0; i<n; i++) {
		long z;
		cin >> z;
		summs.push_back(summs[i]+z);
	}
	string ans;
	ans.reserve(m*7);
	for(int i=0; i<m; i++) {
		long l,s,a;
		cin >> l >> s;
		a = lower_bound(0,n+1-l,l,s);
		if(a+l>=n+1 || summs[a+l]-summs[a] != s){
			ans += to_string(-1)+"\n";
		}
		else
			ans += to_string(a+1)+"\n";
	}
	cout << ans;
}