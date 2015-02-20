# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:41:40 2015

@author: Markus Pfundstein, Thomas Meijers, Cornelis Boon
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams, sort_ngrams
from a1_step2 import get_sentences, calc_probabilities_seq_file
from argparse import ArgumentParser
from collections import Counter
from sys import exit
from itertools import product, chain


def make_unseen(n_grams, n_min_1, n):
    """
    Adds unseen events to the bi-gram model
    """
    print(len(n_grams))        
    new_grams = (' '.join(i) for i in product(n_min_1.iterkeys(), repeat=n))
    
    n_grams = dict(n_grams)
    unseen = ((new_gram, 0) for new_gram in new_grams if new_gram not in n_grams)
    print('Gen2')
    n_grams.update(unseen)
    print(len(n_grams))    
    exit()    
    #return n_grams
#%%
def add_1_smoothing():
    """
    Applies add-1 smoothing to the bi-gram model
    """
    
#%%
def good_turing_smoothing():
    """
    Applies good-turing smoothing to the bi-gram model
    """
    
def smoothe_min_1():
    """
    Smoothes the unigram model to suit the new bi-gram model
    """

#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment A, Step 2')
    parser.add_argument('-train-corpus', dest ='train_file', type=str, help='Path to train corpus file')
    parser.add_argument('-test-corpus', dest ='test_file', type=str, help='Path to test corpus file')
    parser.add_argument('-n', dest='n', default=2, type=int, help='Length of word-sequences to process (n-grams) [1,inf]')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of sequences to show in output')
    parser.add_argument('-smoothing', dest='smoothing', type=str, default=None, help='Method of smoothing [add1|gt]')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.train_file or not args.n or not args.test_file or args.n < 1:
        parser.print_help()
        exit('Missing required arguments')        
        
    # split and flatten array
    # sentences is list of sentences that start with START and end with STOP
    sentences = get_sentences(add_start_stop(args.train_file, args.n if not args.m else 1))
    
    
    n_grams = Counter(list(chain(*[parse_ngrams(sen, args.n) for sen in sentences])))
    n_min_1_grams = Counter(list(chain(*[parse_ngrams(sen, args.n - 1) for sen in sentences])))    
    
    n_grams = make_unseen(n_grams, n_min_1_grams, args.n)
    #if(args.smoothing == 'gt'):
    #    n_grams = good_turing_smoothing(n_grams)
    #    n_min_1_grams =
    #if(args.smoothing == 'add1'):
    #    n_grams = add_1_smoothing
    #if(args.smoothing is not None):
    #    n_min_1_grams = smoothe_min_1(n_min_1_grams)
    #    
    #calc_probabilities_seq_file(args.test_file, args.n, n_grams, n_min_1_grams)