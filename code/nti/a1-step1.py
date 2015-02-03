#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 20:34:12 2015

@author: markus
"""

from argparse import ArgumentParser
from collections import OrderedDict
from string import join


def make_grams(words, n):
    """
    make n-grams from list of words
    """
    
    n_grams = []
    for i in range(len(words)-n+1):
        n_grams.append(join(words[i:i+n]))
    
    return n_grams

def slurp(file_in):
    """
    slurps entire file_in into string
    """
    
    corpus = ''
    with open(file_in) as f:
        corpus = f.read()
    return corpus

def parse_ngrams(file_in, n):
    """
    parses a file and makes (unsorted) frequency table of n-grams
    """
    
    n_grams_frequency = {}    
    if n < 1:
        return n_grams_frequency
        
    splitted_line = slurp(file_in).split()
    if n > 1:
        splitted_line = make_grams(splitted_line, n)
    for word in splitted_line:
        if word in n_grams_frequency.keys():
            n_grams_frequency[word] += 1
        else:
            n_grams_frequency[word] = 1
                
    return n_grams_frequency
    
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
    
    parser = ArgumentParser(description='Assignment 1, Step 1')
    parser.add_argument('input_file')
    parser.add_argument('-n', dest='n', type=int, help='Length of word-sequences to process (n-grams)')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    args = parser.parse_args()
    
    n_grams_frequency = parse_ngrams(args.input_file, args.n)
    
    # sort n_grams by value in descending order
    n_grams_frequency = OrderedDict(sorted(n_grams_frequency.items(), key=lambda x: x[1], reverse=True))
    
    print_ngrams(n_grams_frequency, args.m)
