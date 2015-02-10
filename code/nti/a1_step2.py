# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 11:36:38 2015

@author: markus
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams, sort_ngrams
from argparse import ArgumentParser
import itertools

if __name__ == "__main__":
    # here code for program
    
    parser = ArgumentParser(description='Assignment A, Step 1')
    parser.add_argument('-corpus', dest ='input_file', type=str, help='Path to corpus file')
    parser.add_argument('-n', dest='n', type=int, help='Length of word-sequences to process (n-grams)')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    parser.add_argument('-conditional-prob-file', dest='cond_file', type=str, help='file for conditional probabilities')
    args = parser.parse_args()
    
    # get list of lines with START and STOP added
    ss = add_start_stop(args.input_file)
    # split and flatten array
    start_stop_lines = list(itertools.chain(*[w.split() for w in ss]))

    # create n-grams and (n - 1)-grams
    n_grams = parse_ngrams(start_stop_lines, args.n)
    n_min_1_grams = parse_ngrams(start_stop_lines, args.n - 1)
    
    # when conditional prob file is NOT given, print 10 most bigrams
    if args.m:
        print('n-grams:')
        print_ngrams(sort_ngrams(n_grams), args.m)
        print('\n(n-1)-grams')
        print_ngrams(sort_ngrams(n_min_1_grams), args.m)
    
    