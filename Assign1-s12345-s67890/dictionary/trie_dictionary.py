from operator import index
from re import search
from tkinter import N
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
        

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED
        for wf in words_frequencies:
            self.add_word_frequency(words_frequencies[wf])

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        node = self.root

        for letter in word:
            if letter in node.children:
                node = node.children[letter]
            else:
                return 0
        

        return node.frequency


    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        # TO BE IMPLEMENTED

        node = self.root

        for letter in word_frequency.word:
            if  (letter in node.children):
                node = node.children[letter]
            else:
                new_node = TrieNode(letter)

                node.children[letter] = new_node
                node = new_node
        node.is_last =True
        node.frequency = word_frequency.frequency

        return True

    def delete_word(self, word: str, node=None, index = 0) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        ## if word exists
        
        if (index == 0):
            if self.search(word) == 0:
                return False
        
        
        if (node == None):
            node = self.root
            
        if (len(word) == index):
            node.is_last = False
            return True

        letter = word[index]
        if (letter not in node.children):
            return True

        if (self.delete_word(word, node.children[letter], index+1)):
            return True

        node.children.pop(letter)
        return bool(node.children) or node.is_last 


    def autocomplete(self, word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        return []
