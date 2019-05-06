---
typora-root-url: ../
title: "Java | 语言基础"
categories: "technology"
tags:
  - java
---


Java 系列将从：Java语言基础，JVM，并发编程三方面从介绍到深入理解Java。本文是该系列的语言基础篇。

---

## Java基础知识

- [Java入门教程](https://www.tutorialspoint.com/java/index.htm)  
- [JDK源码](http://grepcode.com/snapshot/repository.grepcode.com/java/root/jdk/openjdk/8-b132/)  

- 开发环境教程：[IntelliJ IDEA 使用教程](http://wiki.jikexueyuan.com/project/intellij-idea-tutorial/)  

### 字符串String、StringBufer、StringBuilder区别

#### String

String是典型的Immutable类，被声明成为final class，所有属性也都是final的。也由于它的不可变性，类似拼接、裁剪字符串等动作，都会产生新的String对象。

- String的创建机理

  由于String在Java世界中使用过于频繁，Java为了避免在一个系统中产生大量的String对象，引入了字符串常量池。其运行机制是:创建一个字符串时，首先检查池中是否有值相同的字符串对 象，如果有则不需要创建直接从池中刚查找到的对象引用;如果没有则新建字符串对象，返回对象引用，并且将新创建的对象放入池中。但是，通过new方法创建的String对象是不检查字符串 池的，而是直接在堆区或栈区创建一个新的对象，也不会把对象放入池中。上述原则只适用于通过直接量给String对象引用赋值的情况。 

  ```java
  String str1 = "123"; //通过直接量赋值方式，放入字符串常量池
  String str2 = new String(“123”);//通过new方式赋值方式，不放入字符串常量池
  ```

- String的特性
  - 不可变。是指String对象一旦生成，则不能再对它进行改变。不可变的主要作用在于当一个对象需要被多线程共享，并且访问频繁时，可以省略同步和锁等待的时间，从而大幅度提高系统性能。不可变模式是一个可以提高多线程程序的性能，降低多线程程序复杂度的设计模式。

  - 针对常量池的优化。当2个String对象拥有相同的值时，他们只引用常量池中的同一个拷贝。当同一个字符串反复出现时，这个技术可以大幅度节省内存空间。 

#### StringBuffer/StringBuilder

StringBuffer/StringBuilder是为解决拼接产生太多中间对象的问题而提供的类。

StringBuffer和StringBuilder都实现了AbstractStringBuilder抽象类，拥有几乎一致对外提供的调用接口；其底层在内存中的存储方式与String相同，都是以一个有序的字符序列(char类型的数组)进行存储，不同点是StringBuffer/StringBuilder对象的值是可以改变的，并且值改变以后，对象引用不会发生改变;两者对象在构造过程中，首先按照默认大小申请一个字符数组，由于会不断加入新数据，当超过默认大小后，会创建一个更大的数组，并将原先的数组内容复制过来，再丢弃旧的数组。因此，对于较大对象的扩容会涉及大量的内存复制操作，如果能够预先评估大小，可提升性能。 

唯一需要注意的是:StringBufer是线程安全的，但是StringBuilder是线程不安全的。可参看Java标准类库的源代码，StringBufer类中方法定义前面都会有synchronize关键字。为此，StringBufer的性能要远低于StringBuilder。 

|               | 底层                                   | 接口                              | 扩容                         |                                   |
| ------------- | -------------------------------------- | --------------------------------- | ---------------------------- | --------------------------------- |
| String        | 不可变的char类型的数组                 |                                   |                              |                                   |
| StringBuffer  | 可变的char类型的数组（java9 byte类型） | 实现了AbstractStringBuilder抽象类 | 创建一个更大的数组，复制数据 | 方法定义前有synchronized 线程安全 |
| StringBuilder | 可变的char类型的数组（java9 byte类型） | 实现了AbstractStringBuilder抽象类 | 创建一个更大的数组，复制数据 | 线程不安全                        |



#### 应用场景

- 在字符串内容不经常发生变化的业务场景优先使用String类。例如：常量声明、少量的字符串拼接操作等。如果有大量的字符串内容拼接，避免使用String与String之间的“+”操作，因为这样会产生大量无用的中间对象，耗费空间且执行效率低下(新建对象、回收对象花费大量时间)。
- 在频繁进行字符串的运算(如拼接、替换、删除等)，并且运行在多线程环境下，建议使用StringBufer，例如XML解析、HTTP参数解析与封装。 
- 在频繁进行字符串的运算(如拼接、替换、删除等)，并且运行在单线程环境下，建议使用StringBuilder，例如SQL语句拼装、JSON封装等。 



### 原始数据类型和boxed类型

Java的8个原始数据类型(Primitive Types，boolean、byte 、short、char、int、foat、double、long)

#### 理解自动装箱、拆箱

自动装箱实际上算是一种语法糖。javac替我们自动把装箱转换为Integer.valueOf() ，把拆箱替换为Integer.intValue() ，这似乎这也顺道回答了另一个问题，既然调用的是Integer.valueOf ， 自然能够得到缓存的好处啊。 

这种缓存机制并不是只有Integer才有，同样存在于其他的一些包装类，比如: 

- Boolean，缓存了true/false对应实例，确切说，只会返回两个常量实例Boolean.TRUE/FALSE。
- Short，同样是缓存了-128到127之间的数值。
- Byte，数值有限，所以全部都被缓存。 
- Character，缓存范围'\u0000' 到 '\u007F'。 

#### 原始类型线程安全

- 原始数据类型的变量，显然要使用并发相关手段，才能保证线程安全，这些我会在专栏后面的并发主题详细介绍。如果有线程安全的计算需要，建议考虑使用类 似AtomicInteger、AtomicLong这样的线程安全类。 

- 部分比较宽的数据类型，比如foat、double，甚至不能保证更新操作的原子性，可能出现程序读取到只更新了一半数据位的数值

#### 原始数据类型和引用类型局限性 

再从Java平台发展的角度来看看，原始数据类型、对象的局限性和演进。 

- 原始数据类型和Java泛型并不能配合使用

  这是因为Java的泛型某种程度上可以算作伪泛型，它完全是一种编译期的技巧，Java编译期会自动将类型转换为对应的特定类型，这就决定了使用泛型，必须保证相应类型可以转换为Object。 无法高效地表达数据，也不便于表达复杂的数据结构，比如vector和tuple 

- 我们知道Java的对象都是引用类型，如果是一个原始数据类型数组，它在内存里是一段连续的内存，而对象数组则不然，数据存储的是引用，对象往往是分散地存储在堆的不同位置。这种设计虽然带来了极大灵活性，但是也导致了数据操作的低效，尤其是无法充分利用现代CPU缓存机制。 

- Java为对象内建了各种多态、线程安全等方面的支持，但这不是所有场合的需求，尤其是数据处理重要性日益提高，更加高密度的值类型是非常现实的需求。 

## Java集合框架

**Java集合框架(Java collections framework, JCF)**([参考这里](https://en.wikipedia.org/wiki/Java_collections_framework))用来表示和操作集合的统一框架，它包含接口，实现类以及一些编程辅助算法，具体位于`java.util`包下。集合框架示意图如下(实际远比下图复杂)，图片来源于[这里](https://www.cnblogs.com/nayitian/p/3266090.html)

![Alt Text](/images/java/collections-framework-overview_thumb.png )

常用的集合类:

> `ArrayList` `LinkedList` `HashMap` `LinkedHashMap` `TreeMap` `HashSet` `LinkedHashSet` `TreeSet`

线程安全的集合类。`java.util.concurrent.*`包含许多线程安全、测试良好、高性能的并发构建块，目的就是要实现 Collection 框架对数据结构所执行的并发操作，性能优于`java.util.*`中的集合类：
> `ConcurrentHashMap` `CopyOnWriteArrayList` `CopyOnWriteArraySet` `ConcurrentLinkedDeque` `ConcurrentLinkedQueue` `ConcurrentSkipListMap` `ConcurrentSkipListSet`

> `Vector` `Collections.synchronizedCollection(...)` `Collections.synchronizedList(List)` `Collections.synchronizedMap(Map)` `Collections.synchronizedSet(Set)`  `Collections.synchronizedSortedSet(Set)` 

### ArrayList/Vector 的底层分析

#### ArrayList

`ArrayList` 实现于 `List`、`RandomAccess` 接口。可以插入空数据，也支持随机访问。

`ArrayList `相当于动态数组，其中最重要的两个属性分别是:
`elementData` 数组，以及 `size` 大小。
在调用 `add()` 方法的时候：

```java
    public boolean add(E e) {
        ensureCapacityInternal(size + 1);  // Increments modCount!!
        elementData[size++] = e;
        return true;
    }
```

- 首先进行扩容校验。
- 将插入的值放到尾部，并将 size + 1 。

如果是调用 `add(index,e)` 在指定位置添加的话：
```java
    public void add(int index, E element) {
        rangeCheckForAdd(index);

        ensureCapacityInternal(size + 1);  // Increments modCount!!
        //复制，向后移动
        System.arraycopy(elementData, index, elementData, index + 1,
                         size - index);
        elementData[index] = element;
        size++;
    }
```


- 也是首先扩容校验。
- 接着对数据进行复制，目的是把 index 位置空出来放本次插入的数据，并将后面的数据向后移动一个位置。

其实扩容最终调用的代码:
```java
    private void grow(int minCapacity) {
        // overflow-conscious code
        int oldCapacity = elementData.length;
        int newCapacity = oldCapacity + (oldCapacity >> 1);
        if (newCapacity - minCapacity < 0)
            newCapacity = minCapacity;
        if (newCapacity - MAX_ARRAY_SIZE > 0)
            newCapacity = hugeCapacity(minCapacity);
        // minCapacity is usually close to size, so this is a win:
        elementData = Arrays.copyOf(elementData, newCapacity);
    }
```

也是一个数组复制的过程。

由此可见 `ArrayList` 的主要消耗是数组扩容以及在指定位置添加数据，在日常使用时最好是指定大小，尽量减少扩容。更要减少在指定位置插入数据的操作。


由于 ArrayList 是基于动态数组实现的，所以并不是所有的空间都被使用。因此使用了 `transient` 修饰，可以防止被自动序列化。

```java
transient Object[] elementData;
```

因此 ArrayList 自定义了序列化与反序列化：

```java
    private void writeObject(java.io.ObjectOutputStream s)
        throws java.io.IOException{
        // Write out element count, and any hidden stuff
        int expectedModCount = modCount;
        s.defaultWriteObject();

        // Write out size as capacity for behavioural compatibility with clone()
        s.writeInt(size);

        // Write out all elements in the proper order.
        //只序列化了被使用的数据
        for (int i=0; i<size; i++) {
            s.writeObject(elementData[i]);
        }

        if (modCount != expectedModCount) {
            throw new ConcurrentModificationException();
        }
    }

    private void readObject(java.io.ObjectInputStream s)
        throws java.io.IOException, ClassNotFoundException {
        elementData = EMPTY_ELEMENTDATA;

        // Read in size, and any hidden stuff
        s.defaultReadObject();

        // Read in capacity
        s.readInt(); // ignored

        if (size > 0) {
            // be like clone(), allocate array based upon size not capacity
            ensureCapacityInternal(size);

            Object[] a = elementData;
            // Read in all elements in the proper order.
            for (int i=0; i<size; i++) {
                a[i] = s.readObject();
            }
        }
    }
```

> 当对象中自定义了 writeObject 和 readObject 方法时，JVM 会调用这两个自定义方法来实现序列化与反序列化。


从实现中可以看出 ArrayList 只序列化了被使用的数据。


#### Vector

`Vector` 也是实现于 `List` 接口，底层数据结构和 `ArrayList` 类似,也是一个动态数组存放数据。不过是在 `add()` 方法的时候使用 `synchronized` 进行同步写数据，但是开销较大，所以 `Vector` 是一个同步容器并不是一个并发容器。

以下是 `add()` 方法：
```java
    public synchronized boolean add(E e) {
        modCount++;
        ensureCapacityHelper(elementCount + 1);
        elementData[elementCount++] = e;
        return true;
    }
```

以及指定位置插入数据:
```java
    public void add(int index, E element) {
        insertElementAt(element, index);
    }
    public synchronized void insertElementAt(E obj, int index) {
        modCount++;
        if (index > elementCount) {
            throw new ArrayIndexOutOfBoundsException(index
                                                     + " > " + elementCount);
        }
        ensureCapacityHelper(elementCount + 1);
        System.arraycopy(elementData, index, elementData, index + 1, elementCount - index);
        elementData[index] = obj;
        elementCount++;
    }
```


### LinkedList 底层分析

![](https://ws4.sinaimg.cn/large/006tKfTcly1fqzb66c00gj30p7056q38.jpg)

如图所示 `LinkedList` 底层是基于双向链表实现的，也是实现了 `List` 接口，所以也拥有 List 的一些特点(Java7/8 之后取消了循环，修改为双向链表)。

#### 新增方法

```java
    public boolean add(E e) {
        linkLast(e);
        return true;
    }
     /**
     * Links e as last element.
     */
    void linkLast(E e) {
        final Node<E> l = last;
        final Node<E> newNode = new Node<>(l, e, null);
        last = newNode;
        if (l == null)
            first = newNode;
        else
            l.next = newNode;
        size++;
        modCount++;
    }
```

可见每次插入都是移动指针，和 ArrayList 的拷贝数组来说效率要高上不少。

#### 查询方法

```java
    public E get(int index) {
        checkElementIndex(index);
        return node(index).item;
    }
    
    Node<E> node(int index) {
        // assert isElementIndex(index);

        if (index < (size >> 1)) {
            Node<E> x = first;
            for (int i = 0; i < index; i++)
                x = x.next;
            return x;
        } else {
            Node<E> x = last;
            for (int i = size - 1; i > index; i--)
                x = x.prev;
            return x;
        }
    }
```

上述代码，利用了双向链表的特性，如果`index`离链表头比较近，就从节点头部遍历。否则就从节点尾部开始遍历。使用空间（双向链表）来换取时间。

- `node()`会以`O(n/2)`的性能去获取一个结点
- 如果索引值大于链表大小的一半，那么将从尾结点开始遍历

这样的效率是非常低的，特别是当 index 越接近 size 的中间值时。

总结：

- LinkedList 插入，删除都是移动指针效率很高。
- 查找需要进行遍历查询，效率较低。

### Java提供的默认排序算法

需要区分是Arrays.sort()还是Collections.sort() 

- 对于原始数据类型，目前使用的是所谓双轴快速排序(Dual-Pivot QuickSort)，是一种改进的快速排序算法，早期版本是相对传统的快速排序，可以阅读[源码](http://hg.openjdk.java.net/jdk/jdk/file/26ac622a4cab/src/java.base/share/classes/java/util/DualPivotQuicksort.java)。 

- 而对于对象数据类型，目前则是使用[TimSort](http://hg.openjdk.java.net/jdk/jdk/file/26ac622a4cab/src/java.base/share/classes/java/util/TimSort.java)，思想上也是一种归并和二分插入排序(binarySort)结合的优化排序算法。TimSort并不是Java的独创，简单说它的思路是查找数据集中已经排好序的分区(这里叫run)，然后合并这些分区来达到排序的目的。 

- 另外，Java 8引入了并行排序算法(直接使用parallelSort方法)，这是为了充分利用现代多核处理器的计算能力，底层实现基于fork-join框架 

### HashMap 底层分析

大部分使用Map的场景，通常就是放入、访问或者删除，而对顺序没有特别要求。HashMap的性能表现非常依赖于哈希码的有效性，请务必 掌握hashCode和equals的一些基本约定，比如: 

- equals相等，hashCode一定要相等。 
- 重写了hashCode也要重写equals。 
- hashCode需要保持一致性，状态改变返回的哈希值仍然要一致。
- equals的对称、反射、传递等特性。 

![](https://ws2.sinaimg.cn/large/006tNc79gy1fn84b0ftj4j30eb0560sv.jpg)

如图所示，HashMap 底层是基于数组和链表实现的。其中有两个重要的参数：

- 容量
- 负载因子

容量的默认大小是 16，负载因子是 0.75，当 `HashMap` 的 `size > 16*0.75` 时就会发生扩容(容量和负载因子都可以自由调整)。

#### put 方法

首先会将传入的 Key 做 `hash` 运算计算出 hashcode,然后根据数组长度取模计算出在数组中的 index 下标。

由于在计算中位运算比取模运算效率高的多，所以 HashMap 规定数组的长度为 `2^n` 。这样用 `2^n - 1` 做位运算与取模效果一致，并且效率还要高出许多。

由于数组的长度有限，所以难免会出现不同的 Key 通过运算得到的 index 相同，这种情况可以利用链表来解决，HashMap 会在 `table[index]`处形成链表，采用头插法将数据插入到链表中。

```java
public V put(K key, V value) {
	return putVal(hash(key), key, value, false, true);
}
```

```java
fnal V putVal(int hash, K key, V value, boolean onlyIfAbent, boolean evit) {
	Node<K,V>[] tab; Node<K,V> p; int i;
	if ((tab = table) == null || (n = tab.length) = 0)
		n = (tab = resize()).length;
	if((p=tab[i=(n-1)&hash])==ull)
		tab[i] = newNode(hash, key, value, nll);
	else {
		// ...
	if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for first treeifyBin(tab, hash);
		// ...
  }
}
```

putVal方法分析：

- 如果表格是null，resize方法会负责初始化它，这从tab = resize()可以看出。
- resize方法兼顾两个职责，创建初始存储表格，或者在容量不满足需求的时候，进行扩容(resize)。
- 在放置新的键值对的过程中，如果发生`++size > threshold`条件，就会发生扩容。

```java
fnal Node<K,V>[] resize() { 
  // ...
	else if ((newCap = oldCap << 1) < MAXIMUM_CAPACIY && oldCap >= DEFAULT_INITIAL_CAPAITY)
		newThr = oldThr << 1; // double there 
  	// ...
	else if (oldThr > 0) // initial capacity was placed in threshold 
    newCap = oldThr;
	else {
		// zero initial threshold signifes using defaultsfults 
    newCap = DEFAULT_INITIAL_CAPAITY;
		newThr = (int)(DEFAULT_LOAD_ATOR* DEFAULT_INITIAL_CAPACITY);
  }
	if (newThr ==0) {
	  foat ft = (foat)newCap * loadFator;
  	newThr = (newCap < MAXIMUM_CAPACITY && ft < (foat)MAXIMUM_CAPACITY) ? (int)ft : Integer.MAX_VALUE); 
  }
	threshold = neThr;
	Node<K,V>[] newTab = (Node<K,V>[])new Node[newap]; 
  table = n;
	// 移动到新的数组结构e数组结构
}
```

依据resize源码，不考虑极端情况(容量理论最大极限由MAXIMUM_CAPACITY指定，数值为 1<<30，也就是2的30次方)，我们可以归纳为：

- 门限值等于(负载因子)x(容量)，如果构建HashMap的时候没有指定它们，那么就是依据相应的默认常量值。
- 门限通常是以倍数进行调整 (newThr = oldThr << 1)，我前面提到，根据putVal中的逻辑，当元素个数超过门限大小时，则调整Map大小。
- 扩容后，需要将老的数组中的元素重新放置到新的数组，这是扩容的一个主要开销来源。

#### get 方法

get 和 put 类似，也是将传入的 Key 计算出 index ，如果该位置上是一个链表就需要遍历整个链表，通过 `key.equals(k)` 来找到对应的元素。

#### 遍历方式

```java
Iterator<Map.Entry<String, Integer>> entryIterator = map.entrySet().iterator();
while (entryIterator.hasNext()) {
  Map.Entry<String, Integer> next = entryIterator.next();
  System.out.println("key=" + next.getKey() + " value=" + next.getValue());
}
```

```java
Iterator<String> iterator = map.keySet().iterator();
while (iterator.hasNext()){
  String key = iterator.next();
  System.out.println("key=" + key + " value=" + map.get(key));
}
```

```java
map.forEach((key,value)->{
    System.out.println("key=" + key + " value=" + value);
});
```

**强烈建议**使用第一种 EntrySet 进行遍历。

第一种可以把 key value 同时取出，第二种还得需要通过 key 取一次 value，效率较低, 第三种需要 Java8 以上，通过外层遍历 table，内层遍历链表或红黑树。 

#### 


#### 注意JDK1.7

JDK1.7在并发环境下使用 `HashMap` 容易出现死循环，丢数据。

并发场景发生扩容，调用 `resize()` 方法里的 `rehash()` 时，容易出现环形链表。这样当获取一个不存在的 `key` 时，计算出的 `index` 正好是环形链表的下标时就会出现死循环。

![](https://ws2.sinaimg.cn/large/006tNc79gy1fn85u0a0d9j30n20ii0tp.jpg)

> 所以 HashMap 只能在单线程中使用，并且尽量的预设容量，尽可能的减少扩容。

#### 注意JDK1.8

在 `JDK1.8` 中对 `HashMap` 进行了优化：

当 `hash` 碰撞之后写入链表的长度超过了阈值(默认为8)时，链表将会转换为**红黑树**。提高了查询效率。

JDK1.8在并发环境下使用 `HashMap` 不会出现死循环，但是会出现丢数据。

并发场景发生扩容，调用 `resize()` 方法，移动原来容器中的数据时保持原来链表的顺序，不会出现环形链表。`resize()`方法中主要逻辑如下：

```java
    // preserve order
    Node<K,V> loHead = null, loTail = null;
    Node<K,V> hiHead = null, hiTail = null;
    Node<K,V> next;
    do {
        next = e.next;
        if ((e.hash & oldCap) == 0) {
            if (loTail == null)
                loHead = e;
            else
                loTail.next = e;
            loTail = e;
        }
        else {
            if (hiTail == null)
                hiHead = e;
            else
                hiTail.next = e;
            hiTail = e;
        }
    } while ((e = next) != null);
```

**多线程场景下推荐使用 ConcurrentHashMap**



### LinkedHashMap 底层分析

[HashMap](https://github.com/crossoverJie/Java-Interview/blob/master/MD/HashMap.md) 是一个无序的 `Map`，因为每次根据 `key` 的 `hashcode` 映射到 `Entry` 数组上，所以遍历出来的顺序并不是写入的顺序。基于 `HashMap` 但具有顺序的 `LinkedHashMap` 来解决有排序需求的场景。它的底层是继承于 `HashMap` 实现的，由一个双向链表所构成。

`LinkedHashMap` 的排序方式有两种：

- 根据写入顺序排序。
- 根据访问顺序排序。

其中根据访问顺序排序时，每次 `get` 都会将访问的值移动到链表末尾，这样重复操作就能得到一个按照访问顺序排序的链表。源码可以看到：

```java
    /**
     * The head of the doubly linked list.
     */
    private transient Entry<K,V> header;

    /**
     * The iteration ordering method for this linked hash map: <tt>true</tt>
     * for access-order, <tt>false</tt> for insertion-order.
     *
     * @serial
     */
    private final boolean accessOrder;
    
    private static class Entry<K,V> extends HashMap.Entry<K,V> {
        // These fields comprise the doubly linked list used for iteration.
        Entry<K,V> before, after;

        Entry(int hash, K key, V value, HashMap.Entry<K,V> next) {
            super(hash, key, value, next);
        }
    }  
```

其中 `Entry` 继承于 `HashMap` 的 `Entry`，并新增了上下节点的指针，也就形成了双向链表。还有一个 `header` 的成员变量，是这个双向链表的头结点。 

总结成一张示意图如下：

![](https://ws1.sinaimg.cn/large/006tKfTcgy1fodggwc523j30za0n4wgj.jpg)

第一个类似于 `HashMap` 的结构，利用 `Entry` 中的 `next` 指针进行关联。下边则是 `LinkedHashMap` 如何达到有序的关键，就是利用了头节点和其余的各个节点之间通过 `Entry` 中的 `after` 和 `before` 指针进行关联。

其中还有一个 `accessOrder` 成员变量，默认是 `false`，默认按照插入顺序排序，为 `true` 时按照访问顺序排序，也可以调用:

```java
    public LinkedHashMap(int initialCapacity,
                         float loadFactor,
                         boolean accessOrder) {
        super(initialCapacity, loadFactor);
        this.accessOrder = accessOrder;
    }
```

这个构造方法可以显式的传入 `accessOrder `。


#### 构造方法

`LinkedHashMap` 的构造方法:

```java
    public LinkedHashMap() {
        super();
        accessOrder = false;
    }
```

其实就是调用的 `HashMap` 的构造方法:

```java
    public HashMap(int initialCapacity, float loadFactor) {
        if (initialCapacity < 0)
            throw new IllegalArgumentException("Illegal initial capacity: " +
                                               initialCapacity);
        if (initialCapacity > MAXIMUM_CAPACITY)
            initialCapacity = MAXIMUM_CAPACITY;
        if (loadFactor <= 0 || Float.isNaN(loadFactor))
            throw new IllegalArgumentException("Illegal load factor: " +
                                               loadFactor);

        this.loadFactor = loadFactor;
        threshold = initialCapacity;
        //HashMap 只是定义了改方法，具体实现交给了 LinkedHashMap
        init();
    }
```

可以看到里面有一个空的 `init()`，具体是由 `LinkedHashMap` 来实现的：

```java
    @Override
    void init() {
        header = new Entry<>(-1, null, null, null);
        header.before = header.after = header;
    }
```
其实也就是对 `header` 进行了初始化。

#### put() 方法

看 `LinkedHashMap` 的 `put()` 方法之前先看看 `HashMap` 的 `put` 方法：

```java
    public V put(K key, V value) {
        if (table == EMPTY_TABLE) {
            inflateTable(threshold);
        }
        if (key == null)
            return putForNullKey(value);
        int hash = hash(key);
        int i = indexFor(hash, table.length);
        for (Entry<K,V> e = table[i]; e != null; e = e.next) {
            Object k;
            if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
                V oldValue = e.value;
                e.value = value;
                //空实现，交给 LinkedHashMap 自己实现
                e.recordAccess(this);
                return oldValue;
            }
        }

        modCount++;
        // LinkedHashMap 对其重写
        addEntry(hash, key, value, i);
        return null;
    }
    
    // LinkedHashMap 对其重写
    void addEntry(int hash, K key, V value, int bucketIndex) {
        if ((size >= threshold) && (null != table[bucketIndex])) {
            resize(2 * table.length);
            hash = (null != key) ? hash(key) : 0;
            bucketIndex = indexFor(hash, table.length);
        }

        createEntry(hash, key, value, bucketIndex);
    }
    
    // LinkedHashMap 对其重写
    void createEntry(int hash, K key, V value, int bucketIndex) {
        Entry<K,V> e = table[bucketIndex];
        table[bucketIndex] = new Entry<>(hash, key, value, e);
        size++;
    }       
```

主体的实现都是借助于 `HashMap` 来完成的，只是对其中的 `recordAccess(), addEntry(), createEntry()` 进行了重写。`LinkedHashMap` 的实现：

```java
    //就是判断是否是根据访问顺序排序，如果是则需要将当前这个 Entry 移动到链表的末尾
    void recordAccess(HashMap<K,V> m) {
        LinkedHashMap<K,V> lm = (LinkedHashMap<K,V>)m;
        if (lm.accessOrder) {
            lm.modCount++;
            remove();
            addBefore(lm.header);
        }
    }
        
    //调用了 HashMap 的实现，并判断是否需要删除最少使用的 Entry(默认不删除)    
    void addEntry(int hash, K key, V value, int bucketIndex) {
        super.addEntry(hash, key, value, bucketIndex);

        // Remove eldest entry if instructed
        Entry<K,V> eldest = header.after;
        if (removeEldestEntry(eldest)) {
            removeEntryForKey(eldest.key);
        }
    }
    
    void createEntry(int hash, K key, V value, int bucketIndex) {
        HashMap.Entry<K,V> old = table[bucketIndex];
        Entry<K,V> e = new Entry<>(hash, key, value, old);
        //就多了这一步，将新增的 Entry 加入到 header 双向链表中
        table[bucketIndex] = e;
        e.addBefore(header);
        size++;
    }
    
    //写入到双向链表中
    private void addBefore(Entry<K,V> existingEntry) {
        after  = existingEntry;
        before = existingEntry.before;
        before.after = this;
        after.before = this;
    }
```

#### get 方法

LinkedHashMap 的 `get()` 方法也重写了：

```java
    public V get(Object key) {
        Entry<K,V> e = (Entry<K,V>)getEntry(key);
        if (e == null)
            return null;
            
        //多了一个判断是否是按照访问顺序排序，是则将当前的 Entry 移动到链表头部。   
        e.recordAccess(this);
        return e.value;
    }
    
    void recordAccess(HashMap<K,V> m) {
        LinkedHashMap<K,V> lm = (LinkedHashMap<K,V>)m;
        if (lm.accessOrder) {
            lm.modCount++;
            
            //删除
            remove();
            //添加到头部
            addBefore(lm.header);
        }
    }
```

`clear()` 清空就要比较简单了：

```java
    //只需要把指针都指向自己即可，原本那些 Entry 没有引用之后就会被 JVM 自动回收。
    public void clear() {
        super.clear();
        header.before = header.after = header;
    }
```

### Java 8 Stream & Java 9 静态工厂方法

在Java 8之中，Java平台支持了Lambda和Stream，相应的Java集合框架也进行了大范围的增强，以支持类似为集合创建相应stream或者parallelStream的方法实现，我们可以非常方便的实现函数式代码。

在Java 9中，Java标准类库提供了一系列的静态工厂方法，比如，List.of()、Set.of()，利用新的容器静态工厂方法，简化了构建小的容器实例的代码量并且保证了不可变性。

### 线程安全的容器

利用并发包提供的线程安全容器类：

- 各种并发容器，比如ConcurrentHashMap、CopyOnWriteArrayList。
- 各种线程安全队列(Queue/Deque)，如ArrayBlockingQueue、SynchronousQueue。
- 各种有序容器的线程安全版本等。







## Java IO总结

主要介绍文件IO和网络IO。

### IO方式面向字节/字符

Java的IO操作中有面向字节(Byte)和面向字符(Character)两种方式。

- 面向字节的操作为以8位为单位对二进制的数据进行操作，对数据不进行转换，这些类都是InputStream和OutputStream的子类。
- 面向字符的操作为以字符为单位对数据进行操作，在读的时候将二进制数据转为字符，在写的时候将字符转为二进制数据，这些类都是Reader和Writer的子类。

总结：以InputStream（输入）/OutputStream（输出）为后缀的是字节流；以Reader（输入）/Writer（输出）为后缀的是字符流。Java流类图结构如下：

![Alt Text](/images/java/java_io_stream.jpg )

### BIO,NIO,AIO 总结

Java 中的 BIO、NIO和 AIO 理解为是 Java 语言对操作系统的各种 IO 模型的封装。程序员在使用这些 API 的时候，不需要关心操作系统层面的知识，也不需要根据不同操作系统编写不同的代码。只需要使用Java的API就可以了。


在讲 BIO,NIO,AIO 之前先来回顾一下这样几个概念：同步与异步，阻塞与非阻塞。

**同步与异步**

- **同步：** 同步就是发起一个调用后，被调用者未处理完请求之前，调用不返回。
- **异步：** 异步就是发起一个调用后，立刻得到被调用者的回应表示已接收到请求，但是被调用者并没有返回结果，此时我们可以处理其他的请求，被调用者通常依靠事件，回调等机制来通知调用者其返回结果。

同步和异步的区别最大在于异步的话调用者不需要等待处理结果，被调用者会通过回调等机制来通知调用者其返回结果。

**阻塞和非阻塞**

- **阻塞：** 阻塞就是发起一个请求，调用者一直等待请求结果返回，也就是当前线程会被挂起，无法从事其他任务，只有当条件就绪才能继续。
- **非阻塞：** 非阻塞就是发起一个请求，调用者不用一直等着结果返回，可以先去干其他事情。

举个生活中简单的例子，你妈妈让你烧水，小时候你比较笨啊，在哪里傻等着水开（**同步阻塞**）。等你稍微再长大一点，你知道每次烧水的空隙可以去干点其他事，然后只需要时不时来看看水开了没有（**同步非阻塞**）。后来，你们家用上了水开了会发出声音的壶，这样你就只需要听到响声后就知道水开了，在这期间你可以随便干自己的事情，你需要去倒水了（**异步非阻塞**）。


### BIO (Blocking I/O)

同步阻塞I/O模式，数据的读取写入必须阻塞在一个线程内等待其完成。

#### 传统 BIO

BIO通信（一请求一应答）模型图如下(图源网络，原出处不明)：

![传统BIO通信模型图](https://my-blog-to-use.oss-cn-beijing.aliyuncs.com/2.png)

采用 **BIO 通信模型** 的服务端，通常由一个独立的 Acceptor 线程负责监听客户端的连接。我们一般通过在`while(true)` 循环中服务端会调用 `accept()` 方法等待接收客户端的连接的方式监听请求，请求一旦接收到一个连接请求，就可以建立通信套接字在这个通信套接字上进行读写操作，此时不能再接收其他客户端连接请求，只能等待同当前连接的客户端的操作执行完成， 不过可以通过多线程来支持多个客户端的连接，如上图所示。

如果要让 **BIO 通信模型** 能够同时处理多个客户端请求，就必须使用多线程（主要原因是`socket.accept()`、`socket.read()`、`socket.write()` 涉及的三个主要函数都是同步阻塞的），也就是说它在接收到客户端连接请求之后为每个客户端创建一个新的线程进行链路处理，处理完成之后，通过输出流返回应答给客户端，线程销毁。这就是典型的 **一请求一应答通信模型** 。我们可以设想一下如果这个连接不做任何事情的话就会造成不必要的线程开销，不过可以通过 **线程池机制** 改善，线程池还可以让线程的创建和回收成本相对较低。使用`FixedThreadPool` 可以有效的控制了线程的最大数量，保证了系统有限的资源的控制，实现了N(客户端请求数量):M(处理客户端请求的线程数量)的伪异步I/O模型（N 可以远远大于 M），下面一节"伪异步 BIO"中会详细介绍到。

**我们再设想一下当客户端并发访问量增加后这种模型会出现什么问题？**

在 Java 虚拟机中，线程是宝贵的资源，线程的创建和销毁成本很高，除此之外，线程的切换成本也是很高的。尤其在 Linux 这样的操作系统中，线程本质上就是一个进程，创建和销毁线程都是重量级的系统函数。如果并发访问量增加会导致线程数急剧膨胀可能会导致线程堆栈溢出、创建新线程失败等问题，最终导致进程宕机或者僵死，不能对外提供服务。

#### 伪异步 IO

为了解决同步阻塞I/O面临的一个链路需要一个线程处理的问题，后来有人对它的线程模型进行了优化一一一后端通过一个线程池来处理多个客户端的请求接入，形成客户端个数M：线程池最大线程数N的比例关系，其中M可以远远大于N.通过线程池可以灵活地调配线程资源，设置线程的最大值，防止由于海量并发接入导致线程耗尽。

伪异步IO模型图(图源网络，原出处不明)：

![伪异步IO模型图](https://my-blog-to-use.oss-cn-beijing.aliyuncs.com/3.png)

采用线程池和任务队列可以实现一种叫做伪异步的 I/O 通信框架，它的模型图如上图所示。当有新的客户端接入时，将客户端的 Socket 封装成一个Task（该任务实现java.lang.Runnable接口）投递到后端的线程池中进行处理，JDK 的线程池维护一个消息队列和 N 个活跃线程，对消息队列中的任务进行处理。由于线程池可以设置消息队列的大小和最大线程数，因此，它的资源占用是可控的，无论多少个客户端并发访问，都不会导致资源的耗尽和宕机。

伪异步I/O通信框架采用了线程池实现，因此避免了为每个请求都创建一个独立线程造成的线程资源耗尽问题。不过因为它的底层任然是同步阻塞的BIO模型，因此无法从根本上解决问题。

#### 代码示例

下面代码中演示了BIO通信（一请求一应答）模型。我们会在客户端创建多个线程依次连接服务端并向其发送"当前时间+:hello world"，服务端会为每个客户端线程创建一个线程来处理。代码示例出自闪电侠的博客，原地址如下：        

[https://www.jianshu.com/p/a4e03835921a](https://www.jianshu.com/p/a4e03835921a)

**客户端**

```java
/**
 * 
 * @author 闪电侠
 * @date 2018年10月14日
 * @Description:客户端
 */
public class IOClient {

  public static void main(String[] args) {
    // TODO 创建多个线程，模拟多个客户端连接服务端
    new Thread(() -> {
      try {
        Socket socket = new Socket("127.0.0.1", 3333);
        while (true) {
          try {
            socket.getOutputStream().write((new Date() + ": hello world").getBytes());
            Thread.sleep(2000);
          } catch (Exception e) {
          }
        }
      } catch (IOException e) {
      }
    }).start();

  }

}

```

**服务端**

```java
/**
 * @author 闪电侠
 * @date 2018年10月14日
 * @Description: 服务端
 */
public class IOServer {

  public static void main(String[] args) throws IOException {
    // TODO 服务端处理客户端连接请求
    ServerSocket serverSocket = new ServerSocket(3333);

    // 接收到客户端连接请求之后为每个客户端创建一个新的线程进行链路处理
    new Thread(() -> {
      while (true) {
        try {
          // 阻塞方法获取新的连接
          Socket socket = serverSocket.accept();

          // 每一个新的连接都创建一个线程，负责读取数据
          new Thread(() -> {
            try {
              int len;
              byte[] data = new byte[1024];
              InputStream inputStream = socket.getInputStream();
              // 按字节流方式读取数据
              while ((len = inputStream.read(data)) != -1) {
                System.out.println(new String(data, 0, len));
              }
            } catch (IOException e) {
            }
          }).start();

        } catch (IOException e) {
        }

      }
    }).start();

  }

}
```

#### 总结

在活动连接数不是特别高（小于单机1000）的情况下，这种模型是比较不错的，可以让每一个连接专注于自己的 I/O 并且编程模型简单，也不用过多考虑系统的过载、限流等问题。线程池本身就是一个天然的漏斗，可以缓冲一些系统处理不了的连接或请求。但是，当面对十万甚至百万级连接的时候，传统的 BIO 模型是无能为力的。因此，我们需要一种更高效的 I/O 处理模型来应对更高的并发量。



### NIO (New I/O)

#### NIO 简介

 NIO是一种同步非阻塞的I/O模型，在Java 1.4 中引入了NIO框架，对应 java.nio 包，提供了 Channel , Selector，Buffer等抽象。

NIO中的N可以理解为Non-blocking，不单纯是New。它支持面向缓冲的，基于通道的I/O操作方法。 NIO提供了与传统BIO模型中的 `Socket` 和 `ServerSocket` 相对应的 `SocketChannel` 和 `ServerSocketChannel` 两种不同的套接字通道实现,两种通道都支持阻塞和非阻塞两种模式。阻塞模式使用就像传统中的支持一样，比较简单，但是性能和可靠性都不好；非阻塞模式正好与之相反。对于低负载、低并发的应用程序，可以使用同步阻塞I/O来提升开发速率和更好的维护性；对于高负载、高并发的（网络）应用，应使用 NIO 的非阻塞模式来开发。

#### NIO的特性/NIO与IO区别

如果是在面试中回答这个问题，我觉得首先肯定要从 NIO 流是非阻塞 IO 而 IO 流是阻塞 IO 说起。然后，可以从 NIO 的3个核心组件/特性为 NIO 带来的一些改进来分析。如果，你把这些都回答上了我觉得你对于 NIO 就有了更为深入一点的认识，面试官问到你这个问题，你也能很轻松的回答上来了。

##### 1)Non-blocking IO（非阻塞IO）

**IO流是阻塞的，NIO流是不阻塞的。**

Java NIO使我们可以进行非阻塞IO操作。比如说，单线程中从通道读取数据到buffer，同时可以继续做别的事情，当数据读取到buffer中后，线程再继续处理数据。写数据也是一样的。另外，非阻塞写也是如此。一个线程请求写入一些数据到某通道，但不需要等待它完全写入，这个线程同时可以去做别的事情。

Java IO的各种流是阻塞的。这意味着，当一个线程调用 `read()` 或  `write()` 时，该线程被阻塞，直到有一些数据被读取，或数据完全写入。该线程在此期间不能再干任何事情了

##### 2)Buffer(缓冲区)

**IO 面向流(Stream oriented)，而 NIO 面向缓冲区(Buffer oriented)。**

Buffer是一个对象，它包含一些要写入或者要读出的数据。在NIO类库中加入Buffer对象，体现了新库与原I/O的一个重要区别。在面向流的I/O中·可以将数据直接写入或者将数据直接读到 Stream 对象中。虽然 Stream 中也有 Buffer 开头的扩展类，但只是流的包装类，还是从流读到缓冲区，而 NIO 却是直接读到 Buffer 中进行操作。

在NIO厍中，所有数据都是用缓冲区处理的。在读取数据时，它是直接读到缓冲区中的; 在写入数据时，写入到缓冲区中。任何时候访问NIO中的数据，都是通过缓冲区进行操作。

最常用的缓冲区是 ByteBuffer,一个 ByteBuffer 提供了一组功能用于操作 byte 数组。除了ByteBuffer,还有其他的一些缓冲区，事实上，每一种Java基本类型（除了Boolean类型）都对应有一种缓冲区。

##### 3)Channel (通道)

NIO 通过Channel（通道） 进行读写。

通道是双向的，可读也可写，而流的读写是单向的。无论读写，通道只能和Buffer交互。因为 Buffer，通道可以异步地读写。

##### 4)Selectors(选择器)

NIO有选择器，而IO没有。

选择器用于使用单个线程处理多个通道。因此，它需要较少的线程来处理这些通道。线程之间的切换对于操作系统来说是昂贵的。 因此，为了提高系统效率选择器是有用的。

![一个单线程中Slector维护3个Channel的示意图](https://my-blog-to-use.oss-cn-beijing.aliyuncs.com/2019-2/Slector.png)

#### NIO 读数据和写数据方式
通常来说NIO中的所有IO都是从 Channel（通道） 开始的。

- 从通道进行数据读取 ：创建一个缓冲区，然后请求通道读取数据。
- 从通道进行数据写入 ：创建一个缓冲区，填充数据，并要求通道写入数据。

数据读取和写入操作图示：

![NIO读写数据的方式](https://my-blog-to-use.oss-cn-beijing.aliyuncs.com/2019-2/NIO读写数据的方式.png)


#### NIO核心组件简单介绍

NIO 包含下面几个核心的组件：

- Channel(通道)
- Buffer(缓冲区)
- Selector(选择器)

整个NIO体系包含的类远远不止这三个，只能说这三个是NIO体系的“核心API”。我们上面已经对这三个概念进行了基本的阐述，这里就不多做解释了。

#### 代码示例

代码示例出自闪电侠的博客，原地址如下：        

[https://www.jianshu.com/p/a4e03835921a](https://www.jianshu.com/p/a4e03835921a)

客户端 IOClient.java 的代码不变，我们对服务端使用 NIO 进行改造。以下代码较多而且逻辑比较复杂，大家看看就好。

```java
/**
 * 
 * @author 闪电侠
 * @date 2019年2月21日
 * @Description: NIO 改造后的服务端
 */
public class NIOServer {
  public static void main(String[] args) throws IOException {
    // 1. serverSelector负责轮询是否有新的连接，服务端监测到新的连接之后，不再创建一个新的线程，
    // 而是直接将新连接绑定到clientSelector上，这样就不用 IO 模型中 1w 个 while 循环在死等
    Selector serverSelector = Selector.open();
    // 2. clientSelector负责轮询连接是否有数据可读
    Selector clientSelector = Selector.open();

    new Thread(() -> {
      try {
        // 对应IO编程中服务端启动
        ServerSocketChannel listenerChannel = ServerSocketChannel.open();
        listenerChannel.socket().bind(new InetSocketAddress(3333));
        listenerChannel.configureBlocking(false);
        listenerChannel.register(serverSelector, SelectionKey.OP_ACCEPT);

        while (true) {
          // 监测是否有新的连接，这里的1指的是阻塞的时间为 1ms
          if (serverSelector.select(1) > 0) {
            Set<SelectionKey> set = serverSelector.selectedKeys();
            Iterator<SelectionKey> keyIterator = set.iterator();

            while (keyIterator.hasNext()) {
              SelectionKey key = keyIterator.next();

              if (key.isAcceptable()) {
                try {
                  // (1)
                  // 每来一个新连接，不需要创建一个线程，而是直接注册到clientSelector
                  SocketChannel clientChannel = ((ServerSocketChannel) key.channel()).accept();
                  clientChannel.configureBlocking(false);
                  clientChannel.register(clientSelector, SelectionKey.OP_READ);
                } finally {
                  keyIterator.remove();
                }
              }

            }
          }
        }
      } catch (IOException ignored) {
      }
    }).start();
    new Thread(() -> {
      try {
        while (true) {
          // (2) 批量轮询是否有哪些连接有数据可读，这里的1指的是阻塞的时间为 1ms
          if (clientSelector.select(1) > 0) {
            Set<SelectionKey> set = clientSelector.selectedKeys();
            Iterator<SelectionKey> keyIterator = set.iterator();

            while (keyIterator.hasNext()) {
              SelectionKey key = keyIterator.next();

              if (key.isReadable()) {
                try {
                  SocketChannel clientChannel = (SocketChannel) key.channel();
                  ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
                  // (3) 面向 Buffer
                  clientChannel.read(byteBuffer);
                  byteBuffer.flip();
                  System.out.println(
                      Charset.defaultCharset().newDecoder().decode(byteBuffer).toString());
                } finally {
                  keyIterator.remove();
                  key.interestOps(SelectionKey.OP_READ);
                }
              }

            }
          }
        }
      } catch (IOException ignored) {
      }
    }).start();

  }
}
```

为什么大家都不愿意用 JDK 原生 NIO 进行开发呢？从上面的代码中大家都可以看出来，是真的难用！除了编程复杂、编程模型难之外，它还有以下让人诟病的问题：

- JDK 的 NIO 底层由 epoll 实现，该实现饱受诟病的空轮询 bug 会导致 cpu 飙升 100%
- 项目庞大之后，自行实现的 NIO 很容易出现各类 bug，维护成本较高，上面这一坨代码我都不能保证没有 bug

Netty 的出现很大程度上改善了 JDK 原生 NIO 所存在的一些让人难以忍受的问题。

### AIO (Asynchronous I/O)

AIO 也就是 NIO 2。在 Java 7 中引入了 NIO 的改进版 NIO 2,它是异步非阻塞的IO模型。异步 IO 是基于事件和回调机制实现的，也就是应用操作之后会直接返回，不会堵塞在那里，当后台处理完成，操作系统会通知相应的线程进行后续的操作。

AIO 是异步IO的缩写，虽然 NIO 在网络操作中，提供了非阻塞的方法，但是 NIO 的 IO 行为还是同步的。对于 NIO 来说，我们的业务线程是在 IO 操作准备好时，得到通知，接着就由这个线程自行进行 IO 操作，IO操作本身是同步的。（除了 AIO 其他的 IO 类型都是同步的，这一点可以从底层IO线程模型解释，推荐一篇文章：[《漫话：如何给女朋友解释什么是Linux的五种IO模型？》](https://mp.weixin.qq.com/s?__biz=Mzg3MjA4MTExMw==&mid=2247484746&amp;idx=1&amp;sn=c0a7f9129d780786cabfcac0a8aa6bb7&source=41#wechat_redirect) ）

查阅网上相关资料，我发现就目前来说 AIO 的应用还不是很广泛，Netty 之前也尝试使用过 AIO，不过又放弃了。


### Reactor模式

IO并发设计：Reactor模式与Proactor模式


## Java特性

### Java反射与javassist

反射与工厂模式 `java.lang.reflect.*`

### Annotation用法

`java.lang.annotation.*`

### Java序列化

什么是序列化，为什么序列化 序列化与单例模式 `java.io.Serializable`

定义了如下的Employee类，该类实现了 Serializable 接口

```java
public class Employee implements java.io.Serializable {
  public String name;
  public String address;
  public transient int SSN;
  public int number;

  public void mailCheck() {
    System.out.println("Mailing a check to " + name
          + " " + address);
  }
}
```

一个类的对象要想序列化必须满足两个条件：

- 该类必须实现 java.io.Serializable 对象。
- 该类的所有属性必须是可序列化的。如果有一个属性不是可序列化的，则该属性必须注明是短暂（transient）的。如果你想知道一个Java标准类是否是可序列化的，请查看该类的文档。检验一个类的实例是否能序列化十分简单， 只需要查看该类有没有实现java.io.Serializable接口。

**序列化和反序列化**

```java
import java.io.*;

public class Main {
  public static void main(String [] args) {
    String ser_filename = "./employee.ser";
    {
      // Serialize demo
      Employee e = new Employee();
      e.name = "Reyan Ali";
      e.address = "Phokka Kuan, Ambehta Peer";
      e.SSN = 11122333;
      e.number = 101;

      try {
        FileOutputStream fileOut =
                new FileOutputStream(ser_filename);
        ObjectOutputStream out = new ObjectOutputStream(fileOut);
        out.writeObject(e);
        out.close();
        fileOut.close();
        System.out.println("Serialized data is saved in " + ser_filename);
      } catch(IOException i) {
        i.printStackTrace();
      }
    }

    {
      // Deserialize demo
      Employee e = null;
      try {
        FileInputStream fileIn = new FileInputStream(ser_filename);
        ObjectInputStream in = new ObjectInputStream(fileIn);
        e = (Employee) in.readObject();
        in.close();
        fileIn.close();
      } catch(IOException i) {
        i.printStackTrace();
        return;
      } catch(ClassNotFoundException c) {
        System.out.println("Employee class not found");
        c.printStackTrace();
        return;
      }
      System.out.println("Deserialized Employee from " + ser_filename + " ..." );
      System.out.println("Name: " + e.name);
      System.out.println("Address: " + e.address);
      System.out.println("SSN: " + e.SSN);
      System.out.println("Number: " + e.number);
      e.mailCheck();
    }
  }
}
```

输出结果：

```markdown
Serialized data is saved in ./employee.ser
Deserialized Employee from ./employee.ser ...
Name: Reyan Ali
Address: Phokka Kuan, Ambehta Peer
SSN: 0
Number: 101
Mailing a check to Reyan Ali Phokka Kuan, Ambehta Peer
```

### 虚引用，弱引用，软引用

`java.lang.ref.*` 实验这些引用的回收

### Java系统属性

`java.util.Properties`

### JMS

`javax.jms.*`

### JMX

`java.lang.management.*` `javax.management.*`

### 泛型和继承，泛型和擦除

### java.lang.Void类使用

### Java Agent，premain函数

`java.lang.instrument`

### 单元测试

[Junit](http://junit.org/)

[Jmockit](https://code.google.com/p/jmockit/)

[djUnit](http://works.dgic.co.jp/djunit/)

### Java正则表达式

`java.lang.util.regex.*`

### 常用的Java工具库

`commons.lang` `commons.*...` `guava-libraries`

`guava` 是谷歌开源的Java标准包扩展项目

### API & SPI

[http://en.wikipedia.org/wiki/Application_programming_interface](http://en.wikipedia.org/wiki/Application_programming_interface)

[http://en.wikipedia.org/wiki/Service_provider_interface](http://en.wikipedia.org/wiki/Service_provider_interface)

[http://stackoverflow.com/questions/2954372/difference-between-spi-and-api](http://stackoverflow.com/questions/2954372/difference-between-spi-and-api)

[http://stackoverflow.com/questions/11404230/how-to-implement-the-api-spi-pattern-in-java](http://stackoverflow.com/questions/11404230/how-to-implement-the-api-spi-pattern-in-java)

### Apache Maven

[Apache Maven Project](http://maven.apache.org/index.html)

[IntelliJ IDEA中Maven功能](http://www.youmeek.com/intellij-idea-part-xviii-maven/)

## 参考资料

- [JDK src.zip 源代码  http://openjdk.java.net/](http://openjdk.java.net/)
- [http://commons.apache.org/](http://commons.apache.org/)
- [https://code.google.com/p/guava-libraries/](https://code.google.com/p/guava-libraries/)
- [Java Core Sprout](https://github.com/crossoverJie/JCSprout)
- [JavaGuide](https://github.com/Snailclimb/JavaGuide)
- [Java NIO浅析](https://zhuanlan.zhihu.com/p/23488863)
- 《Netty 权威指南》第二版
- [http://netty.io/](http://netty.io/)
