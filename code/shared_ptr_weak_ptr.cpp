#include <iostream>
#include <memory>
using namespace std;

class B;

class A
{
  public:
    // 为了省去一些步骤这里 数据成员也声明为 public
    // weak_ptr<B> pb;
    shared_ptr<B> pb;  // 声明为 shared_ptr 会产生循环引用的问题

    void doSomthing()
    {
        cout << "I'm A" << endl;
    }

    ~A()
    {
        cout << "kill A" << endl;
    }
};

class B
{
  public:
    shared_ptr<A> pa;

    ~B()
    {
        cout <<"kill B" << endl;
    }
};

int main(int argc, char** argv)
{
    {
        shared_ptr<A> sa(new A());
        shared_ptr<B> sb(new B());

        if(sa && sb)
        {
            sa->pb=sb;
            sb->pa=sa;
        }
        sa->doSomthing();
        cout << "sa use count:" << sa.use_count() << endl;
        cout << "sb use count:" << sb.use_count() << endl;
    }

    return 0;
}