# coding: utf-8
# Utilities for List, Tuple, Iterator, String, Range ...

import collections

from itertools import *

# zip() したシーケンスを元のリストに変換する.
def unzip(*iterables):
    """
        zipped = zip(seq1, seq2, seq3)
        (seq1, seq2, seq3) == unzip( *zipped )

        >>> unzip((1,2,3,4), (10,20,30,400), (100,200,300,400))
        ([1, 10, 100], [2, 20, 200], [3, 30, 300], [4, 40, 400])
    """
    if not iterables: return tuple()
    size = len(iterables[0])
    res = [[] for x in range(size)]
    for t in iterables:
        for i, part in enumerate(t):
            res[i].append(part)

    return tuple(res)

# ネストしたリストを一つのリストにするジェネレータ
def flatten(lst):
    """
        Flatten the nested list

        >>> list( flatten([1,[21,22],3,[41,[421,422],43,44],5]) )
        [1, 21, 22, 3, 41, 421, 422, 43, 44, 5]
    """
    if isinstance(lst, list):
        for i in range(len(lst)):
            for e in flatten(lst[i]):
                yield e
    else:
        yield lst

# シーケンスの先頭の要素を n 個分 インデックス付きで取り出す.
# n が負なら末尾からの要素を返す.
def take(iterable, n):
    """
        Return first n items of the iterable with its indices

        >>> list(take([0,1,4,9,16,25,36,49,64,81], 5))
        [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
    """
    iterated = iter if n >= 0 else reversed
    return zip(range(n), iterated(iterable))

# シーケンスの先頭の要素を n 個分取り出す.
def head(iterable, n):
    """
        Return first n items of the iterable

        >>> list(head(range(100), 7))
        [0, 1, 2, 3, 4, 5, 6]
    """
    return (item for i, item in zip(range(n), iter(iterable)))

# シーケンスの末尾の要素を n 個分取り出す.
def tail(iterable, n):
    """
        Return last n items of the list

        >>> gen = (i*i for i in range(1293))
        >>> list(tail(gen, 7))
        [1293, 1292, 1291, 1290, 1289, 1288, 1287]
    """
    return (item for i, item in zip(range(n), reversed(iterable)))

# 重複を除いたリストを返す. 順序は保持される.
def uniqued(iterable):
    """
        Return unique items in the sequence

        >>> list(uniqued([1,3,4,0,3,2,4,1,1]))
        [1, 3, 4, 0, 2]
    """
    return sorted(set(sequence), key=sequence.index)

# n 個ずつ切り出して行くイテレータ
def multiwise(iterable, n):
    """
        >>> list(multiwise([1, 2, 3, 4, 5], 2))
        [(1, 2), (2, 3), (3, 4), (4, 5)]
    """
    deque = collections.deque([], maxlen=n)
    for x in iterable:
        deque.append(x)
        if len(deque) >= n:
            yield tuple(deque)


# 同じイテレータを n 回繰り返すイテレータ
def ncycles(iterable, n):
    """
        Return items of the iterable n times
    """
    saved = []
    for element in iterable:
        yield element
        saved.append(element)

    if saved:
        for i in range(n):
            for element in saved:
                yield element

# 与えられたシーケンスを順番にひとつずつピックアップしていくイテレータ
def roundrobin(iterable):
    """
        >>> list(roundrobin('ABC', 'D', 'EF'))
        ['A', 'D', 'E', 'B', 'F', 'C']
    """
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


if __name__=="__main__":
    import doctest
    doctest.testmod()
