# Sequence Alignment #
Implementation of sequence alignment algorithms using dynamic programming. Initially created for BCSR CMPT-353 Assignment 2, Problem 3.  

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


## Results ##

Below is a table of my results using a gap penalty of -1, and where applicable, an affine penalty of 0.

Note: The first two cases are the most important, but I decided to compare the "moderns" as well out of curiosity.

| *sequence 1*   | test_medieval.fasta          | test_medieval.fasta  | ypestis_modern.fasta         |
|----------------|------------------------------|----------------------|------------------------------|
| *sequence 2*   | yenterocolitica_modern.fasta | ypestis_modern.fasta | yenterocolitica_modern.fasta |
| **global**     | 15315                        | 20778                | 15310                        |
| **local**      | 15809                        | 20779                | 15803                        |
| **affine**     | 16521                        | 20778                | 16515                        |                     |

The results show that Y. pestis is more closely related to the medieval bacterium than Y. enterocolitica is. This is because the alignment scores are consistently higher.

## Assignment Questions ##

### Which scoring matrix to use? ###

I decided on the scoring matrix displayed on Slides-10 (p37) because it takes into account the likelihood of the different processes happening. More specifically, we want to note that it is more likely that there is a mutation that preserves the number of rings than changes the number of rings.

Slides referenced:
* http://hope.simons-rock.edu/~mbarsky/bio2018/lectures/Lecture10_String%20similarity%20and%20alignments.pdf

### Any commands you need to run in the shell? ###

See the "How to Run" section above.

### What are the Results? ###

See the "Results" section above.

### (Optional Q4) - How could Paul McCartney use alignment to help prove to the world that his songs are being stolen? ###

Paul McCartney could run an alignment algorithm on a sequence that represents his song lyrics, and another sequence that represents the suspected stolen song's lyrics. To show that it is significantly more similar than most songs are, he could also run the alignment algorithm between his song and many other songs to show that the likely stolen song is indeed, likely stolen, if the score is much higher.
