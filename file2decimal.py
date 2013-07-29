from __future__ import with_statement

def long_from_bytes(s):
    """Convert string to base-256 integer, first byte is highest"""
    num = 0
    for c in s:
        num <<= 8
        num |= ord(c)
    return num

def decimal_digits( num, den ):
    """Returns decimal digits of a rational number in range [0; 1) """
    while num > 0:
        num *= 10
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
    

USAGE = """python %s INPUT_FILE [OUTPUT_FILE]"""
if __name__=="__main__":
    import sys
    script = sys.argv[0]
    args = sys.argv[1:]
    argc = len(args)
    if argc < 1:
        print(USAGE % script)
        exit(0)
    if argc > 2:
        print "Too many command line arguments"
        exit(1)

    ifile = args[0]
    ofile = args[1] if argc >= 2 else None

    with open(ifile, "rb") as hifile:
        if ofile is not None:
            with open(ofile, "w") as hofile:
                encode_file(hifile, hofile)
        else:
            encode_file(hifile, sys.stdout) 
    
        
