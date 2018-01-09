# Biotools
<hr>

## What is it?
A collection of bioinformatics related scripts suited for specific taskes including
automated multisequence alignment and protein comparisons such as accepted amino
acid regions. Most tools are written in python 3.6.


## Installation
To use tools in this package, simply clone/download the repository and run the
scripts on the commandline. Examples for each script are listed below demonstrating
what options are available. In addition to this documentation scripts contain a description and usage example for aid.


## Script Docs

| <h3>is_aligned.py</h3> |
|---|
|Checks a directory or file of alignments in fasta format for alignment. Based on checking for dashes, this is a useful tool for verifying files before running them through analysis if there are large sets of alignment files. |
|<h4>Options</h4> **-path** the directory or file to check<br>|
|<h4>Example</h4> `./is_aligned.py -path /example/file.fasta`|

| <h3>prot_comp.py</h3> |
|---|
|Computes comparisions on directory or file of alignments in fasta format between 2 groups of sequences. comparison options are specified in a control file.|
|<h4>Example</h4> `./prot_comp.py control.json`|

| <h3>muscle_automate.py</h3> |
|---|
|Uses the MUSCLE command line program to perform alignment on a fasta file or directory of fasta files. (NOTE: the muscle program must be in your path for subprocess to call it properly, and it must be named 'muscle')|
|<h4>Example</h4> `./muscle_automate.py fasta_files/ output_dir/`|

| <h3>pal2nal_automate.py</h3> |
|---|
|This script allows for running pal2nal on a directory or single file in order to automate the computation on a large set of data (REASON: pal2nal is a program used to create codon alignments from protein alignments and mrna sequences.)|
|<h4>Example</h4> `./pal2nal_automate.py peptide_alignments/ mrna_alignments/ output_dir/`|

| <h3>prot_comp.py</h3> |
|---|
|This script allows for the comparative analysis of aligned fasta containing two groups of species at each site in the alignment. The control file contains options for the program which can the be simply run on the command line.|
|<h4>Example</h4> `./prot_comp.py path_to_control.file`|

| <h3>Blast Databases</h3> |
|---|
|Tools for making local blast databases and running blast. In order to run blast locally we first must setup a blast database given a fasta file of protein sequences. After that we can then use a fasta file for some species and compute a blast with each protein sequence against the proteins sequences in the database.|
|<h4>Example</h4> demonstrated in the overview file in the directory.|

## Contacts
<strong>Programmer / Researcher</strong> Robby Boney <br> <robby.boney@wsu.edu>
                    
