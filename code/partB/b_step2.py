# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:26:01 2015

@author: T.M. Meijers, C.J. Boon, M. Pfundstein
"""

from sexp_parser import tokenize, parse_root
from b_step1 import get_sentences, binarize, get_depth
from argparse import ArgumentParser
from sys import exit
import re

#%%
def markov_init(sentence, h, v):
    if not v and not h:
        return binarize(sentence)
    else:
        return markovize(sentence, h, v)
        
def markovize(sen, h, v):
    if v > 1:
        v_sen = markovize_v(sen, v)
        sen = str(v_sen).replace('[', '(').replace(']', ')').replace('\'', '').replace('(,', '(+').replace(',)', '+)').replace(',', '').replace('+', ',')

    if not h > 0:
        return sen
    
    markov_sen = []
    sub_sen = re.search(r'\((.*)\)', sen).group(1).split()
    #Add ROOT to the list
    root = sub_sen[0]
    markov_sen.append(root)
    #Cleanup sub sentence to make parsing easier
    sub_sen = " ".join(sub_sen[1:]).replace(",", "+").replace("'", '"')

    markov_sen = markovize_recursive_h(markov_sen, sub_sen, root, h) 
    return  str(markov_sen).replace('[', '(').replace(']', ')').replace("'", "").replace(",", "").replace("+", ",").replace('"',"'")

#%%
def markovize_v(sub_sen, v):
    # parse sexp to tree
    tree = parse_root(tokenize(sub_sen))
    # add vertical markovization to tree
    parse_node(tree, [], 0, v)
    return write_tree(tree)

#%%
def parse_node(node, parents, depth, v):

    node_name = node[0] 
    node_children = node[1] if type(node[1]) is list else []

    if v > 1 and depth > 1 and node_children:
        node[0] = node[0] + '^' + "-".join(parents[-(v-1):])    
    
    for child in node_children:
        new_parents = parents + [node_name] if depth > 0 else parents
        parse_node(child, new_parents, depth + 1, v)

        
#%%
def write_tree(node):
    node_children = node[1] if type(node[1]) is list else []
    for child in node_children:
        write_tree(child)

    if node_children:
        for c in node_children:
            node.append(c)
        del node[1]

    return node
    
#%%
def get_left_and_right_sub(sub_sen):
    depth = get_depth(sub_sen)
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
    
    if not right_sub: right_sub = None
    return left_sub, right_sub

#%%    
def markovize_recursive_h(markov_sen, sub_sen, root, h):
      
    left_sub, right_sub = get_left_and_right_sub(sub_sen)
   
    right_root = left_sub[0] + "@"

    # If the left part is binarized, add to the result.
    if len(left_sub) is 2:
        markov_sen.append(left_sub)
    
    #Else keep markovizing
    else:
        markov_sen.append([left_sub[0]])
        left_sub = " ".join(left_sub[1:])
        # Recurse on the left part of the sub sentence
        markov_sen[1] = markovize_recursive_h(markov_sen[1], left_sub, root, h)
    # If there is a right part
    if right_sub:
        #Add a new inner-symbol that shows the horizontal markovization
        if "@" in markov_sen[0]:            
            new_inner = markov_sen[0].split('_')
            #Retrieve the last element of the list
            if len(new_inner) is h+1:                
                prev_inner = new_inner[2:]
            else:
                prev_inner = new_inner[1:]
            if prev_inner:
                new_inner = new_inner[0] + '_' + '_'.join(prev_inner) + "_" + markov_sen[1][0]
            else:
                new_inner = new_inner[0] + '_' + markov_sen[1][0]
        else:
            new_inner = "@" + markov_sen[0] + "->_" + markov_sen[1][0]
            
        markov_sen.append([new_inner])
        right_sub = new_inner + right_sub
        
        #Right part is fully markovized 
        if len(right_sub.split()) == 3:
            right_sub = re.search(r'\((.*)\)', right_sub).group(1)
            markov_sen[2].append([right_sub])
            return markov_sen
        else:
            #Recurse on the right part of the sub sentence
            markov_sen[2] = markovize_recursive_h(markov_sen[2], right_sub, right_root, h)
    return markov_sen

#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment B, Step 2')
    parser.add_argument('-hor', dest='h', type=int, default=0, help='Parameter max-length horizontal histories')
    parser.add_argument('-ver', dest='v', type=int, default=0, help='Vertical history parameter. Either 1 or 2')    
    parser.add_argument('-input', dest='input_file', type=str, default=None, help='Path to input file')
    parser.add_argument('-output', dest='output_file', type=str, default=None, help='Path to output file')
    args = parser.parse_args()
    
    # INPUT CHECKS 
    if not args.input_file or not args.output_file:
        parser.print_help()
        exit('Input or output file not specified')
    if args.v is 1:
        args.v = 0
    elif args.v < 0:
        parser.print_help()
        exit('v must be a positive integer')
    if args.h < 0:
        parser.print_help()
        exit('h should be either 0 (for an infinite history) or a positive integer')
    
    sentences = get_sentences(args.input_file)
    sentences = [markov_init(sen, args.h, args.v) + '\n' for sen in sentences]
    with open(args.output_file, 'w+') as f:
        f.writelines(sentences)