#!/usr/bin/env python3

###########################################

### OVERVIEW :
# Checks if a directory of alignment files is 
# aligned according to fasta format.


### EXAMPLE :
# ARGV  :  0            1
# COMM  :  ./is_aligned dir_of_files

###########################################
import os
import sys


def checkfile(fl):
    # only look at .fasta files
    if fl.endswith(".fasta"):
        fileName = os.path.basename(fl)
        tempF = open(fl, "r")
        tempFText = tempF.read()

        # see if "-" is not in file
        if "-" not in tempFText:
            i = tempFText.count(">")
            if i == 1:
                print(fileName, "Only contains 1 species. Not proper alignment file")
            else:
                print(fileName, "may not be aligned!")

        # close opened file handle
        tempF.close()


def main():

    # =======================================
    # first read user input from command line
    #

    if len(sys.argv) != 2:
        exit("ERROR: invalid number of arguments")
    else:
        input_fl = sys.argv[1]


    # =======================================
    # check all input files for alignment
    #
    try:
        if (os.path.isdir(input_fl) is True):
            for file in os.listdir(input_fl):
                flname = input_fl + file
                checkfile(fl=flname)

        elif (os.path.isfile(input_fl) is True):
            checkfile(fl=input_fl)

    except:
        exit("ERROR: Path name was not valid")


if __name__ == '__main__':
    main()
