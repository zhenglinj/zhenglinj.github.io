---
typora-root-url: ../
title: "Google C++ Style Guide中英对照 (1)"
categories: "technology"
tags:
  - c++
  - google
---

Google C++ Style Guide翻译版中英对照

---

## 1 Background 背景

C++ is the main development language used by many of Google\'s open-source projects. As every C++ programmer knows, the language has many powerful features, but this power brings with it complexity, which in turn can make code more bug-prone and harder to read and maintain.

C++是许多Google的开源项目的主要开发语言。正如每个C++语言的程序员都知道，C++语言有许多强大的功能，但这也带来了复杂性，使代码更容易出错，难以阅读和维护。

The goal of this guide is to manage this complexity by describing in detail the dos and don\'ts of writing C++ code. These rules exist to keep the code base manageable while still allowing coders to use C++ language features productively.

本指南的目标是通过详细阐述在C++代码中注意事项，来驾驭其复杂性。这些规则在保证代码易于管理的同时，允许程序员高效使用C++的特性。

Style, also known as readability, is what we call the conventions that govern our C++ code. The term Style is a bit of a misnomer, since these conventions cover far more than just source file formatting.

风格，也被称为可读性，也就是指导C++编程的约定。称它为风格是有点用词不当，因为这些习惯远不止常见的源代码格式这么简单。

One way in which we keep the code base manageable is by enforcing consistency. It is very important that any programmer be able to look at another\'s code and quickly understand it. Maintaining a uniform style and following conventions means that we can more easily use "pattern-matching" to infer what various symbols are and what invariants are true about them. Creating common, required idioms and patterns makes code much easier to understand. In some cases there might be good arguments for changing certain style rules, but we nonetheless keep things as they are in order to preserve consistency.

保持代码易于管理的一种方法是加强一致性。使任何程序员都能快速看懂你的代码是很重要的。保持统一编程风格并遵守下面的约定意味着我们可以更容易的使用“模式匹配”来推断各种标识符的含义，以及什么不变量[^1]是真的。创建通用的、必需的习惯用语和模式可以使代码更容易理解。在某些情况下，即使我们有充分的理由去改变某些风格，但为了保持一致性，我们尽量不这么做。

Another issue this guide addresses is that of C++ feature bloat. C++ is a huge language with many advanced features. In some cases we constrain, or even ban, use of certain features. We do this to keep code simple and to avoid the various common errors and problems that these features can cause. This guide lists these features and explains why their use is restricted.

本指南解决的另一个问题是，C ++的功能膨胀。C++是一门包含大量高级特性的庞大语言。某些情况下我们需要限制甚至禁止一些特性的使用。这是为了保持代码的简洁和避免那些特性常常引起的问题。本指南列出了这些特性并解释为什么它们被限制使用。

Open-source projects developed by Google conform to the requirements in this guide.

Google主导的开源项目都遵守本指南中的要求。

Note that this guide is not a C++ tutorial: we assume that the reader is familiar with the language.

注意：本指南不是C++的入门手册，我们假定读者熟悉C++。

## 2 Header Files 头文件

In general, every .cc file should have an associated .h file. There are some common exceptions, such as unittests and small .cc files containing just a main() function.

通常每个.cc文件都应该有一个对应的.h文件。也有一些常见的例外，如单元测试文件和只包含main()函数的.cc文件。

Correct use of header files can make a huge difference to the readability, size and performance of your code.

正确的使用头文件可以令你的代码的可读性、大小和性能上大为改观。

The following rules will guide you through the various pitfalls of using header files.

下面的几条准则会指引你避开几种使用头文件时的陷阱。

### 2.1 The #define Guard #define保护

All header files should have #define guards to prevent multiple inclusion. The format of the symbol name should be `<PROJECT>_<PATH>_<FILE>_H_`.

每个头文件都应该使用#define来避免多次加载[^2]。#define定义的名字应该遵循以下格式：`<项目名>_<路径名>_<文件名>_H_`。

To guarantee uniqueness, they should be based on the full path in a project\'s source tree. For example, the file foo/src/bar/baz.h in project foo should have the following guard:

为保证唯一性, 头文件的命名应该依据所在项目源代码树的全路径。例如，foo项目中位于foo/src/bar的baz.h文件可按如下格式保护：

```cpp
#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_
...
#endif // FOO_BAR_BAZ_H_
```

### 2.2 Forward Declarations  前向声明

You may forward declare ordinary classes in order to avoid unnecessary `#includes`.

前向声明可以避免不必要的#include[^3]。

Definition:

A "forward declaration" is a declaration of a class, function, or template without an associated definition. `#include` lines can often be replaced with forward declarations of whatever symbols are actually used by the client code.

定义：

如果只声明类、函数或模板而不定义的话，这种声明称为前向声明。将客户代码中实际用到的所有符号都进行前向声明的话，常常可以替代`#include`语句。

Pros:

1. Unnecessary #includes force the compiler to open more files and process more input.
2. They can also force your code to be recompiled more often, due to changes in the header.

优点：

1. 不必要的#include会迫使编译器打开更多的文件，产生更多的输入[^4]。
2. 不必要的#include也会导致一旦头文件有更改，你的代码就需要重新编译。

Cons:

1. It can be difficult to determine the correct form of a forward declaration in the presence of features like templates, typedefs, default parameters, and using declarations.
2. It can be difficult to determine whether a forward declaration or a full #include is needed for a given piece of code, particularly when implicit conversion operations are involved. In extreme cases, replacing an #include with a forward declaration can silently change the meaning of code.
3. Forward declaring multiple symbols from a header can be more verbose than simply #includeing the header.
4. Forward declarations of functions and templates can prevent the header owners from making otherwise-compatible changes to their APIs; for example, widening a parameter type, or adding a template parameter with a default value.
5. Forward declaring symbols from namespace std:: usually yields undefined behavior.
6. Structuring code to enable forward declarations (e.g. using pointer members instead of object members) can make the code slower and more complex.
7. The practical efficiency benefits of forward declarations are unproven.

缺点：

1. 在诸如模板、typedef、默认参数和使用声明等特性面前，很难确定正确的前向声明的形式[^5]。
2. 对于给定的代码片段，很难确定它更需要前向声明还是完整的#include，尤其是当涉及隐式转换操作[^6]时。极端情况下，将#include更换为前向声明会导致代码的含义被难以察觉的改变。
3. 前向声明同一个头文件中的多个符号要比简单的#include头文件更冗长罗嗦。
4. 对函数和模板进行前向声明会导致头文件的作者无法对他们的API作出可兼容的改动[^7]，例如扩大参数类型范围，增加一个有默认值的模板参数等等。
5. 前向声明std命名空间中的符号经常会导致未定义的行为。
6. 为了允许前向声明而构建的代码（例如用指针来取代对象成员）会导致代码更复杂更慢[^8]。
7. 前向声明在实际应用上效率的收益并未得到证实。

Decision:

1. When using a function declared in a header file, always #include that header.
2. When using a class template, prefer to #include its header file.
3. When using an ordinary class, relying on a forward declaration is OK, but be wary of situations where a forward declaration may be insufficient or incorrect; when in doubt, just #include the appropriate header.
4. Do not replace data members with pointers just to avoid an #include.

结论：

1. 当使用一个声明在头文件中的函数时，总是#include那个头文件。
2. 当使用类模板时，倾向于#include类的头文件。
3. 当使用一个普通类时，依赖于前向声明是可以的，但要警惕一些前向声明并不足够[^9]或是不正确的场合。如果确定不下来用哪个，就直接#include适当的头文件。
4. 不要只是为了省掉#include就把数据成员替换为指针。

Always #include the file that actually provides the declarations/definitions you need; do not rely on the symbol being brought in transitively via headers not directly included. One exception is that myfile.cc may rely on #includes and forward declarations from its corresponding header file myfile.h.

总是#include实际提供了你需要的声明/定义的头文件[^10]；不要依赖于通过没有直接引用的头文件传递进来的符号。一个例外是myfile.cc可能会依赖于它关联的头文件myfile.h以及其中的前向声明。

### 2.3 Inline Functions 内联函数

Define functions inline only when they are small, say, 10 lines or less.

只有在函数很小，比如10行或更短时，才应该将其定义为内联函数。

Definition:

You can declare functions in a way that allows the compiler to expand them inline rather than calling them through the usual function call mechanism.

定义：

你可以通过某种方式声明函数，来允许编译器将它们内联展开[^11]，而不是通过通常的函数调用机制来调用它。

Pros:

Inlining a function can generate more efficient object code, as long as the inlined function is small. Feel free to inline accessors and mutators, and other short, performance-critical functions.

优点：

当函数很小时，内联该函数可以生成更高效[^12]的目标代码。鼓励将取值函数，设值函数，以及其它短的或对性能要求较高的函数进行内联。

Cons:

Overuse of inlining can actually make programs slower. Depending on a function\'s size, inlining it can cause the code size to increase or decrease. Inlining a very small accessor function will usually decrease code size while inlining a very large function can dramatically increase code size. On modern processors smaller code usually runs faster due to better use of the instruction cache.

缺点：

过度使用内联实际上会拖慢程序。内联一个函数会导致代码大小增加或减少（取决于函数大小）。将一个非常小的取值函数内联化通常可以减少代码的大小，而将一个非常大的函数内联化则会戏剧性的增加代码大小[^13]。现代处理器由于更好的利用了指令缓存, 小巧的代码往往执行更快。

Decision:

结论：

A decent rule of thumb is to not inline a function if it is more than 10 lines long. Beware of destructors, which are often longer than they appear because of implicit member- and base-destructor calls!

一个较为合理的经验法则是：不要内联超过10行的函数。谨慎对待析构函数，它们通常会比看起来要更长，因为有隐式的成员和基类的析构函数[^14]的调用！

Another useful rule of thumb: it\'s typically not cost effective to inline functions with loops or switch statements (unless, in the common case, the loop or switch statement is never executed).

另一个实用的经验法则是：内联带有循环或switch语句的函数常常得不偿失（除非大多数情况下不会执行循环或switch）。

It is important to know that functions are not always inlined even if they are declared as such; for example, virtual and recursive functions are not normally inlined. Usually recursive functions should not be inline. The main reason for making a virtual function inline is to place its definition in the class, either for convenience or to document its behavior, e.g., for accessorsand mutators.

一个被声明为内联的函数不是总会被内联展开，这点很重要。例如，虚函数和递归函数一般不会被内联。通常递归函数也不应该被内联[^15]。将一个虚函数声明为内联的主要原因是为方便起见而将它的定义放进类中，或是当作一种文档，比如取值和设值函数。

### 2.4 The -inl.h Files Cinl.h文件

You may use file names with a -inl.h suffix to define complex inline functions when needed.

复杂的内联函数的定义,  应放在后缀名为 -inl.h 的头文件中。

The definition of an inline function needs to be in a header file, so that the compiler has the definition available for inlining at the call sites. However, implementation code properly belongs in .cc files, and we do not like to have much actual code in .h files unless there is a readability or performance advantage.

内联函数的定义需要在一个头文件里，编译器才能在内联函数调用处展开其定义。但是，实现代码应该属于.cc文件，我们不希望在.h文件中有太多实现代码[^16]，除非在可读性上或性能上有明显优势。

If an inline function definition is short, with very little, if any, logic in it, you should put the code in your .h file. For example, accessors and mutators should certainly be inside a class definition. More complex inline functions may also be put in a .h file for the convenience of the implementer and callers, though if this makes the .h file too unwieldy you can instead put that code in a separate -inl.h file. This separates the implementation from the class definition, while still allowing the implementation to be included where necessary.

如果一个内联函数的定义很短且逻辑简单，你应该把它放到.h文件中。例如取值和设值函数就应该放在类中[^17]。为了实现者和调用者的方便，更复杂的内联函数也可以放入.h文件中，如果你觉得这样.h文件太臃肿，你也可以将这些代码放到一个分离的-inl.h文件[^18]中。这样把实现和类定义分离开来, 当需要时包含对应的-inl.h 即可。

Another use of -inl.h files is for definitions of function templates. This can be used to keep your template definitions easy to read.

-inl.h文件的另一个用途是放置函数模板的定义[^19]。能增强模板定义的可读性。

Do not forget that a -inl.h file requires a #define guard just like any other header file.

不要忘了-inl.h像其它头文件一样，也需要用#define保护。

### 2.5 Function Parameter Ordering函数参数顺序

When defining a function, parameter order is: inputs, then outputs.

定义一个函数时，参数顺序是：输入参数，然后是输出参数。

Parameters to C/C++ functions are either input to the function, output from the function, or both. Input parameters are usually values or const references, while output and input/output parameters will be non-const pointers. When ordering function parameters, put all input-only parameters before any output parameters. In particular, do not add new parameters to the end of the function just because they are new; place new input-only parameters before the output parameters.

C/C++函数的参数包括输入参数，输出参数，输入/输出参数。输入参数通常传值或常量引用，而输出参数和输入/输出参数需要用非常量的指针。排列函数参数时，把输入参数放到所有输出参数的前面。特别是不要把新加入的参数直接放到函数参数表的最后，要把新的输入参数放到输出参数前面。

This is not a hard-and-fast rule. Parameters that are both input and output (often classes/structs) muddy the waters, and, as always, consistency with related functions may require you to bend the rule.

这不是一个硬性的规则。输入/输出参数[^20]（通常是类或结构体）把事情弄复杂了，但为了保持与相关函数的一致性你也可能需要变通。

### 2.6 Names and Order of Includes头文件的名字和顺序

Use standard order for readability and to avoid hidden dependencies: C library, C++ library, other libraries\' .h, your project\'s .h.

使用标准的头文件包含顺序可增强可读性，避免隐藏的依赖关系[^21]：C的库，C++的库，其它库的.h文件，本项目中的.h文件。

All of a project\'s header files should be listed as descendants of the project\'s source directory without use of UNIX directory shortcuts . (the current directory) or .. (the parent directory). For example, google-awesome-project/src/base/logging.h should be included as

项目内头文件应按照项目源代码目录树结构排列，避免使用 UNIX 特殊的快捷目录.和..[^22]。例如，google-awesome-project/src/base/logging.h应该按如下格式引入：

```cpp
#include "base/logging.h"
```

In dir/foo.cc or dir/foo_test.cc, whose main purpose is to implement or test the stuff in dir2/foo2.h, order your includes as follows:

1. dir2/foo2.h (preferred location ― see details below).
2. C system files.
3. C++ system files.
4. Other libraries\' .h files.
5. Your project\'s .h files.

又如，dir/foo.cc文件的主要目的是实现或测试dir2/foo2.h，它应该按如下顺序排列头文件：

1. dir2/foo2.h（优先位置――详情见下）。
2. C的库文件。
3. C++的库文件。
4. 其它库的.h文件。
5. 本项目中的.h文件。

With the preferred ordering, if dir2/foo2.h omits any necessary includes, the build of dir/foo.cc or dir/foo_test.cc will break. Thus, this rule ensures that build breaks show up first for the people working on these files, not for innocent people in other packages.

按这种顺序，如果dir2/foo2.h省略了任何必要的头文件，dir/foo.cc的构建就会中止。这个法则确保构建的中止首先会被作者发现，而不用等到其它人来发现。[^23]

dir/foo.cc and dir2/foo2.h are often in the same directory (e.g. base/basictypes_test.cc and base/basictypes.h), but can be in different directories too.

dir/foo.cc和dir2/foo2.h一般在相同的目录下（例如base/basictypes_test.cc和base/basictypes.h），但也可以在不同的目录下。

Within each section the includes should be ordered alphabetically. Note that older code might not conform to this rule and should be fixed when convenient.

各部分的引入文件应该按字母顺序排列。请注意，旧的代码可能不符合这个规则，应该在方便的时候修复这个问题。

For example, the includes in google-awesome-project/src/foo/internal/fooserver.cc might look like this:

例如，在google-awesome-project/src/foo/internal/fooserver.cc中的引入文件看起来可能是这样的：

```cpp
#include "foo/public/fooserver.h" // Preferred location.
#include <sys/types.h>
#include <unistd.h>
#include <hash_map>
#include <vector>
#include "base/basictypes.h"
#include "base/commandlineflags.h"
#include "foo/public/bar.h"
```

## 3 Scoping 作用域

### 3.1 Namespaces命名空间

Unnamed namespaces in .cc files are encouraged. With named namespaces, choose the name based on the project, and possibly its path. Do not use a using-directive.

鼓励在.cc文件中使用未命名空间[^24]。对于命名空间，要基于项目来选择它的名字，也可以基于路径。不用加上using指示符。

Definition:

Namespaces subdivide the global scope into distinct, named scopes, and so are useful for preventing name collisions in the global scope.

定义：

命名空间将全局作用域细分成不同的、有名字的作用域，可以有效避免全局作用域下的命名冲突[^25]。

Pros:

Namespaces provide a (hierarchical) axis of naming, in addition to the (also hierarchical) name axis provided by classes.

For example, if two different projects have a class Foo in the global scope, these symbols may collide at compile time or at runtime. If each project places their code in a namespace, project1::Foo and project2::Foo are now distinct symbols that do not collide.

优点：

类提供了一个命名轴线，命名空间又补充了一个命名轴线[^26]。

例如，如果两个不同的项目的全局作用域下都有一个名字为Foo的类，运行或者编译时这两个名字就可能会出现冲突。如果每个项目都把代码放入它们自己的命名空间中，新的名字project1::Foo和project2::Foo现在就不会冲突了。

Cons:

Namespaces can be confusing, because they provide an additional (hierarchical) axis of naming, in addition to the (also hierarchical) name axis provided by classes.

Use of unnamed namespaces in header files can easily cause violations of the C++ One Definition Rule (ODR).

缺点：

命名空间也可能令人迷惑，因为它在由类划分的命名层次之上又新增了一些层次[^27]。

在头文件中使用未命名空间很容易违反C++的唯一定义原则[^28]。

Decision:

Use namespaces according to the policy described below. Terminate namespaces with comments as shown in the given examples.

结论：

根据下列政策来使用命名空间。在下面的例子中用注释来标注命名空间的结束。

**Unnamed Namespaces未命名空间**

Unnamed namespaces are allowed and even encouraged in .cc files, to avoid runtime naming conflicts:

在.cc文件中未命名空间是允许的而且我们鼓励这么做[^29]，来避免运行时的命名冲突：

```cpp
namespace { // This is in a .cc file.
// The content of a namespace is not indented
// 命名空间中的内容不需要缩进
enum { kUnused, kEOF, kError }; // Commonly used tokens.常用的符号。
bool AtEof() { return pos_ == kEOF; } // Uses our namespace's
EOF.使用我们的命名空间中的EOF符。

} // namespace
```

However, file-scope declarations that are associated with a particular class may be declared in that class as types, static data members or static member functions rather than as members of an unnamed namespace.

但是，文件作用域内的一些与某个类有关的声明也可以声明为那个类的自定义类型[^30]、静态数据成员或是静态函数成员，而不是声明在未命名空间内。

- Do not use unnamed namespaces in .h files.

在.h文件中不要用未命名空间[^31]。

**Named Namespaces 命名空间**

Named namespaces should be used as follows:

命名空间应该按以下方式使用：

1. Namespaces wrap the entire source file after includes, gflags definitions/declarations, and forward declarations of classes from other namespaces:

用命名空间把引入语句、全局符号的定义/声明、以及其它命名空间的类的前向声明之外的源代码包裹起来[^32]。

```cpp
// In the .h file

namespace mynamespace {
// All declarations are within the namespace scope.所有的声明都在这个命名空间作用域下。
// Notice the lack of indentation.注意一下没有缩进。
class MyClass {
 public:
  ...
  void Foo();
};

} // namespace mynamespace
```

```cpp
// In the .cc file
namespace mynamespace {
// Definition of functions is within scope of the namespace.函数的定义也在命名空间的作用域内
void MyClass::Foo() {
  ...
}
} // namespace mynamespace
```

The typical .cc file might have more complex detail, including the need to reference classes in other namespaces.

典型的.cc文件细节处也许更复杂，包括了需要引用其它命名空间的类。

```cpp
#include "a.h"

DEFINE_bool(someflag, false, "dummy flag");

class C; // Forward declaration of class C in the global namespace.
         // 前向声明全局作用域下的类C。

namespace a { class A; } // Forward declaration of a::A.前向声明a::A。

namespace b {
  ...code for b... // Code goes against the left margin.代码贴着左边的空白。
} // namespace b
```

2. Do not declare anything in namespace std, not even forward declarations of standard library classes. Declaring entities in namespace std is undefined behavior, i.e., not portable. To declare entities from the standard library, include the appropriate header file.

不要在std命名空间内声明任何东西，即使是标准库类的前置声明。在std中声明一个东西是未定义的行为，即不可移植的。要声明标准库中的东西就直接引入相应的头文件
。

3. You may not use a using-directive to make all names from a namespace available.

不推荐用using指示符来引入一个命名空间中所有可用的名字[^33]。

```cpp
// Forbidden -- This pollutes the namespace.禁止――这会污染这个命名空间。

using namespace foo;
```

4. You may use a using-declaration anywhere in a .cc file, and in functions, methods or classes in .h files.

你可以在.cc文件中使用using指示符，也可以在.h文件的函数、方法或是类中使用（即不能在.h文件的公共作用域内[^34]）。

```cpp
// OK in .cc files.
// Must be in a function, method or class in .h files.
using ::foo::bar;
```

5. Namespace aliases are allowed anywhere in a .cc file, anywhere inside the named namespace that wraps an entire .h file, and in functions and methods.

允许在.cc文件的任何地方为命名空间起别名，在.h文件的命名空间内的任何地方或是函数方法内也可以这么做。

```cpp
// Shorten access to some commonly used names (in a .cc files).在.cc文件中为一些常用的名字起个短名。
namespace fbz = ::foo::bar::baz;
// Shorten access to some commonly used names (in a .h file).在.h文件中为一些常用的名字起个短名。
namespace librarian {
// The following alias is available to all files including
// this header (in namespace librarian):下面的别名在所有引入这个头文件的文件中都生效（在librarian空间内）。
// alias names should therefore be chosen consistently
// within a project.因此在一个项目中选择别名时要保持一致性。
namespace pd_s = ::pipeline_diagnostics::sidetable;

inline void my_inline_function() {
  // namespace alias local to a function (or method).
  namespace fbz = ::foo::bar::baz;
  ...
}

} // namespace librarian
```

Note that an alias in a .h file is visible to everyone #including that file, so public headers (those available outside a project) and headers transitively #included by them, should avoid defining aliases, as part of the general goal of keeping public APIs as small as possible.

注意到，在一个.h文件中的别名会在所有引入这个头文件的地方可见，所以公有的头文件（在项目之外仍可使用）和被它们#include引入的其它头文件，不应该用别名[^35]，部分因为要保持公有API尽量小的目的。

### 3.2 Nested Classes嵌套类

Although you may use public nested classes when they are part of an interface, consider a namespace to keep declarations out of the global scope.

当公有嵌套类作为接口的一部分[^36]时，虽然可以直接将他们保持在全局作用域中，但将嵌套类的声明置于命名空间内是更好的选择。

Definition:

A class can define another class within it; this is also called a member class.

定义：

一个类可以被定义在另一个类内，它也被称为成员类。

```cpp
class Foo {
 private:
  // Bar is a member class, nested within Foo.Bar是Foo中嵌套的成员类。
  class Bar {
    ...
  };
};
```

Pros:

This is useful when the nested (or member) class is only used by the enclosing class; making it a member puts it in the enclosing class scope rather than polluting the outer scope with the class name. Nested classes can be forward declared within the enclosing class and then defined in the .cc file to avoid including the nested class definition in the enclosing class declaration, since the nested class definition is usually only relevant to the implementation.

优点：

当嵌套类只被外围类使用时[^37]很有用；把它放到外围类中要比占用了外部作用域的可用名字更好。嵌套类可以在外围类中前向声明而将其定义放到.cc文件中，以避免在外围类的声明中引入嵌套类的定义，因为嵌套类的定义通常只和实现有关[^38]。

Cons:

Nested classes can be forward-declared only within the definition of the enclosing class. Thus, any header file manipulating a Foo::Bar* pointer will have to include the full class declaration for Foo.

缺点：

嵌套类只有在外围类中才能前向声明。因为任何要用到Foo::Bar*指针[^39]的头文件都需要引入Foo的整个类声明。

Decision:

Do not make nested classes public unless they are actually part of the interface, e.g., a class that holds a set of options for some method.

结论：

不要将嵌套类定义成公有，除非它们是接口的一部分，比如，嵌套类含有某些方法的多个选项。

### 3.3 Nonmember, Static Member, and Global Functions 非成员函数，静态成员函数，全局函数

Prefer nonmember functions within a namespace or static member functions to global functions; use completely global functions rarely.

推荐使用在命名空间内的非成员函数或是静态成员函数来取代全局函数；尽量少用完全的全局函数。

Pros:

Nonmember and static member functions can be useful in some situations. Putting nonmember functions in a namespace avoids polluting the global namespace.

优点：

非成员函数和静态成员函数在一些场合很有用。将非成员函数放入一个命名空间内可以避免污染全局空间。

Cons:

Nonmember and static member functions may make more sense as members of a new class, especially if they access external resources or have significant dependencies.

缺点：

将非成员函数和静态成员函数作为一个新的类的成员时可能更有意义，尤其是当它们访问外部资源或是有着显著的依赖关系时。

Decision:

Sometimes it is useful, or even necessary, to define a function not bound to a class instance. Such a function can be either a static member or a nonmember function. Nonmember functions should not depend on external variables, and should nearly always exist in a namespace. Rather than creating classes only to group static member functions which do not share static data, use namespaces instead.

结论：

定义一个不属于类的实例的函数有时是有用的，甚至是必要的[^40]。这样的一个函数可以是静态成员函数或是非成员函数。非成员函数应该不依赖于外部变量，且应该在命名空间内。如果为了将静态成员函数组合起来而创建一个没有共享静态数据的类，不如将它们放到命名空间中。

Functions defined in the same compilation unit as production classes may introduce unnecessary coupling and link-time dependencies when directly called from other compilation units; static member functions are particularly susceptible to this. Consider extracting a new class, or placing the functions in a namespace possibly in a separate library.

定义在同一个编译单元内的函数在被其它编译单元调用时可能会引入不必要的耦合和链接时依赖；静态成员函数尤其容易受此影响。此时可考虑提取出一个新的类或是将这些函数放到独立库的命名空间内。

If you must define a nonmember function and it is only needed in its .cc file, use an unnamed namespace or static linkage (eg static int Foo() {...}) to limit its scope.

如果你必须定义一个只用于本文件的非成员函数，可以将它放到未命名空间内或是在前面加上static符以限制它的作用范围。

### 3.4 Local Variables 局部变量

Place a function\'s variables in the narrowest scope possible, and initialize variables in the declaration.

将一个函数的变量放到允许的最小作用域内，并且在声明处进行初始化。

C++ allows you to declare variables anywhere in a function. We encourage you to declare them in as local a scope as possible, and as close to the first use as possible. This makes it easier for the reader to find the declaration and see what type the variable is and what it was initialized to. In particular, initialization should be used instead of declaration and assignment, e.g.

C++允许你在函数的任何地方声明变量。我们鼓励你在局部作用域内声明变量，且尽可能靠近它第一次使用的地方。这能方便读者找到声明，得悉变量的类型和初始值。尤其是
初始化应该用于取代声明+赋值[^41]，例如：

```cpp
int i;
i = f(); // Bad -- initialization separate from declaration.不好的――初始化与声明分离。
int j = g(); // Good -- declaration has initialization.//好的――声明即初始化。
```

Note that gcc implements `for (int i = 0; i < 10; ++i)` correctly (the scope of i is only the scope of the for loop), so you can then reuse i in another for loop in the same scope. It also correctly scopes declarations in if and while statements, e.g.

注意到GCC能正确实现`for (int i = 0; i < 10; ++i)`（i的作用范围仅限于循环体内），所以你可以在同一个作用域中重复使用i。在if和while语句中GCC仍能正确限制变量的作用域[^42]。例如：

```cpp
while (const char* p = strchr(str, '/'))
str = p + 1;
```

There is one caveat: if the variable is an object, its constructor is invoked every time it enters scope and is created, and its destructor is invoked every time it goes out of scope.

警告：如果变量是一个类的对象，每次进入这个作用域都会调用它的构建函数并创建对象，离开作用域时同样会调用析构函数。

```cpp
// Inefficient implementation:低效的实现
for (int i = 0; i < 1000000; ++i) {
  Foo f; // My ctor and dtor get called 1000000 times each.构造函数和析构函数要调用100万次。
  f.DoSomething(i);
}
```

It may be more efficient to declare such a variable used in a loop outside that loop:

更高效的方法是在循环外面声明这个变量：

```cpp
Foo f; // My ctor and dtor get called once each.构造函数和析构函数只调用1次。
for (int i = 0; i < 1000000; ++i) {
  f.DoSomething(i);
}
```

### 3.5 Static and Global Variables静态变量和全局变量

Static or global variables of class type are forbidden: they cause hard-to-find bugs due to indeterminate order of construction and destruction.

禁止使用类类型的静态变量或全局变量：因为构建和析构顺序不确定，出bug了很难找。

Objects with static storage duration, including global variables, static variables, static class member variables, and function static variables, must be Plain Old Data (POD): only ints, chars, floats, or pointers, or arrays/structs of POD.

需要持续存在的静态对象，包换全局变量，静态变量，静态成员变量，以及函数中的静态变量，必须是老式的平坦数据类型（POD）：只有内置类型或指针或是数组和结构体才是POD类型[^43]。

The order in which class constructors and initializers for static variables are called is only partially specified in C++ and can even change from build to build, which can cause bugs that are difficult to find. Therefore in addition to banning globals of class type, we do not allow static POD variables to be initialized with the result of a function, unless that function (such as getenv(), or getpid()) does not itself depend on any other globals.

C++中没有指定类的静态变量的构造和初始化顺序，这顺序每次构建都可能改变，这会导致一些bug很难被发现。因此除了禁止全局的类类型变量外，出于同样的理由，我们也不允许静态POD变量利用函数的返回值进行初始化，除非那个函数（如getenv()或getpid()）不依赖于其它的全局符号。

Likewise, the order in which destructors are called is defined to be the reverse of the order in which the constructors were called. Since constructor order is indeterminate, so is destructor order. For example, at program-end time a static variable might have been destroyed, but code still running -- perhaps in another thread -- tries to access it and fails. Or the destructor for a static 'string' variable might be run prior to the destructor for another variable that contains a reference to that string.

同样地，析构过程需要与构造过程的顺序相反。因为构造过程的顺序是不确定的，所以析构过程的顺序也是不确定的。例如，在程序结束时一个静态变量可能需要被移除，但代码仍然在运行――也许是其它线程――试图调用这个变量然后失败了。或者一个静态string变量也许已经析构了而另一个变量中还包含对它的引用。

As a result we only allow static variables to contain POD data. This rule completely disallows vector (use C arrays instead), or string (use const char[]).

结论是我们只允许POD类型的静态变量。这个准则完全不允许vector（换成C风格的数组）或是string（换成C风格的字符串）。

If you need a static or global variable of a class type, consider initializing a pointer (which will never be freed), from either your main() function or from pthread_once(). Note that this must be a raw pointer, not a "smart" pointer, since the smart pointer\'s destructor will have the order-of-destructor issue that we are trying to avoid.

如果你需要一个类类型的静态或全局变量，考虑在主函数或是在线程初始化处初始化一个指针（永远不会被释放[^44]）。要注意它必须是原始的指针而不是智能指针[^45]，因为智能指针的析构器同样存在我们极力避免的析构顺序的问题。

* * *

## 脚注

[^1]: 帮助确定哪些不变量保持为真

[^2]: 会导致重复声明

[^3]: 前向声明是为了降低编译依赖，防止修改一个头文件引发多米诺效应

[^4]: 于是编译时间大大延长

[^5]: 此时的声明形式会很复杂，尤其涉及到依赖的声明时

[^6]: 有重载函数时可能改变匹配的函数

[^7]: 这些改动只需要改变声明，不需要改变实际的调用处代码

[^8]: 用指针代替对象，可能需要进行堆的分配，并且每个操作都要进行间接跳转，可还需要查询虚函数表

[^9]: 不允许访问类的定义的前提下, 我们在一个头文件中能对类 Foo 做哪些操作? 我们可以将数据成员类型声明为 Foo * 或 Foo &. 我们可以将函数参数 / 返回值的类型声明为 Foo (但不能定义实现). 我们可以将静态数据成员的类型声明为 Foo, 因为静态数据成员的定义在类定义之外.

[^10]: .cc文件总是需要#include的，因为需要知道具体实现

[^11]: 将最终代码直接嵌入调用处，不会产生实际的函数和函数调用

[^12]: 省去了函数调用和返回的开销

[^13]: 因为编译器会在所有调用处展开函数的代码

[^14]: 先析构成员，再依次向上调用基类的析构函数

[^15]: 递归调用堆栈的展开并不像循环那么简单, 比如递归层数在编译时可能是未知的, 大多数编译器都不支持内联递归函数

[^16]: 实现与接口分离，首先阅读清晰，其次减少编译次数，最重要的，降低耦合

[^17]: 增加可读性

[^18]: .h中不需要include这个inl.h文件，.cc中需要，这样用起来很方便，编译也简单

[^19]: 模板的定义一般也推荐放到头文件中

[^20]: 尽量减少用此类参数，数组除外

[^21]: 比如头文件中缺少必要的include时，如果.cc文件中恰好include了这个文件，就发现不了错误

[^22]: 包含文件的名称使用 . 和 .. 虽然方便却易混乱, 使用比较完整的项目路径看上去很清晰, 很条理

[^23]: 包含文件的次序除了美观之外, 最重要的是可以减少隐藏依赖, 使每个头文件在 “最需要编译” 的地方编译, 有人提出库文件放在最后,这样出错先是项目内的文件, 头文件都放在对应源文件的最前面, 这一点足以保证内部错误的及时发现了.

[^24]: 每个文件有自己的未命名空间，其中的名字只能在本文件内用，不用加域作用符，不得与全局符号同名。.h文件可以有未命名空间，包含它的各个文件中，空间内的名字将定义不同的实体。

[^25]: C中是用static来实现这个功能的，但用static无法将实现与接口分离。

[^26]: 就是增加了一层作用域，能避免不属于类的全局元素的命名冲突

[^27]: 层次越多越乱套，知识越多越反动

[^28]: 因为这时相当于多次定义，但不会造成冲突

[^29]: 本文件使用的全局符号都放到未命名空间内。

[^30]: 可以将能整合成一个类的各种符号整合起来

[^31]: 违背了唯一定义的原则

[^32]: 一般来说把自己的所有声明和实现都用命名空间包起来

[^33]: 本来命名空间就是为了避免很难定位的命名冲突，如果直接引入一整套名字，很容易就会引进命名冲突

[^34]: 为了避免包含这个.h的.cc文件无意间引入了一个名字造成冲突

[^35]: .h文件要尽量精简，避免无意间影响包含它的文件

[^36]: 此时嵌套类实际上不依赖于接口的实现类，因此可以直接拿出来

[^37]: 也符合最大化封装的原则

[^38]: 接口与实现分离

[^39]: 前面说了只用类的指针的话可以进行前向声明，但这里涉及到了外围类，需要知道外围类的具体布局信息

[^40]: 各种方法的目的是避免命名冲突，减少耦合

[^41]: 内置类型这两种没区别，类必须在声明时初始化，否则会多一次复制的开销

[^42]: 如果不需要在局部作用域外保持变量的值，就在这几个语句中声明+初始化，能避免一些变量使用上的隐蔽的错误

[^43]: 即C中的各种类型，因为类有很多的运行时才确定的东西，对顺序要求很高

[^44]: 可以确定构造和析构的顺序了

[^45]: 智能指针也是类的对象

