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
def run_blast(blastp, query_prots, sp_dbs, outbls):
    
    command = "nohup {} -query {} -db {} -out {} -num_alignments 1 -num_descriptions 1 &".format(blastp, query_prots, sp_dbs, outbls)
    os.system(command)
    
def main():
    """
    The goal of this script is to download all protein sequences for the 
    provided list of zebrafish genes.
    """
    
    # Setup paths to needed directories
    #
    for arg in range(len(sys.argv)):
        if "-seqs" in sys.argv[arg]:
            try:
                prot_seqs_path = sys.argv[arg+1]
            except:
                exit("ERROR: invalid argument for -seqs")
        elif "-dbs" in sys.argv[arg]:
            try:
                prot_dbs_out_path = sys.argv[arg+1]
            except:
                exit("ERROR: invalid argument for -seqs")

    #prot_seqs_path = "prot_seqs/"
    #prot_dbs_out_path = "prot-dbs/"
    #blast_rec_path = "Blast-Result-Reciprocals/"

    # command line args check
    #
    
    
    # Create new database folders
    #
    for file in os.listdir(prot_seqs_path):
        temp = file.split("_")
        new_dir = temp[0][:3] + "_" + temp[1][:3]
        os.system("mkdir {}{}".format(prot_dbs_out_path, new_dir))
        print(new_dir)

    # Create new database files
    #
    for file in os.listdir(prot_seqs_path):
        temp = file.split("_")
        new_dir = temp[0][:3] + "_" + temp[1][:3]
        db_path = prot_dbs_out_path + new_dir + "/" + new_dir + ".fa"
        prot_path = prot_seqs_path + file
        
        command = "makeblastdb -dbtype prot -in {} -out {} -parse_seqids".format(prot_path, db_path)
        os.system(command)
    

if __name__ == '__main__':
    main()
