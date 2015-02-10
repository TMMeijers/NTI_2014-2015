# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 11:36:38 2015

@author: markus
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams, sort_ngrams
from argparse import ArgumentParser
from collections import Counter
import itertools

#%%
def calc_probability_seq(seq, n_grams, n_min_1_grams):
    words = seq.split()
    
    # get w_n word
    w_n = words[-1]
    
    # P(w_n|w_1,w)2,...,w_{n-1}) = P(w_1, ..., w_n) / P(w_1, ..., w_{n-1})
    
    
#%%
def calc_probabilities_cond_file(cond_file, n_grams, n_min_1_grams):
    with open(cond_file) as f:
        return [calc_probability_seq(seq, n_grams, n_min_1_grams) for seq in f]

#%%
def get_sentences(ss):
    sentences = []    
    line_accum = []
    for l in ss:
        line_accum.append(l.split())
        if l[-5:-1] == 'STOP':
            sentences.append(list(itertools.chain(*line_accum)))
            line_accum = []
            
    return sentences
            
#%%
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
    sentences = get_sentences(ss)
    
    # statistics for all sentences
    n_grams = Counter()
    n_min_1_grams = Counter()
    for sen in sentences:
        n_grams += parse_ngrams(sen, args.n)
        n_min_1_grams += parse_ngrams(sen, args.n - 1)

    # create n-grams and (n - 1)-grams
    #n_grams = parse_ngrams(start_stop_lines, args.n)
    #n_min_1_grams = parse_ngrams(start_stop_lines, args.n - 1)
    
    # when conditional prob file is NOT given, print 10 most bigrams
    if args.m:
        print('n-grams:')
        print_ngrams(sort_ngrams(n_grams), args.m)
        print('\n(n-1)-grams')
        print_ngrams(sort_ngrams(n_min_1_grams), args.m)
        
    if args.cond_file:
        calc_probabilities_cond_file(args.cond_file, n_grams, n_min_1_grams)
    
    