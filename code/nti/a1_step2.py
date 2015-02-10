# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 11:36:38 2015

@author: markus
"""

# import add_start_stop function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams
import itertools

if __name__ == "__main__":
    # here code for program
    
    parser = ArgumentParser(description='Assignment A, Step 1')
    parser.add_argument('-corpus', dest ='input_file', type=str, help='Path to corpus file')
    parser.add_argument('-n', dest='n', type=int, help='Length of word-sequences to process (n-grams)')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    args = parser.parse_args()
    
    start_stop_lines = list(itertools.chain(*[w.split() for w in add_start_stop(args.input_file)]))

    n_grams = parse_ngrams(start_stop_lines, args.n)
    n_min_1_grams = parse_ngrams(start_stop_lines, args.n - 1)