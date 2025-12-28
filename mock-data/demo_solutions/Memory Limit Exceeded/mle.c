#include <stdlib.h>

int main() {
    // 不斷申請 1MB 的空間，直到被沙盒強制終止
    while (1) {
        char *ptr = (char *)malloc(1024 * 1024);
        if (ptr == NULL) break;
    }
    return 0;
}