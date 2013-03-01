from __future__ import with_statement
from itertools import izip, izip_longest
import struct
from StringIO import StringIO as sio

def chainfrac(a, b):
    """Generate chain fraction for the given rational number"""
    while b > 0:
        yield a/b
        a, b = b, a%b

def nearest_chain(a, b):
    """Find chain fraction decomposition of a simplest rational number p/q, such that
    a/b <= p/q < (a+1)/b
    """
    for c1, c2 in izip_longest( chainfrac(a,b), chainfrac(a+1,b)):
        if c1 is None:
            return #First chain finished. Nearest fraction is the given fraction itself.
        if c1 == c2:
            yield c1
        else:
            if (c2 is not None) and c1 > c2:
                yield c2+1
            else: #either second fraction is finished (infinity), or we are on negative slope
                yield c1+1
            return
            
def from_chainfrac(cf):
    """Convert chain fraction coefficients back to the rational fraction.
    Returns tuple: (numerator, denominator)"""
    #Incremental algorithm, that works from head
    num_k, num_b = 0, 1  #0*x + 1
    den_k, den_b = 1, 0  #1*x + 0
    for k in cf:
        num_k, num_b, den_k, den_b = \
            num_b, num_k+k*num_b,\
            den_b, den_k+k*den_b
    return num_b, den_b

def encode_hex_str( s ):
    """Encode hex string, return result as 2 hex strings, separated by space"""
    num = int( s, 16 )
    den = 16**len(s)
    num1, den1 = from_chainfrac(nearest_chain(num, den))
    return "%x %x"%(num1, den1)

def decode_hex_string( st, n ):
    """Takes hexadecimal string, containing numerator and denominator, separated by single space, and returns first n decoded hexadecimal digits
    """
    num, den = [ int(s, 16) for s in st.split(" ") ]
    s = sio()
    for i in xrange(n):
        num = num*16
        d = num / den
        num = num % den
        s.write("%x"%d)
    return s.getvalue()

def long_to_bytes( n ):
    """Convert long value to string"""
    odata = sio()
    while n > 0:
        odata.write(chr(n & 0xff))
        n >>= 8
    return odata.getvalue()[::-1]

def long_from_bytes(s):
    """Convert string to base-256 integer, first byte is highest"""
    num = 0
    for c in s:
        num <<= 8
        num |= ord(c)
    return num

def encode_bytes( s ):
    """Encode binary string. Returns 3-tuple: 
    - Original data size, 
    - Numerator (byte-string)
    - Denominator (byte-string)
    """
    num, den = from_chainfrac(nearest_chain(
            long_from_bytes(s), 
            1<<(8*len(s))))
    return len(s), long_to_bytes(num), long_to_bytes(den)

def rational_to_file( n, num, den, ostream ):
    """Decode original sequence of bytes from numerator and denominator:
    write first n base-256 digits of the x=num/den
    """
    while n > 0:
        nbytes =  min(n, 8)
        num <<= (8*nbytes)
        d = num / den
        num = num % den
        ostream.write( long_to_bytes(d) )
        n -= nbytes

def rational_to_string( n, num, den ):
    """Decode original sequence from nuerator and denominator"""
    s = sio()
    rational_to_file( n, num, den, s )
    return s.getvalue()

def encode_file( ifile, ofile ):
    """Encode a file"""
    n, num, den = encode_bytes( ifile.read() )
    ofile.write( struct.pack("ii", n, len(num)))
    ofile.write( num )
    ofile.write( den )

def parse_encoded_file(ifile):
    """Parse format, produced by the encoder, returning 3-tuple: 
    (n, numerator, denominator)
    """
    n, num, den = parse_encoded_file( ifile )
    n, m = struct.unpack("ii", ifile.read(8))
    num = ifile.read(m)
    den = ifile.read()
    if len(num) != m: 
        raise ValueError, "Unexpected end of file: numerator incomplete"
    if len(den) < len(num): 
        raise ValueError, "Unexpected end of file: denominator shorter than numerator"
    return n, long_from_bytes(num), long_from_bytes(den)

def decode_file( ifile, ofile ):
    """Decode a file of the following format:
    bytes 0-3: number bytes to decode
    bytes 4-7: number of bytes in numerator
    <numerator bytes>
    <denominator bytes>
    EOF
    """
    n, num, den = parse_encoded_file( ifile )
    rational_to_file( n, num, den, ofile )

def dump_continuous_fraction(hifile, hofile):
    """Read a binary fraction from the input file, and put its 
    continuous fraction coefficients to the output file, one number per line
    """
    s = hifile.read()
    num = long_from_bytes(s)
    den = 1<<(8*len(s))
    for k in nearest_chain( num, den ):
        hofile.write("%d\n"%k)

if __name__=="__main__":
    import sys
    from optparse import OptionParser
    parser = OptionParser(usage = "%prog [options] [--] input output\nBabushkin-encode/decode file")

    parser.add_option("-e", "--encode", dest="encode", action="store_true", 
                      default=True,
                      help="Set encode mode (default)")
    parser.add_option("-d", "--decode", dest="encode", action="store_false", 
                      help="Set decode mode")

    parser.add_option("-c", "--cfrac", dest="cfrac_file", metavar="FILE",
                      default = None,
                      help="Dump continuous fraction coefficient to the FILE (one number per line)")
    (options, args) = parser.parse_args()
    if options.cfrac_file:
        if not options.encode:
            parser.error("Dumping continuous fraction is only possible, when encoding data")
        if len(args) != 1:
            parser.error("No output is generated, when dumping continuous fraction coefficients")
        ifile = args[0]
        with open(ifile, "rb") as hifile:
            with open(options.cfrac_file, "w") as hdumpfile:
                print "Dumping CF expansion of %s to %s"%(ifile, options.cfrac_file)
                dump_continuous_fraction(hifile, hdumpfile)
                exit(0)
        

    if len(args) != 2:
        parser.error("Must have 2 arguments: input and output")
    ifile, ofile = args
    with open(ifile, "rb") as hifile:
        with open(ofile, "wb") as hofile:
            if options.encode:
                print "Encoding %s to %s"%(ifile, ofile)
                encode_file(hifile, hofile)
            else:
                print "Decoding %s from %s"%(ofile, ifile)
                decode_file(hifile, hofile)
