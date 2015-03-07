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
from pos_parser import add_start_stop_to_sentence, get_tags_from_sentences, get_words_from_sentences, pos_file_parser
from sys import exit
from a1_step3 import gt_smooth, gt_smoothe_min_1
import sets
from operator import itemgetter

#%%
# good trial run
#(lang_mod, lexi_mod) = test(); nm1_gram = ['START', 'DT']; print(lang_mod.next_n_min1_grams(nm1_gram)); print(lexi_mod.emission_prob('A', nm1_gram));

#%%
class LanguageModel:
    def __init__(self, tags, n, smoothe):
        """
        initializes language model. 
        """
        self.n_grams = Counter(list(chain(*[make_grams(add_start_stop_to_sentence(t, n-1), n) for t in tags])))
        self.n_min1_grams = Counter(list(chain(*[make_grams(add_start_stop_to_sentence(t, n-1), n - 1) for t in tags]))) 
        self.smoothed = False
        if smoothe:
            self.smoothed = True  
            unigrams = len(list(chain(*[make_grams(add_start_stop_to_sentence(t, 1), 1) for t in tags])))            
            self.N = {i : len([n_gram for n_gram in self.n_grams.values() if n_gram is i]) for i in xrange(6) if i is not 0}
            self.N[0] = unigrams**2 - len(self.n_grams)
            self.smoothe()          
            self.n_min1_grams = gt_smoothe_min_1(self.n_grams)        
           
    def cond_prob(self, tags):
        """
        returns cond probability for a tag N-gram.
        cond_prob([t1,t2,t3]) = P([t3|t2,t1]) = count('t1 t2 t3')/count('t1 t2')
        """        
        t_all = ' '.join(tags)
        if t_all in self.n_grams: 
            p_all = self.n_grams[t_all]
            p_rest = self.n_min1_grams[' '.join(tags[:-1])]
            return float(p_all) / p_rest if p_rest else 0.0
        elif self.smoothed:
            return float(self.N[1])/(self.N[0]*len(self.n_grams))
        else:
            return 0.0
        
    def next_n_min1_grams(self, n_min1_gram):
        """
        returns list of tuples that map n_min1_grams to probabilities of transition
        from n_min1_gram given as argument
        
        E.g., on simple.pos:
        IN:  lang_mod.next_n_min1_grams(['START', 'DT'])
        OUT: [(('DT', 'JJS'), 0.0), (('DT', 'JJ'), 0.0), (('DT', 'NN'), 1.0)]
        """
    
        first_tag = n_min1_gram[0]
        last_tag = n_min1_gram[1]
        next_min1_grams = [[last_tag, t] for t in self.possible_transition_from_tag(last_tag)]
            
        probs = [(tuple(n), self.cond_prob([first_tag] + n)) for n in next_min1_grams]
        return [p for p in probs if p[1] != 0.0]
        
    def get_start_probabilites(self):
        """
        returns probability for each possible start sequence
        """
        probs = [('START', 'START', t) for t in self.possible_transition_from_tag('START')]
        ps =  [(wt, self.cond_prob(wt)) for wt in probs]
        return [((p[0][0], p[0][2]), p[1]) for p in ps if p[1] != 0.0]

    def possible_transition_from_tag(self, tag):
        """
        returns a list of tags that can follow a certain n_min1_gram
        """
        return list(set([t[1] for t in [k.split() for k in self.n_grams.keys()] if t[0] == tag]))
    
    def smoothe(self):
        """
        Smoothes the language model
        """
        k = 4
        for ng in self.n_grams:
            if  self.n_grams[ng] < (k+1) and self.n_grams[ng] > 0:
                self.n_grams[ng] = gt_smooth(self.n_grams[ng], self.N, k)
        
#%%
class LexicalModel:
    def __init__(self, sentences, tags, smoothe):
        """
        initializes lexical model
        """
        self.unigrams = Counter(list(chain(*[make_grams(t, 1) for t in tags])))
        self.word_tag_pairs = Counter([' '.join(wt) for wt in chain(*sentences)])
        self.smoothed = False
        if smoothe:
            self.smoothed = True
            self.words = set([wt[0] for wt in chain(*sentences)])
            self.smooth()
            
            
    def emission_prob(self, word, n_min1_gram):
        """
        given an n_min1_gram, returns emission probability
        """
        return self.cond_prob([word, n_min1_gram[1]])
        
    def cond_prob(self, word_tag_pair):
        """
        returns cond probability for tag word combination
        cond_prob([word, tag]) = P(word|tag) = count('word  tag')/count('tag')
        """
        wtpair = ' '.join(word_tag_pair)
        p_rest = self.unigrams[word_tag_pair[1]]        
        if wtpair in self.word_tag_pairs:
            p_all = self.word_tag_pairs[wtpair]
            return float(p_all) / p_rest if p_rest else 0.0
        
        #In case of unseen event and model is smoothed
        elif self.smoothed and word_tag_pair[0] not in self.words:
            return 0.5*float(self.N1[word_tag_pair[1]])/ p_rest if p_rest else 0.0
        else:
            return 0.0
            
    def smooth(self):
        """
        Smoothes the word-tag pairs and then the tags
        """        
        for pair in self.word_tag_pairs:
            if self.word_tag_pairs[pair] is 1:
                self.word_tag_pairs[pair] = 0.5
        
        #Smoothe the tags in the lexical model
        tags = [key.split()[1] for key in self.word_tag_pairs.iterkeys()]
        
        copy = zip(tags, self.word_tag_pairs.itervalues())
        self.unigrams = {tag : 0 for tag in tags}
        self.N1 = {tag : 0 for tag in tags}        
        for thing in copy:
            self.unigrams[thing[0]] += thing[1]
            #Counts the instances of tag-word-pairs that only occur once per tag            
            if thing[1] is 0.5:
                self.N1[thing[0]] += 1
        
        self.unigrams = Counter(self.unigrams)
        self.N1 = Counter(self.N1)
                

#%%
def viterbi_path_to_list(vit_path):
    path = []
    for i,p in enumerate(vit_path):
        if i == 0:
            path += [p[0], p[1]]
        else:
            path += [p[1]]
    return path

#%%
def viterbi(words, lang_mod, lexi_mod):
    words += ['STOP']
    probs = lang_mod.get_start_probabilites()

    tellis = []
    path = {}
    
    for (i, w) in enumerate(words):
        tellis.append({})
        next_probs = []
        new_path = {}
        for p in probs:
            tags = p[0]
            p_tags = p[1]
            
            p_emit = 0.0
            # if we are not at the end then we can calculate the emission
            # probabilites. 
            if i < len(words) - 1:
                p_emit = lexi_mod.emission_prob(w, tags)
            # otherwise check if we transmit to STOP. if yes
            # emission P is logically 1.0
            elif tags[-1] == 'STOP':
                p_emit = 1.0

            p_total = p_emit * p_tags

            #print p_total
            # we only expand if we have p_total, no need to do that for
            # zero Probs
            if p_total:
                back_pointer = max_pr = None
                
                if i > 0:
                    # find maximum value from one step back in trellis
                    for os, o_os in tellis[i - 1].iteritems():
                        # check if they are connected
                        if os[1] == tags[0]:
                            pr = o_os * p_total
                            if pr > max_pr:
                                # assign max probability
                                max_pr = pr
                                # keep back pointer
                                back_pointer = os

                # write into tellis the max probability for later retrieval
                tellis[i][tags] = max_pr if max_pr else p_total
                
                # add possible expansions
                next_probs += lang_mod.next_n_min1_grams(tags)
                
                if back_pointer:
                    if back_pointer in path:
                        conc = path[back_pointer] + [back_pointer]
                        new_path[tags] = conc
                    else:
                        new_path[tags] = [back_pointer]
                
        probs = next_probs
        path = new_path
        
    if len(tellis[-1]) > 0:
        return viterbi_path_to_list(path[max(tellis[-1].iteritems(), key=itemgetter(1))[0]][1:])
    else:
        return []
     
#%%
def test(smoothe):
    with open('data/s3/simple.pos') as f: 
        sentences = pos_file_parser(f)
    if not sentences:
        exit('error parsing sentences')
    
    tags = get_tags_from_sentences(sentences)

    n = 3
    lang_mod = LanguageModel(tags, n, smoothe)
    lexi_mod = LexicalModel(sentences, tags, smoothe)
    try:    

        print 'test language model on simple.pos without smoothing:'
        
        assert lang_mod.cond_prob(['START', 'DT', 'NN']) == 1.0, 'test 1 failed'
        print 'test 1 passed'
        
        assert lang_mod.cond_prob(['JJ', 'NN', 'NNS']) == 0.3333333333333333, 'test 2 failed'
        print 'test 2 passed'
        
        assert lang_mod.cond_prob(['NN', 'IN', 'DT']) == 0.5, 'test 3 failed'
        print 'test 3 passed'
            
        print 'test lexical model on simple.pos without smoothing:'
    
        
        assert lexi_mod.cond_prob(['firm', 'NN']) == 0.0, 'test 1 failed'
        print 'test 1 passed'
        
        assert lexi_mod.cond_prob(['investment', 'NN']) == 0.18181818181818182, 'test 2 failed'
        print 'test 2 passed'
        
        assert lexi_mod.cond_prob(['Davis\\Zweig', 'NNP']) == 0.16666666666666666, 'test 3 failed'
        print 'test 3 passed'
        
        print 'test transition probabilities on simple.pos without smoothing:'
        n = lang_mod.next_n_min1_grams(['START', 'DT'])
        assert n == [(('DT', 'NN'), 1.0)], 'test 1 failed'
        print 'test 1 passed'    
        
        n = lang_mod.next_n_min1_grams(['DT', 'NN'])
        assert n == [(('NN', 'MD'), 0.3333333333333333),
                     (('NN', 'JJ'), 0.3333333333333333),
                     (('NN', 'IN'), 0.3333333333333333)] , "test 2 failed"
        print 'test 2 passed'
    
        
        print 'test emission probabilities on simple.pos without smoothing:'
        assert lexi_mod.emission_prob('A', ['START', 'DT']) == 0.16666666666666666, 'test 1 failed'
        print 'test 1 passed'
        
        assert lexi_mod.emission_prob('of', ['NN', 'IN']) == 0.6666666666666666, 'test 2 failed'
        print 'test 2 passed'
        
        assert lexi_mod.emission_prob('on', ['NN', 'IN']) == 0.3333333333333333, 'test 3 failed'
        print 'test 3 passed'
        
        assert lang_mod.get_start_probabilites() == [(('START', 'NNPX'), 0.5), (('START', 'DT'), 0.5)], 'test 4 failed'
        print 'test 4 passed'
        
        print 'ALL TESTS PASSED'
    except AssertionError as e:
        print e
        
    
        
    return (lang_mod, lexi_mod)
    
#%%
def viterbi_test_run(smooth=False):
    with open('data/s3/WSJ02-21.pos') as f:
        sentences = pos_file_parser(f)
    if not sentences:
        exit('error parsing sentences')
    tags = get_tags_from_sentences(sentences)
    
    n = 3

    lang_mod = LanguageModel(tags, n, smooth)
    lexi_mod = LexicalModel(sentences, tags, smooth)
    
    
    path = viterbi('New York is in trouble'.split(), lang_mod, lexi_mod)
    print 'New York is in trouble: ' + str(path)
    
    path = viterbi('New York is in KAUDERWELSCH'.split(), lang_mod, lexi_mod)
    print 'New York is in KAUDERWELSCH: ' + str(path)
    
#%%
def train_and_test(train_file, test_file, smooth, out_file):
    sentences = None    
    with open(train_file) as f: 
        train_sentences = pos_file_parser(f)
    if not train_sentences:
        exit('error parsing sentences')
    
    # Train model
    train_tags = get_tags_from_sentences(train_sentences)
    
    n = 3

    lang_mod = LanguageModel(train_tags, n, smooth)
    lexi_mod = LexicalModel(train_sentences, train_tags, smooth)
    
    with open(test_file) as f:
        test_sentences = pos_file_parser(f)
    if not test_sentences:
        exit('error parsing sentences')
        
    test_tags = get_tags_from_sentences(test_sentences)
    test_words = get_words_from_sentences(test_sentences)
    
    # predict from test set and write to file
    predicted_tags = [viterbi(s, lang_mod, lexi_mod) for s in test_words]    
    
    with open(out_file) as f:
        for words, tags in test_words, predicted_tags:
            f.write(words + '\n')
            f.write(tags + '\n')

    
#%%
if __name__ == "__main__":
    parser = ArgumentParser(description='Assignment A, Step 4')
    parser.add_argument('-train-set', dest ='train_file', type=str, default=None, help='Path to training file')
    parser.add_argument('-test-set', dest='test_file', type=str, default=None, help='Path to test file')
    parser.add_argument('-smoothing', dest='smooth',type=str, default=None, help='Use good-turing (yes/no)')
    parser.add_argument('-test-set-predicted', dest='test_set_pred', default=None, type=str, help='Path to file with predictions')
    args = parser.parse_args()
    
    # INPUT CHECKS 

    if not args.train_file:
        parser.print_help()
        exit('No training file specified (-train-set)')
    if not args.smooth:
        parser.print_help()
        exit('You must indiciate wether you want to use smoothing or not (-smooth))')
    if not args.test_file:
        parser.print_help()
        exit('No test set file specified (-test-file)')
    if not args.test_set_pred:
        parser.print_help()
        exit('No file specified where you want the results to be written to')
        
    if args.smooth == 'yes':
        args.smooth = True
    elif args.smooth == 'no':
        args.smooth = False
    else:
        parser.print_help()
        exit('-smooth must be [yes|no]')
        
    train_and_test(args.train_file, args.test_file, args.smooth, args.test_set_pred)

        

    