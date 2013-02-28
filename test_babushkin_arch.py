from babushkin_arch import *

def poptest(s):
    s1 = babushkindec_bin( *babushkinenc_bin(s))
    assert(s1==s)

def bigtest():
    from random import random, randint
    for i in xrange(1000):
        n = randint(1, 1000)
        s = "".join( chr(randint(0,255)) for _ in xrange(n))
        poptest(s)

