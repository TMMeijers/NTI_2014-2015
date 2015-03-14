# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:19:40 2015

@author: T.M. Meijers, C.J. Boon, M. Pfundstein
"""

#%%

from argparse import ArgumentParser
from sys import exit

def binarize(sentence):
    """
    Takes a sentence and returns a binarized sentence:
    Input:
    (NP (NNP Rolls-Royce) (NNP Motor) (NNPS Cars) (NNP Inc.))
    Output:
    (NP (NNP Rolls-Royce) (@NP-> NNP (NNP Motor) (@NP-> NNP NNP (NNPS
    Cars) (@NP-> NNP NNP NNPS (NNP Inc.)))))
    """
    pass
    
def get_sentences(input_file):
    """
    Takes an input file and copies all the sentences into an array.
    """
    sentences = []
    
    with open(input_file) as f:
    	return [line.rstrip('\n') for line in f if line.rstrip('\n')]
    
    
    
#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment B, Step 1')
    parser.add_argument('-input', dest='input_file', type=str, default=None, help='Path to input file')
    parser.add_argument('-output', dest='output_file', type=str, default=None, help='Path to output file')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.input_file:
        parser.print_help()
        exit('No input file specified (-input)')
    if not args.output_file:
        parser.print_help()
        exit('No output file specified (-output)')
        
    sentences = get_sentences(args.input_file)
    print(sentences)
    with open(args.ouput_file, 'w+') as f:
        for s in sentences:
            f.write(binarize(s))
