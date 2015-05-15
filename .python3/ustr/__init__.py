# coding: utf-8

import string
import random
import hashlib

from string import octdigits, digits, printable, punctuation, \
                   ascii_letters, ascii_lowercase, \
                   ascii_uppercase, hexdigits, whitespace


def hash_digest(path, algorithm='md5', hex=True, blocksize=1024):
    """Calcurate hash of the file."""
    path = str(path)   # for pathlib

    if hasattr(hashlib, algorithm):
        # algorithm: md5, sha1, sha224, sha256, sha384, sha512
        hash_ = eval('hashlib.%s' % algorithm)()
    else:
        raise AttributeError("'module' object has no attribute '%s'" % algorithm)

    with open(path, mode='rb') as f:
        while True:
            chunk = f.read(blocksize)
            if chunk: hash_.update(chunk)
            else: break
    return hash_.hexdigest() if hex else hash_.digest()


def random_hex(byte_length=8):
    return ''.join(hex(random.getrandbits(8))[2:] for i in range(byte_length))

def random_bytes(byte_length=8):
    return bytes(random.getrandbits(8) for i in range(byte_length))

def random_bytearray(byte_length=8):
    return bytearray(random.getrandbits(8) for i in range(byte_length))

def random_password(byte_length=8, chars=string.ascii_letters+string.digits):
    """Generate a random character sequence. """
    return ''.join([random.choice(chars) for i in range(byte_length)])

password = random_password


class Translator(object):
    """
        A wrapper of string.translate().

        ref.) Python Cookbook (O'reilly Japan)

        >>> t = Translator('Chris Perkins: 224-7992')
        >>> t.translate('0123456789', '#')
        'Chris Perkins: ###-####'
        >>> t.translate('0123456789', '#', ' -')
        'ChrisPerkins:#######'
        >>> t.delete('0123456789')
        'Chris Perkins: -'
        >>> t.keep('0123456789')
        '2247992'
    """
    def __init__(self, source):
        self.source = source

    def translate(self, from_charset, to_charset, delete_charset=''):
        if len(to_charset) == 1:
            to_charset *= len(from_charset)
        trans = str.maketrans(from_charset, to_charset)
        return self.source.translate(trans, delete_charset)

    def delete(self, delete_charset):
        return self.source.translate({}, delete_charset)

    def keep(self, keep_charset):
        exclude_charset = keep_charset.translate({}, '')
        delete_charset = trans.translate({}, exclude_charset)
        return self.source.translate({}, delete_charset)

def rotN(s, n=13):
    """Encrypt the `s' by Caesar algorithm. """
    new_str = []
    for c in s:
        # ord(char) returns the ASCII-code of char
        # * ord('A') == 65, ord('Z') == 90 == 65+26 -1
        # * ord('a') == 97, ord('z') == 122 == 97+26 -1
        # chr(i) returns the character with ASCII-code of i
        # * chr(65) == 'A', chr(90) == 'Z'
        # * chr(97) == 'a', chr(122) == 'z'

        i = ord(c)
        if 65 <= i < 91:
            c = chr(((i - 65) + n) % 26 + 65)

        elif 97 <= i < 123:
            c = chr(((i - 97) + n) % 26 + 97)

        new_str.append(c)

    return ''.join(new_str)


def rot13(s):
    """Encrypt the `s' by rot13 algorithm. """
    try:
        return s.encode('rot13')
    except:
        return rotN(s, 13)


def frequency_list(s):
    alphabets = Translator.keep(s.lower(), ascii_lowercase)
    total = float(len(alphabets))
    return [(alphabets.count(c) / total) * 100 for c in sorted(ascii_lowercase)]


def crackCaeser(s, estimated_freqs=[]):
    """Crack the Caesar-encrypted code `s'. """
    if len(estimated_freqs) != 26:
        estimated_freqs = [
            8.1, 1.4, 2.7, 3.8, 13.0, 2.9, 2.0, 5.2, 6.3,
            0.13, 0.4, 3.4, 2.5, 7.1, 7.9, 1.9, 0.11, 6.8,
            6.1, 10.5, 2.4, 0.9, 1.5, 0.15, 1.9, 0.07
        ]

    lower_text = s.lower()
    square_list = []

    for shift_number in range(26):
        plain = rotN(lower_text, shift_number)
        freqsN = frequency_list(plain)
        chi_square = sum((x - y)**2 / y for x, y in zip(freqsN, estimated_freqs))

        square_list.append(chi_square)

    shift_number = square_list.index(min(square_list))
    return shift_number, rotN(s, shift_number)




# vim: ft=python ff=unix fenc=utf-8
