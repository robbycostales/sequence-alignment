# Sequence Alignment #
Implementation of sequence alignment algorithms using dynamic programming. Initially created for BCSR CMPT-353 Assignment 2 Problem 3.  

## Directory / File Guide ##

* scores - contains scoring matrix files for alignments (txt)
* seqs - contains sequence files (txt)

* global.sh - performs global alignment on two sequences
* local.sh - performs local alignment on two sequences
* affine.sh - performs global alignment with affine weights on two sequences

* algs.py - contains all of the alignment algorithms

## How to Run ##

1. Decide what kind of alignment you would like to use, and note the appropriate .sh file
    * (EX) local.sh
2. Decide which sequences you wish to align (from /seqs)
    * (EX) test_medieval.fasta and ypestis_modern.fasta
3. Select a scoring matrix (from /scores)
    * (EX) standard.m
4. Select a gap penalty
    * (EX) -1
5. (For affine only) - Select affine penalty
    * (EX) 0

Run the appropriate .sh file with the parameters from steps 2-4 like so:

`
./local.sh test_medieval.fasta ypestis_modern.fasta -1
`

Note: for the sequences and scoring matrix path, the directories /scores and /seqs is NOT included. The python file takes care of that for us.

If you get a `permission denied` error, enter the following command

`chmod +x example.sh`

and example.sh with the appropriate file name.

## Assignment Questions ##

### Which scoring matrix to use? ###

### Any commands you need to run in the shell? ###

See the "How to Run" section above.

### Results ###
