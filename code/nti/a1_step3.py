# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:41:40 2015

@author: Markus Pfundstein, Thomas Meijers, Cornelis Boon
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams
from a1_step2 import get_sentences
from argparse import ArgumentParser
from collections import Counter, OrderedDict
from sys import exit
from itertools import product, chain

def sort_ngrams_bidirectional(ngrams, order):
    return OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=order))

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
def add_labda_smoothing(test_sentences, n_grams, n_min_1_grams, n):
    """
    Applies add-1 smoothing to the bi-gram model
    """
    # As in assignment: assume V = unique words in train corpus, e.g. length of
    # n_min_1_grams for n = 2
    V = len(n_min_1_grams)
    return {' '.join(w_all) : add_labda_prob(w_all, n_grams, n_min_1_grams, n, V) for w_all in test_sentences}
        
def add_labda_prob(w_all, n_grams, n_min_1_grams, n, V):
    """
    Calculates the probability after add labda smoothing
    """
    parsed_n_grams = parse_ngrams(w_all, n)
    prob = 0
    for ng in parsed_n_grams:
        prob += float(n_grams[ng] + 1) / (V + n_min_1_grams[ng[0]])
    return prob
    
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
    parser.add_argument('-smoothing', dest='smoothing', type=str, default='no', help='Method of smoothing [add1|gt|no]')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.train_file or not args.n or not args.test_file or args.n is not 2:
        parser.print_help()
        exit('Missing required arguments or n is not 2 (assignment is for bigrams)')     
        
    # split and flatten array
    # sentences is list of sentences that start with START and end with STOP
    sentences = get_sentences(add_start_stop(args.train_file, args.n if not args.m else 1))
    test_sentences = get_sentences(add_start_stop(args.test_file, args.n if not args.m else 1))
    
    
    n_grams = Counter(list(chain(*[parse_ngrams(sen, args.n) for sen in sentences])))
    n_min_1_grams = Counter(list(chain(*[parse_ngrams(sen, args.n - 1) for sen in sentences])))   
        
    if args.smoothing == 'add1':
        probs = add_labda_smoothing(test_sentences, n_grams, n_min_1_grams, args.n)
        print('{} most likely sentences:'.format(args.m))
        print_ngrams(sort_ngrams_bidirectional(probs, True), args.m)
        print('{} least likely sentences:'.format(args.m))
        print_ngrams(sort_ngrams_bidirectional(probs, False), args.m)
    elif args.smoothing == 'gt':
        good_turing_smoothing()
    else:
        True
    # Doesn't work like this
    #n_grams = make_unseen(n_grams, n_min_1_grams, args.n)
    #if(args.smoothing == 'gt'):
    #    n_grams = good_turing_smoothing(n_grams)
    #    n_min_1_grams =
    #if(args.smoothing == 'add1'):
    #    n_grams = add_1_smoothing
    #if(args.smoothing is not None):
    #    n_min_1_grams = smoothe_min_1(n_min_1_grams)
    #    
    #calc_probabilities_seq_file(args.test_file, args.n, n_grams, n_min_1_grams)