#!/usr/bin/env python
# coding: utf-8
#
# Author: Takahiro Endo (m.tkhren@gmail.com)
# License: MIT License
# Created: 2013-12-14
#
# お金の計算
#


# 単利計算
# principal : 元本
# rate : 利率（百分率）
# duration : 期間（年、月、日数）
def simple_interest(principal=1., rate=0.01, duration=10):
    """
        Calcurate a simple interest with the `principal',
        the interest `rate' and the `duration'.

        simple interest
            = principal * (1 + rate * duration)

        >>> simple_interest(300, 0.02, 10)
        360.0
    """
    return principal * (1. + rate * duration)


# 複利計算
def compound_interest(principal=1., rate=0.01, duration=10):
    """
        Calcurate a compound interest with the `principal',
        the compound `rate' and the `duration'.

        compound interest
            = principal * (1 + rate)^duration

        >>> compound_interest(300, 0.02, 10)
        365.6983259984272
    """
    return principal * pow(1. + rate, duration)



if __name__ == '__main__':
    import sys
    main(sys.argv)

# vim: ft=python fenc=utf-8 ff=unix :
