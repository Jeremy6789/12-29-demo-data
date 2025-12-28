#include <stdlib.h>
#include <stdio.h>

int main() {
    // 試圖列出伺服器目錄內容，展示沙盒攔截功能
    system("ls -la /etc");
    return 0;
}