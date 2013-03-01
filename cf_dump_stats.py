from __future__ import with_statement
import sys
import math

if __name__=="__main__":
    stats = {}
    n = 0
    with open(sys.argv[1], "r") as dump:
        for s in dump:
            x = int(s)
            stats[x] = stats.get(x,0)+1
            n += 1
    for k in sorted(stats.keys()):
        if k == 0: continue
        #http://en.wikipedia.org/wiki/Gauss%E2%80%93Kuzmin_distribution
        p = -math.log(1.0-1.0/(1+k)**2)/math.log(2)
        sigma = math.sqrt(p*(1-p)*n)
        d = abs(stats.get(k) - p*n)
        print "%d\t%d\t%0.4g\t+-%0.4g\t"%(k, stats.get(k), p*n, 3*sigma),\
            ("*" if d >= 3*sigma else "")
