# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 19:56:40 2015

@author: markus
"""

#%%
import re
import numpy as np
import itertools as it

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

def build_language_model(pos_seq):
    return 0

#%%
def pos_file_parser(in_file):
    """
    parses in_file
    
    return something
    """
    
    sentences = []
    intermediate_sentence = []
    for line in in_file:
        splitted = [s.split('/') for s in remove_if(line.split(), ['[',']'])]
        
            
        # filter all pos tags which are not alphanumeric
        filtered = filter_by_pos(splitted)
        if filtered:
            intermediate_sentence.append(filtered)
        
        if is_end_of_sentence(splitted):
            sentences.append(intermediate_sentence)
            intermediate_sentence = []

    return [[(t[0], t[1]) for t in s] for s in [list(it.chain(*x)) for x in [sen for sen in sentences if sen]]]