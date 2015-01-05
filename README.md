Babuskin's "archiver"
=====================
A proof of concept implementation of the (in)famous data compression algorithm, proposed by A. Babushkin.

Algorithm
---------
Encoding ("compression") algorithm has the following steps:

1.  Data file is represented as one long binary number X; 0 <= X < 1
2.  A pair of minimal natural numbers P,Q is determined such that:
    X ≈ P/Q
    with precision, enough to restore original number X with all digits.
3.  Sizes of the original file and numbers P, Q are written to the compressed file.

Properties
----------
Practice shows that this algorithm is unable to compress most types of files, usually considered easy to compress. For most files, output file will even be a several bytes longer. However, there are files that can be effectively compressed: namely, the files ending with repeating sequence.

For example, consider the following file helloworlds.txt:

    Hello world world world world world world world world world world world world world world world world world world world world 

(without the final end of line), encoded with the following command:

    $ python babushkin_arch.py samples/helloworlds.txt samples/helloworlds.txt.enc

will produce file "helloworlds.txt.enc" having size 30 bytes, whereas original file is 126 bytes.
But any minor variation in the trailing sequence, such as final newline, will destroy the compression effect.

This is a consequence of the well known property of rational numbers: their base-n fractions are periodical after some moment.


Implementation
--------------
The crucial moment is the algorithm, determining a minimal sufficient rational approximation for X (the P/Q pair).
Approach, based on [continued fractions](http://en.wikipedia.org/wiki/Continued_fraction) is used:

    X = a0 + 1/(a1 + 1/(a2 + ... ))

Calculations involve operations on long integers (natively supported by Python). For an average computer, file of around 100 Kb is a practical limit of data size.

Running
-------

To compress file "input", use command:

    $ python babushkin_arch.py input output

To decompress, use:

    $ python babushkin_arch.py -d input output

Data Format
-----------
The archiver produces binary files of the following format:

* offset 0...3: size of the original file (little endian).
* offset 4...7: size (N) of the numerator (P).
* offset 8...N+7: numerator bytes, starting from the most significant.
* offset N+8...end: denominator (Q) bytes, starting from the most significant.

Installation
------------
Not needed (it is not a useful program).
Run script directly from its directory.

Requirements
------------
Requires Python 2.x to run.

