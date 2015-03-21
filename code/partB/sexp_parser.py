# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 14:23:56 2015

@author: markus
"""

#%%
# S-Exp parser taken from: http://stackoverflow.com/questions/19749883/how-to-parse-parenthetical-trees-in-python
# Added own modifications to work for the assignment
def tokenize(s):
    import re
    toks = re.compile(' +|[A-Za-z]+|[()]')
    for match in toks.finditer(s):
        s = match.group(0)
        if s[0] == ' ':
            continue
        if s[0] in '()':
            yield (s, s)
        else:
            yield ('###WORD###', s)


# Parse once we're inside an opening bracket.
def parse_inner(toks):
    ty, name = next(toks)
    children = []
    word = None
    while True:
        ty, s = next(toks)
        if ty == '(':
            children.append(parse_inner(toks))
        elif ty == '###WORD###':
            word = s
        elif ty == ')':
            if word:
                return [name, word]
            else:
                return [name, children]

def parse_root(toks):
    ty, _ = next(toks)
    return parse_inner(toks)