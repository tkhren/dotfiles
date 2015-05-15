# coding: utf-8

class Base10(int):
    """Utility class for a number of base-10
    Constructor:
        Base10(dicimal_number)          # Base10(8128)
        Base10(baseN_string, base=n)    # Base10('021', 3)
    """

    chars32 = '0123456789abcdefghijklmnopqrstuv'
    chars64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

#    def __add__(self, other): return Base10(self._decimal + other)
#    def __radd__(self, other): return Base10(other + self._decimal)
#    def __sub__(self, other): return Base10(self._decimal - other)
#    def __rsub__(self, other): return Base10(other - self._decimal)
#    def __mul__(self, other): return Base10(self._decimal * other)
#    def __rmul__(self, other): return Base10(other * self._decimal)
#    def __truediv__(self, other): return Base10(self._decimal / other)
#    def __rtruediv__(self, other): return Base10(other / self._decimal)
#    def __pow__(self, other): return Base10(self._decimal ** other)
#
    def __init__(self, number, base=0):
        if isinstance(number, str):
            self._decimal = int(number, base)
        else:
            self._decimal = int(number)
        self.base10 = str(self._decimal)

        self._cache_base = {}

    def __repr__(self):
        return "Base10(%s)" % self.base10

    def __str__(self):
        return self.base10

    @property
    def base2(self):
        return self.baseN(2)

    @property
    def base8(self):
        return self.baseN(8)

    @property
    def base16(self):
        return self.baseN(16)


    def baseN(self, n, chars=None):
        """Returns a string of the base-N number.
        The decimal `n` must be gigger than 2.
        If `n` is bigger than 64, you need to replace the `chars`
        an alternative longer strings to stands for all base-N
        numbers.
        >>> d12 = Base10(12)
        >>> d12.base2     # conversion to a binary system
        '1100'
        >>> d12.base16    # conversion to a hex system
        'c'
        >>> d12.baseN(3)  # conversion to a base-3 system
        '110'
        """
        key = (n, chars)
        try:
            return self._cache_base[key]
        except KeyError:
            pass

        if chars is None:
            chars = self.chars32 if (n < 33) else self.chars64

        if n > len(chars):
            raise ValueError("There is insufficient characters in "
                             "order to be expessed as a base-N number.")
        if n < 2:
            raise ValueError("The base-%d system does not exist. "
                             "The `n` must be bigger than 1." % n)

        if self._decimal == 0:
            return chars[0]

        _baseN = []
        _quo = self._decimal

        while _quo > 0:
            (_quo, _rem) = divmod(_quo, n)
            _baseN.append(chars[_rem])

        _baseN.reverse()

        return self._cache_base.setdefault(key, ''.join(_baseN))


# vim: ft=python fenc=utf-8 ff=unix
