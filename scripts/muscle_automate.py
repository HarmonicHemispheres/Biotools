#!/usr/bin/env python3

#######################################################

### AUTOMATING muscle alignment input dir ###
# 
# this script will also maintain the original order
# of species by rearranging the species order in the
# final alignment file after alignment is complete
#
# Example
# ARG ::  0                    1                   2
# COM ::  ./muscle_automate.py fasta_files/ output_dir/
#
#
# NOTES:
# - the muscle program must be in your path for subprocess to
#   call it properly, and it must be named 'muscle'
#
# - arg(1) can be a file or dir

#######################################################


import os
import sys
import subprocess

def main():
    
    ### check command line args for errors ###
    if len(sys.argv) != 3:
        exit("ERROR: incorrect number of arguments")

    else:
        indir = sys.argv[1]
        outdir = sys.argv[2]
        if os.path.isdir(outdir) is False:
            exit("ERROR: outdir is not a directory!")
    
    ### Iterate over input files and write output to output_dir
    if os.path.isdir(indir) is True:        
        
        for fl in os.listdir(indir):

            if ".DS_Store" not in fl:
                in_path = indir + "/" + fl
                out_path = outdir + "/" + fl
                align_file(in_path, out_path)


    elif os.path.isfile(indir) is True:
        if ".DS_Store" not in indir:
            out_path = outdir + "/" + os.path.basename(indir)
            
            align_file(indir, out_path)


    ### Then rearrange species order in output files to match
    ### the original order of the input files
    # (NOTE: this is useful for programs such as pal2nal)


def align_file(in_p, out_p):
    """ Use muscle to align a single file and then reorganize 
    the species to match the order of the original file """

    ### Make sure the output file exists
    if os.path.isfile(out_p) is False:
        subprocess.call(["touch", out_p])


    ### Record the order of the original file
    aln_order = []

    with open(in_p, "r") as fl:
        for line in fl.read().splitlines():
            if ">" in line:
                id_extract = line.split(">")[1].split()[0]
                
                if "|" in id_extract:
                    id_extract = id_extract.split("|")[0]
                    print("FIXING: " + id_extract)
                
                aln_order.append(id_extract)

    ### Perform alignment on the sequence file
    subprocess.run(["muscle", "-in", in_p, "-out", out_p])


    ### Reorder finished alignment
    aln = {}
    with open(out_p, "r") as fl:
        for entry in fl.read().split(">")[1:]:
            aln_id = entry.split()[0]

            if "|" in aln_id:
                aln_id = aln_id.split("|")[0]

            aln[aln_id] = ">" + entry

    print(aln.keys())
    s = ""
    for i in aln_order:
        print("Searched: " + i)
        s += aln[i]

    with open(out_p, "w+") as fl:
        fl.write(s)





if __name__ == '__main__':
    main()
