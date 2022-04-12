#include <bits/stdc++.h>
using namespace std;
class Node {
public:
int data;
Node* next;
};
int main()
{
Node* one = NULL;
Node* two = NULL;
Node* three = NULL;
Node* four = NULL;
Node* five = NULL;
one = new Node();
two = new Node();
three = new Node();
four = new Node();
five = new Node();
one->data = 10;
one->next = two;
two->data = 20;
two->next = three;
three->data = 30;
three->next = four;
four->data = 50;
four->next = five;
five->data = 80;
five->next = NULL;
std::cout << "linked list got created" << std::endl;
while (one != NULL) {
std::cout << "Data inside linked list is ::" << std::endl;
cout << one->data << " ::";
one = one->next;
}
return 0;
}