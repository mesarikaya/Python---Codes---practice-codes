# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:38:32 2017

@author: sarikaya.me
"""

import string
import time
from nltk.corpus import stopwords
from nltk.corpus import reuters
from collections import Counter
from nltk.corpus import brown


class Dictionary:
    """ This class aims to find the most similar word in a dictionay and
    it can be used to guide the users in case they have made errors in their 
    typing. It can be thought as similar as Google's "Did yo mean this?" 
    functionality
    
    Success criteria: 
        1) Absolute Match
        2) Method 1: The lease number of replacement and additions
            - From the list that is generated from combination of provided list
            and existing word dictionary -if exits
        3) Method 2: Highest probaility of a word appearing in english
            - From the list that is generated from combination of provided list
            and existing word dictionary -if exits
     """
    
    def __init__(self, words=None, method = 1, user_reuters_words = False, user_brown_words = True):
        # words is the list created via using the nltk package
        if user_reuters_words == False and user_brown_words == False and words !=None:
            if len(words) > 0:
                self.words = words
                self.word_counts = Counter(self.words)
            else:
                print("Please enter a valid word list or activate usage of reuter list.")
                raise
        else:
            stop = stopwords.words('english')
            if user_reuters_words == True: # Prioritize reuters list over brown
                self.words = [i.lower() for i in reuters.words() if i not in stop]
            else:
                self.words = [i.lower() for i in brown.words() if i not in stop]
            self.word_counts = Counter(self.words)
            self.word_counts = dict(self.word_counts.most_common(int(len(self.word_counts)*0.1)))
       
        # Create parameters
        self.alphabet =  list(string.ascii_lowercase)
        self.user_reuters_words = user_reuters_words
        self.user_brown_words = user_brown_words
        self.method = method
        
    
    def set_probs(self, word): 
        "Probability of 'word'"
        N=sum(self.word_counts.values())
        return self.word_counts[word] / N

    def correction(self, word): 
        "Most probablility from the list generated after modifications for the word"
        return max(self.available_words(word), key=self.set_probs)
    
    def available_words(self, word): 
        "Generate possible spelling corrections for word."
        return (self.check_the_list([word]) or self.check_the_list(self.modify1(word)) 
                or self.check_the_list(self.modify2(word)) or [word])
    
    def check_the_list(self, word): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in word if w in self.words)
    
    def modify1(self, word):
        "All edits that are one edit away from `word`."
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in self.alphabet]
        inserts    = [L + c + R               for L, R in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)
    
    def modify2(self,word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.modify1(word) for e2 in self.modify1(e1))
          
    def find_most_similar(self,term):
        # term: search term entered by the user
        
        # Search if there is absolute match and return the match
        
        try:
            self.words.index(term)
            return term
        except ValueError:
            # If there is no absolute match
            # Create a list that shows the count of letters for the term
            self.term_letter_counts = [term.count(i) for i in self.alphabet]
            
            # Create a list that shows the count of letters for the dictionary
            self.dict_letter_counts = []
            
            # Create a new list with 1 and 2 modification levels and the original list
            k_1 = self.modify1(term)
            #k_2 = [e2 for e1 in k_1 for e2 in self.modify1(e1)]
            k_3 = set(self.words)
#            self.candidate_word_list = set(k_1).union(k_2)
            self.candidate_word_list =set(k_1).union(k_3)
            self.candidate_word_list = [i for i in self.candidate_word_list if i in self.words]
            print(len(self.candidate_word_list))
            self.dict_letter_counts = [[i.count(j) for j in self.alphabet] for i in self.candidate_word_list ]
            # Apply Method 1: min replacement + addition rule or Method 2: Max probability
            if self.method == 1:      
                # Create a list for differences per the dictionary item
                difference = [[i[j]-self.term_letter_counts[j] for j in range(len(i))] for i in self.dict_letter_counts]
                # Find the total number of letters to be added or removed
                # Sum up the total difference (Only for negative numbers)
                m1_result = [sum([abs(j) for j in difference[i]]) for i in range(len(difference))]
                
                return self.candidate_word_list[m1_result.index(min(m1_result))]
            else:
                m2_result = [self.set_probs(i) for i in self.candidate_word_list]
                return self.candidate_word_list[m2_result.index(max(m2_result))]

word_list=['cherry', 'peaches', 'peack', 'pineapple', 'melon', 'strawberry', 'raspberry', 'apple', 'coconut', 'banana']

# Use nltk package to guess usin ght english dictionary

# If not available, install nltk package and download relevant file
#import nltk
#nltk.download()

#word_list = words.words()
start = time.time()
test_dict=Dictionary(words=word_list, method = 2)
print(test_dict.find_most_similar("gentl"))
end = time.time()
print(end - start)