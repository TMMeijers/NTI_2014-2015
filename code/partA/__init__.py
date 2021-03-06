a1_step1.py                                                                                         000755  000765  000024  00000003773 12466704161 013536  0                                                                                                    ustar 00markus                          staff                           000000  000000                                                                                                                                                                         #!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 20:34:12 2015

@author: Markus Pfundstein, Thomas Meijers, Cornelis Boon
"""

from argparse import ArgumentParser
from collections import OrderedDict
from collections import Counter
import string

def sort_ngrams(ngrams):
    return OrderedDict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))

 
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
    return splitted_line
    
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
    n_grams_frequency = Counter(parse_ngrams(lines, args.n))
    
    freq_sum = sum(n_grams_frequency.values())
    print 'sum: {}'.format(freq_sum)
    
    # sort n_grams by value in descending order
    n_grams_frequency = sort_ngrams(n_grams_frequency)
    
    print_ngrams(n_grams_frequency, args.m)
     a1_step2.py                                                                                         000644  000765  000024  00000014531 12470142143 013515  0                                                                                                    ustar 00markus                          staff                           000000  000000                                                                                                                                                                         # -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 11:36:38 2015

@author: markus
"""

from __future__ import print_function
from start_stop_adder import add_start_stop
from a1_step1 import parse_ngrams, print_ngrams, sort_ngrams
from argparse import ArgumentParser
from collections import Counter
from sys import exit
import itertools

#%%
def set_permutations(s):
    """
    generates all permutations from set s
    
    resulting array will be of length |s|!
    """
    return [list(p) for p in itertools.permutations(s)]

#%%
def product(lst):
    """
    calculates product of a list
    """
    return reduce(lambda x,y: x*y, lst)

#%%
def seq_prob(w_all, n, n_grams, n_min_1_grams):
    
    m = n - 1# if n > 1 else n
    
    # add START and STOPS
    for i in xrange(0, m):
        w_all.insert(0, 'START')
        w_all.append('STOP')

    parsed_n_grams = parse_ngrams(w_all, n)
    #print(parsed_n_grams)

    if n is 1:
        return product([rel_prob(ng.split(), n_grams) for ng in parsed_n_grams])
    
    return product([cond_prob(ng.split(), ng.split()[0:-1], n_grams, n_min_1_grams) for ng in parsed_n_grams])

#%%
def rel_prob(w_all, n_grams):
    """ 
    calculates relative probability of sentence w_all given histogram n_grams
    """
    
    s = sum(n_grams.values())
    # divison by zero
    if not s:
        return 0.0
    p_all = n_grams[' '.join(w_all)]
    return float(p_all) / s

#%%
def cond_prob(w_all, w_rest, n_grams, n_min_1_grams):
    """
    calculates conditional probability of w_all|w_rest given histogram n_grams
    and n_min_1_grams
    
    P(w_n|w_1,w)2,...,w_{n-1}) = P(w_1, ..., w_n) / P(w_1, ..., w_{n-1})
    """
    p_all = n_grams[' '.join(w_all)]
    p_rest = n_min_1_grams[' '.join(w_rest)]
    
    # avoid division by zero
    if not p_rest:
        return 0.0
    
    return float(p_all) / p_rest
    
#%%
def calc_probabilities_cond_file(cond_file, n, n_grams, n_min_1_grams):
    """
    calculates all probabilities for cond_file given n_grams and n_min_1_grams
    considers only sentences of length n
    """
    with open(cond_file) as f:
        # dictionary for storing 'sentence' -> probability mapping
        probs = {}
        for seq in f:
            # only consider sentences of length n
            words = seq.split()
            if len(words) is not n:
                continue
            p = -1
            # conditional prob is only possible when n > 1. P(x|a)
            # so this will return 0.0
            p = cond_prob(words, words[0:-1], n_grams, n_min_1_grams)
            probs[seq.strip()] = p
            
        return probs

#%%
def get_sentences(ss):
    """
    parses from START to STOP and puts every sentence in a list
    """
    sentences = []    
    line_accum = []
    for l in ss:
        # put current line on accumulator
        line_accum.append(l.split())
        # we have a stop line, thus we flatten accumulator list and put stuff
        # into sentences list
        if l[-5:-1] == 'STOP':
            sentences.append(list(itertools.chain(*line_accum)))
            line_accum = []
            
    return sentences
            
#%%
def calc_probabilities_seq_file(seq_file, n, n_grams, n_min_1_grams):
    with open(seq_file) as f:
        return {seq.strip() : seq_prob(seq.split(), n, n_grams, n_min_1_grams) for seq in f}
            
#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment A, Step 2')
    parser.add_argument('-corpus', dest ='input_file', type=str, help='Path to corpus file')
    parser.add_argument('-n', dest='n', default=2, type=int, help='Length of word-sequences to process (n-grams) [1,inf]')
    parser.add_argument('-m', dest='m', type=int, default=None, help='Number of n-grams to show in output')
    parser.add_argument('-conditional-prob-file', dest='cond_file', type=str, help='file for conditional probabilities')
    parser.add_argument('-sequence-prob-file', dest='seq_file', type=str, help='file for sequence probabilities')
    parser.add_argument('-scored-permutations', action='store_true', dest='scored_perms', help='check permutations')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.input_file or not args.n or args.n < 1:
        parser.print_help()
        exit('Missing required arguments')
        
    if args.scored_perms and args.n is not 2:
            exit('n must be 2 when using permutations')
            
    if not args.cond_file and not args.m and not args.seq_file and not args.scored_perms:
        parser.print_help()
        exit('What shall I do?')
    
    # split and flatten array
    # sentences is list of sentences that start with START and end with STOP
    sentences = get_sentences(add_start_stop(args.input_file, args.n if not args.m else 1))

    #print(sentences)
    
    n_grams = Counter(list(itertools.chain(*[parse_ngrams(sen, args.n) for sen in sentences])))
    n_min_1_grams = Counter(list(itertools.chain(*[parse_ngrams(sen, args.n - 1) for sen in sentences])))

    # when n=1 n_min_1_grams would become a dict instead of a Counter. To keep
    # stuff consistent...
    if not n_min_1_grams:
        n_min_1_grams = Counter()

    # if wished, print m most bigrams
    if args.m:
        print('n-grams:')
        print_ngrams(sort_ngrams(n_grams), args.m)
        print('\n(n-1)-grams')
        print_ngrams(sort_ngrams(n_min_1_grams), args.m)
        exit()

    # if cond file is given calculate probabilities
    if args.cond_file:
        probs = calc_probabilities_cond_file(args.cond_file, args.n, n_grams, n_min_1_grams)
        print(probs)
        exit()
        
    # calculate probabilities of sequence file
    if args.seq_file:
        probs = calc_probabilities_seq_file(args.seq_file, args.n, n_grams, n_min_1_grams)
        print(probs)
        exit()
        
    # calculate probabilities of permutations         
    if args.scored_perms:
        set_a = ['know', 'I', 'opinion', 'do', 'be', 'your', 'not', 'may', 'what']
        set_b = ['I', 'do', 'not', 'know']
        
        perms_a = set_permutations(set_a)
        perms_b = set_permutations(set_b)
        
        p_perms_a = Counter({' '.join(seq) : seq_prob(seq, args.n, n_grams, n_min_1_grams) for seq in perms_a})
        p_perms_b = Counter({' '.join(seq) : seq_prob(seq, args.n, n_grams, n_min_1_grams) for seq in perms_b})
        
        print(p_perms_a.most_common(2))
        print(p_perms_b.most_common(2))
        
        exit()                                                                                                                                                                       start_stop_adder.py                                                                                 000644  000765  000024  00000004464 12466704161 015455  0                                                                                                    ustar 00markus                          staff                           000000  000000                                                                                                                                                                         # -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 10:52:24 2015

@author: markus
"""

from __future__ import print_function
from argparse import ArgumentParser

#%%
def add_start_stop(in_file, n = 1):

    line_count = 0 # current line
    lines = [] # lines
    
    last_line_newline = False # bool that indicates if last line was '\n'
    start_after_stop = False # avoid multiple stops
    
    sym_start = 'START ';
    sym_stop = ' STOP';

    # n is for multiplying the START, STOP symbols. When n = 2 we want
    # START at the beginning for each sentence. Hence sym_start * (n-1)
    # If n = 1, we want the same
    n -= 1
    if not n: n = 1
    
    # idea is to read in the whole file into an array and to record where 
    # we encounter START and STOPS. 
    with open(in_file) as f_in:
        for l in f_in: 
            
            lines.append(l)
            #print(repr(l))
            
            if l == '\n':
                if start_after_stop:
                    stop_line = lines[line_count - 1].replace('\n', '') + (sym_stop * n) + '\n'
                    lines[line_count - 1] = stop_line
                    start_after_stop = False
                last_line_newline = False 
                #print(r'STOP at line {}'.format(line_count - 1))
                last_line_newline = True

            elif line_count == 0: # first line in text and there is text
                lines[0] = (sym_start * n) + lines[0]
                last_line_newline = False
                start_after_stop = True
            elif last_line_newline: # line before current line was '\n'
                lines[line_count] = (sym_start * n) + lines[line_count]
                last_line_newline = False
                start_after_stop = True
                
            line_count += 1
    
    return lines
    
#%%
if __name__ == "__main__":
    # here code for program
    
    parser = ArgumentParser(description='Adds START AND STOP')
    parser.add_argument('-corpus', dest ='input_file', type=str, help='Path to corpus file')
    parser.add_argument('-target', dest ='output_file', type=str, help='Path to edited file')
    
    args = parser.parse_args()
    
    start_stop_lines = add_start_stop(args.input_file, 1)
    with open(args.output_file, 'w') as f_out:
        for l in start_stop_lines:
            f_out.write(l)

    
                                                                                                                                                                                                                a1-step1                                                                                            000755  000765  000024  00000000223 12466704161 013010  0                                                                                                    ustar 00markus                          staff                           000000  000000                                                                                                                                                                         #!/bin/sh

# if you use different python program than change this
PY=python

# pass all arguments to script to python script
python a1_step1.py $@
                                                                                                                                                                                                                                                                                                                                                                             a1-step2                                                                                            000755  000765  000024  00000000223 12466704161 013011  0                                                                                                    ustar 00markus                          staff                           000000  000000                                                                                                                                                                         #!/bin/sh

# if you use different python program than change this
PY=python

# pass all arguments to script to python script
python a1_step2.py $@
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             