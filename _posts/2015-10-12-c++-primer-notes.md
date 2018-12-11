---
typora-root-url: ../
title: "C++ Primer 第5版笔记"
categories: "technology"
tags: [c++]
---

C++ Primer 第5版笔记及部分内容补充

------



# 第4章表达式

主要介绍C++11中类型转换，4种显示类型转换

## 显示类型转换

强制类型转换具有以下形式：

`cast-name<type>(expression);`

| cast-name          | 用处                                             |
| ------------------ | ------------------------------------------------ |
| `static_cast`      | 任何具有明确定义的类型转换，只要不包含底层 const |
| `const_cast`       | 只能改变运算对象的底层 const                     |
| `reinterpret_cast` | 通常为运算对象的位模式提供较低层次上的重新解释   |
| `dynamic_cast`     |                                                  |

### static_cast

- 把一个较大的算术类型赋值给较小类型时，`static_cast` 非常有用；
- 对于编译器无法自动执行的类型转换也非常有用。

```cpp
// 强制类型转换以便执行浮点除法
double slope = static_cast<double>(j) / i;

// 编译器无法自动类型转换
double d;
void* p = &d;
double* dp = static_cast<double*>(p);
```

### const_cast

- 一般称为“去掉 const 性质（cast away the const）”；
  - 如果对象本身不是一个常量，执行后获取写权限是合法行为；如果对象是一个常量，执行写操作会产生未定义的后果；
- 只能改变表达式的常量属性，不能改变表达式的类型。

```cpp
const char *pc;
char *p = const_cast<char*>(pc);

const char* cp;
// 错误：static_cast 不能去掉 const 性质
char* q = static_cast<char*>(cp);
// 正确：字符串字面值转换成 string 类型
static_cast<string>(cp);
// 错误：const_cast 只能改变常量属性
const_cast<string>(cp);
```

### reinterpret_cast

使用 `reinterpret_cast` 是非常危险的，可以看如下例子：

```cpp
int *ip;
// 必须记住 pc 所指向的真实对象是一个 int 而非字符
char *pc = reinterpret_cast<char*>(ip);
// 错误：把 pc 当成普通字符指针使用可能在运行时发生错误
string str(pc);
```

以上代码中用 pc 初始化 str 语句可能导致异常的运行时行为。其中的关键问题是类型改变了，但编译器没有给出任何警告或者错误的提示信息。

### dynamic_cast



## 旧式的强制类型转换

```markdown
type (expr);
(type) expr;
```

旧式的强制类型转换分别具有与 `const_cast`, `static_cast`, `reinterpret_cast` 相似的行为。



---

# 第12章动态内存

本文主要介绍C++11中3种智能指针的用处，以及循环引用导致的问题及其解决方法。

## 智能指针介绍

由于 C++ 语言没有自动内存回收机制，程序员每次 new 出来的内存都要手动 delete，比如流程太复杂，最终导致没有 delete，异常导致程序过早退出，没有执行 delete 的情况并不罕见，并造成内存泄露。如此c++引入智能指针 ，智能指针即是C++ RAII的一种应用，可用于动态资源管理，资源即对象的管理策略。 智能指针在 `<memory>` 标头文件的 std 命名空间中定义。 它们对 RAII 或获取资源即初始化编程惯用法至关重要。RAII 的主要原则是为所有堆分配资源提供所有权，例如动态分配内存或系统对象句柄、析构函数包含要删除或释放资源的代码的堆栈分配对象，以及任何相关清理代码。

C++ 11 智能指针主要包括：`unique_ptr`, `shared_ptr`, `weak_ptr`, 这三种，其中 `auto_ptr` 已被遗弃。

### unique_ptr

只允许基础指针的一个所有者。 可以移到新所有者(具有移动语义)，但不会复制或共享（即我们无法得到指向同一个对象的两个 `unique_ptr`）。 替换已弃用的 `auto_ptr`。 相较于 `boost::scoped_ptr`。 `unique_ptr` 小巧高效；大小等同于一个指针，支持 rvalue 引用，从而可实现快速插入和对 STL 集合的检索。 头文件：`<memory>`。
使用 `unique_ptr`，可以实现以下功能：

1. 为动态申请的内存提供异常安全。
2. 将动态申请内存的所有权传递给某个函数。
3. 从某个函数返回动态申请内存的所有权。
4. 在容器中保存指针。
5. 所有auto_ptr应该具有的（但无法在C++ 03中实现的）功能。

如下代码所示：

```cpp
class A;
// 如果程序执行过程中抛出了异常，unique_ptr就会释放它所指向的对象
// 传统的new 则不行
unique_ptr<A> fun1()
{
    unique_ptr p(new A);
    //do something
    return p;
}
void fun2()
{   //  unique_ptr具有移动语义
    unique_ptr<A> p = f();// 使用移动构造函数
    // do something
}// 在函数退出的时候，p以及它所指向的对象都被删除释放
```

### shared_ptr

采用引用计数的智能指针。 `shared_ptr`基于“引用计数”模型实现，多个`shared_ptr`可指向同一个动态对象，并维护了一个共享的引用计数器，记录了引用同一对象的`shared_ptr`实例的数量。当最后一个指向动态对象的`shared_ptr`销毁时，会自动销毁其所指对象(通过delete操作符)。`shared_ptr`的默认能力是管理动态内存，但支持自定义的Deleter以实现个性化的资源释放动作。头文件：`<memory>`。
基本操作：`shared_ptr`的创建、拷贝、绑定对象的变更(reset)、`shared_ptr`的销毁(手动赋值为nullptr或离开作用域)、指定deleter等操作。
 `shared_ptr`的创建,有两种方式，一，使用函数`make_shared`(会根据传递的参数调用动态对象的构造函数)；二，使用构造函数(可从原生指针、`unique_ptr`、另一个`shared_ptr`创建)

```cpp
shared_ptr<int> p1 = make_shared<int>(1);// 通过make_shared函数
shared_ptr<int> p2(new int(2));// 通过原生指针构造
```

此外智能指针若为“空”，即不指向任何对象，则为false，否则为true，可作为条件判断。可以通过两种方式指定deleter，一是构造`shared_ptr`时，二是使用reset方法时。可以重载的`operator->`, `operator *`，以及其他辅助操作如`unique()`, `use_count()`, `get()`等成员方法。

### weak_ptr

结合 `shared_ptr` 使用的特例智能指针。 `weak_ptr` 提供对一个或多个 `shared_ptr` 实例所属对象的访问，但是，不参与引用计数。 如果您想要观察对象但不需要其保持活动状态，请使用该实例。 在某些情况下需要断开 `shared_ptr` 实例间的循环引用。 头文件：<memory>。

`weak_ptr`的用法如下：

`weak_ptr`用于配合`shared_ptr`使用，并不影响动态对象的生命周期，即其存在与否并不影响对象的引用计数器。`weak_ptr`并没有重载`operator->`和`operator *`操作符，因此不可直接通过`weak_ptr`使用对象。提供了`expired()`与`lock()`成员函数，前者用于判断`weak_ptr`指向的对象是否已被销毁，后者返回其所指对象的`shared_ptr`智能指针(对象销毁时返回“空”`shared_ptr`)。循环引用的场景：如二叉树中父节点与子节点的循环引用，容器与元素之间的循环引用等。

### 循环引用问题

循环引用问题可以参考[这个链接](http://stackoverflow.com/questions/4984381/shared-ptr-and-weak-ptr-differences)上的问题理解，“循环引用”简单来说就是：两个对象互相使用一个`shared_ptr`成员变量指向对方的会造成循环引用。导致引用计数失效。下面给段代码来说明循环引用：

```cpp
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
```

运行结果为：

```markdown
sa use count:2
sb use count:2
```

注意此时 sa, sb 都没有释放，产生了内存泄露问题！！！

**即A内部有指向B，B内部有指向A，这样对于A，B必定是在A析构后B才析构，对于B，A必定是在B析构后才析构A**，这就是循环引用问题，违反常规，导致内存泄露。

一般来讲，解除这种循环引用有下面有三种可行的方法(参考)：

1. 当只剩下最后一个引用的时候需要手动打破循环引用释放对象。
2. 当A的生存期超过B的生存期的时候，B改为使用一个普通指针指向A。
3. 使用弱引用的智能指针打破这种循环引用。

虽然这三种方法都可行，但方法1和方法2都需要程序员手动控制，麻烦且容易出错。我们一般使用第三种方法：弱引用的智能指针 `weak_ptr`。

**强引用和弱引用**

一个强引用当被引用的对象活着的话，这个引用也存在（就是说，当至少有一个强引用，那么这个对象就不能被释放）。`shared_ptr` 就是强引用。相对而言，弱引用当引用的对象活着的时候不一定存在。仅仅是当它存在的时候的一个引用。弱引用并不修改该对象的引用计数，这意味这弱引用它并不对对象的内存进行管理，在功能上类似于普通指针，然而一个比较大的区别是，弱引用能检测到所管理的对象是否已经被释放，从而避免访问非法内存。
**使用`weak_ptr`来打破循环引用，将以上代码中 pb 声明为 `weak_ptr` 即可解决。**
输出结果：

```markdown
sa use count:2
sb use count:1
kill B
kill A
```

**需要知道的**

`weak_ptr`除了对所管理对象的基本访问功能（通过`get()`函数）外，还有两个常用的功能函数：`expired()`用于检测所管理的对象是否已经释放；`lock()`用于获取所管理的对象的强引用指针。不能直接通过`weak_ptr`来访问资源。那么如何通过`weak_ptr`来间接访问资源呢？答案是：在需要访问资源的时候`weak_ptr`为你生成一个`shared_ptr`，`shared_ptr`能够保证在`shared_ptr`没有被释放之前，其所管理的资源是不会被释放的。创建`shared_ptr`的方法就是`lock()`方法。


## 栈与堆比较

另外补充话题 C++ 内存管理，对比堆栈的区别并得出结论，何时用栈（Stack），何时用堆（Heap）。

|    | 大小 | 是否可变                 | 生命周期                               | 效率                    |
|----|------|--------------------------|----------------------------------------|-------------------------|
| 栈 | 较小 | 不可变，在编译期就要确定 | 生命周期结束时，会自动调用析构函数     | 更高效                  |
| 堆 | 较大 | 可变                     | 需要手动释放内存，必须警觉内存泄漏问题 | new / malloc() 较慢操作 |

**例子：**

```cpp
class Thingy;

Thingy* foo()
{
  Thingy B; // this thingy lives on the stack and will be deleted when we return from foo
  Thingy *pointerToB = &B; // this points to an address on the stack
  Thingy *pointerToC = new Thingy(); // this makes a Thingy on the heap.
                                     // pointerToC contains its address.

  // this is safe: C lives on the heap and outlives foo().
  // Whoever you pass this to must remember to delete it!
  return pointerToC;

  // this is NOT SAFE: B lives on the stack and will be deleted when foo() returns.
  // whoever uses this returned pointer will probably cause a crash!
  return pointerToB;
}
```

**结论**

> Store it on the stack, if you CAN.
>
> Store it on the heap, if you NEED TO.
>
> Therefore, prefer the stack to the heap. Some possible reasons that you can't store something on the stack are:
>
> - It's too big - on multithreaded programs on 32-bit OS, the stack has a small and fixed (at thread-creation time at least) size (typically just a few megs. This is so that you can create lots of threads without exhausting address space. For 64-bit programs, or single threaded (Linux anyway) programs, this is not a major issue. Under 32-bit Linux, single threaded programs usually use dynamic stacks which can keep growing until they reach the top of the heap.
> - You need to access it outside the scope of the original stack frame - this is really the main reason.
>
> It is possible, with sensible compilers, to allocate non-fixed size objects on the heap (usually arrays whose size is not known at compile time).

如果可以优先考虑将对象存放在栈上，如果由于空间限制（不同平台的栈空间限制不同）则考虑将对象放在堆上。不能将对象放在栈上的可能原因有：

- 对象太大；不同平台有不同的限制；
- 对象在其作用域外被使用。

## 参考

[C++ 智能指针及循环引用问题](http://blog.csdn.net/daniel_ustc/article/details/23096229)  
[智能指针（现代 C++）](http://msdn.microsoft.com/zh-cn/library/hh279674.aspx)  
[关于避免循环引用](http://www.dewen.org/q/8560/%E5%85%B3%E4%BA%8E%E9%81%BF%E5%85%8D%E5%BE%AA%E7%8E%AF%E5%BC%95%E7%94%A8)  
[Proper stack and heap usage in C++](http://stackoverflow.com/questions/599308/proper-stack-and-heap-usage-in-c)  
[Stack vs. Heap](http://www.programgo.com/article/9288878764/)  

