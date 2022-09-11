from array import array
from ctypes import sizeof
from typing import List
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
import bisect


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Array-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class ArrayDictionary(BaseDictionary):

    def __init__(self):
        pass


    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED
    
        #creates a sorted array dictionary of word frequencies
        self.array = sorted([wordfrequency for wordfrequency in words_frequencies], key=lambda y: y.word)


    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        
        #iterates throught the array attempting to find the specific word
        for i in self.array:
            if (i.word == word):
                return i.frequency
            
        
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED


        
        #searches if the word already exists or not, if it does it does not add a word
        if self.search(word_frequency.word) != 0:
            return False
        
        
        #adds the word to the array dictionaru
        bisect.insort_left(self.array, word_frequency, key=lambda y: y.word)
        return True
        

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        
        # TO BE IMPLEMENTED
        
        #sorts the word based on alphabetical order, then if it finds the word it deletes it
        index = bisect.bisect_left(self.array, word, key=lambda y: y.word)
        if index != len(self.array):
            del self.array[index]
            return True

        return False

    def autocomplete(self, prefix_word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        def prefix(word_frequency: WordFrequency):
            #finds the prefix word and then if it starts with the prefix word it returns the word
            if word_frequency.word.startswith(prefix_word):
                return True
            else:
                return False
        result = filter(prefix, self.array)
        return sorted(result, key=lambda y: y.frequency, reverse=True)[:3]
        


        
    
    

        
