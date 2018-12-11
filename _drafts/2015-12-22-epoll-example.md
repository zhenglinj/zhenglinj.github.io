---
layout: post
title: "Linux Socket 事件触发模型 epoll 示例"
description: "这里写一个用C语言的TCP服务器的完全实现的简单程序"
draft: true
category: "technology"
tags: [socket, epoll, notes]
---

这里写一个用C语言的TCP服务器的完全实现的简单程序

---

## 背景介绍

通常的网络服务器实现，是对每一个连接使用一个单独的线程或进程。对高性能应用而言，由于需要同时处理非常多的客户请求，所以这种方式并不能工作得很好，因为诸如资源使用和上下文切换所需的时间影响了在一时间内对多个客户端进行处理。另一个可选的途径是在一个单独的线程里采用非阻塞的I/O，这样当可以从一个socket中读取或写入更多数据时，由一些已经准备就绪的通知方式来告知我们。

这篇文章介绍 Linux 的 epoll 方法， 它是Linux上最好的就绪通知方式。我们会写一个用C语言的TCP服务器的完全实现的简单程序。假设你已有C编程的经验，知道在Linux 下编译和运行程序， 并且会用 manpages 来查看所使用的 C 函数。

`epoll`是在 Linux 2.6 才引进的，而且它并不适用于其它 Unix-like 系统。它提供了一个与`select`和`poll`函数相似的功能：

+ `select`可以在某一时间监视最大达到`FD_SETSIZE`数量的文件描述符， 通常是由在 libc 编译时指定的一个比较小的数字。
+ `poll`在同一时间能够监视的文件描述符数量并没有受到限制，即使除了其它因素，更加的是我们必须在每一次都扫描所有通过的描述符来检查其是否存在己就绪通知，它的时间复杂度为 O(n) ，是缓慢的。
+ `epoll`没有以上所示的限制，并且不用执行线性扫描。因此，它能有更高的执行效率且可以处理大数量的事件。
<!-- TODO -->

一个epoll实例可以通过返回epoll实例的`epoll_create`或者`epoll_create1`函数来创建。`epoll_ctl`是用来在epoll实例中 添加／删除 被监视的文件描述符的。`epoll_wait`是用来等待所监听描述符事件的，它会阻塞到事件到达。 可以在 manpages上查看更多信息。

当描述符被添加到epoll实例中，有两种添加模式：level triggered（水平触发） 和 edge triggered（边沿触发） 。

+ 当使用 level triggered (LT) 模式并且数据就绪待读，`epoll_wait`总是会返加就绪事件。如果你没有将数据读取完，并且调用`epoll_wait`在epoll实例上再次监听这个描述符， 由于还有数据是可读的，它会再次返回。
+ 在 edge triggered (ET) 模式时，你只会得一次就绪通知。如果你没有将数据读完，并且再次在epoll实例上调用`epoll_wait`，由于就绪事件已经被发送所以它会阻塞。

## epoll相关函数

### epoll_create或epoll_cteate1

```c
int epoll_create1(int flags);
```

函数参数：

`flags`: 当前版本只支持`EPOLL_CLOEXEC`标志(请注意不支持`EPOLL_NONBLOCK`标志)
其实我们也能够通过`epoll_create(int size)`这个函数来创建epoll实例，只不过这个函数中的size在2.6.27内核开始就不必要了，新的内核已经能够动态地管理所需的内存分配了。我们视之为废弃。

根据惯例，如果返回-1，则标志出现了问题，我们可以读取errno来定位错误，有如下errno会被设置：

+ `EINVAL`: 无效的标志
+ `EMFILE`: 用户打开的文件超过了限制
+ `ENFILE`: 系统打开的文件超过了限制
+ `ENOMEM`: 没有足够的内存完成当前操作

### epoll_ctl

```c
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
```

函数参数：

+ `epfd` : epoll实例的fd
+ `op` : 操作标志，下文会描述
+ `fd` : 监控对象的fd
+ `event` : 事件的内容，下文描述

op可以有3个值，分别为：

+ `EPOLL_CTL_ADD` : 添加监听的事件
+ `EPOLL_CTL_DEL` : 删除监听的事件
+ `EPOLL_CTL_MOD` : 修改监听的事件

传递到`epoll_ctl`的epoll事件结构体`epoll_event`如下所示。对每一个被监听的描述符，你可以关联到一个整数或一个作为用户数据的指针。

```cpp
typedef union epoll_data
{
  void        *ptr;
  int          fd;
  __uint32_t   u32;
  __uint64_t   u64;
} epoll_data_t;

struct epoll_event
{
  __uint32_t   events; /* Epoll events */
  epoll_data_t data;   /* User data variable */
};
```

其中，data是一个联合体，能够存储fd或其它数据，我们需要根据自己的需求定制。events表示监控的事件的集合，是一个状态值，通过状态位来表示，可以设置如下事件：

+ `EPOLLERR`: 文件上发上了一个错误。这个事件是一直监控的，即使没有明确指定
+ `EPOLLHUP`: 文件被挂断。这个事件是一直监控的，即使没有明确指定
+ `EPOLLRDHUP`: 对端关闭连接或者shutdown写入半连接
+ `EPOLLET`: 开启边缘触发，默认的是水平触发，所以我们并未看到EPOLLLT
+ `EPOLLONESHOT`: 一个事件发生并读取后，文件自动不再监控
+ `EPOLLIN`: 文件可读
+ `EPOLLPRI`: 文件有紧急数据可读
+ `EPOLLOUT`: 文件可写
+ `EPOLLWAKEUP`: 如果`EPOLLONESHOT`和`EPOLLET`清除了，并且进程拥有`CAP_BLOCK_SUSPEND`权限，那么这个标志能够保证事件在挂起或者处理的时候，系统不会挂起或休眠

注意一下，`EPOLLHUP`并不代表对端结束了连接，这一点需要和`EPOLLRDHUP`区分。通常情况下`EPOLLHUP`表示的是本端挂断，造成这种事件出现的原因有很多，其中一种便是出现错误，更加细致的应该是和RST联系在一起，不过目前相关文档并不是很全面，本文会进一步跟进。

根据惯例，如果返回-1，则标志出现了问题，我们可以读取errno来定位错误，有如下errno会被设置：

+ `EBADF`: epfd或者fd不是一个有效的文件描述符
+ `EEXIST`: op为`EPOLL_CTL_ADD`，但fd已经被监控
+ `EINVAL`: epfd是无效的epoll文件描述符
+ `ENOENT`: op为`EPOLL_CTL_MOD`或者`EPOLL_CTL_DEL`，并且fd未被监控
+ `ENOMEM`: 没有足够的内存完成当前操作
+ `ENOSPC`: epoll实例超过了`/proc/sys/fs/epoll/max_user_watches`中限制的监听数量

### epoll_wait

```c
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
```

函数参数：

+ `epfd` : epoll实例的fd
+ `events` : 储存事件的数组首地址
+ `maxevents` : 最大事件的数量
+ `timeout` : 等待的最长时间

如果函数返回获得的时间的数量，如果返回-1，则标志出现了问题，我们可以读取errno来定位错误，有如下errno会被设置：

+ `EBADF` : epfd不是一个有效的文件描述符
+ `EFAULT` : events指向的内存无权访问
+ `EINTR` : 在请求事件发生或者过期之前，调用被信号打断
+ `EINVAL` : epfd是无效的epoll文件描述符

## 水平触发和边缘触发

用英文来表示，水平触发为Level Trigger，边缘触发为Edge Trigger:

+ LT 意思是水平触发 如果有数据到来没有被处理或者没有处理完(数据没有接收全)那么下次会再次进行通知；
+ ET 意思是边缘触发 数据到来只通知一次，即使没有处理或者没有处理完也不再通知；

那么为什么在这里突兀得提及ET和LT呢？是这样的，想必各位应该已经注意到EPOLLET了，这个就代表ET事件，而epoll默认采取的是LT，也就是说在能够正确使用epoll之前，我们必须弄明白ET和LT。有一点需要强调ET模式只能应用于设置了O_NONBLOCK的fd，而LT则同时支持阻塞和非阻塞。使用得当ET效率比LT高，但是LT更加易用，不容易除错。

通过上面的简单解释我相信大家应该知道两者的差别了：

1. LT 保证了数据不会丢失，但是性能低
2. ET 不保证数据安全，但是性能高效

可以通过在添加事件的时候添加EPOLLET(边缘触发)开启边缘触发，默认是水平触发。poll和select都只支持水平触发。下面是对两种模式的处理方式:

**LT模式:**

```c
if (events[i].events & EPOLLIN) // 数据可读事件
{
    // 在一次数据到来的时候，下面这段代码可能会被触发多次
    // 因为buf没有存放完所有的数据，所以还会再次触发事件进行读取
    printf("trigger one\n");
    bzero(buf, sizeof(buf));
    int ret = recv(sockfd, buf, sizeof(buf)-1, 0);
    if (ret < 0) {
        close(sockfd);
        continue;
    }
    printf("get some bytes data\n");
}
```

**ET模式:**

```c
if (events[i].events & EPOLLIN) // 数据可读事件
{
    // 在一次数据到来的时候,下面这段代码只触发一次
    printf("only trigger one\n");
    while (1) {
        bzero(buf, sizeof(buf));
        int ret = recv(sockfd, buf, sizeof(buf)-1, 0);
        if (ret < 0) {
            // 非阻塞的socket描述符当errno出现这两种情况表明数据读取完毕
            if ((errno == EAEGIN) || (errno == EWOULDBLOCK)) {
                printf("read later\n");
                break;
            }
            close(sockfd);
            break;
        } else if (ret == 0) {
            close(sockfd);
        } else {
            printf("get some bytes data\n");
        }
    }
}
```

## epoll的使用模式

解释了这个多，我们应该怎么来用epoll呢？简单的几个函数，用起来可着实不轻松。好在，这里有一个大概的模式供大家参考，如下为伪代码:

```c
epfd = epoll_init1(0);
event.events = EPOLLET | EPOLLIN;
event.data.fd = serverfd;
epoll_ctl(epfd, EPOLL_CTL_ADD, serverfd, &event);

while (true) {
    // 这里的timeout很重要，实际使用中灵活调整
    count = epoll_wait(epfd, events, MAXEVENTS, timeout);
    for (i = 0; i < count; ++i) {
        if (events[i].events & EPOLLERR || events[i].events & EPOLLHUP) {
            // 处理错误
            continue;
        }
        if (events[i].events & EPOLLIN) {
            if(events[i].data.fd == serverfd) {
                // 处理接入的socket
                // 为接入的连接注册事件
            } else {
                // 有数据可读
                read(events[i].data.fd, buf, len);
                event.events = EPOLLET | EPOLLOUT;
                event.data.fd = events[i].data.fd;
                epoll_ctl(epfd, EPOLL_CTL_MOD, events[i].data.fd, &event);
            }
        } else if (events[i].events & EPOLLOUT) {
            if (events[i].data.fd != serverfd) {
                // 有数据可写
                write(events[i].data.fd, buf, len);
                // 后续可以关闭fd或者MOD至EPOLLOUT
            }
        }
    }
}
```

使用上述的框架，我们可以完成很多事情，但是内部的细节，比如错误处理，信号处理等，还是不能大意，需要完善。

## epoll实例echo man

接下来，让我们来看个示例吧。这只是一个hello world级别的代码，无论是你发送什么数据给它，它只会回复 "it's echo man"。使用的是ET模式，相信对于大家应该有些许参考价值。

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <netdb.h>
#include <sys/epoll.h>
#include <string.h>

#define MAXEVENTS 64

int create_and_bind(int port) {
    int sfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sfd == -1) {
        return -1;
    }
    struct sockaddr_in sa;
    bzero(&sa, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_port   = htons(port);
    sa.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(sfd, (struct sockaddr*)&sa, sizeof(struct sockaddr)) == -1) {
        return -1;
    }
    return sfd;
}

int make_socket_non_blocking (int sfd) {
    int flags = fcntl (sfd, F_GETFL, 0);
    if (flags == -1) {
        return -1;
    }
    if (fcntl(sfd, F_SETFL, flags | O_NONBLOCK) == -1) {
        return -1;
    }
    return 0;
}

/* 此函数用于读取参数或者错误提示 */
int read_param(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s [port]\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    return atoi(argv[1]);
}

int main (int argc, char *argv[]) {
    int sfd, s;
    int efd;
    struct epoll_event event;
    struct epoll_event *events;

    int port = read_param(argc, argv);

    /* 创建并绑定socket */
    sfd = create_and_bind(port);
    if (sfd == -1) {
        perror("create_and_bind");
        abort ();
    }

    /* 设置sfd为非阻塞 */
    s = make_socket_non_blocking(sfd);
    if (s == -1) {
        perror("make_socket_non_blocking");
        abort();
    }

    /* SOMAXCONN 为系统默认的backlog */
    s = listen(sfd, SOMAXCONN);
    if (s == -1) {
        perror("listen");
        abort();
    }

    efd = epoll_create1(0);
    if (efd == -1) {
        perror("epoll_create");
        abort();
    }
    event.data.fd = sfd;
    /* 设置ET模式 */
    event.events = EPOLLIN | EPOLLET;
    s = epoll_ctl(efd, EPOLL_CTL_ADD, sfd, &event);
    if (s == -1) {
        perror("epoll_ctl");
        abort();
    }
    /* 创建事件数组并清零 */
    events = calloc(MAXEVENTS, sizeof(event));
    /* 开始事件循环 Event loop*/
    while (1) {
        int n, i;
        n = epoll_wait(efd, events, MAXEVENTS, -1);
        for (i = 0; i < n; i++) {
            if (events[i].events & (EPOLLERR | EPOLLHUP)) {
                /* 监控到错误或者挂起 */
                fprintf(stderr, "epoll error\n");
                close(events[i].data.fd);
                continue;
            }
            if (events[i].events & EPOLLIN) {
                if (sfd == events[i].data.fd) {
                    /* 处理新接入的socket */
                    while (1) {
                        struct sockaddr_in sa;
                        socklen_t len = sizeof(sa);
                        char hbuf[INET_ADDRSTRLEN];
                        int infd = accept (sfd, (struct sockaddr*)&sa, &len);
                        if (infd == -1) {
                            if ((errno == EAGAIN) || (errno == EWOULDBLOCK)) {
                                /* 资源暂时不可读，再来一遍 */
                                break;
                            } else {
                                perror("accept");
                                break;
                            }
                        }
                        inet_ntop(AF_INET, &sa.sin_addr, hbuf, sizeof(hbuf));
                        printf("Accepted connection on descriptor %d "
                               "(host=%s, port=%d)\n", infd, hbuf, ntohs(sa.sin_port));
                        /* 设置接入的socket为非阻塞 */
                        s = make_socket_non_blocking(infd);
                        if (s == -1)
                            abort();
                        /* 为新接入的socket注册事件 */
                        event.data.fd = infd;
                        event.events = EPOLLIN | EPOLLET;
                        s = epoll_ctl(efd, EPOLL_CTL_ADD, infd, &event);
                        if (s == -1) {
                            perror("epoll_ctl");
                            abort();
                        }
                    }
                    // continue;
                } else {
                    /* 接入的socket有数据可读 */
                    while (1) {
                        ssize_t count;
                        char buf[512];
                        count = read(events[i].data.fd, buf, sizeof(buf));
                        if (count == -1) {
                            if (errno != EAGAIN) {
                                perror("read");
                                close(events[i].data.fd);
                            }
                            break;
                        } else if (count == 0) {
                            /* 数据读取完毕，结束 */
                            close(events[i].data.fd);
                            printf("Closed connection on descriptor %d\n", events[i].data.fd);
                            break;
                        }
                        /* 输出到stdout */
                        s = write(1, buf, count);
                        if (s == -1) {
                            perror("write");
                            abort();
                        }
                        event.events = EPOLLOUT | EPOLLET;
                        epoll_ctl(efd, EPOLL_CTL_MOD, events[i].data.fd, &event);
                    }
                    // continue;
                }
            } else if (events[i].events & EPOLLOUT) {
                if (events[i].data.fd != sfd) {
                    /* 接入的socket有数据可写 */
                    write(events[i].data.fd, "it's echo man\n", 14);
                    event.events = EPOLLET | EPOLLIN;
                    epoll_ctl(efd, EPOLL_CTL_MOD, events[i].data.fd, &event);
                    // continue;
                }
            }
        }
    }
    free(events);
    close(sfd);
    return EXIT_SUCCESS;
}
```

我们可以通过ncat命令和它聊天：

```markdown
$ ncat 127.0.0.1 8000
hello
it's echo man
```

ncat和echo_man通信的时候其实用的是长连接（除非我们自己CTRL+C）。对于长连接需要一定的处理策略。一般而言，我们会采用如下几种策略来处理：

+ 心跳，通过这个来表示长连接有效，没有了心跳自然就表示结束
+ 特殊字符，标记数据传输完毕
+ 协议中添加length，这个比较常规
+ 设置timeout，超过这个threshold就关闭半连接或者全连接

总之，长连接绝对是个好东西，在很大程度上避免了建立和关闭TCP连接时握手带来的延迟，不过，想要让服务端一直持有长连接也是有点理想化。

## echo man代码分析

`main()`首先调用`create_and_bind()`来新建一个socket。然后将其设置为非阻塞`make_socket_non_blocking()`，再调用 `listen()`。之后，我们新建一个epoll实例`efd`，并将监听套接字`sfd`以采用边沿触发的方式加入它，用以监听输入事件。
在外面的while循环是主要的事件循环(Event loop)。它调用`epoll_wait()`，它所在线程以阻塞的方式来等待事件的到来。当事件就绪，`epoll_wait()`在其`epoll_event`类型的参数中返回相应的事件。

其中，**事件循环**有很多讨论情况。当我们添加新的传入连接，当他们终止时我们删除现有的连接，epoll 的实例 `efd` 的事件循环不断更新。
当事件的状态为可用的时候，他们有以下三种类型：
**错误**：当错误情况发生时，或者事件是不是一个有关数据可以被读取的通知，我们只需关闭相关的描述符。关闭描述符会自动移除其 epoll 实例 `efd`。
**新的连接**：当监听到 descriptor `sfd` 已经准备好用于读取的时候，这意味着已经到达一个或多个新的连接。当有新连接时，`accept()`连接`infd`，打印关于连接的信息，并设置 socket `infd` 非阻塞，并将其添加到 epoll 实例 `efd` 监听事件。
**客户端数据**：当数据在客户端描述符上为可读状态，我们在 `read()` 中使用 while 循环来读去存储在512位数据块`buf`中的数据。这是因为我们现在要读取所有可用的数据，在 edge-triggered 模式下，我们不会进一步获取事件描述符。使用 `write()` 将读取的数据被写入到 stdout (fd=1)，如果 `read()` 返回 0，这意味着到达了一个 EOF(End of File)，这时我们就可以断开与客户端的连接。如果 `read()` 返回 -1，errno 为 EAGAIN，这意味着该事件所有的数据已读完，我们可以返回主循环了。

就是这样，它在一个循环中一遍又一遍地执行，在监听的集合中添加和删除描述。

## EPOLLONESHOT事件

实际多线程开发过程中容易出现这样的一个问题，对于一个socket发送过来的数据只希望被同一个线程所处理在这种情况下，如果一个线程使用ET模式接收到客户发送过来的数据，当这个线程正在处理数据的时候，这个客户再次发送数据此时这个数据被另外一个线程接收进行处理，这就导致了一个客户的数据被两个线程处理的尴尬局面。epoll中的`EPOLLONESHOT`事件可以很好的解决这个问题，当socket描述符注册了`EPOLLONESHOT`事件那么当一次事件触发后下次需要重新给这个socket设置事件。

## 小结

+ 只返回就绪的描述符
+ 支持边缘触发和水平触发
+ 支持更多的事件类型
+ 使用回调机制检测就绪事件(复杂度O(1))，而不是poll和select中的轮询机制(复杂度O(n))

这就是epoll简单应用的全部内容了，当然一旦涉及多线程和多进程，那么这种场景下处理epoll会变得极其有趣。
