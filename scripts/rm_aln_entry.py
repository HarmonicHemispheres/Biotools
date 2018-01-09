#!/usr/bin/env python3

#######################################################

### Remove Entry from alignment ###
# 
# this script will remove any species from a list of 
# fasta alignments and write the new sequence files to
# a new output file. This is useful for modifying or cleaning
# up sequence files if undesired species happen to be in the
# sequence file.
#
# Example
# ARG ::  0                 1            2           3
# COM ::  ./rm_aln_entry.py fasta_files/ output_dir/ specie
#
#
# NOTES:
# - 

#######################################################


import os
import sys
import subprocess

def main():
    
    ### check command line args for errors ###
    if len(sys.argv) != 4:
        exit("ERROR: incorrect number of arguments")

    else:
        indir = sys.argv[1]
        outdir = sys.argv[2]
        spe = sys.argv[3]

        if os.path.isdir(outdir) is False:
            exit("ERROR: outdir is not a directory!")
    
    ### Iterate over input files and write output to output_dir
    if os.path.isdir(indir) is True:        
        
        for fl in os.listdir(indir):

            if ".fasta" in fl:
                in_path = indir + "/" + fl
                out_path = outdir + "/" + fl
                gen_new_file(in_path, out_path, spe)


    elif os.path.isfile(indir) is True:
        if ".DS_Store" not in indir:
            out_path = outdir + "/" + os.path.basename(indir)
            
            gen_new_file(indir, out_path, spe)


    ### Then rearrange species order in output files to match
    ### the original order of the input files
    # (NOTE: this is useful for programs such as pal2nal)

def gen_new_file(_in, _out, _id):
    """ generates a new file with the selected id removed"""
    
    ### Make sure the output file exists
    out_fl = open(_out, "w+")
    
    ### Verify the input file is not empty
    with open(_in, "r") as fl:
        if len( fl.read().splitlines() ) == 0:
            print("ERROR: file has no content")
            return False
        
    ### open sequence file and build new list
    new_list = []

    with open(_in, "r") as fl:

        for entry in fl.read().split(">")[1:]:
            
            entry_spe = entry.splitlines()[0].split("[")[-1].split("]")[0]
            
            if _id not in entry_spe:
                new_list.append(">" + entry)

            else:
                print("MESSAGE: removing {} from {}".format(_id, os.path.basename(_in)))

    # add new content to output string
    out_str = ""
    for i in new_list:
        out_str += i

    out_fl.write(out_str)
    out_fl.close()


if __name__ == '__main__':
    main()



