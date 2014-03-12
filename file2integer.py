from __future__ import with_statement
def long_from_bytes(s):
    """Convert string to base-256 integer, first byte is highest"""
    num = 0
    for c in s:
        num <<= 8
        num |= ord(c)
    return num

def encode_file( ifile, ofile ):
    """Encode a file"""
    ofile.write(str(long_from_bytes(ifile.read())))

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
    
        
