# Making local blast databases and running blast
In order to run blast locally we first must setup a blast database given
a fasta file of protein sequences. After that we can then use a fasta file
for some species and compute a blast with each protein sequence against the
proteins sequences in the database.

## Usage

This project has 2 script, on for setting up the database and one for running
the blast. It is important to note that the ncbi blastp package needs to be 
installed for this to work. simply finding the blastp and makeblastdb binary files 
and using those as input should also work.
these files can be found at [ncbi](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

<br>

### make_dbs.py
|variable |description |
|-|-|
|-seqs | the file with all the protein sequences which should be in the database |
|-dbs |the path to write the database to |

<br>

### run_blast.py
|variable |description |
|-|-|
|-query_fa |the fasta file with protein sequences to blast with |
|-dbs |the path of the database to blast against |
|-out |the path to write the blast results to |
|-blastp |the path to the blast binary from ncbi |

## Example
All files in this directory correspond to this example

== STEP 1: setup database ==
```bash
user@host~$ ./make_dbs.py -seqs prot_seqs/ -dbs db/
```

== STEP 2: blast the query file against the database ==
```bash
user@host~$ ./run_blast.py -query ZB.txt -out /blast_res -blastp blastp -db db/fel_cat/fel_cat.fa
```

the blast results are located in blast_res.bls file and can be viewed in a text editor.