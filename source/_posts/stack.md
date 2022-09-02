---
title: stack
date: 2022-09-02 20:32:12
tags:
cover: https://w.wallhaven.cc/full/9m/wallhaven-9mjoy1.png
---

c实现栈

1.线性表

```c++
#include <stdio.h>
#include <stdbool.h>
#define MaxSize 100
typedef struct
{
    /* data */
    int Data[MaxSize];
    int topIdx=0;//待填的值
}SeqStack;
bool push( SeqStack *L,int e ){
    if(L->topIdx==MaxSize){
        return false;
    }
    L->Data[L->topIdx++]=e;
    return true;
}
bool pop( SeqStack *L)
{
    if(L->topIdx==0){
        return 0;
    }
    return L->topIdx--;
} 
int top( SeqStack *L)
{
    return L->Data[L->topIdx-1];
}
bool isEmpty(SeqStack *L)
{
    if(L->topIdx==0)return true;
    else return false;
}
bool isFull(SeqStack *L)
{
    if(L->topIdx==MaxSize)return true;
    else return false;
}
int main()
{
    // printf("hello");
    SeqStack s;
    printf("%d\n",isEmpty(&s));
    push(&s,2);
    push(&s,3);
    printf("%d\n",top(&s));
    pop(&s);
    printf("%d\n",top(&s));
    return 0;
}
```

2.链表

```c++
#include <stdio.h>
#include <stdlib.h>
typedef struct stack_Lnode
{
    int val;
    struct stack_Lnode *next;
}Lnode;
void push(Lnode *l,int val)
{
    Lnode* newl=(Lnode *)malloc(sizeof(Lnode));
    newl->val=val;
    newl->next=l->next;
    l->next=newl;
}
int pop(Lnode *l)
{
    if(l->next==NULL)return 0;
    Lnode *tem= l->next;
    l->next=tem->next;
    free(tem);
    return 1;
}
int top(Lnode *l)
{
    Lnode *L=l->next;
    int res=L->val;
    return res;
}
int main()
{
    Lnode *res=(Lnode *)malloc(sizeof(Lnode));
    push(res,20);
    push(res,30);
    printf("%d\n",top(res));
    pop(res);
    printf("%d\n",top(res));
    pop(res);
    return 0;
}
```

