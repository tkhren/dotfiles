# coding: utf-8

def fibonacci():
    """
        Generator of Fibonacci sequence

        >>> [n for i,n in zip(range(15), fibonacci())]
        [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    """
    a = b = 1
    while True:
        yield a
        a, b = b, a+b

def ackermann(x, y):
    """
        Ackermann function
    """
    # すごい勢いで発散するので実行には注意が必要
    # RuntimeError が発生するのはほぼ確実
    # 実用性は皆無
    if x == 0: return y + 1
    if y == 0: return ackermann(x-1, 1)
    return ackermann(x-1, ackermann(x, y-1))

def permutation(n, k):
    """
        Permutation nPk
            = n! / (n-k)!
            = n(n-1)(n-2)...(n-k+1)
        where
            The positive integers n and k must be n > k.

        >>> [permutation(5,i) for i in range(5)]
        [1, 5, 20, 60, 120]
    """
    return math.factorial(n) / math.factorial(n-k)


def combination(n, k):
    """
        Combination nCk
            = n! / k!(n-k)!
            = ( n(n-1)...(n-k+1) ) / ( k(k-1)...1 )
        where
            The positive integers n and k must be n > k.

        >>> [combination(5,i) for i in range(6)]
        [1, 5, 10, 10, 5, 1]
    """
    if k == 0: return 1
    return permutation(n, k) / math.factorial(k)


def repeated_combination(n, k):
    """
        Repeated Combination nHk
            = nCk (n+k-1, k)
            = (n+k-1)! / k!(n-1)!
        where
            The positive integers n and k must be n > k.

        >>> [repeated_combination(5,i) for i in range(6)]
        [1, 5, 15, 35, 70, 126]
    """
    return combination(n+k-1, k)


def circular_permutation(n):
    # 円順列
    """
        Circular permutation
            = (n-1)!
    """
    return math.factorial(n-1)




if __name__=="__main__":
    import doctest
    doctest.testmod()

# vim: ft=python fenc=utf-8 ff=unix
