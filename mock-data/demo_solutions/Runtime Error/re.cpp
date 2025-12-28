#include <iostream>

int main() {
    int a = 10;
    int b = 0;
    // 除以零會觸發 SIGFPE 訊號，導致 Runtime Error
    std::cout << a / b << std::endl;
    return 0;
}