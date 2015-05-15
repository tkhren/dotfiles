# coding: utf-8

import random
import cmath
import fractions
import functools

# 虚部が無い、つまり実数ならば True を返す.
def isreal(z):
    return z.imag == 0

# n乗根のリストを返す. 複素数のリストになる.
def nth_root(z, n):
    if not isinstance(n, int):
        raise TypeError('The given `n\' must be an integer.')
    if n <= 0:
        raise ValueError('The given `n\' must be a positive integer.')

    r, phi = cmath.polar(z)
    N = 1 / n
    a = 2 * cmath.pi
    zf = lambda k: pow(r,N) * cmath.exp(1j * (phi + a*k) * N)
    return [zf(k) for k in range(n)]

# n乗根の実数解を返す
def real_nth_root(x, n):
    if n == 0:
        raise ValueError('0th root is not defined')
    return pow(x, 1/n)

# 少数を有理化して分数にする.
# 文字列またはDecimalオブジェクトを引数として与える.
def rationalize(x, *args, **kwds):
    """
        Convert a float value into its corresponding fraction

        >>> rationalize('3.14')
        Fraction(157, 50)
    """
    return fractions.Fraction(x, *args, **kwds)

# 約数のリストを返す
def divisors(n):
    """
        List of its divisors

        >>> divisors(212)
        [1, 2, 4, 53, 106, 212]
    """
    return [i for i in range(1, n+1) if n % i == 0]

# 素因数のリストを返す
# 単純なアルゴリズムなので素因数が巨大なときは、時間がかかる
def primes(n):
    """
        List of prime numbers
        >>> primes(2124)
        [2, 2, 3, 3, 59]
    """
    ps = []

    (quo, rem) = divmod(n, 2)
    while n >= 4 and rem == 0:
        ps.append(2)
        n = quo
        (quo, rem) = divmod(n, 2)

    d = 3
    (quo, rem) = divmod(n, d)
    while quo >= d:
        if rem == 0:
            ps.append(d)
            n = quo
        else:
            d += 2
        (quo, rem) = divmod(n, d)

    ps.append(n)
    return ps

# 素数判定（失敗確率は 2^(-2k) ）
def isprime(n, k=50):
    """
        Test whether `n' is a prime using Miller-Rabin primality test.
        The fault rate is 1/(4^k).
    """
    # フェルマーの小定理
    #
    #       a**(n-1) mod n = 1 or (n-1)   ...(1)
    #
    # ここで, a と n が互いに素であれば、式(1)が成り立つ.
    # 入力された n が素数ならば、a はどんな数でも成り立つはずである.
    # しかし、aが擬素数の場合、この等式(1)は成り立たない.
    # そのため、aをランダムに変えて、試行することにより、素数かどうかを
    # 判定することが可能である.
    #
    # すべての整数 N は奇数 d ([1,N-1]) と 自然数 s ([0,n-1]) を用いると 次の形で表せる.
    #       N = 2**s * d   ...(2)
    #
    # ここで N = n-1 と置き、d, s を求める.
    #       n-1 = 2**s * d   ...(3)
    #
    # d は奇数であり、n-1 を 2 で割り続ければ求められる.
    # 割った回数が s である.
    #
    # 式(3)をフェルマーの定理に当てはめると, 式(4)が得られる.
    #       a**(2**s * d) mod n = 1       { s = 0 }           ...(4a)
    #       a**(2**s * d) mod n = (n-1)   { s = 1,2,...,n }   ...(4b)
    #
    # 0 <= r < s のいずれかにおいて, 式(4a) または 式(4b) が成り立つならば,
    # n は素数であると言える.
    #
    # ミラーラビンテストでは, この対偶を考える.
    # すなわち,
    #       a**(2**0 * d) mod n != 1   ...(5a)
    #
    # かつ, 任意の 0 <= r < s に関して
    #       a**(2**r * d) mod n != (n-1)   ...(5b)
    #
    # が成り立つものは合成数である. といえる.
    #
    # また, 奇素数 n と互いに素な y の平方剰余は 1 か n-1 である.
    #       y**2 mod n = 1 or (n-1)
    #

    # 2以外の偶数は素数にならないので弾く
    if n == 2: return True
    if n < 2 or n & 1 == 0: return False

    d_ = (n-1) >> 1
    while d_ & 1 == 0:
        d_ >>= 1

    # [1,n-1] の範囲内の数をランダムに選んで a とする.
    k = k if k < n else (n-2)
    randoms = random.sample(range(1, n-1), k)

    for a in randoms:
        d = d_
        y = pow(a, d, n)
        while d != n-1 and y != 1 and y != n-1:
            ## 平方剰余を求める.
            y = pow(y, 2, n)
            ## s 回左シフトすれば d は (n-1) に戻る.
            d <<= 1

        #  0 < r < s において y が (n-1) にならなかった場合、
        # n は必ず合成数である.
        #
        # (0 < r < s の時, シフトされているので d は必ず偶数である.)
        if y != n-1 and d & 1 == 0:
            return False

    return True

def _gcd(a, b):
    while b:
        a, b = b, a%b
    return a

# 最大公約数を求める
def gcd(xs):
    """
        Calcurate the greatest common divisor between the `a' and `b'.
        >>> gcd([32, 24])
        8
    """
    return functools.reduce(_gcd, xs)

# 最小公倍数を求める
def lcm(xs):
    """
        Calcurate the lowest common multiple between the `a' and `b'.
        >>> lcm([9, 12])
        36
    """
    return functools.reduce(lambda a,b: a*b / _gcd(a,b), xs)

# 幾何平均（相乗平均）を求める
def geometric_mean(xs):
    n = len(xs)
    if n == 0:
        raise ValueError('geometric_mean requires at least one data point')
    p = functools.reduce(lambda y,z: y*z, xs)
    return pow(p, 1/n)

# 算術平均（ただの平均）を求める
def arithmetic_mean(xs):
    n = len(xs)
    if n == 0:
        raise ValueError('arithmetic_mean requires at least one data point')
    return sum(xs) / n

mean = arithmetic_mean

# 中央値を求める
def median(xs):
    n = len(xs)
    if n == 0:
        raise ValueError('no median for empty data')
    if n%2 == 1:
        return sorted(xs)[n//2]
    else:
        i = n//2
        xs = sorted(xs)
        return (xs[i-1] + xs[i]) / 2

# 中央値を求める
# 偶数個の時、小さい方の値を返す
def median_low(xs):
    n = len(xs)
    if n == 0:
        raise ValueError('no median for empty data')
    if n%2 == 1:
        return sorted(xs)[n//2]
    else:
        return sorted(xs)[n//2 - 1]

# 中央値を求める
# 偶数個の時、大きい方の値を返す
def median_high(xs):
    n = len(xs)
    if n == 0:
        raise ValueError('no median for empty data')
    return sorted(xs)[n//2]

# 最頻値を求める
def mode(xs):
    n = len(xs)
    if n == 0:
        raise ValueError('no mode for empty data')

    table = collections.Counter(xs).most_common()
    if table:
        return table[0][0]

# カウントリストを返す
def count(xs, n=None):
    return collections.Counter(xs).most_common(n)

# 温度単位の相互変換
def C2K(celsius): return celsius + 273.15
def K2C(kelvin): return kelvin - 273.15
def C2F(celsius): return (9/5) * celsius + 32
def F2C(fahrenheit): return (5/9) * (fahrenheit - 32)
def F2K(fahrenheit): return C2K(F2C(fahrenheit))
def K2F(kelvin): return C2F(K2C(kelvin))

if __name__=="__main__":
    import doctest
    doctest.testmod()

# vim: ft=python fenc=utf-8 ff=unix
