# coding: utf-8

__all__ = [
    'levenshtein_distance',
    'damerau_levenshtein_distance',
    'hamming_distance',
    'jaro_distance',
    'jaro_winkler_distance',
]


# リーベンシュテイン距離
def levenshtein_distance(s1, s2):
    """
        Return the Levenshtein distance between `s1' and `s2'
        using not-recursive algorithm.

        The Levenshtein distance between two strings is defined
        as the minimum number of edits needed to transform one
        string into the other, with the allowable edit operations
        being insertion, deletion, or substitution of a single
        character.
    """
    distance = {}

    for i in range(-1, len(s1) + 1):
        distance[(i, -1)] = i+1

    for j in range(-1, len(s2) + 1):
        distance[(-1, j)] = j+1

    for i, c1 in enumerate(s1):
        for j, c2 in enumerate(s2):
            cost = int(c1 != c2)
            distance[(i, j)] = min(
                    distance[(i-1, j)] + 1,
                    distance[(i, j-1)] + 1,
                    distance[(i-1, j-1)] + cost
            )

    return distance[len(s1)-1, len(s2)-1]


# ダメラウ・リーベンシュテイン距離
def damerau_levenshtein_distance(s1, s2):
    """
        Return the Damerau-Levenshtein distance between `s1' and `s2'
        using not-recursive algorithm.

        The Damerau-Levenshtein distance between two strings is
        defined as the minimum number of edits needed to transform one
        string into the other, with the allowable edit operations
        being insertion, deletion, substitution or transposition of a
        single character.
    """
    distance = {}

    for i in range(-1, len(s1) + 1):
        distance[(i, -1)] = i+1

    for j in range(-1, len(s2) + 1):
        distance[(-1, j)] = j+1

    for i, c1 in enumerate(s1):
        for j, c2 in enumerate(s2):
            cost = int(c1 != c2)
            distance[(i, j)] = min(
                    distance[(i-1, j)] + 1,
                    distance[(i, j-1)] + 1,
                    distance[(i-1, j-1)] + cost
            )

            # transposition
            if i and j and c1 == s2[j-1] and c2 == s1[i-1]:
                distance[(i, j)] = min(
                        distance[(i,j)],
                        distance[(i-2, j-2)] + cost
                )
    return distance[len(s1)-1, len(s2)-1]


# ハミング距離
def hamming_distance(s1, s2):
    """
        Return the Hamming distance between `s1' and `s2'.
    """
    offset = abs(len(s1) - len(s2))
    return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2) + offset


def _jaro_match(s1, s2):
    """ Return number of matching characters """
    pivot = min(len(s1), len(s2)) - 1
    if pivot < 0: pivot = 0

    commons = []
    for i in range(len(s1)):
        start = max(0, i - pivot)
        end = min(i + pivot, len(s2))

        for j in range(start, end):
            if s1[i] == s2[j]:
                commons.append(s1[i])
                break

    return u''.join(commons)


# ジャロ距離
def jaro_distance(s1, s2):
    """
        Return the Jaro distance between `s1' and `s2'
    """
    if s1 == s2: return 1.0

    j_matches12 = _jaro_match(s1, s2)
    j_matches21 = _jaro_match(s2, s1)
    j_transposition = hamming_distance(j_matches12, j_matches21)

    j_tp = j_transposition / 2.0
    j_m = max(len(j_matches12), len(j_matches21))
    if not j_m: return 0.0

    jaro_dist = ( (len(j_matches12) / len(s1))
                + (len(j_matches21) / len(s2))
                + ((j_m - j_tp) / j_m)
                ) / 3.0

    return jaro_dist


def _winkler_length(s1, s2, maximum=4):
    """
        Return length of common prefix as the start of the string up to
        a maximum of 4 characters
    """
    for i, (c1i, c2i) in enumerate(zip(s1[:maximum], s2[:maximum])):
        if c1i != c2i:
            return i


# ジャロ・ウィンクラー距離
def jaro_winkler_distance(s1, s2, maximum=4, scale=0.1):
    """
        Return the Jaro-Winkler distance between `s1' and `s2'
    """
    if s1 == s2: return 1.0

    jaro_dist = jaro_distance(s1, s2)
    wkr_len = _winkler_length(s1, s2, maximum)
    return wkr_len * scale * (1.0 - jaro_dist) + jaro_dist


if __name__ == "__main__":
    import unittest

    class StrSimTest(unittest.TestCase):
        def test_levenshtein_distance(self):
            cases = [('', '', 0),
                     ('abc', '', 3),
                     ('bc', 'abc', 1),
                     ('kitten', 'sitting', 3),
                     ('Saturday', 'Sunday', 3),
            ]

            for (s1, s2, value) in cases:
                self.assertEqual( levenshtein_distance(s1, s2), value )

        def test_damerau_levenshtein_distance(self):
            cases = [('', '', 0),
                     ('abc', '', 3),
                     ('bc', 'abc', 1),
                     ('abc', 'acb', 1),
            ]

            for (s1, s2, value) in cases:
                self.assertEqual( damerau_levenshtein_distance(s1, s2), value )

        def test_hamming_distance(self):
            cases = [('', '', 0),
                     ('abc', '', 3),
                     ('abc', 'abc', 0),
                     ('acc', 'abc', 1),
                     ('abcd', 'abc', 1),
                     ('abc', 'abcd', 1),
                     ('testing', 'this is a test', 13),
            ]

            for (s1, s2, value) in cases:
                self.assertEqual( hamming_distance(s1, s2), value )

        def test_jaro_winkler_distance(self):
            cases = [('', '', 1.000),
                     ('abc', 'abc', 1.000),
                     ('dixon', 'dicksonx', 0.8133),
                     ('martha', 'marhta', 0.9611),
                     ('dwayne', 'duane', 0.8400),
                     ]

            for (s1, s2, value) in cases:
                self.assertAlmostEqual( jaro_winkler_distance(s1, s2), value,
                                       places=4)


        def test_jaro_distance(self):
            cases = [('', '', 1.000),
                     ('abc', 'abc', 1.000),
                     ('dixon', 'dicksonx', 0.7667),
                     ('martha', 'marhta', 0.9444),
                     ('dwayne', 'duane', 0.8222),
                     ]

            for (s1, s2, value) in cases:
                self.assertAlmostEqual( jaro_distance(s1, s2), value, places=4)

    unittest.main()

# vim: ft=python ff=unix fenc=utf-8
