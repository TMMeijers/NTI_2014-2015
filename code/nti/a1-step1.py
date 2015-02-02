# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 20:34:12 2015

@author: markus
"""

from argparse import ArgumentParser

if __name__ == "__main__":
    # here code for program
    
    parser = ArgumentParser(description='Assignment 1, Step 1')
    parser.add_argument('file')
    parser.add_argument('-n', dest='n', type=int, help='Length of word-sequences to process (n-grams)')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    
    args = parser.parse_args()
    print args