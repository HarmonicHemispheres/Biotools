#!/usr/bin/env python3

import os
import sys
import time

def stats(f):
    """
    OVERVIEW:
        stats, is a decorator function for timing other functions
    NOTES:
        this decorator function has one package dependancy
        - time
    """
    def caller(*args, **kwds):
        t0 = time.time()
        ret = f(*args, **kwds)
        t1 = time.time()
        out = str(
        '''function title:    ''' + str(f.__name__) +
        '''\n run time(sec):    ''' + str(round(t1-t0, 5)))
        print (out)
        return ret
    return caller

@stats
def run_blast(blastp, query_prots, sp_dbs, outbls, quiet=0):
    if quiet:
        command = "nohup {} -query {} -db {} -out {} -num_alignments 1 -num_descriptions 1 &".format(blastp, query_prots, sp_dbs, outbls)    
    else:
        command = "{} -query {} -db {} -out {} -num_alignments 1 -num_descriptions 1".format(blastp, query_prots, sp_dbs, outbls)
        
    os.system(command)
    
def main():
    """
    The goal of this script is to download all protein sequences for the 
    provided list of zebrafish genes.
    """

    # Setup paths to needed directories
    #
    quiet = 0
    blastp = ""
    for arg in range(len(sys.argv)):
        if "-query" in sys.argv[arg]:
            try:
                query_fa = sys.argv[arg+1]
            except:
                exit("ERROR: invalid argument for -query")
        elif "-db" in sys.argv[arg]:
            try:
                dbs = sys.argv[arg+1]
            except:
                exit("ERROR: invalid argument for -db")
        elif "-out" in sys.argv[arg]:
            try:
                out_bls_path = str(sys.argv[arg+1]) + ".bls"
            except:
                exit("ERROR: invalid argument for -out")
        elif "-blastp" in sys.argv[arg]:
            try:
                blastp = sys.argv[arg+1]
            except:
                exit("ERROR: invalid argument for -blastp")

    print("SUCCESS: starting blast with {}".format(query_fa))
    run_blast(blastp, query_fa, dbs, out_bls_path)  

    

if __name__ == '__main__':
    main()
