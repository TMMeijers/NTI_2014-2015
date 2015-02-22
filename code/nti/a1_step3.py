# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:41:40 2015

@author: Markus Pfundstein, Thomas Meijers, Cornelis Boon
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams
from a1_step2 import get_sentences, calc_probabilities_seq_file
from argparse import ArgumentParser
from collections import Counter, OrderedDict
from sys import exit
from itertools import product, chain

def sort_ngrams_bidirectional(ngrams, order):
    return OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=order))

#%%
def cond_prob_add1(w_all, w_rest, n_grams, n_min_1_grams):
    """
    calculates conditional probability of w_all|w_rest given histogram n_grams
    and n_min_1_grams with add 1 smoothing
    
    P(w_n|w_1,w)2,...,w_{n-1}) = P(w_1, ..., w_n) + 1 / P(w_1, ..., w_{n-1}) + V
    """
    p_all = n_grams[' '.join(w_all)]
    p_rest = n_min_1_grams[' '.join(w_rest)]
        
    return (float(p_all) + 1) / (p_rest + len(n_min_1_grams))

#%%
def add_labda_smoothing(test_sentences, n_grams, n_min_1_grams, n):
    """
    Applies add-1 smoothing to the bi-gram model
    """
    # As in assignment: assume V = unique words in train corpus, e.g. length of
    # n_min_1_grams for n = 2
    V = len(n_min_1_grams)
    return {' '.join(w_all): add_labda_prob(w_all, n_grams, n_min_1_grams, n, V) for w_all in test_sentences}
        
def add_labda_prob(w_all, n_grams, n_min_1_grams, n, V):
    """
    Calculates the probability after add labda smoothing
    """
    parsed_n_grams = parse_ngrams(w_all, n)
    prob = 0
    for ng in parsed_n_grams:
            prob += float(n_grams[ng] + 1) / (1 + n_min_1_grams[' '.join(ng.split()[0])] + V)
    return prob
    
#%%
def good_turing_smoothing(test_sens, n_grams, n_min_1, n):
    """
    Applies good-turing smoothing to the bi-gram model
    """
    # Total unseen events    
    Nzero = len(n_min_1_grams)**2 - len(n_grams)
    #Upper bound for smoothing    
    k = 5    
    # Frequency of frequencies for frequencies of 0 to 6
    N = {i : len([ngram for ngram in n_grams.values() if ngram is i]) for i in xrange(k+2) if i is not 0}
    N[0] = Nzero
    
    #Smoothe the bi-gram model 
    for ng in n_grams:
        if  n_grams[ng] < 6 and n_grams[ng] > 0:
            n_grams[ng] = gt_smooth(n_grams[ng], N, k)    
    
    return {' '.join(w_all) : good_turing_prob(w_all, n_grams, n_min_1, n, k, N) for w_all in test_sens}
    
def good_turing_prob(w_all, ngrams, nmin1, n, k, N):
    """
    Returns the probability of sentences once the bi-grams have been smoothed
    """
    parsed_n_grams = parse_ngrams(w_all, n)
    prob = 0

    #Calculate the probabilities    
    for ng in parsed_n_grams:
        if ng not in n_grams:
            prob += N[1]/(N[0]*len(n_grams))
        else:
            normalizer = sum(n_grams[ngram] for ngram in n_grams if ngram.split()[0] == ng.split()[0])
            if normalizer == 0:
                normalizer = 1
            prob += n_grams[ng]/normalizer
    return prob
    
def gt_smooth(c, N, k):    
    return float( ((c +1)* (N[c+1]/N[c]) - c*(((k+1)*N[k+1])/N[1]) )/(1 - (((k+1)*N[k+1])/N[1] )))


#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment A, Step 2')
    parser.add_argument('-train-corpus', dest ='train_file', type=str, help='Path to train corpus file')
    parser.add_argument('-test-corpus', dest ='test_file', type=str, help='Path to test corpus file')
    parser.add_argument('-n', dest='n', default=2, type=int, help='Length of word-sequences to process (n-grams) [1,inf]')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of sequences to show in output')
    parser.add_argument('-smoothing', dest='smoothing', type=str, default=None, help='Method of smoothing [add1|gt|no]')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.train_file or not args.n or not args.test_file or args.n is not 2:
        parser.print_help()
        exit('Missing required arguments or n is not 2 (assignment is for bigrams)')     
        
    # split and flatten array
    # sentences is list of sentences that start with START and end with STOP
    sentences = get_sentences(add_start_stop(args.train_file, args.n if not args.m else 1))
    
    
    n_grams = Counter(list(chain(*[parse_ngrams(sen, args.n) for sen in sentences])))
    n_min_1_grams = Counter(list(chain(*[parse_ngrams(sen, args.n - 1) for sen in sentences])))   
        
    if args.smoothing:
        test_sentences = get_sentences(add_start_stop(args.test_file, args.n if not args.m else 1))        
        if args.smoothing == 'add1':
            probs = add_labda_smoothing(test_sentences, n_grams, n_min_1_grams, args.n)
        elif args.smoothing == 'gt':
            probs = good_turing_smoothing(test_sentences, n_grams, n_min_1_grams, args.n)        
        percentagenonzero = 100 *len([prob for    prob in probs if probs[prob] != 0])/len(probs)
        print('{} % of {} have a nonzero probability'.format(percentagenonzero, len(probs)))        
        print('{} most likely sentences:'.format(args.m))
        print_ngrams(sort_ngrams_bidirectional(probs, True), args.m)
        print('{} least likely sentences:'.format(args.m))
        print_ngrams(sort_ngrams_bidirectional(probs, False), args.m)
        
    else:
        probs = calc_probabilities_seq_file(args.test_file, args.n, n_grams, n_min_1_grams)
        print(probs)
        exit()