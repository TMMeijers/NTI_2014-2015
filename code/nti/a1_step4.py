# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 19:56:40 2015

@author: markus
"""

#%%
import re
import numpy as np
import itertools as it
from a1_step1 import make_grams
from argparse import ArgumentParser
from collections import Counter, OrderedDict
from sys import exit

#%%
def is_end_of_sentence(seq):
    """
    returns true iff seq is a end-of-line sequence
    """
    return ['.', '.'] in seq or (len(seq) == 1 and re.match('(^=*$)+', seq[0][0]) is not None)

#%%
def remove_if(seq, one_of):
    """
    filters sequence by all elements in one_of. 
    
    returns new seq
    """
    return [x for x in seq if not x in one_of]

#%%
def filter_by_pos(seq):
    """
    remove all tags where the first charactger of a pos-tag is not
    an alpha numeric character. 
    
    returns new seq
    """
    return [s for s in seq if len(s) > 1 and not (len(s) == 2 and not s[1][0].isalnum())]

#%%
def make_language_model(tags, n):
    return Counter(list(it.chain(*[make_grams(add_start_stop_to_sentence(t, n - 1), n) for t in tags])))

#n_grams = Counter(list(chain(*[parse_ngrams(sen, args.n) for sen in sentences])))

#%%
def add_start_stop_to_sentence(sentence, n):
    return ['START'] * n + sentence + ['STOP'] * n

#%%
def get_tags_from_sentences(sentences):
    """
    returns each sentence as a list of pos-tags only
    """
    return [[t[1] for t in s] for s in sentences]

#%%
def fix_splitted(splitted):
    """
    takes care of some edge cases where for instance the sentence
    [ pianist\/bassoonist\/composer/NN ] would become
    [ pianist, bassoonist, composer, NN] but should actually be
    [ pianost//bassoonist//composer, NN] 
    
    and
    
    [['read', 'NNP|VBR']] would become
    [ read, NNP|VBR ] but should become
    [ read, NNP ] (thus dropping the VBR)

    """
    fixed = []
    for s in splitted:
        copy = list(s) # copy, list function call is necessary
        
        # composed word edge case
        if len(s) > 2:
            size = len(s)
            for i in xrange(1, size-1):
                copy[0] += s[i]
            copy[1] = copy[size-1]
            for i in xrange(2, size-1):
                del copy[i]
            del copy[-1]
            
        # two tags after word edge case
        if len(copy) > 1 and '|' in copy[1]:
            copy[1] = copy[1].split('|')[0]
        fixed.append(copy)
    return fixed

#%%
def pos_file_parser(in_file):
    """
    parses in_file
    
    return list of sentences which are list of tuples (word,tag)
    """
    
    sentences = []
    intermediate_sentence = []
    for line in in_file:
        splitted = fix_splitted([s.split('/') for s in remove_if(line.split(), ['[',']'])])
            
        # filter all pos tags which are not alphanumeric
        filtered = filter_by_pos(splitted)
        if filtered:
            intermediate_sentence.append(filtered)
        
        if is_end_of_sentence(splitted):
            sentences.append(intermediate_sentence)
            intermediate_sentence = []

    return [[(t[0], t[1]) for t in s] for s in [list(it.chain(*x)) for x in [sen for sen in sentences if sen]]]
    
#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment A, Step 4')
    parser.add_argument('-train-set', dest ='train_file', type=str, help='Path to training file')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.train_file:
        parser.print_help()
        exit('No training file specified')

    sentences = None    
    with open(args.train_file) as f: 
        sentences = pos_file_parser(f)
    if not sentences:
        exit('error parsing sentences')
    
    tags = get_tags_from_sentences(sentences)

    n = 3

    n_grams = make_language_model(tags, n)
    n_min1_grams = make_language_model(tags, n - 1)
    