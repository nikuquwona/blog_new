---
title: test
date: 2022-09-01 10:20:06
tags:
---



# 测试文件

*你好👋*

```cpp
#include <iostream>
#include <vector>

using namespace std;
 struct TreeNode {
     int val;
     TreeNode *left;
     TreeNode *right;
     TreeNode() : val(0), left(nullptr), right(nullptr) {}
     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 };

class Solution {
public:
    // bool ff=1;
    TreeNode* dfs(vector<int> preorder,int start1,int end1,vector<int> inorder,int start2,int end2)
    {
        TreeNode *res;
        if(start1>end1)return nullptr;
        res=new TreeNode(preorder[start1]);
        int i=start2;
        while(inorder[i]!=preorder[start1])i++;
        int size=i-start2;
        res->left=dfs(preorder,start1+1,start1+size,inorder,start2,i-1);
        res->right=dfs(preorder,start1+size+1,end1,inorder,i+1,end2);
        return res;
    }
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        TreeNode * res,*r;
        r=dfs(preorder,0,preorder.size()-1,inorder,0,inorder.size()-1);
        return r;
    }
};
int main()
{
    // preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
    vector<int>preorder ={3,9,20,15,7};//h l r
    vector<int>inorder ={9,3,15,20,7};//l h r

    Solution s;
    TreeNode* t=s.buildTree(preorder,inorder);
    cout<<t->val<<endl;
    cout<<((t->left)->val)<<endl;
    
    return 0;
}

```

