from __future__ import with_statement

def gcd(a,b):
    "Greatest common divisor"
    while True:                
        if b==0: return a
        if a%b==0: return b
        a,b = b,a%b

def long_from_bytes(s):
    """Convert string to base-256 integer, first byte is highest"""
    num = 0
    for c in s:
        num <<= 8
        num |= ord(c)
    return num

def decimal_digits( num, den, base=10 ):
    """Returns decimal digits of a rational number in range [0; 1) """
    while num > 0:
        den_divisor = gcd( den, base )
        num_multiplier = base / den_divisor
        num *= num_multiplier
        den /= den_divisor
        yield num / den
        num = num % den
    
def encode_file( ifile, ofile ):
    """Encode a file"""
    data = ifile.read()
    num = long_from_bytes(data)
    den = 1 << (8*len(data))
    ofile.write("0.")
    for digit in decimal_digits(num, den):
        ofile.write(str(digit))
    

USAGE = """"""
if __name__=="__main__":
    from optparse import OptionParser
    import sys
    parser = OptionParser(usage = "python %prog INPUT_FILE [OUTPUT_FILE]\npython %prog --help")
    (options, args) = parser.parse_args()
    argc = len(args)
    if argc < 1:
        parser.error("Input file not specified.")
    if argc > 2:
        parser.error("Too many arguments.")

    ifile = args[0]
    ofile = args[1] if argc >= 2 else None

    with open(ifile, "rb") as hifile:
        if ofile is not None:
            with open(ofile, "w") as hofile:
                encode_file(hifile, hofile)
        else:
            encode_file(hifile, sys.stdout) 
    
        
