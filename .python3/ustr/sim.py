# coding: utf-8

from __future__ import division
import math
import difflib

__all__ = [
    'ngram',
    'bigram',
    'trigram',
    'lcs_set',
    'similarity'
    'jaccard_index',
    'simpson_index',
    'cosine_index',
    'dice_index',
]

def ngram(s, n):
    return set(s[i:i+n] for i in range(len(s) - 1))

def bigram(s):
    return ngram(s, 2)

def trigram(s):
    return ngram(s, 3)


# 最長共通部分文字列の集合を求める
def lcs_set(s1, s2):
    """
        Return the set of the Longest Common s1ubstring (LCs1)
        between the sequence `s1' and `s2'.
    """
    lcsset = set()
    num = [[0] * (len(s2)+1) for i in range(len(s1) + 1)]
    longest = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                v = num[i][j] + 1
                num[i+1][j+1] = v
                if v > longest:
                    longest = v
                    lcsset = set()
                if v == longest:
                    if type(s1) is list:
                        lcsset.add( tuple(s1[i-v+1:i+1]) )
                    else:
                        lcsset.add( s1[i-v+1:i+1] )
    return lcsset


# ジャッカード類似度係数を求める
def jaccard_index(aset1, aset2):
    """
        The Jaccard index, also known as the Jaccard similarity coefficient,
        is a statistic used for comparing the similarity and diversity of
        sample sets.

        Jaccard index between X and Y
            = |X ^ Y| / |X v Y|
    """
    if not aset1 and not aset2:
        return 1.00

    overlap = len(aset1 & aset2)
    union   = len(aset1 | aset2)

    return overlap / union


# ダイス類似度係数を求める
def dice_index(aset1, aset2):
    """
        The Dice's coefficient is a degree of similarity
        between the `aset1' and the `aset2'.

        Dice coefficient between X and Y
            = 2 * |X ^ Y| / (|X| + |Y|)
    """
    if not aset1 and not aset2:
        return 1.00

    overlap = len(aset1 & aset2)
    total = len(aset1) + len(aset2)

    return 2 * overlap / total

# オーバーラップ類似度係数を求める
def overlap_index(aset1, aset2):
    """
        The Overlap coefficient is a degree of similarity
        between the `aset1' and the `aset2'.

        Overlap coefficient between X and Y
            = 2 * |X ^ Y| / min(|X|, |Y|)
    """
    if not aset1 and not aset2:
        return 1.00

    overlap = len(aset1 & aset2)
    minimum = min(len(aset1), len(aset2))

    return 2 * overlap / minimum


# シンプソン類似度係数を求める
def simpson_index(aset1, aset2):
    """
        The Simpson's diversity index, also known as the Simpson's
        coefficient, is a statistic used for comparing the similarity
        and diversity of sample sets.

        Simpson's diversity index between X and Y
            = |X ^ Y| / min(|X|, |Y|)
    """
    if not aset1 and not aset2:
        return 1.00

    overlap = len(aset1 & aset2)
    minimum = min(len(aset1), len(aset2))

    return overlap / minimum


# コサイン類似度を求める
def cosine_index(aset1, aset2):
    """
        The cosine similarity between two strings.

        cosine similarity between X and Y
            = |X ^ Y| / sqrt(|X| * |Y|)
    """
    if not aset1 and not aset2:
        return 1.00

    overlap = len(aset1 & aset2)
    norms   = math.sqrt(len(aset1) * len(aset2))

    return overlap / norms


# 文字列の類似度を測定 (python difflib を使用)
# 一番それっぽい結果が返ってくる
def similarity(s1, s2):
    """
        Return the cosine similarity between `s1' and `s2'
        using difflib.SequenceMatcher().
    """
    smo = difflib.SequenceMatcher(None, s1, s2)
    return smo.ratio()


if __name__ == '__main__':
    import unittest

    class StrSimTest(unittest.TestCase):
        def test_lcs_set(self):
            return
            cases = [('', '', 1.000),
                     ('a', 'b', 1.000),
                     ('abcd', 'abcd', 1.000),
                     ('abcd', 'a@cd', 0.200),
                     ('abcd', 'bdac', 0.000),
                     ('abcdefg', 'babcdfa', 0.333),
                     ('sunday', 'saturday', 0.200),
                    ]

            for (s1, s2, value) in cases:
                aset1, aset2 = bigram(s1), bigram(s2)
                self.assertAlmostEqual( lcs_set(aset1, aset2), value, places=3)

        def test_jaccard_index(self):
            cases = [('', '', 1.000),
                     ('a', 'b', 1.000),
                     ('abcd', 'abcd', 1.000),
                     ('abcd', 'a@cd', 0.200),
                     ('abcd', 'bdac', 0.000),
                     ('abcdefg', 'babcdfa', 0.333),
                     ('sunday', 'saturday', 0.200),
                    ]

            for (s1, s2, value) in cases:
                aset1, aset2 = bigram(s1), bigram(s2)
                self.assertAlmostEqual( jaccard_index(aset1, aset2), value, places=3)

        def test_dice_index(self):
            cases = [('', '', 1.000),
                     ('a', 'b', 1.000),
                     ('abcd', 'abcd', 1.000),
                     ('abcd', 'a@cd', 0.333),
                     ('abcd', 'bdac', 0.000),
                     ('abcdefg', 'babcdfa', 0.500),
                     ('sunday', 'saturday', 0.333),
                    ]

            for (s1, s2, value) in cases:
                aset1, aset2 = bigram(s1), bigram(s2)
                self.assertAlmostEqual( dice_index(aset1, aset2), value, places=3)

        def test_overlap_index(self):
            cases = [('', '', 1.000),
                     ('a', 'b', 1.000),
                     ('abcd', 'abcd', 2.000),
                     ('abcd', 'a@cd', 0.667),
                     ('abcd', 'bdac', 0.000),
                     ('abcdefg', 'babcdfa', 1.00),
                     ('sunday', 'saturday', 0.800),
                    ]

            for (s1, s2, value) in cases:
                aset1, aset2 = bigram(s1), bigram(s2)
                self.assertAlmostEqual( overlap_index(aset1, aset2), value, places=3)

        def test_simpson_index(self):
            cases = [('', '', 1.000),
                     ('a', 'b', 1.000),
                     ('abcd', 'abcd', 1.000),
                     ('abcd', 'a@cd', 0.333),
                     ('abcd', 'bdac', 0.000),
                     ('abcdefg', 'babcdfa', 0.500),
                     ('sunday', 'saturday', 0.400),
                    ]

            for (s1, s2, value) in cases:
                aset1, aset2 = bigram(s1), bigram(s2)
                self.assertAlmostEqual( simpson_index(aset1, aset2), value, places=3)

        def test_cosine_index(self):
            cases = [('', '', 1.000),
                     ('a', 'b', 1.000),
                     ('abcd', 'abcd', 1.000),
                     ('abcd', 'a@cd', 0.333),
                     ('abcd', 'bdac', 0.000),
                     ('abcdefg', 'babcdfa', 0.500),
                     ('sunday', 'saturday', 0.338),
                    ]

            for (s1, s2, value) in cases:
                aset1, aset2 = bigram(s1), bigram(s2)
                self.assertAlmostEqual( cosine_index(aset1, aset2), value, places=3)

    unittest.main()


# vim: ft=python fenc=utf-8 ff=unix
