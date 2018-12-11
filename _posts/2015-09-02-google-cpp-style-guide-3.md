---
typora-root-url: ../
title: "Google C++ Style Guide中英对照 (3)"
categories: "technology"
tags:
  - c++
  - google
---


Google C++ Style Guide翻译版中英对照

---

## 1 Naming 命名规则

The most important consistency rules are those that govern naming. The style of a name immediately informs us what sort of thing the named entity is: a type, avariable, a function, a constant, a macro, etc., without requiring us to search for the declaration of that entity. The pattern-matching engine in our brains relies a great deal on these naming rules.

最重要的一致性规则是命名管理。命名的风格能立刻告诉我们这个名字代表的实体到底是什么东西：类型，变量，函数，常量，宏，等等，而不需要我们去寻找该实体的声明。我们头脑中的模式匹配引擎大量依赖于这些命名规则。

Naming rules are pretty arbitrary, but we feel that consistency is more important than individual preferences in this area, so regardless of whether you find them sensible or not, the rules are the rules.

命名规则是很随意的，但我们觉得这方面一致性要比个人喜好重要得多，所以不管你怎么想，规则就是规则。

### 1.1 General Naming Rules 通用命名规则

Function names, variable names, and filenames should be descriptive; eschew abbreviation. Types and variables should be nouns, while functions should be "command" verbs.

函数名，变量名，和文件名应该是描述性的；不要过度缩写。类型名和变量名应该是名词，而函数名应该是命令式的动词。

**How to Name 怎么命名**

Give as descriptive a name as possible, within reason. Do not worry about saving horizontal space as it is far more important to make your code immediately understandable by a new reader. Examples of well-chosen names:

尽量有理由的起一个描述性的名字。别担心行空间的问题[^1] ，让你的代码能被新读者很快理解远远比这更重要。好的例子：

```cpp
int num_errors;                  // Good.
int num_completed_connections;   // Good.
```

Poorly-chosen names use ambiguous abbreviations or arbitrary characters that do not convey meaning:

不好的名字使用模棱两可的缩写或难以传达其含义的任意字符：

```cpp
int n;                           // Bad - meaningless.无含义
int nerr;                        // Bad - ambiguousabbreviation.模糊的缩写
int n_comp_conns;                // Bad - ambiguousabbreviation.模糊的缩写
```

Type and variable names should typically be nouns: e.g., FileOpener, num_errors.

类型名和变量名通常应该是名词：如FileOpener，num_errors。

Function names should typically be imperative (that is they should be commands): e.g.,`OpenFile()`, `set_num_errors()`. There is an exception for accessors, which, described more completely in Function Names, should be named the same as the variable they access.

函数名通常应该是祈使语气的（即命令性的）：如`OpenFile()`，`set_num_errors()`。取值函数[^2]是个特例，函数名应该与变量名相同，这样函数名的含义更完整。

**Abbreviations 缩写**

Do not use abbreviations unless they are extremely well known outside your project. For example:

不要使用缩写，除非这个缩写在你的项目之外也被广泛使用。例如：

```cpp
// Good
// These show proper names with noabbreviations.
int num_dns_connections;  // Most people know what "DNS"stands for.
int price_count_reader;   // OK, price count. Makes sense.

// Bad!
// Abbreviations can be confusing orambiguous outside a small group.
int wgc_connections;  // Only your group knows what this standsfor.
int pc_reader;        // Lots of things can be abbreviated"pc".
```

Never abbreviateby leaving out letters:

永远不要用省略字母的缩写。

```cpp
int error_count;  // Good.
int error_cnt;    // Bad.
```

### 1.2 File Names 文件名

Filenames should be all lowercase and can include underscores (`_`) or dashes (`-`). Follow the convention that your project uses. If there is no consistent local pattern to follow, prefer "_".

文件名应该全都用小写，中间用“-”或“\_”当分隔符。根据你的项目的惯例。如果没有固定的习惯的话，推荐用“\_”。

Examples ofacceptable file names:

可接受的文件名示例：

```
my_useful_class.cc
my-useful-class.cc
myusefulclass.cc
myusefulclass_test.cc // _unittest and_regtest are deprecated.这两个后缀不建议使用了。
```

C++ files should end in .cc and header files should end in .h.

C++文件应该以.cc结尾，头文件以.h结尾。

Do not use filenames that already exist in /usr/include, such as db.h.

不要用系统头文件中已经存在的名字，如db.h。

In general, make your filenames very specific. For example, use `http_server_logs.h` rather than `logs.h`. A very common case is to have a pair of files called, e.g., `foo_bar.h` and `foo_bar.cc`, defining a class called FooBar.

通常来说，让你的文件名非常的具体。例如用`http_server_logs.h`就比`logs.h`更好。定义类时文件名经常成对出现，如`foo_bar.h`和`foo_bar.cc`，对应类FooBar。

Inline functions must be in a .h file. If your inline functions are very short, they should godirectly into your .h file. However, if your inline functions include a lot of code, they may go into a third file that ends in -inl.h. In a class with a lot of inline code, your class could have three files:

内联函数必须放在.h文件中。如果内联函数很短，就直接放进.h文件中。否则就应该放进-inl.h文件中。一个有着很多内联代码的类，可以对应三个文件：

```cpp
url_table.h      // The class declaration.类的声明
url_table.cc     // The class definition.类的定义
url_table-inl.h  // Inline functions that include lots ofcode.代码较多的内联函数的定义
```

See also thesection -inl.h Files

### 1.3 Type Names 类型名

Type names start with a capital letter and have a capital letter for each new word, with no underscores: MyExcitingClass, MyExcitingEnum.

类型名以大写字母开头，且其中每个词第一个字母都大写，不用下划线：MyExcitingClass，MyExcitingEnum。

The names of all types ― classes, structs, typedefs, and enums ― have the same naming convention. Type names should start with a capital letter and have a capital letter for each new word. No underscores. For example:

所有类型――类，结构体，自定义类型，和枚举――都有着相同的命名惯例。类型名以大写字母开头，且其中每个词也都以大写字母开头。不用下划线。例如：

```cpp
// classes and structs
class UrlTable { ...
class UrlTableTester { ...
struct UrlTableProperties { ...

// typedefs
typedef hash_map<UrlTableProperties *,string> PropertiesMap;

// enums
enum UrlTableErrors { ...
```

### 1.4 Variable Names 变量名

Variable names are all lowercase, with underscores between words. Class member variables have trailing underscores. For instance: `my_exciting_local_variable`, `my_exciting_member_variable_`.

变量名都是小写的，每个词之间用下划线连接。类的成员变量名结尾有个下划线。例如：`my_exciting_local_varialbe`；`my_exciting_member_variable_`。

**Common Variable names 普通变量名**

For example:

例如：

```cpp
string table_name;  // OK - uses underscore.
string tablename;   // OK - all lowercase.

string tableName;   // Bad - mixed case.
```
**Class Data Members类的数据成员**

Data members(also called instance variables or member variables) are lowercase with optional underscores like regular variable names, but always end with a trailing underscore.

数据成员（也被称为实例变量或成员变量）的名字都是小写的，可以像通常的变量名一样带下划线，但结尾总要有个下划线。

```cpp
string table_name_;  // OK - underscore at end.
string tablename_;   // **OK.
```

**Struct Variables 结构体变量**

Data members instructs should be named like regular variables without the trailing under scoresthat data members in classes have.

结构体中的数据成员要像常规变量那么命名，结尾不像类的数据成员那样有下划线。

```cpp
struct UrlTableProperties {
  string name;
  intnum_entries;
}
```

See Structs vs.Classes for a discussion of when to use a struct versus a **class.

**Global Variables 全局变量**

There are nospecial requirements for global variables, which should be rare in any case, but if you use one, consider prefixing it with g_ or some other marker to easily distinguish it from local variables.

对于全局变量没有特别要求，少用就好，但如果你要用，考虑加个g_前缀，**或其它能很容易的区分全局变量与局部变量的标记。

### 1.5 Constant Names 常量名

Use a k followed by mixed case: kDaysInAWeek.

在名称前加k，其后与变量相同：kDaysInAWeek。

All compile-time constants, whether they are declared locally, globally, or as part of a class, follow a slightly different naming convention from other variables. Use a k followed by words with uppercase first letters:

所有的编译期变量，不管是局部变量，全局变量，还是类的一部分，都要遵守一个与其它变量不同的惯例。在名称前加k，后面接第一个字母大写的各个单词：

```cpp
const int kDaysInAWeek = 7;
```

### 1.6 Function Names 函数名

Regular functions have mixed case; accessors and mutators match the name of the variable: `MyExcitingFunction()`, `MyExcitingMethod()`, `my_exciting_member_variable()`, `set_my_exciting_member_variable()`.

常规函数的名字大小写混合；取值和设值函数要与对应的变量名匹配：`MyExcitingFunction()`，`MyExcitingMethod()`，`my_exciting_member_variable()`，`set_my_exciting_member_variable()`。

**Regular Functions 常规函数**

Functions should start with a capital letter and have a capital letter for each new word. No underscores.

函数名中每个单词首字母都大写。没有下划线。

If your function crashes upon an error, you should append OrDie to the function name. This only applies to functions which could be used by production code and to errors that are reasonably likely to occur during normal operation.

如果你的函数可能出现错误，你应该在函数名后面加上OrDie。这只适用于能用于生产[^3] ，且在正常操作中可能会发生有原因的错误的函数上。

```
AddTableEntry()
DeleteUrl()
OpenFileOrDie()
```

**Accessors and Mutators 取值和设值函数**

Accessors andmutators (get and set functions) should match the name of the variable they are getting and setting. This shows an excerpt of a class whose instance variableis `num_entries_`.

取值和设值函数应该与相关的变量名匹配。这里摘录一个有着名为`num_entries_`的成员的类。

```cpp
class MyClass {
 public:
  ...
  intnum_entries() const { return num_entries_; }
  voidset_num_entries(int num_entries) { num_entries_ = num_entries; }

 private:
  intnum_entries_;
};
```

You may also use lowercase letters for other very short inlined functions. For example if a function were so cheap you would not cache the value if you were calling it ina loop, then lowercase naming would be acceptable.

其它的一些非常短的内联函数也可以全用小写。例如，如果一个函数的开销小到了你在循环中调用它都不需要将结果缓存起来的话，用小写的名字就很合适了。

### 1.7 Namespace Names 命名空间的名字

Namespace names are all lower-case, and based on project names and possibly their directory structure: `google_awesome_project`.

命名空间的名字都是小写的，与项目名，可能还包括目录结构，相关。

See Namespaces for a discussion of namespaces and how to name them.

### 1.8 Enumerator Names 枚举名

Enumerators should be named either like constants or like macros: either kEnumName or ENUM_NAME.

枚举的命名应当和常量或宏一致：kEnumName或是ENUM_NAME。

Preferably, the individual enumerators should be named like constants. However, it is also acceptable to name them like macros. The enumeration name, UrlTableErrors (andAlternateUrlTableErrors), is a type, and therefore mixed case.

单独的枚举应该优先采用常量的命名方式。但宏方式的命名也可以接受。枚举名，UrlTableErrors （和AlternateUrlTableErrors），是类型，因此要大小写混合。

```cpp
enum UrlTableErrors {
  kOK= 0,
  kErrorOutOfMemory,
  kErrorMalformedInput,
};

enum AlternateUrlTableErrors {
  OK =0,
  OUT_OF_MEMORY = 1,
  MALFORMED_INPUT = 2,
};
```

Until January 2009, the style was to name enum values like macros. This caused problems withname collisions between enum values and macros. Hence, the change to preferconstant-style naming was put in place. New code should prefer constant-style naming if possible. However, there is no reason to change old code to useconstant-style names, unless the old names are actually causing a compile-time problem.

2009年1月前，我们的建议是枚举名的风格和宏一致。这导致了一些枚举与宏的命名冲突。因此，现在改为采用常量风格的命名。新代码应该尽量采用常量风格。但也不必将旧代码改成常量风格的，除非旧的名字确实会导致编译错误。

### 1.9 Macro Names 宏名

You\'re notreally going to define a macro, are you? If you do, they\'re like this: `MY_MACRO_THAT_SCARES_SMALL_CHILDREN`.

你不会真的要定义宏吧？非得用宏的话，要这么命名：`MY_MACRO_THAT_SCARES_SMALL_CHILDREN`。

Please see the description of macros; in general macros should not be used. However, if they are absolutely needed, then they should be named with all capitals and underscores.

请看宏的描述；通常不该用宏。但是，如果真的需要宏，宏名应该全是大写，词之前用下划线分隔。

```cpp
#define ROUND(x) ...
#define PI_ROUNDED 3.0
```

### 1.10 Exceptionsto Naming Rules 命名规则中的例外

If you are naming something that is analogous to an existing C or C++ entity then you can follow the existing naming convention scheme.

如果你命名的实体与已有C/C++实体类似，可参考现有命名策略。

`bigopen()`

- function name, follows form of open() 函数名，参考open()

`uint`

- typedef 自定义类型

`bigpos`

- struct or class, follows form of pos 结构体或类，参考pos

`sparse_hash_map`

- STL-like entity; follows STL namingconventions STL风格实体；参考STL命名惯例

`LONGLONG_MAX`

- a constant, as in `INT_MAX` 常量，参考`INT_MAX`

## 2 Comments 注释

Though a pain to write, comments are absolutely vital to keeping our code readable. The following rules describe what you should comment and where. But remember: while comments are very important, the best code is self-documenting. Giving sensible names to types and variables is much better than using obscure names that you must then explain through comments.

注释尽管写起来很痛苦，但在保持代码的可读性方面至关重要。下面的规则描述了你应该在哪注释什么。但要记住：注释很重要，但最好的代码本身就是文档。给类型和变量起有意义的名字要比用难懂的名字导致必须得用注释解释强得多。

When writing your comments, write for your audience: the next contributor who will need to understand your code. Be generous ― the next one may be you!

在写注释时，目标是你的观众：下一个需要看懂你代码的作者。要好好写[^4] ――下一个作者可能就是你！

### 2.1 CommentStyle 注释风格

Use either the // or /* */ syntax, as long as you are consistent.

用//和/**/都行，尽量保持一致就行。

You can use either the // or the /* */ syntax; however, // is much more common. Be consistent with how you comment and what style you use where.

你既可以用//也可以用/**/；但//更常用。保持注释风格和注释位置与内容的一致性。

### 2.2 FileComments 文件注释

Start each file with license boilerplate, followed by a description of its contents.

每个文件的开始是版权公告，其后是文件内容描述。

**Legal Notice and Author Line 法律声明和作者信息**

Every file should contain license boilerplate. Choose the appropriate boilerplate for the license used by the project (for example, Apache 2.0, BSD, LGPL, GPL).

每个文件都应包括许可证信息。为项目选择适合的许可证版本（如Apache2.0、BSD、LGPL、GPL）。

If you make significant changes to a file with an author line, consider deleting the authorline.

如果你对一个有作者信息的文件进行了大修改，考虑删掉作者信息。

**File Contents 文件内容**

Every file should have a comment at the top describing its contents.

每个文件都应在开头用注释描述文件内容。

Generally a .h file will describe the classes that are declared in the file with an overview of what they are for and how they are used. A .cc file should contain more information about implementation details or discussions of tricky algorithms. If you feel the implementation details or a discussion of the algorithms would be useful for someone reading the .h, feel free to put it there instead, but mention in the .cc that the documentation is in the .h file.

通常来说.h文件会描述文件内声明的类的用途和用法。.cc文件应该包括更多关于实现细节或算法细节讨论等信息。如果你觉得实现细节或算法细节讨论会对阅读.h文件的人有帮助，就可以将这些描述放到.h文件里，但要在.cc中注明文档在.h文件中。

Do not duplicate comments in both the .h and the .cc. Duplicated comments diverge.

不要在.h和.cc中重复注释。这种做法偏离了注释的意义。

### 2.3 Class Comments 类注释

Every class definition should have an accompanying comment that describes what it is for and how it should be used.

每个类定义都应伴随着描述用途和用法的注释。

```cpp
// Iterates over the contents of aGargantuanTable.  Sample usage:
//   GargantuanTableIterator* iter = table->NewIterator();
//   for (iter->Seek("foo"); !iter->done(); iter->Next()){
//     process(iter->key(), iter->value());
//   }
//   delete iter;

class GargantuanTableIterator {
  ...
};
```

If you have already described a class in detail in the comments at the top of your file feel free to simply state "See comment at top of file for a complete description", but be sure to have some sort of comment.

如果你已经在文件开头描述了类的细节，可以简单的标注“见文件开头的完整描述”，但务必确保确实有这类注释。

Document the synchronization assumptions the class makes, if any. If an instance of the class can be accessed by multiple threads, take extra care to document the rules and invariants surrounding multithreaded use.

如果类有任何同步前提，要文档说明。如果类的实例需要在多线程环境下被访问，要特别注意文档说明多线程使用中的规则和常量使用。

### 2.4 Function Comments 函数注释

Declaration comments describe use of the function; comments at the definition of a function describe operation.

声明处的注释描述了函数的用途；定义处的注释描述了具体的操作。

**Function Declarations 函数声明**

Every function declaration should have comments immediately preceding it that describe what the function does and how to use it. These comments should be descriptive("Opens the file") rather than imperative ("Open thefile"); the comment describes the function, it does not tell the function what to do. In general, these comments do not describe how the function performs its task. Instead, that should be left to comments in the function definition.

每个函数声明前面都应有注释来描述函数的用途和用法。这些注释应该是叙述性的（“打开了文件”）而不是命令式的（“打开文件”）；注释是描述函数的，而不是命令函数去做什么。通常这些注释不会描述函数如何工作的，这些内容留给函数定义处的注释去做。

Types of things to mention in comments at the function declaration:

1.    What the inputs and outputsare.
2.    For class member functions: whether the object remembers reference arguments beyond the duration of the method call, and whether it will free them or not.
3.    If the function allocates memory that the caller must free.
4.    Whether any of the arguments can be a null pointer.
5.    If there are any performance implications of how a function is used.
6.    If the function is re-entrant.What are its synchronization assumptions?

在函数声明处注释要提及的事物：

1.    输入和输出是什么。
2.    对于类的成员函数：在函数调用之外对象是否保持对参数的引用，是否会释放这种引用。
3.    函数是否进行了调用者必须释放的内存分配。
4.    函数的参数可不可以是空指针。
5.    函数的使用方法上有没有性能隐患。
6.    如果函数是可重入的，其同步前提是什么？

Here is anexample:

这里有个例子：

```cpp
// Returns an iterator for this table.  It is the client's
// responsibility to delete the iteratorwhen it is done with it,
// and it must not use the iterator once theGargantuanTable object
// on which the iterator was created hasbeen deleted.
//
// The iterator is initially positioned atthe beginning of the table.
//
// This method is equivalent to:
//   Iterator* iter = table->NewIterator();
//   iter->Seek("");
//   return iter;
// If you are going to immediately seek toanother place in the
// returned iterator, it will be faster touse NewIterator()
// and avoid the extra seek.
Iterator* GetIterator() const;
```

However, do not be unnecessarily verbose or state the completely obvious. Notice below that it is not necessary to say "returns false otherwise" because this is implied.

但不必太啰嗦，或做些显而易见的说明。注意下面的注释没有必要加上`returns false otherwise`，因为这是显然的。

```cpp
// Returns true if the table cannot hold anymore entries.
bool IsTableFull();
```

When commenting constructors and destructors, remember that the person reading your code knows what constructors and destructors are for, so comments that just say something like "destroys this object" are not useful. Document what constructors do with their arguments (for example, if they take ownership of pointers), and what cleanup the destructor does. If this is trivial, just skip the comment. It is quite common for destructors not to have a header comment.

在注释构造函数和析构函数时，记住看你代码的人知道什么是构造函数什么是析构函数，所以如“会销毁此对象“之类的注释都是废话。文档中要说明构造函数对参数做了什么（例如是否取得指针所有权），和析构函数都清理了什么。如果这些都无关紧要，就省略注释。析构函数没有头注释是很常见的。

**Function Definitions 函数定义**

Each function definition should have a comment describing what the function does if there\'s anything tricky about how it does its job. For example, in the definition comment you might describe any coding tricks you use, give an overview of the steps you go through, or explain why you chose to implement the function in the way you did rather than using a viable alternative. For instance, you mightmention why it must acquire a lock for the first half of the function but why itis not needed for the second half.

每个函数定义处都应该有注释描述函数功能和实现要点。例如你用的编程技巧，实现的大致步骤，或解释为什么你用这种方法实现这个函数而不是用另一种方法。例如你可以提一下为什么函数的前一半需要锁而后一半不需要。

Note you should not just repeat the comments given with the function declaration, in the .h file or wherever. It\'s okay to recapitulate briefly what the function does, but the focus of the comments should be on how it does it.

要注意你不能只是重复函数声明处的注释。可以简短的概述一下函数做了什么，但注释的目的是要说明它是怎么做的。**

### 2.5 Variable Comments 变量注释

In general the actual name of the variable should be descriptive enough to give a good idea of what the variable is used for. In certain cases, more comments are required.

通常变量的名字就应该足够描述清楚变量的用途的了。在某些场合时，也需要额外的注释。

**Class Data Members 类数据成员**

Each class data member (also called an instance variable or member variable) should have acomment describing what it is used for. If the variable can take sentinel values with special meanings, such as a null pointer or -1, document this. For example:

每个类的数据成员（也被称为实例变量或成员变量）应该有描述其用途的注释。如果这个变量可以取到有特殊含义的值，如空指针或-1，要文档说明。例如：

```cpp
private:
 // Keeps track of the total number of entries in the table.
 // Used to ensure we do not go over the limit. -1 means
 // that we don't yet know how many entries the table has.
 intnum_total_entries_;
```

**Global Variables 全局变量**

As with data members, all global variables should have a comment describing what they are and what they are used for. For example:

与数据成员一样，所有的全局变量都应该用注释来描述变量的含义和用途。例如：

```cpp
// The total number of tests cases that we runthrough in this regression test.
const int kNumTestCases = 6;
```

### 2.6 Implementation Comments 实现注释

In your implementation you should have comments in tricky, non-obvious, interesting, or important parts of your code.

对于代码中巧妙的、晦涩的、有趣的、或重要的部分，应用注释说明。

**Class Data Members 类数据成员**

Tricky or complicated code blocks should have comments before them. Example:

巧妙的或复杂的代码段应该在前面注释。例如：

```cpp
// Divide result by two, taking into accountthat x
// contains the carry from the add.
for (int i = 0; i < result->size();i++) {
  x =(x << 8) + (*result)[i];
  (*result)[i] = x >> 1;
  x&= 1;
}
```

**Line Comments 行注释**

Also, lines that are non-obvious should get a comment at the end of the line. These end-of-line comments should be separated from the code by 2 spaces. Example:

同样的，含义不明的行应该在行尾注释。这些行尾的注释应该与代码保持2个空格的间隙。如：

```cpp
// If we have enough memory, mmap the dataportion too.
mmap_budget = max<int64>(0,mmap_budget - index_->length());
if (mmap_budget >= data_size_ &&!MmapData(mmap_chunk_bytes, mlock))
  return;  // Error already logged.
```

Note that there are both comments that describe what the code is doing, and comments that mention that an error has already been logged when the function returns.

注意到有两条注释，一条描述了代码在做什么，另一条提到了在函数因为错误而返回时错误已经被记录在日志中了。

If you have several comments on subsequent lines, it can often be more readable to line them up:

如果你需要连续进行多行注释，可以使之对齐获得更好的可读性：

```cpp
DoSomething();                  // Comment here so thecomments line up.
DoSomethingElseThatIsLonger();  // Comment here so there are two spacesbetween
                                // the code and the comment.
{ // One space before comment when opening anew scope is allowed,
  //thus the comment lines up with the following comments and code.
  DoSomethingElse();  // Two spacesbefore line comments normally.
}
```

**nullptr/NULL, true/false, 1, 2, 3... 直接量**

When you pass in a null pointer, boolean, or literal integer values to functions, you should consider adding a comment about what they are, or make your code self-documenting by using constants. For example, compare:

当你向函数传递了一个空指针，布尔量，或直接量时，应考虑增加一个注释说明它们是什么，或用常量来让你的代码自文档化。例如，比如：

````cpp
bool success = CalculateSomething(interesting_value,
                                  10,
                                  false,
                                  NULL);  // What are these arguments??
````

versus:

与：

````cpp
bool success = CalculateSomething(interesting_value,
                                  10,     // Default base value.
                                  false,  // Not the first time we're calling this.
                                  NULL);  // No callback.
````

Or alternatively, constants or self-describing variables:

或者用常量或自描述型的变量：

````cpp
const int kDefaultBaseValue = 10;
const bool kFirstTimeCalling = false;
Callback *null_callback = NULL;
bool success = CalculateSomething(interesting_value,
                                  kDefaultBaseValue,
                                  kFirstTimeCalling,
                                  null_callback);
````

**Don\'ts 不要做的事**

Note that you should never describe the code itself. Assume that the person reading the code knows C++ better than you do, even though he or she does not know what you aretrying to do:

要注意你永远都不该自然语言翻译代码。要假设看你代码的人比你更懂C++，即便他或她不知道你的用意：

```
// Now go through the b array and make sure that if i occurs,
// the next element is i+1.
...       // Geez.  What a useless comment.
```

### 2.7 Punctuation, Spelling and Grammar 标点，拼写和语法

Pay attention top unctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.

要注意标点、拼写和语法；写的好的注释要比写的差的更容易阅读。

Comments should be as readable as narrative text, with proper capitalization and punctuation. In many cases, complete sentences are more readable than sentence fragments.Shorter comments, such as comments at the end of a line of code, can sometimes be less formal, but you should be consistent with your style.

注释应该和叙事文本一样可读，有着适当的大小写和标点。在许多情况下，完整的句子要比句子碎片更易阅读。比较短的注释，如在行尾的注释，有时可能不够正式，但你应该和你的风格保持一致。

Although it can be frustrating to have a code reviewer point out that you are using a comma when you should be using a semicolon, it is very important that source code maintain a high level of clarity and readability. Proper punctuation, spelling, and grammar help with that goal.

虽然被别人指出该用分号时却用了逗号多少有些尴尬，但清晰易读的代码还是很重要的。合适的标点、拼写和语法能帮助你实现这一目标。

### 2.8 TODO Comments TODO注释

Use TODO comments for code that is temporary, a short-term solution, or good-enough but not perfect.

将TODO注释用在临时性的、短期解决方案、或足够好但还不完美的代码上。

TODOs should include the string TODO in all caps, followed by the name, e-mail address, or other identifier of the person who can best provide context about the problem referenced by the TODO. A colon is optional. The main purpose is to have aconsistent TODO format that can be searched to find the person who can provide more details upon request. A TODO is not a commitment that the personreferenced will fix the problem. Thus when you create a TODO, it is almost always your name that is given.

TODO注释应该包括全大写的“TODO”，接着是能提供最多信息的人的名字，邮箱地址，或其它个人信息。冒号是可选的。主要目的是能让添加注释的人（或可提供最多信息的人）按统一的TODO格式搜索到。TODO注释不表示相关的人承诺会修复此问题。因此当你新建了一个TODO注释，它给出的总是你的名字。

```
// TODO(kl@gmail.com): Use a "*" herefor concatenation operator.
// TODO(Zeke) change this to use relations.
```

If your TODO is of the form "At a future date do something" make sure that you either include a very specific date ("Fix by November 2005") or a very specific event ("Remove this code when all clients can handle XMLresponses.").

如果你的TODO注释是“未来某时会做某事[^5]”的格式，要确保你要么包括了一个具体的时间（“2005年11月修复”）要么包括具体的事件（“当所有客户端都能处理XML反馈后移除此代码”）。

### 2.9 Deprecation Comments 过期内容的注释

Mark deprecated interface points with DEPRECATED comments.

用DEPRECATED注释来标记过期的接口。

You can mark an interface as deprecated by writing a comment containing the word DEPRECATED inall caps. The comment goes either before the declaration of the interface or onthe same line as the declaration.

你可以通过给某接口加上DEPRECATED的注释来标记其为过期的。可以在接口声明之前注释，也可在同一行注释。

After the word DEPRECATED, write your name, e-mail address, or other identifier in parentheses.

在DEPRECATED单词后的括号里写上你的名字、邮箱或其它个人信息。

A deprecation comment must include simple, clear directions for people to fix their callsites. In C++, you can implement a deprecated function as an inline function that calls the new interface point.

过期内容的注释必须包括简单清晰的用于指导用户修正调用的提示。在C++中，你可以将一个过期的函数实现为内联函数，在其中调用新的接口点。

Marking an interface point DEPRECATED will not magically cause any call sites to change. If you want people to actually stop using the deprecated facility, you will haveto fix the call sites yourself or recruit a crew to help you.

用DEPRECATED标记一个接口不会魔术般的导致任何调用被改变。如果你想要用户真的停止使用过期的设施，你需要自己修复调用或招几个人来帮你。

New code should not contain calls to deprecated interface points. Use the new interface point instead. If you cannot understand the directions, find the person who created the deprecation and ask them for help using the new interface point.

新代码中不应包含对过期接口点的调用。改为使用新接口点。如果你看不懂提示，就找添加了这个过期说明的人，然后请求他帮你使用新接口点。

## 3 Formatting 格式

Coding style and formatting are pretty arbitrary, but a project is much easier to follow if everyone uses the same style. Individuals may not agree with every aspect ofthe formatting rules, and some of the rules may take some getting used to, butit is important that all project contributors follow the style rules so that they can all read and understand everyone\'s code easily.

代码风格与格式确实很随意，但如果所有人都使用同样的风格，项目就能更容易进行。个体可能不同意格式规则中的每一方面，一些规则也可能需要一些时间来适应，但所有的项目成员都遵守相同的风格规则是很重要的，这样他们就可以很容易的看懂每个人的代码了。

To help you format code correctly, we\'ve created a settings file for emacs.

### 3.1 Line Length 行宽

Each line of text in your code should be at most 80 characters long.

你每行代码的文本最多只允许80个字符宽。

We recognize that this rule is controversial, but so much existing code already adheres to it, and we feel that consistency is important.

我们承认这条规则有争议，但有这么多现存的代码已经遵守它了，我们感觉一致性更重要。

Pros:

Those who favor this rule argue that it is rude to force them to resize their windows and there is no need for anything longer. Some folks are used to having several code windows side-by-side, and thus don\'t have room to widen their windows in anycase. People set up their work environment assuming a particular maximum window width, and 80 columns has been the traditional standard. Why change it?

优点：

喜欢这条规则的人主张强迫他们改变编辑器窗口大小很野蛮，而且更长的代码也没什么必要。一些人习惯多个代码窗口挨着排，因此没办法让他们的窗口再宽一点点了。人们都将他们的工作环境设为某个特定的窗口宽度，而80列就是传统的标准。为什么要改变它？

Cons:

Proponents of change argue that a wider line can make code more readable. The 80-column limitis an hide bound throwback to 1960s main frames; modern equipment has widescreens that can easily show longer lines.

缺点：

支持改变此规则的人认为更宽的行能令代码更有可读性。80列的限制可以回溯到古老的1960年代的主机；现代机器有着更宽的屏幕，能轻易的显示更宽的行。

Decision:

结论：

80 characters is the maximum.

80个字符，不能再多了。

Exception: if a comment line contains an example command or a literal URL longer than 80 characters, that line may be longer than 80 characters for ease of cut and paste.

例外：如果注释行包括了一个示例命令或URL的文本超过了80个字符，这行就可以超过80个字符，以便复制剪切。

Exception: an `#include` statement with a long path may exceed 80 columns. Try to avoid situations where this becomes necessary.

例外：`#include`语句如果路径很长的话可能超过80列。试着避免出现这种情况。

Exception: you needn\'t be concerned about header guards that exceed the maximum length.

例外：你不必关心头文件的守卫是否超过了最大长度。

### 3.2 Non-ASCII Characters 非ASCII字符

Non-ASCII characters should be rare, and must use UTF-8 formatting.

要少用非ASCII字符，即使用的话也必须用UTF-8格式。

You shouldn\'t hard-code user-facing text in source, even English, so use of non-ASCII characters should be rare. However, in certain cases it is appropriate to include such words in your code. For example, if your code parses data files from foreign sources, it may be appropriate to hard-code the non-ASCII string(s) used in those data files as delimiters. More commonly, unittest code (which does not need to be localized) might contain non-ASCII strings. In such cases, you should use UTF-8, since that is an encoding understood by most tools able to handle more than just ASCII. Hex encoding is also OK, and encouraged where it enhances readability ― for example, "\xEF\xBB\xBF" is the Unicode zero-width no-break space character, which would be invisible if included in the source as straight UTF-8.

你不应将用户界面文本硬编码进源文件中，即使是英文，这样就不怎么需要用非ASCII字符了。但是，有些场合就适合将非ASCII单词放进代码中。例如，如果你的代码要解析国外来源的数据文件，将在这些文件中充当定界符的非ASCII字符串硬编码可能会比较合适。更常见的情况是单元测试代码（不需要本地化）可能会包含非ASCII字符。这些场合你都应该用UTF-8格式，因为这种编码被大多数能处理不止ASCII这一种编码的工具所支持。16进制编码也可以，在能增强可读性的地方推荐这种编码――例如，“\xEF\xBB\xBF”是Unicode零宽度无间断空格字符，而如果直接按UTF-8格式加进源文件中就看不到这个字符[^6] 了。

### 3.3 Spaces vs.Tabs 空格还是制表符

Use only spaces, and indent 2 spaces at a time.

只使用空格，每次缩进2个空格[^7] 。

We use spaces for indentation. Do not use tabs in your code. You should set your editor to emit spaces when you hit the tab key.

我们用空格进行缩进。不要在你的代码中用tab。你应该将你的编辑器设置为点击tab键时输出空格。

### 3.4 FunctionDeclarations and Definitions 函数声明和定义

Return type on the same line as function name, parameters on the same line if they fit.

返回值类型要与函数名同行，参数名如果合适的话也在同行。

Functions look like this:

像这样的函数：

```cpp
ReturnType ClassName::FunctionName(Typepar_name1, Type par_name2) {
  DoSomething();
  ...
}
```

If you have too much text to fit on one line:

如果你有太多东西写在了同一行：

```cpp
ReturnTypeClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                            Type par_name3) {
  DoSomething();
  ...
}
```

or if you cannot fit even the first parameter:

或如果你连第一个参数都放不进同一行：

```cpp
ReturnTypeLongClassName::ReallyReallyReallyLongFunctionName(
   Type par_name1,  // 4 space indent
   Type par_name2,
   Type par_name3) {
  DoSomething();  // 2 space indent
  ...
}
```

Some points to note:

1.  The return type is always onthe same line as the function name.
2.  The open parenthesis is always on the same line as the function name.
3.  There is never a space between the function name and the open parenthesis.
4.  There is never a space between the parentheses and the parameters.
5.  The open curly brace is always at the end of the same line as the last parameter.
6.  The close curly brace is either on the last line by itself or (if other style rules permit) on the same line asthe open curly brace.
7.  There should be a space between the close parenthesis and the open curly brace.
8.  All parameters should be named, with identical names in the declaration and implementation.
9.  All parameters should bealigned if possible.
10. Default indentation is 2 spaces.
11. Wrapped parameters have a 4 space indent.

一些要记住的要点：

1.  返回值类型总是与函数名在同一行。
2.  开括号[^8] 总要与函数名在同一行。
3.  在函数名与开括号间不要有空格。
4.  在括号和参数间不要有空格。
5.  开的大括号[^9] 总与最后一个参数同行。
6.  闭的大括号可以自己在最后一行或（如果其它规则允许）与开的大括号在同一行。
7.  在闭括号与开大括号间应该有个空格。
8.  所有的参数都要有名字，声明和实现中的名字要相同。
9.  如果可能，所有参数都应该对齐。
10. 默认缩进是2个空格。
11. 换行后的参数有4个空格的缩进。

If someparameters are unused, comment out the variable name in the functiondefinition:

如果一些参数没被用到，在函数定义处将参数名注释起来。

```cpp
// Always have named parameters ininterfaces.
class Shape {
 public:
  virtual void Rotate(double radians) = 0;
}

// Always have named parameters in thedeclaration.
class Circle : public Shape {
 public:
  virtual void Rotate(double radians);
}

// Comment out unused named parameters indefinitions.
void Circle::Rotate(double /*radians*/) {}

// Bad - if someone wants to implementlater, it's not clear what the
// variable means.
void Circle::Rotate(double) {}
```

### 3.5 FunctionCalls 函数调用

On one line ifit fits; otherwise, wrap arguments at the parenthesis.

尽量放在同一行，否则，将实参封装在圆括号中。

Function calls have the following format:

函数调用遵循下面的格式：

bool retval = DoSomething(argument1,argument2, argument3);

If the arguments do not all fit on one line, they should be broken up onto multiple lines, with each subsequent line aligned with the first argument. Do not add spaces after the open paren or before the close paren:

如果实参放不进一行，就将它们分成多行，分出的每行都要和第一个参数对齐。不要在开括号后和闭括号前加空格：

````cpp
bool retval = DoSomething(averyveryveryverylongargument1,
                          argument2,argument3);
````

If the function has many arguments, consider having one per line if this makes the code more readable:

如果函数有很多参数，考虑每行写一个参数，可以增强可读性：

```cpp
bool retval = DoSomething(argument1,
                          argument2,
                          argument3,
                          argument4);
```

If the function signature is so long that it cannot fit within the maximum line length, you may place all arguments on subsequent lines:

如果函数原型太长，以至于超过了行的最大长度，你可以将所有参数独立成行：

```cpp
if (...) {
  ...
  ...
  if(...) {
   DoSomethingThatRequiresALongFunctionName(
       very_long_argument1,  // 4 spaceindent
       argument2,
       argument3,
       argument4);
  }
```

### 3.6 Conditionals 条件语句

Prefer no spaces inside parentheses. The else keyword belongs on a new line.

建议括号内没有空格。else关键字放在新行中。

There are two acceptable formats for a basic conditional statement. One includes spacesbetween the parentheses and the condition, and one does not.

有两种基本的条件语句格式都可使用。一种在括号和条件式之间有空格，另一种没有。

The most common form is without spaces. Either is fine, but be consistent. If you are modifyinga file, use the format that is already present. If you are writing new code,use the format that the other files in that directory or project use. If indoubt and you have no personal preference, do not add the spaces.

最常见的格式是没有空格的。用哪种都可以，但要保持一致。如果你修改一个文件，就用当前的格式。如果你在写新代码，用项目或目录中其它文件的格式。如果不知道用哪个，你也没有个人倾向的话，不要加空格。

````cpp
if (condition) {  // no spaces inside parentheses
  ...  // 2 space indent.
} else if (...) {  // The else goes on the same line as theclosing brace.
  ...
} else {
  ...
}
````

If you prefer you may add spaces inside the parentheses:

如果你喜欢的话，也可以在括号与条件式之间加空格：

````cpp
if ( condition ) {  // spaces inside parentheses - rare
  ...  // 2 space indent.
} else { // The else goes on the same line as the closing brace.
  ...
}
````

Note that in all cases you must have a space between the if and the open parenthesis. You must also have a space between the close parenthesis and the curly brace, if you\'re using one.

注意任何情况下你都要在if和开括号间放一个空格。你也必须在闭括号和大括号间放空格。

```cpp
if(condition)     // Bad - space missing after IF.
if (condition){   // Bad - space missing before {.
if(condition){    // Doubly bad.

if (condition) {  // Good - proper space after IF and before {.
```

Short conditional statements may be written on one line if this enhances readability. You may use this only when the line is brief and the statement does not use theelse clause.

短的条件语句也可以写在同一行内，如果不影响可读性的话。只有在行很短且没有else分句时才能这么用。

```cpp
if (x == kFoo) return new Foo();
if (x == kBar) return new Bar();
```

This is not allowed when the if statement has an else:

如果if语句包含else的话不许如下这么用：

```cpp
// Not allowed - IF statement on one linewhen there is an ELSE clause
if (x) DoThis();
else DoThat();
```

In general, curly braces are not required for single-line statements, but they are allowed if you like them; conditional or loop statements with complex conditions or statements may be more readable with curly braces. Some projects require that an if must always always have an accompanying brace.

通常开的大括号不需要单独一行，但你喜欢的话也可以；有着复杂的条件或状态的条件语句和循环语句后面跟大括号的话，可能会更有可读性。一些项目要求if后面必须跟着大括号。

```cpp
if (condition)
  DoSomething();  // 2 space indent.

if (condition) {
  DoSomething();  // 2 space indent.
}
```

However, if one part of an if-else statement uses curly braces, the other part must too:

但是，如果if-else语句中的一部分用大括号了，另一部分也必须用：

```cpp
// Not allowed - curly on IF but not ELSE
if (condition) {
  foo;
} else
  bar;

// Not allowed - curly on ELSE but not IF
if (condition)
  foo;
else {
  bar;
}

// Curly braces around both IF and ELSErequired because
// one of the clauses used braces.
if (condition) {
  foo;
} else {
  bar;
}
```

### 3.7 Loops andSwitch Statements 循环和switch语句

Switch statements may use braces for blocks. Empty loop bodies should use {} or continue.

switch语句可以用大括号来分段。空循环体应该用{}或continue。

case blocks in switch statements can have curly braces or not, depending on your preference. If you do include curly braces they should be placed as shown below.

switch的case块可以用大括号包起来，也可以不用，取决于你的喜好。如果你引入大括号了，应该参照下面的用法。

If not conditional on an enumerated value, switch statements should always have adefault case (in the case of an enumerated value, the compiler will warn you if any values are not handled). If the default case should never execute, simply assert:

如果有不满足case条件的枚举值，switch语句应该总是包含一个默认case块（如果有输入值没有case条件去处理，编译器会警告）。如果默认case永远都不该执行，就放一个assert。

```cpp
switch (var) {
  case0: {  // 2 space indent
    ...     // 4 space indent
    break;
  }

  case1: {
   ...
   break;
  }

  default: {
    assert(false);
  }
}
```

Empty loop bodies should use {} or continue, but not a single semicolon.

空的循环体应该用{}或continue，而不是单独的一个分号。

```
while (condition) {
  // Repeat test until it returns false.
}

for (int i = 0; i < kSomeNumber; ++i){}  // Good - empty body.
while (condition) continue;  // Good - continue indicates no logic.

while (condition);  // Bad - looks like part of do/while loop.
```

### 3.8 Pointerand Reference Expressions 指针和引用表达式

No spaces around period or arrow. Pointer operators do not have trailing spaces.

在句点和箭头前后没有空格。指针操作符后面没有尾随的空格。

The following are examples of correctly-formatted pointer and reference expressions:

下面是格式正确的指针和引用表达式：

```cpp
x = *p;
p = &x;
x = r.y;
x = r->y;
```

Note that:

1.    There are no spaces around the period or arrow when accessing a member.
2.    Pointer operators have no space after the * or &.

注意：

1.    在访问成员时，句点和箭头的前后没有空格。
2.    指针操作符中*和&后面没有空格。

When declaring a pointer variable or argument, you may place the aste risk adjacent to either the type or to the variable name:

当声明指针变量或参数时，星号可以挨着类型也可以挨着变量名：

```cpp
// These are fine, space preceding.
char *c;
const string &str;

// These are fine, space following.
char* c;   // but remember to do "char* c, *d, *e, ...;"!
const string& str;

char * c; // Bad - spaces on both sides of *
const string & str;  // Bad - spaces on both sides of &
```

You should do this consistently within a single file, so, when modifying an existing file, use the style in that file.

你应该在同一个文件中保持一致，所以在修改一个已有的文件时，用文件原有的风格。

### 3.9 Boolean Expressions 布尔表达式

When you have a boolean expression that is longer than the standard line length, be consistent in how you break up the lines.

如果一个布尔表达式比标准行宽还要长，你要像其它情况一样将它分成多行。

In this example, the logical AND operator is always at the end of the lines:

这个例子中，与操作符总是在行尾[^10] ：

```cpp
if (this_one_thing > this_other_thing&&
   a_third_thing == a_fourth_thing &&
   yet_another && last_one) {
   ...
}
```

Note that when the code wraps in this example, both of the && logical AND operators are at the end of the line. This is more common in Google code, though wrapping all operators at the beginning of the line is also allowed. Feel free to insert extra parentheses judiciously because they can be very helpful in increasing readability when used appropriately. Also note that you should always use the punctuation operators, such as && and ~, rather than the word operators, such as and and compl.

注意到本例中代码被分成多行，其中的&&操作符都在行尾。尽管也可以将所有操作符都对齐到行首，本例中的用法在谷歌的代码中更常见。这样可以方便插入括号，适当使用对提升可读性很有帮助。同样注意，你应该总是用符号表示的操作符，如&&和~，而不是用单词表示[^11] ，如and和compl。

### 3.10 ReturnValues 返回值

Do not needlessly surround the return expression with parentheses.

不要用不必要的括号括起返回表达式。

Use parentheses in return expr; only where you would use them in x = expr;.

返回表达式expr只有在令它为赋值式时会引起歧义的地方才能用括号括起：

```cpp
return result;                  // No parentheses in thesimple case.简单场合不用括号
return (some_long_condition &&  // Parentheses ok to make a complex复杂表达式用括号可读性更好
        another_condition);     //     expression more readable.

return (value);                // You wouldn't write var = (value);你不会写var=(value)这样的式子的[^12] ！
return(result);                // return is not a function!return不是个函数！
```

### 3.11 Variableand Array Initialization 变量和数组初始化

Your choice of = or ().

可以用=也可以用()。

You may choosebetween = and (); the following are all correct:

你可以在=和()中选一种形式[^13] ；下面的例子都是正确的：

```
int x = 3;
int x(3);
string name("Some Name");
string name = "Some Name";
```

### 3.12 PreprocessorDirectives 预处理指令

The hash mark that starts a preprocessor directive should always be at the beginning of the line.

预处理指令应该总在行首，不要缩进。

Even when preprocessor directives are within the body of indented code, the directives should start at the beginning of the line.

即使预处理指令位于缩进的代码块中，它们也不缩进而是总在行首。

```cpp
// Good - directives at beginning of line
  if (lopsided_score) {
#if DISASTER_PENDING      // Correct -- Starts at beginning of line
    DropEverything();
#if NOTIFY                // OK but not required -- Spacesafter #可以但不需要#后面有空格
    NotifyClient();
#endif
#endif
    BackToNormal();
  }

// Bad - indented directives
  if (lopsided_score) {
  #if DISASTER_PENDING  //Wrong!  The "#if" should be at beginning of line
    DropEverything();
  #endif                //Wrong!  Do not indent "#endif"
    BackToNormal();
  }
```

### 3.13 ClassFormat 类格式

Sections in public, protected and private order, each indented one space.

类中各部分按public、protected和private的顺序，每个关键字缩进1个空格。

The basic formatfor a class declaration (lacking the comments, see Class Comments for a discussion of what comments are needed) is:

类声明的基本格式（省略了注释）是：

```cpp
class MyClass : public OtherClass {
  public:     // Note the 1 space indent!
  MyClass();  // Regular 2 spaceindent.
  explicit MyClass(int var);
  ~MyClass() {}

  voidSomeFunction();
  voidSomeFunctionThatDoesNothing() {

  }

  voidset_some_var(int var) { some_var_ = var; }
  intsome_var() const { return some_var_; }

 private:
  boolSomeInternalFunction();
  intsome_var_;
  intsome_other_var_;
 DISALLOW_COPY_AND_ASSIGN(MyClass);
};
```

Things to note:

1.    Any base class name should beon the same line as the subclass name, subject to the 80-column limit.
2.    The public:, protected:, andprivate: keywords should be indented one space.
3.    Except for the first instance,these keywords should be preceded by a blank line. This rule is optional in small classes.
4.    Do not leave a blank line afterthese keywords.
5.    The public section should be first, followed by the protected and finally the private section.
6.    See Declaration Order for rules on ordering declarations within each of these sections.

注意事项：

1.    任何基类的名字都应与子类名字在同一行，遵循80列宽的限制。
2.    public、protected、private关键字应该缩进1个空格。
3.    除了第一个出现的关键字，其后的关键字前面应该有个空行。此规则对于较小的类是可选的。
4.    不要在这些关键字后留空行。
5.    public段应在最前，其后是protected段，最后是private段。

### 3.14 Constructor Initializer Lists 构造函数初始化列表

Constructor initializer lists can be all on one line or with subsequent lines indented four spaces.

构造函数初始化列表可以都放在一行中也可以分成多行，每行缩进4个空格。

There are two acceptable formats for initializer lists:

初始化列表有两种可选格式：

```cpp
// When it all fits on one line:
MyClass::MyClass(int var) : some_var_(var),some_other_var_(var + 1) {}
```

or

或

```cpp
// When it requires multiple lines, indent 4spaces, putting the colon on
// the first initializer line:
MyClass::MyClass(int var)
    :some_var_(var),             // 4 spaceindent
     some_other_var_(var + 1) {  // lined up
  ...
  DoSomething();
  ...
}
```

### 3.15 NamespaceFormatting 命名空间格式

The contents of namespaces are not indented.

命名空间的内容不缩进。

Namespaces donot add an extra level of indentation. For example, use:

命名空间不会增加一层缩进。例如：

```cpp
namespace {
void foo() { // Correct.  No extra indentationwithin namespace.
  ...
}
}  // namespace
```

Do not indentwithin a namespace:

命名空间内不要缩进：

```cpp
namespace {
  // Wrong.  Indented when it should not be.
  void foo() {
    ...
  }
}  // namespace
```

When declaring nested namespaces, put each namespace on its own line.

声明嵌套命名空间时，每个命名空间单独一行。

```cpp
namespace foo {
namespace bar {
```

### 3.16 Horizontal Whitespace 水平留白

Use of horizontal whitespace depends on location. Never put trailing whitespace at the end of aline.

分情况使用水平留白。永远不要在行尾放空格。

**General 通常情况**

```cpp
void f(bool b) {  // Open braces should always have a spacebefore them.开括号前应该有一个空格
  ...
int i = 0; // Semicolons usually have no space before them.分号前通常没有空格
int x[] = { 0 };  // Spaces inside braces for array initialization are数组初始化时括号内的空格可选
int x[] = {0};    // optional. If you use them, put them on both sides!用的时候要两边都加空格
// Spaces around the colon in inheritanceand initializer lists.继承和初始化列表中的冒号前后要有空格

class Foo : public Bar {
 public:
  //For inline function implementations, put spaces between the braces
  //and the implementation itself.内联函数的实现中，要在括号和实现本身前都加空格
  Foo(int b) : Bar(), baz_(b) {}  //No spaces inside empty braces.空括号内没有空格
  voidReset() { baz_ = 0; }  // Spacesseparating braces from implementation.空格分开了括号和实现
  ...
```

Adding trailing whitespace can cause extra work for others editing the same file, when they merge, as can removing existing trailing whitespace. So: Don\'t introducetrailing whitespace. Remove it if you\'re already changing that line, or do itin a separate clean-up operation (preferably when no-one else is working on the file).

添加冗余的留白会给其他人编辑时造成额外负担，合并行时还需要去除多余的空格。所以：不要引入多余的留白。如果你已经改变完成一行后就去掉行尾的空格，或进行单独的清理操作（推荐在没人使用此文件时进行）。

**Loops and Conditionals 循环和条件语句**

```cpp
if (b) {          // Space after the keyword inconditions and loops.循环和条件句的关键字后有空格

} else {          // Spaces around else. else前后要有空格

}

while (test) {}   // There is usually no space insideparentheses. while的括号里通常没空格
switch (i) {
for (int i = 0; i < 5; ++i) {
switch ( i ) {    // Loops and conditions may have spacesinside 循环和条件句内可以有空格，但很罕见
if ( test ) {     // parentheses, but this is rare.  Be consistent.
for ( int i = 0; i < 5; ++i ) {
for ( ; i < 5 ; ++i) {  // For loops always have a space after thefor循环的分号后总有空格，分号前
  ...                   //semicolon, and may have a space before the 可以有空格
                        // semicolon.

for (auto x : counts) {  // Range-based for loops always have a 基于范围的for循环的冒号前后都有空格
  ...                    // spacebefore and after the colon.
}

switch (i) {
  case1:         // No space before colon in aswitch case. case条件中的冒号前没空格
   ...
  case2: break;  // Use a space after a colonif there's code after it.
```

冒号后有代码时要有1个空格

**Operators 操作符**

```cpp
x = 0;              // Assignment operators alwayshave spaces around 赋值符前后要有空格
                    // them.
x = -5;             // No spaces separating unaryoperators and their
```

单独的单目操作符和参数间没有空格

```cpp
++x;                // arguments.
if (x && !y)
  ...
v = w * x + y / z;  // Binary operators usually have spacesaround them,
```

双目操作符前后通常有空格

```cpp
v = w*x + y/z;      // but it's okay to remove spaces aroundfactors.
```

但在运算符前后可以去掉空格

```cpp
v = w * (x + z);    // Parentheses should have no spaces insidethem. 括号内侧不应有空格
```

**Templates and Casts 模板和转换**

```
vector<string> x;           // No spaces inside the angle 角括号内侧没有空格
y = static_cast<char*>(x);  // brackets (< and >), before 角括号和圆括号间没有空格
                            // <, or between>( in a cast.
vector<char *> x;           // Spaces between type and pointer are
```

类型和星号间可以有空格，但要保持一致

```
                            // okay, but beconsistent.
set<list<string>> x;        // Permitted in C++11 code. C++11中允许此代码
set<list<string> > x;       // C++03 required a space in >>.C++03中需要在>>中插入空格[^14]
set< list<string> > x;      // You may optionally use 此时你也可以对称的在前面也加个空格
                            // symmetricspacing in < <.
```

### 3.17 VerticalWhitespace 垂直留白

Minimize use of vertical whitespace.

尽量少用垂直留白。

This is more a principle than a rule: don\'t use blank lines when you don\'t have to. In particular, don\'t put more than one or two blank lines between functions, resist starting functions with a blank line, don\'t end functions with a blankline, and be discriminating with your use of blank lines inside functions.

这不仅仅是规则而是原则问题：不必要的时候不要用空行。尤其是不要在函数间留超过一到两个空格，函数首尾不要留空行，函数中也要谨慎使用空行。

The basic principle is: The more code that fits on one screen, the easier it is to follow and understand the control flow of the program. Of course, readability can suffer from code being too dense as well as too spread out, so use your judgement. But in general, minimize use of vertical whitespace.

基本原则是：同一屏幕内能显示的代码越多，理解掌握程序的控制流越容易。当然，思路过分发散，导致代码过于密集，也会导致可读性下降，所以需要你自己把握。但通常来说要尽量少用垂直留白。

Some rules ofthumb to help when blank lines may be useful:

1.    Blank lines at the beginning or end of a function very rarely help readability.
2.    Blank lines inside a chain of if-else blocks may well help readability.

使用空行的一些经验法则：

1.    函数首尾的空行对提高可读性没有帮助。
2.    if-else链中各块间的空行可能会对此有帮助。

## 4 Exceptions to the Rules 规则的例外

The coding conventions described above are mandatory. However, like all good rules, these sometimes have exceptions, which we discuss here.

上面叙述的代码习惯是强制性的。但是，像所有的良好规则一样，这些规则有时也有例外，此处就讨论这些例外。

### 4.1 Existing Non-conformant Code现有不合规范的代码

You may diverge from the rules when dealing with code that does not conform to this styleguide.

在处理不符合本风格规范的代码时，你可以不遵守上面的规则。

If you find yourself modifying code that was written to specifications other than those presented by this guide, you may have to diverge from these rules in order to stay consistent with the local conventions in that code. If you are in doubt about how to do this, ask the original author or the person currently responsible for the code. Remember that consistency includes local consistency,too.

如果你在修改不符合本规范的代码时，你可能需要放弃这些规则，来和代码中原有的习惯保持一致。如果你困惑该怎么做，就去问原作者或当前负责此代码的人。记得要保持局部一致性。

### 4.2 Windows Code Windows代码

Windows programmers have developed their own set of coding conventions, mainly derived from the conventions in Windows headers and other Microsoft code. We want tomake it easy for anyone to understand your code, so we have a single set of guidelines for everyone writing C++ on any platform.

Windows程序员已经发展出了他们自己的编程习惯，主要源于Windows头文件和其它微软代码中的习惯。我们想让任何人都能顺利理解你的代码，所以我们为在任何平台写C++代码的人都准备了一个单独的规范集合。

It is worth reiteratinga few of the guidelines that you might forget if you are used to the prevalent Windows style:

1.    Do not use Hungarian notation (for example, naming an integer iNum). Use the Google naming conventions, including the .cc extension for source files.
2.    Windows defines many of its ownsynonyms for primitive types, such as DWORD, HANDLE, etc. It is perfectly acceptable, and encouraged, that you use these types when calling Windows API functions. Even so, keep as close as you can to the underlying C++ types. Forexample, use const TCHAR * instead of LPCTSTR.
3.    When compiling with Microsoft Visual C++, set the compiler to warning level 3 or higher, and treat allwarnings as errors.
4.    Do not use `#pragma once;` instead use the standard Google include guards. The path in the include guards should be relative to the top of your project tree.
5.    In fact, do not use any nonstandard extensions, like `#pragma` and `__declspec`, unless you absolutely must. Using `__declspec(dllimport)` and `__declspec(dllexport)` is allowed; however, you must use them through macros such as DLLIMPORT and DLLEXPORT, sothat someone can easily disable the extensions if they share the code.

如果你习惯了通行的Windows风格，就很有必要重申一些你可能忘记的规范：

1.    不要用匈牙利命名法（例如将整数命名为iNum）。用谷歌的命名规范，源代码文件扩展名用.cc。
2.    Windows定义了许多它独有的内置类型的别名，如DWORD和HANDLE等等。在你调用Windows API时鼓励用这些类型。即使这样，你也应该尽量使用C++的类型名。例如，用constTCHAR*去替代LPCTSTR。
3.    用VC++编译代码时，将警告等级调到3或更高，并将所有警告都视作错误。
4.    不要用`#pragma once`；改用标准的头文件守卫规则。在`#define`中的路径要相对于项目根目录。
5.    事实上不要用任何不标准的编译器扩展，如`#pragma`和`__declspec`，除非你必须得这么做。用`__declspec(dllimport)`和`__declspec(dllexport)`是允许的；但你必须通过宏来调用它们，如DLLIMPORT和DLLEXPORT， 这样别人就可以在分享使用此代码时方便的禁用这些扩展了。

However, there are just a few rules that we occasionally need to break on Windows:

1.    Normally we forbid the use of multiple implementation inheritance; however, it is required when using COM andsome ATL/WTL classes. You may use multiple implementation inheritance to implement COM or ATL/WTL classes and interfaces.
2.    Although you should not use exceptions in your own code, they are used extensively in the ATL and some STLs, including the one that comes with Visual C++. When using the ATL, youshould define `_ATL_NO_EXCEPTIONS` to disable exceptions. You should investigate whether you can also disable exceptions in your STL, but if not, it is OK toturn on exceptions in the compiler. (Note that this is only to get the STL to compile. You should still not write exception handling code yourself.)
3.    The usual way of working with precompiled headers is to include a header file at the top of each source file, typically with a name like StdAfx.h or precompile.h. To make your code easier to share with other projects, avoid including this file explicitly (except inprecompile.cc), and use the /FI compiler option to include the fileautomatically.
4.    Resource headers, which areusually named resource.h and contain only macros, do not need to conform tothese style guidelines.

但是，在Windows中还是有些场合我们必须打破某些规则：

1.    通常我们禁止使用多个有实现的继承；但在用COM和一些ATL/WTL类时需要这么做。这时你就可以使用多个有实现的继承了。
2.    尽管你不应该在自己的代码中用到异常，但异常被广泛用在ATL和一些VC++的STL实现中。用ATL时，你应该定义`_ATL_NO_EXCEPTIONS`来禁用异常。你应该研究一下是否也可以禁用STL中的异常，如果不能的话启用异常也没关系。（注意这只是为了编译STL，自己的代码中仍然不允许用异常。）
3.    Windows代码文件中通常都包括预编译好的头文件StdAfx.h或precompile.h。为了让你的代码方便与其它项目分享，避免显式include此文件（除了precompile.cc），用/FI编译选项来自动包括此文件。
4.    资源头文件通常被命名为resource.h且只包括宏，不需要遵守这些风格规范。

## 5 Parting Words 结束语

Use common senseand BE CONSISTENT.

运用常识，并**保持一致**。

If you are editing code, take a few minutes to look at the code around you and determineits style. If they use spaces around their if clauses, you should, too. If their comments have little boxes of stars around them, make your comments have little boxes of stars around them too.

如果你在编辑代码，花一些时间看看周围的代码再决定用哪种风格。如果它们在if分句前后留有空白，你也应该这么做。如果它们的注释用星号组成的矩形框包起来，你也这么做。

The point of having style guidelines is to have a common vocabulary of coding so people can concentrate on what you are saying, rather than on how you are saying it. Wepresent global style rules here so people know the vocabulary. But local styleis also important. If code you add to a file looks drastically different from the existing code around it, the discontinuity throws readers out of their rhythm when they go to read it. Try to avoid this.

风格指南的重点是提供一个通用的编程规范，这样人们就可以专注于实现内容，而不是表达方式。我们展示了全局的风格，但局部风格也很重要。如果你加进一个文件的代码与原有代码完全不同，这种不连续会破坏读者阅读的节奏。试着避免这种情况。

OK, enough writing about writing code; the code itself is much more interesting. Have fun!

好吧，关于编程规范写的够多了；代码本身更有趣。尽情享受吧！

* * *

## 脚注

[^1]: 但一行超过80个字符后还是要分行的

[^2]: vector.size()

[^3]: 我的理解是会给程序引入一些数据或主动的改变程序状态的代码，不是验证性的

[^4]: 注释要言简意赅, 不要拖沓冗余

[^5]: TODO 很不错, 有时候, 注释确实是为了标记一些未完成的或完成的不尽如人意的地方, 这样一搜索, 就知道还有哪些活要干, 日志都省了

[^6]: 意思是用UTF-8就只会看到一个空格，就丢失了16进制能表现的含义了？

[^7]: 这条其实不太能接受，看看别的规范怎么说

[^8]: 指左括号，右括号可能因为放不下在别的行

[^9]: 指左大括号

[^10]: 为了避免读者漏掉&&，还能让后面各行看着没那么别扭

[^11]: 用宏实现，应该是来自basic和pascal的习惯

[^12]: 意思就是不要这么用

[^13]: 推荐用()进行初始化，对于类对象，如果用=相当于是构造函数+赋值函数两项的开销

[^14]: 避免被识别为>>操作符

