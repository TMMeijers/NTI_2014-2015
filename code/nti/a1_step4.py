# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 19:56:40 2015

@author: markus
"""

#%%

from itertools import chain
from a1_step1 import make_grams
from argparse import ArgumentParser
from collections import Counter
from pos_parser import add_start_stop_to_sentence, get_tags_from_sentences, pos_file_parser
from sys import exit

#%%
class LanguageModel:
    def __init__(self, tags, n):
        """
        initializes language model. 
        """
        self.n_grams = Counter(list(chain(*[make_grams(add_start_stop_to_sentence(t, 1), n) for t in tags])))
        self.n_min1_grams = Counter(list(chain(*[make_grams(add_start_stop_to_sentence(t, 1), n - 1) for t in tags])))

    def cond_prob(self, tags):
        """
        returns cond probability for a tag N-gram.
        cond_prob([t1,t2,t3]) = P([t3|t2,t1]) = count('t1 t2 t3')/count('t1 t2')
        """        
        p_all = self.n_grams[' '.join(tags)]
        p_rest = self.n_min1_grams[' '.join(tags[:-1])]
    
        return float(p_all) / p_rest if p_rest else 0.0

#%%
class LexicalModel:
    def __init__(self, sentences, tags):
        """
        initializes lexical model
        """
        self.unigrams = Counter(list(chain(*[make_grams(t, 1) for t in tags])))
        self.word_tag_pairs = Counter([' '.join(wt) for wt in chain(*sentences)])

        
    def cond_prob(self, word_tag_pair):
        """
        returns cond probability for tag word combination
        cond_prob([word, tag]) = P(word|tag) = count('word  tag')/count('tag')
        """
        
        p_all = self.word_tag_pairs[' '.join(word_tag_pair)]
        p_rest = self.unigrams[word_tag_pair[1]]
                
        return float(p_all) / p_rest if p_rest else 0.0

     
#%%
def test():
    with open('data/s3/simple.pos') as f: 
        sentences = pos_file_parser(f)
    if not sentences:
        exit('error parsing sentences')
    
    tags = get_tags_from_sentences(sentences)

    print 'test language model on simple.pos without smoothing:'
    n = 3
    lang_mod = LanguageModel(tags, n)
    
    assert lang_mod.cond_prob(['START', 'DT', 'NN']) == 1.0, "lang_mod.cond_prob(['START', 'DT', 'NN']) should be 1.0 but isn't"
    print 'test 1 passed'
    
    assert lang_mod.cond_prob(['JJ', 'NN', 'NNS']) == 0.3333333333333333, "lang_mod.cond_prob(['JJ', 'NN', 'NNS']) should be 0.3333333333333333 but isn't"
    print 'test 2 passed'
    
    assert lang_mod.cond_prob(['NN', 'IN', 'DT']) == 0.5, "lang_mod.cond_prob(['NN', 'IN', 'DT']) should be 0.5 but isn't"
    print 'test 3 passed'
        
    print 'test lexical model on simple.pos without smoothing:'
    lexi_mod = LexicalModel(sentences, tags)
    
    assert lexi_mod.cond_prob(['firm', 'NN']) == 0.0, "lexi_mod.cond_prob(['firm', 'NN']) should be 0.0 but isn't"
    print 'test 1 passed'
    
    assert lexi_mod.cond_prob(['investment', 'NN']) == 0.2, "lexi_mod.cond_prob(['investment', 'NN']) should be 0.2 but isn't"
    print 'test 2 passed'
    
    assert lexi_mod.cond_prob(['Davis\\Zweig', 'NNP']) == 0.16666666666666666, "lexi_mod.cond_prob(['Davis\\Zweig', 'NNP']) should be 0.16666666666666666, but isn't"
    print 'test 3 passed'
    
    return (lang_mod, lexi_mod)

    
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

    lang_mod = LanguageModel(tags, n)
    lexi_mod = LexicalModel(sentences, tags)
