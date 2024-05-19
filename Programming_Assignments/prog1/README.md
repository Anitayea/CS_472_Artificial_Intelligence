# AI programming 1

## input files
change the content in 'input.txt' for Budget-ID and 'input_hc.txt' for Budget-HC, keeping the original format of taeget, budget, and flag: V for verbose, C for compact, separated by a space. 

create a new input file if you wish and call run_id(filename) or run_hc(filename) in main.

### notes on input files

All the input files are plain text files.

comment out the other test input1-4.txt or input1-4_hc.txt if you do not wish to test them. 

For the iterative deepening program, the first line is the target value and the budget, as integers, followed by a flag for the type of output: 'V' for verbose or 'C' for compact.

For the hill climbing program, the first line has additionally the number of restarts to try.

Example for 'input.txt' (add 3 for hc):
20 10 V (3)
U 10 8
V 8 4
W 7 3
X 6 3
Y 4 1

## run the program
simply run 'Budget-ID.py' and 'Budget-HC.py', the input file path are all written. 

Note that it is originally written in jupyter notebook, so you can also view the notebook with outputs of all test input files. 

