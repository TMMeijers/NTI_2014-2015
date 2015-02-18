# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:41:40 2015

@author: Markus Pfundstein, Thomas Meijers, Cornelis Boon
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams, sort_ngrams
from a1_step2 import get_sentences
from argparse import ArgumentParser
from collections import Counter
from sys import exit
import itertools

#%%
def add_1_smoothing():
    
#%%
def good_turing_smoothing():
    

#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment A, Step 2')
    parser.add_argument('-train-corpus', dest ='train_file', type=str, help='Path to train corpus file')
    parser.add_argument('-test-corpus', dest ='test_file', type=str, help='Path to test corpus file')
    parser.add_argument('-n', dest='n', default=2, type=int, help='Length of word-sequences to process (n-grams) [1,inf]')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of sequences to show in output')
    parser.add_argument('-smoothing', dest='smoothing', type=str, default='no', help='Method of smoothing [no|add1|gt]')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.train_file or not args.n or not args.test_file or args.n < 1:
        parser.print_help()
        exit('Missing required arguments')        
        
    # split and flatten array
    # sentences is list of sentences that start with START and end with STOP
    sentences = get_sentences(add_start_stop(args.input_file, args.n if not args.m else 1))
    
    n_grams = Counter(list(itertools.chain(*[parse_ngrams(sen, args.n) for sen in sentences])))
    n_min_1_grams = Counter(list(itertools.chain(*[parse_ngrams(sen, args.n - 1) for sen in sentences])))