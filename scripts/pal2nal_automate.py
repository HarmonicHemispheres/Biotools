#!/usr/bin/env python3

#############################################

### AUTOMATING pal2nal for a dir of input ###
#
# This script allows for running pal2nal on a directory or single file in
# order to automate the computation on a large set of data
#
# REASON:
# pal2nal is a program used to create codon alignments from protein 
# alignments and mrna sequences.
#
# Example
# ARGS ::  0                     1                   2                3
# COMM ::  ./pal2nal_automate.py peptide_alignments/ mrna_alignments/ output_dir/  

# NOTE: 
# - the pal2nal program must be in your path for subprocess to
#   call it properly, and it must be named 'pal2nal'
# - alignments MUST be aligned protein files in fasta/clustalW format

#############################################


import os
import sys
import subprocess

def main():
    
    ### check command line args for errors ###
    if len(sys.argv) != 4:
        exit("ERROR: incorrect number of arguments")

    else:
        in_pep_p = sys.argv[1]
        in_mrna_p = sys.argv[2]
        out_dir = sys.argv[3]

        if os.path.isdir(out_dir) is False:
            exit("ERROR: outdir is not a directory!")

    
    ### Iterate over input files and write output to output_dir
    if os.path.isdir(in_pep_p) is True and os.path.isdir(in_mrna_p) is True:
        
        for fl in os.listdir(in_pep_p):
            in_pep = in_pep_p + "/" + fl
            in_mrna = in_mrna_p + "/" + fl
            out_path = out_dir + "/" + "p2n_out_" + fl
            #print("{}  ++  {}".format(in_pep, in_mrna))

            palnal_run(in_pep, in_mrna, out_path)


    elif os.path.isfile(in_pep_p) is True and os.path.isfile(in_mrna_p) is True:
        out_path = out_dir + "/" + "p2n_out_" + os.path.basename(in_pep_p)
        palnal_run(in_pep_p, in_mrna_p, out_path)



def palnal_run(in_pep, in_mrna, out_p):
    """ runs pal2nal for the given file """

    ### Make sure the output file exists
    if os.path.isfile(out_p) is False:
        subprocess.call(["touch", out_p])


    ### call the program
    with open(out_p, "w") as fl_out:
        #subprocess.call(my_cmd, stdout=outfile)
        subprocess.call(["pal2nal.pl", in_pep, in_mrna], stdout=fl_out)


if __name__ == '__main__':
    main()
