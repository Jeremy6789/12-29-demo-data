#include <iostream>
#include <algorithm>
using namespace std;
int main() {
    long long a, b;
    if (!(cin >> a >> b)) return 0;
    while (b) {
        a %= b;
        swap(a, b);
    }
    cout << a << endl;
    return 0;
}