from ast import Delete
from http.client import NOT_FOUND
from lib2to3.pytree import Node
import string
from tokenize import String
from typing import List
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency


class ListNode:
    '''
    Define a node in the linked list
    '''

    def __init__(self, word_frequency: WordFrequency):
        self.word_frequency = word_frequency
        self.next = None

# ------------------------------------------------------------------------
# This class  is required TO BE IMPLEMENTED
# Linked-List-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class LinkedListDictionary(BaseDictionary):

    def __init__(self):
        # TO BE IMPLEMENTED

        self.head = None
        self.next = None
        pass


    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED
        #adds each word frequency in word frequencies 
        for wf in words_frequencies:
            self.add_word_frequency(wf)


    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """

        # TO BE IMPLEMENTED
        
        #word iterates from the head of the list until it finds the specific word
        current = self.head
        while current:
            if (current.word_frequency.word == word):
                return current.word_frequency.frequency
            current = current.next
          
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """

        # TO BE IMPLEMENTED
        #if there is no head , create head inside the list
        if (self.head is None):
            self.head = ListNode(word_frequency)
            return True
        #if there is a head add the new node into the list
        newNode = ListNode(word_frequency)
        if (self.head):
            current = self.head
            while(current.next):
                current = current.next
            current.next = newNode
        else:
            self.head = newNode      
        return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """

        # TO BE IMPLEMENTED
        #if the word does not exist within the list it returns false
        if (self.search(word) == 0):
            return False
        #if the word is inside the list, it searches throught the list from the head and deletes the node of the word from the list
        if (self.head):
            current = self.head
            if (current.word_frequency.word == word):
                self.head = None
                return True
            while(current.next):
                previous = current
                current = current.next
                if(current.word_frequency.word == word):
                    previous.next = current.next
                    return True   
        return False


    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """

        # TO BE IMPLEMENTED

        wordlist = []
        #a temporary point of the head of the list
        temporary = self.head
        while temporary:
            #if the word has the prefix/ starting word it adds the word into the result list
            if temporary.word_frequency.word.startswith(word):
                wordlist.append(temporary.word_frequency)
            temporary = temporary.next
        #sorts the word list and then returns the top 3 words with the highest frequency
        wordlist.sort(key = lambda word:word.frequency, reverse=True)
        return wordlist[0:3]



