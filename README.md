Babuskin's "archiver"
=====================
A proof-of concept implementation of the (in)famous data compression algorithm, proposed by Babushkin.

In fact, this algorithm is unable to compress most types of files, usually considered easy to compress. For most files, output file will even be a several bits longer. However, there is one type of files, that can be ffectively compressed: files, ending with repeating sequence.

For example, file helloworlds.txt:

    Hello world world world world world world world world world world world world world world world world world world world world 

(no final end of line), encoded with the following command:

    $ python babushkin_arch.py samples/helloworlds.txt samples/helloworlds.txt.enc

will produce file "helloworlds.txt.enc" having size 30 bytes, whereas original file is 126 bytes.
But eny minor variation in the trailing sequence, for example, final newline, will destroy the compression effect.

This is a consequence of the well known property of rational numbers: their base-n fractions are periodical after some moment.

Algorithm
---------
Encoding ("compression") algorithm has the following steps:

# Data file is represented as one long binary number X; 0 <= X < 1

# A pair of minimal natural numbers P,Q is searched, such that:
   X ≈ P/Q
   with precision, enough to restore original number X with all digits.

# Size of the original file and numbers P, Q are written to the compressed file.

Implementation
--------------
The crucial moment is the algorithm, determining a minimal sufficient rational approximation for X (the P/Q pair).
Approach, based on [continued fractions](http://en.wikipedia.org/wiki/Continued_fraction) is used:

    X = a0 + 1/(a1 + 1/(a2 + ... ))

Calculations involve operations on long integers (natively supported by Python), and thus algorithm's complexity is rather big. For average computer, around 100 Kb is a practical limit of data size.

Running
-------

To compress file "input", use command:

    $ python babushking_encode.py input output

To decompress, use:

    $ python babushking_encode.py -d input output

Installation
------------
Not needed (it is not an useful program).
Run script directly from its directory.

Requirements
------------
Requires Python >= 2.5 to run.

