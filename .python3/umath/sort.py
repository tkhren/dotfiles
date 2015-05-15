# coding: utf-8
#
# ソートアルゴリズム
#  勉強のため。パフォーマンスは list.sort() よりも低い


# バブルソート
def bubble_sort(array):
    u"""
        Bubble sort algorithm:
            Average: -
            Slowest: O( n^2 )
            Stability: stable
    """
    rest_size = len(array) - 1
    while rest_size > 0:
        for i in range(rest_size):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
        rest_size -= 1


# シェーカーソート（バブルソートの改良）
def shaker_sort(array):
    u"""
        Shaker sort algorithm:
            Average: -
            Slowest: O( n^2 )
            Stability: stable
    """
    start = 0
    end = len(array) - 1
    j = -1
    while start < end:
        for i in range(start, end):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                j = i
        end = j

        for i in range(end, start, -1):
            if array[i-1] > array[i]:
                array[i-1], array[i] = array[i], array[i-1]
                j = i
        start = j


# コムソート（バブルソートの改良）
def comb_sort(array):
    u"""
        Comb sort algorithm:
            Average: O( n log n )
            Slowest: O( n log n )
            Stability: stable
    """
    array_size = len(array)
    gap = array_size
    done = False
    while gap > 1 or not done:
        gap = (gap * 10) / 13   # 櫛の間隔を (要素数 / 1.3) にすると高速（経験則）
        if gap == 0:
            gap = 1   # 櫛の間隔が 1 の時は bubble sort と同じ
        elif gap == 9 or gap == 10:
            gap = 11  # 櫛の間隔が 9 か 10 の時は間隔を 11 にすると高速（経験則）
        done = True

        for i in range(array_size - gap):
            if array[i] > array[i + gap]:
                array[i], array[i + gap] = array[i + gap], array[i]
                done = False


# 挿入ソート
def insertion_sort(array):
    u"""
        Insertion sort algorithm:
            Average: O( n + d )
            Slowest: O( n^2 )
            Stability: stable
    """
    array_size = len(array)
    for i in range(1, array_size):
        tmp = array[i]
        j = i
        while j > 0 and array[j-1] > tmp:
            array[j] = array[j-1]
            j -= 1
        array[j] = tmp


# シェルソート（挿入ソートの改良）
def shell_sort(array):
    u"""
        Shell sort algorithm:
            Average: -
            Slowest: O( n log^2 n )
            Stability: unstable
    """
    array_size = len(array)
    gap = array_size / 2
    while gap > 0:
        for i in range(gap, array_size):
            tmp = array[i]
            j = i - gap
            while j >= 0 and array[j] > tmp:
                array[j + gap] = array[j]
                j -= gap
            array[j + gap] = tmp
        gap /= 2

# シェルソート（Knuth の改良法）
# gap = ..., 121, 40, 13, 4, 1
def shell_sort_knuth(array):
    u"""
        Shell sort algorithm (Knuth's improvement):
            Average: -
            Slowest: O( n log^2 n )
            Stability: unstable
    """
    array_size = len(array)
    gap = 1
    while gap < array_size / 9:
        gap = gap * 3 + 1

    while gap > 0:
        for i in range(gap, array_size):
            tmp = array[i]
            j = i - gap
            while j >= 0 and array[j] > tmp:
                array[j + gap] = array[j]
                j -= gap
            array[j + gap] = tmp
        gap /= 3


# クイックソート（再帰版）
def quick_sort(array):
    u"""
        Quick sort algorithm (Recursive version):
            Average: O( n log n )
            Slowest: O( n^2 )
            Stability: unstable
    """
    if len(array) <= 1:
        return array

    pivot = array[0]
    return quick_sort([x for x in array[1:] if x < pivot]) \
            + [pivot] \
            + quick_sort([x for x in array[1:] if x >= pivot])


# クイックソート（非再帰版）
def quick_sort_non_recursive(array):
    u"""
        Quick sort algorithm (Non-recursive version):
            Average: O( n log n )
            Slowest: O( n^2 )
            Stability: unstable
    """
    start = 0
    end = len(array) - 1

    stack = []
    while True:
        if end - start < 32:
            if len(stack) == 0:
                break
            start, end = stack.pop()
        else:
            pivot = array[(start+end)/2]
            i, j = start, end

            while True:
                while pivot > array[i]: i += 1
                while pivot < array[j]: j -= 1

                if i >= j:
                    break

                array[i], array[j] = array[j], array[i]
                i += 1
                j -= 1

            if (i - start) > (end - j):
                stack.append( (start, i-1) )
                start = j + 1
            else:
                stack.append( (j+1, end) )
                end = i - 1
    insertion_sort(array)


# ヒープソート
def _down_heap(array, l, r):
    tmp = array[l]
    parent = l

    while parent < (r + 1) / 2:
        cl = parent * 2 + 1
        cr = cl + 1
        if cr <= r and array[cl] < array[cr]:
            child = cr
        else:
            child = cl
        if tmp >= array[child]:
            break
        array[parent] = array[child]
        parent = child
    array[parent] = tmp

def heap_sort(array):
    array_size = len(array) - 1
    for i in range(array_size / 2, -1, -1):
        _down_heap(array, i, array_size)

    for i in range(array_size, 0, -1):
        array[0], array[i] = array[i], array[0]
        _down_heap(array, 0, i-1)


# 選択ソート
def selection_sort(array):
    u"""
        Selection sort algorithm:
            Average: O( n^2 )
            Slowest: O( n^2 )
            Stability: unstable
    """
    array_size = len(array)
    for i in range(array_size):
        mini = i
        for j in range(i + 1, array_size):
            if array[j] < array[mini]:
                mini = j
        if i != mini:
            array[i], array[mini] = array[mini], array[i]


# マージソート（再帰版）
def _merge(array, start, mid, end):
    buff = []
    i = start
    j = mid + 1
    while i <= mid and j <= end:
        if array[i] > array[j]:
            buff.append(array[j])
            j += 1
        else:
            buff.append(array[i])
            i += 1
    while i <= mid:
        buff.append(array[i])
        i += 1
    while j <= end:
        buff.append(array[j])
        j += 1

    for k in range(0, end - start + 1):
        array[start + k] = buff[k]

def _merge_sort_r(array, start, end):
    u"""
        Merge sort algorithm (recursive version):
            Average: O( n log n )
            Sstartest: O( n log n ) Stability: stable
    """
    if end - start < 32:
        # 挿入ソート
        for i in range(start + 1, end + 1):
            tmp = array[i]
            j = i - 1
            while j >= start and tmp < array[j]:
                if tmp >= array[j]:
                    break
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = tmp
    else:
        mid = (start + end) / 2
        _merge_sort_r(array, start, mid)
        _merge_sort_r(array, mid + 1, end)
        _merge(array, start, mid, end)

def merge_sort(array):
    u"""
        Merge sort algorithm (recursive version):
            Average: O( n log n )
            Sstartest: O( n log n ) Stability: stable
    """
    _merge_sort_r(array, 0, len(array)-1)


# イントロソート（クイックソート + ヒープソート）
def intro_sort(array):
    u"""
        Intro sort algorithm:
            Average: O( n log n )
            Slowest: O( n log n )
            Stability: unstable
    """
    start = 0
    end = len(array) - 1

    stack = []
    while True:
        if end - start < 32:
            if len(stack) == 0:
                comb_sort(array)
                break
            start, end = stack.pop()
        else:
            pivot = array[(start+end)/2]
            i, j = start, end

            while True:
                while pivot > array[i]: i += 1
                while pivot < array[j]: j -= 1

                if i >= j:
                    break

                array[i], array[j] = array[j], array[i]
                i += 1
                j -= 1

            if (i - start) > (end - j):
                stack.append( (start, i-1) )
                start = j + 1
            else:
                stack.append( (j+1, end) )
                end = i - 1



# ティムソート（クイックソート + マージソート）
def tim_sort(array):
    u"""
        Tim sort algorithm:
            Average: O( n log n )
            Slowest: O( n log n )
            Stability: unstable
    """
    pass


if __name__ == '__main__':
    import random
    import copy
    from benchmarker import Benchmarker

    sorted_list = range(1000)
    random_list = range(1000)
    random.shuffle(random_list)

    with Benchmarker() as bm:
        biglist = copy.deepcopy(random_list)
        with bm('Bubble'):
            bubble_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Shaker'):
            shaker_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Insertion'):
            insertion_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Shell'):
            shell_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Shell (Knuth)'):
            shell_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Comb'):
            comb_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Quick (non-recursive)'):
            quick_sort_non_recursive(biglist)
        assert biglist == sorted_list

        #biglist = copy.deepcopy(random_list)
        #with bm('Quick (recursive)'):
            #biglist = quick_sort(biglist)
        #assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Heap'):
            heap_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Selection'):
            selection_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Merge (recursive)'):
            merge_sort(biglist)
        assert biglist == sorted_list

        biglist = copy.deepcopy(random_list)
        with bm('Intro'):
            intro_sort(biglist)
        assert biglist == sorted_list

        #biglist = copy.deepcopy(random_list)
        #with bm('Builtin list.sort()'):
            #biglist.sort()
        #assert biglist == sorted_list







# vim: ft=python fenc=utf-8 ff=unix
