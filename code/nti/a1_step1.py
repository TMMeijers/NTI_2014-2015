#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 20:34:12 2015

@author: Markus Pfundstein, Thomas Meijers, Cornelis Boon
"""

from argparse import ArgumentParser
from collections import OrderedDict
from collections import Counter
import string

def make_grams(words, n):
    """
    make n-grams from list of words
    """
    
    return [string.join(words[i:i+n]) for i in xrange(len(words)-n+1)]

def read_words(file_in):
    """
    returns list of all words in file_in
    """
    
    with open(file_in) as f:
        return [w for w in f.read().split()]


def parse_ngrams(splitted_line, n):
    """
    parses a file and makes (unsorted) frequency table of n-grams
    """
    
    n_grams_frequency = {}    
    if n < 1:
        return n_grams_frequency
        
    if n > 1:
        splitted_line = make_grams(splitted_line, n)
    return Counter(splitted_line)
    
def print_ngrams(n_grams, m = None):
    """
    prints n grams 
    """
    
    idx = 0
    for word, freq in n_grams.items():
        if idx is m:
            break
        idx += 1
        print '{} {}'.format(word, freq)
    
if __name__ == "__main__":
    # here code for program
    
    parser = ArgumentParser(description='Assignment A, Step 1')
    parser.add_argument('-corpus', dest ='input_file', type=str, help='Path to corpus file')
    parser.add_argument('-n', dest='n', type=int, help='Length of word-sequences to process (n-grams)')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    args = parser.parse_args()
    
    lines = read_words(args.input_file)
    n_grams_frequency = parse_ngrams(lines, args.n)
    
    freq_sum = sum(n_grams_frequency.values())
    print 'sum: {}'.format(freq_sum)
    
    # sort n_grams by value in descending order
    n_grams_frequency = OrderedDict(sorted(n_grams_frequency.items(), key=lambda x: x[1], reverse=True))
    
    print_ngrams(n_grams_frequency, args.m)
