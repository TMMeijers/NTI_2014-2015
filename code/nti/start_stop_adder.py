# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 10:52:24 2015

@author: markus
"""

from __future__ import print_function
from argparse import ArgumentParser

#%%
def add_start_stop(in_file):
    line_count = 0 # current line
    lines = [] # lines
    
    last_line_newline = False # bool that indicates if last line was '\n'
    start_after_stop = False # avoid multiple stops
    
    sym_start = 'START ';
    sym_stop = ' STOP';
    
    # idea is to read in the whole file into an array and to record where 
    # we encounter START and STOPS. 
    with open(in_file) as f_in:
        for l in f_in: 
            
            lines.append(l)
            #print(repr(l))
            
            if l == '\n':
                if start_after_stop:
                    stop_line = lines[line_count - 1].replace('\n', '') + sym_stop + '\n'
                    lines[line_count - 1] = stop_line
                    start_after_stop = False
                last_line_newline = False 
                #print(r'STOP at line {}'.format(line_count - 1))
                last_line_newline = True

            elif line_count == 0: # first line in text and there is text
                lines[0] = sym_start + lines[0]
                last_line_newline = False
                start_after_stop = True
            elif last_line_newline: # line before current line was '\n'
                lines[line_count] = sym_start + lines[line_count]
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
    
    start_stop_lines = add_start_stop(args.input_file)
    with open(args.output_file, 'w') as f_out:
        for l in start_stop_lines:
            f_out.write(l)

    
    