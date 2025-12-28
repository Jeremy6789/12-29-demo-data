#include <iostream>
#include <stack>
#include <string>
using namespace std;
int main() {
    string s; cin >> s;
    stack<char> st;
    for(char c : s) {
        if(c=='('||c=='['||c=='{') st.push(c);
        else {
            if(st.empty()) { cout << "No"; return 0; }
            if((c==')'&&st.top()=='(') || (c==']'&&st.top()=='[') || (c=='}'&&st.top()=='{')) st.pop();
            else { cout << "No"; return 0; }
        }
    }
    cout << (st.empty() ? "Yes" : "No"); return 0;
}