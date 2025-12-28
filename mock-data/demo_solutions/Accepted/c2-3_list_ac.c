#include <stdio.h>
#include <stdlib.h>

// 定義鏈表節點結構
struct Node {
    int data;
    struct Node* next;
};

int main() {
    int val;
    struct Node *head = NULL, *tail = NULL;

    // 1. 讀取輸入直到 -1 結束，建立原始鏈表
    while (scanf("%d", &val) != EOF && val != -1) {
        struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
        newNode->data = val;
        newNode->next = NULL;
        
        if (head == NULL) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
    }

    // 如果鏈表是空的，直接結束
    if (head == NULL) return 0;

    // 2. 執行原地 (In-place) 反轉邏輯（這是本題考點）
    struct Node *prev = NULL, *curr = head, *next = NULL;
    while (curr != NULL) {
        next = curr->next;  // 暫存下一個節點
        curr->next = prev;  // 將當前節點指向前一個
        prev = curr;        // 移動 prev
        curr = next;        // 移動 curr
    }
    head = prev; // 反轉後的頭節點

    // 3. 輸出結果
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d", temp->data);
        if (temp->next != NULL) {
            printf(" "); // 節點之間以空格隔開
        }
        temp = temp->next;
    }
    printf("\n"); // 結尾換行

    return 0;
}
