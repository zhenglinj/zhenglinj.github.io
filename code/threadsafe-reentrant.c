/*
  试验方法:
  1. 编译 gcc test.c -lpthread
  在一个终端中运行 ./a.out, 在另一个终端中运行 ps -A|grep a.out可以看到该进程的id
  2. 进行下面4次运行a.out:
  每次运行分别在第1,2,3,4次回车前,在另外一个终端中运行kill -14 pid (这里的pid是上面ps中看到的值)

  试验结果:
  1. 该进程中有3个线程:一个主线程,两个子线程
  2. func_s是thread safe的
  3. func_s不是reentrant的
  4. 信号处理程序会中断主线程的执行,不会中断子线程的执行
  5. 在第1,4次回车前,在另外一个终端中运行kill -14 pid会形成死锁,这是因为
  主线程先锁住了临界区,主线程被中断后,执行handler(以主线程执行),handler试图锁定临界区时,
  由于同一个线程锁定两次,所以形成死锁
  6. 在第2,3次回车前,在另外一个终端中运行kill -14 pid不会形成死锁,这是因为一个子线程先锁住
  了临界区,主线程被中断后,执行handler(以主线程执行),handler试图锁定临界区时,被挂起,这时,子线程
  可以被继续执行.当该子线程释放掉锁以后,handler和另外一个子线程可以竞争进入临界区,然后继续执行.
  所以不会形成死锁.

  结论:
  1. reentrant是对函数相当严格的要求,绝大部分函数都不是reentrant的(APUE上有一个reentrant函数
  的列表).
  什么时候我们需要reentrant函数呢?只有一个函数需要在同一个线程中需要进入两次以上,我们才需要
  reentrant函数.这些情况主要是异步信号处理,递归函数等等.(non-reentrant的递归函数也不一定会
  出错,出不出错取决于你怎么定义和使用该函数). 大部分时候,我们并不需要函数是reentrant的.

  2. 在多线程环境当中,只要求多个线程可以同时调用一个函数时,该函数只要是thread safe的就可以了.
  我们常见的大部分函数都是thread safe的,不确定的话请查阅相关文档.

  3. reentrant和thread safe的本质的区别就在于,reentrant函数要求即使在同一个线程中任意地进入两次以上,
  也能正确执行.

  大家常用的malloc函数是一个典型的non-reentrant但是是thread safe函数,这就说明,我们可以方便的
  在多个线程中同时调用malloc,但是,如果将malloc函数放入信号处理函数中去,这是一件很危险的事情.

  4. reentrant函数肯定是thread safe函数,也就是说,non thread safe肯定是non-reentrant函数
  不能简单的通过加锁,来使得non-reentrant函数变成 reentrant函数
  这个链接是说明一些non-reentrant ===> reentrant和non thread safe ===>thread safe转换的
  http://www.unet.univie.ac.at/aix/aixprggd/genprogc/writing_reentrant_thread_safe_code.htm
*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <signal.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

pthread_mutex_t sharedMutex=PTHREAD_MUTEX_INITIALIZER;

int count;        /*共享数据*/

void* func_s (void* unused)
{
    pthread_mutex_lock(&sharedMutex);    /*进入临界区*/
    printf("locked by thead %d\n", pthread_self());
    if (count == 0)
        count++;
    getchar();
    pthread_mutex_unlock(&sharedMutex);  /*离开临界区*/
    printf("lock released by thead %d\n", pthread_self());
}

void handler (int signal_number)        /*处理SIGALRM信号*/
{
    printf("handler running in %d\n", pthread_self());
    func_s(NULL);
}


int main ()
{
    pthread_t pid1, pid2;
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = &handler;
    sigaction(SIGALRM, &sa, NULL);
    printf("main thread's pid is: %d\n", pthread_self());
    func_s(NULL);
    pthread_create(&pid1, NULL, &func_s, NULL);
    pthread_create(&pid2, NULL, &func_s, NULL);
    pthread_join(pid1, NULL);
    pthread_join(pid2, NULL);
    func_s(NULL);
    return 0;
}
