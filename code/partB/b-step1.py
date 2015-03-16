# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:19:40 2015

@author: T.M. Meijers, C.J. Boon, M. Pfundstein
"""

#%%

from argparse import ArgumentParser
from sys import exit
import re

def get_depth(sub_sen):
#Finds the depth of the current subphrase by counting matching brackets.
#If the subsentence is the root of itself, then return 0
   par_open = 1
   par_closed = 0
   for char in list(re.search(r'\((.*)\)', sub_sen).group(1)):
       if char == "(":
           par_open += 1
       if char == ")":
           par_closed += 1
       if par_open is par_closed:
           return par_closed
   return 0


def binarize_recursive(bin_sen, sub_sen):
    # Find the depth of the current sentence fragment
    depth = get_depth(sub_sen)
    # Initialize left and right part of sentence fragment
    left_sub = ""
    right_sub = ""
    #If the sentence is at the top, just go one layer deeper    
    if depth is 0:
        left_sub = re.search(r'\((.*)\)', sub_sen).group(1)
        
   #Else split the sentence into a left and right part
    else:
        splitted_sub_sen = sub_sen.split(")", depth)
        
        left_sub = ")".join(splitted_sub_sen[0:depth]) + ") "  
        left_sub = re.search(r'\((.*)\)', left_sub).group(1)
        
        right_sub = ") ".join(splitted_sub_sen[depth:])       
        
    left_sub = left_sub.split()
    
    # If the left part if binarized, add to the result.
    if len(left_sub) is 2:
        bin_sen.append(left_sub)
    
    #Else keep binarizing
    else:
        bin_sen.append([left_sub[0]])
        left_sub = " ".join(left_sub[1:])
        # Recurse on the left part of the sub sentence
        bin_sen[1] = binarize_recursive(bin_sen[1], left_sub)
    
    # If there is a right part
    if right_sub:
        #Add a new inner-symbol that shows the horizontal markovization
        if "@" in bin_sen[0]:
            new_inner = bin_sen[0] + "_" + bin_sen[1][0]
        else:
            new_inner = "@" + bin_sen[0] + "->_" + bin_sen[1][0]
            
        bin_sen.append([new_inner])
        right_sub = new_inner + right_sub
        
        #Right part is fully binarized 
        if len(right_sub.split()) == 3:
            right_sub = re.search(r'\((.*)\)', right_sub).group(1)
            bin_sen[2].append([right_sub])
            return bin_sen
        else:
            #Recurse on the right part of the sub sentence
            bin_sen[2] = binarize_recursive(bin_sen[2], right_sub)
    return bin_sen

def binarize(sen):
    """
    Binarizes sentences and sub-parts of sentences.
    Input:
    (NP (NNP Rolls-Royce) (NNP Motor) (NNPS Cars) (NNP Inc.))
    Output:
    (NP (NNP Rolls-Royce) (@NP-> NNP (NNP Motor) (@NP-> NNP NNP (NNPS
    Cars) (@NP-> NNP NNP NNPS (NNP Inc.)))))
    """
   
    bin_sen = []
    #Remove outer brackets
    sub_sen = re.search(r'\((.*)\)', sen).group(1).split()
    #Add ROOT to the list    
    bin_sen.append(sub_sen[0])
    #Cleanup sub sentence to make parsing easier
    sub_sen = " ".join(sub_sen[1:]).replace(",", "+").replace("'", '"')
    # Activate recursion
    bin_sen = binarize_recursive(bin_sen, sub_sen)
    #Recompile the sentence back to its original but binarized state
    return str(bin_sen).replace('[', '(').replace(']', ')').replace("'", "").replace(",", "").replace("+", ",").replace('"',"'")
    
def get_sentences(input_file):
    """
    Takes an input file and copies all the sentences into an array.
    """
    
    with open(input_file) as f:
    	return [line.rstrip('\n') for line in f if line.rstrip('\n')]
    
    
    
#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment B, Step 1')
    parser.add_argument('-input', dest='input_file', type=str, default=None, help='Path to input file')
    parser.add_argument('-output', dest='output_file', type=str, default=None, help='Path to output file')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.input_file:
        parser.print_help()
        exit('No input file specified (-input)')
    if not args.output_file:
        parser.print_help()
        exit('No output file specified (-output)')
        
    sentences = get_sentences(args.input_file)
    with open(args.output_file, 'w+') as f:
        for s in sentences:
            f.write(binarize(s) + '\n\n')
