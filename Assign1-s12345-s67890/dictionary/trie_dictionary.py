from operator import index
from re import search
from tkinter import N
from typing import List
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency

# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Trie-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


# Class representing a node in the Trie
class TrieNode:

    def __init__(self, letter=None, frequency=None, is_last=False):
        self.letter = letter            # letter stored at this node
        self.frequency = frequency      # frequency of the word if this letter is the end of a word
        self.is_last = is_last          # True if this letter is the end of a word
        self.children: dict[str, TrieNode] = {}     # a hashtable containing children nodes, key = letter, value = child node


class TrieDictionary(BaseDictionary):

    def __init__(self):
        # TO BE IMPLEMENTED
        self.root = TrieNode()
        

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED
        for wf in words_frequencies:
            self.add_word_frequency(wf)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        node = self.root
        #if children node is not inside the root node it returns 0
        for currenthead in word:
            if currenthead not in node.children:
                return 0
            #it points the children node as the root node
            node = node.children[currenthead]
            
        

        return node.frequency if node.frequency else 0


    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        # TO BE IMPLEMENTED

        node = self.root
        #if the word is already inside the dictionary dont add it into the children node
        for currenthead in word_frequency.word:
            if  (currenthead not in node.children):
                node.children[currenthead] = TrieNode (letter= currenthead)
            node = node.children[currenthead]
        # adds the word into the dictionary
        node.frequency = word_frequency.frequency

        node.is_last =True
        
        

        return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        
        
        node = self.root
        #if word is not in dictionary returns false
        for currenthead in word:
            if currenthead not in node.children:
                return False
            node = node.children[currenthead]
        #deletes the node
        node.frequency = None
        
        node.is_last = False
        
        
        
        return True



    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        node = self.root
        
        self.result = []
        #if the words with prefix are not inside the dictionary returns empty list
        for currenthead in word:
            if currenthead not in node.children:
                return []
            #adds the words with the prefix inside the list
            node = node.children[currenthead]
        self.depthfirstsearch(node, word[:-1])
        #sorts the list and returns the top 3 words with the highest frequency
        return sorted(self.result, key =lambda y : y.frequency, reverse=True)[:3]
    
    #a method in which it appends the word into the list if the word is in the last node
    def depthfirstsearch(self, node: TrieNode, word: str):
        if node.is_last:
            self.result.append(
                WordFrequency(word=word + node.letter, frequency=node.frequency)
                
            )

        for child in node.children:
            self.depthfirstsearch(node.children[child], word + node.letter)  