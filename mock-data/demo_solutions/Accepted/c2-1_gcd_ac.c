#include <stdio.h>
int main() {
    int a, b; scanf("%d %d", &a, &b);
    while(b) { int t = a % b; a = b; b = t; }
    printf("%d", a); return 0;
}