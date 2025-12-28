#include <vector>
int main() {
    std::vector<int> v;
    while(true) v.push_back(1); // 不斷申請記憶體直到崩潰
    return 0;
}