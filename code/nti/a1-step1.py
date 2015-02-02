# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 20:34:12 2015

@author: markus
"""

from argparse import ArgumentParser

def read_file(file_in, n):
    """
    reads file_in line by line.
    
    returns: map of n-grams with frequency count
    """

    n_grams_frequency = {}    
    
    with open(file_in) as f:
        for line in f:
            print line
            
    return n_grams_frequency
    
if __name__ == "__main__":
    # here code for program
    
    parser = ArgumentParser(description='Assignment 1, Step 1')
    parser.add_argument('input_file')
    parser.add_argument('-n', dest='n', type=int, help='Length of word-sequences to process (n-grams)')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    args = parser.parse_args()
    
    n_grams_frequency = read_file(args.input_file, args.n)