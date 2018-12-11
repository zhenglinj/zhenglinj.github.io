# !/bin/env python3
# http://code.activestate.com/recipes/474088/
from tail_recursion import tail_call_optimized

@tail_call_optimized
def Fib(n,b1=1,b2=1,c=3):
    if n<3:
        return 1
    else:
        if n==c:
            return b1+b2
        else:
            return Fib(n,b1=b2,b2=b1+b2,c=c+1)

Fib(10)
