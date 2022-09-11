import math
import time
import random
from typing import List

from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.array_dictionary import ArrayDictionary
from dictionary.linkedlist_dictionary import LinkedListDictionary
from dictionary.trie_dictionary import TrieDictionary



def readWordList(folder: str, fstr: str) -> List[WordFrequency]:
    data_file = open(folder + fstr, "r")
    word_list = []

    for line in data_file:
        line_data = line.split()
        word = line_data[0]
        frequency = int(line_data[1])
        word_frequency = WordFrequency(word, frequency)
        word_list.append(word_frequency)
    return word_list


def search_test(data: List[WordFrequency], dictionary: BaseDictionary):
    searches = []

    for d in data:
        start = time.time() * 1000000000
        dictionary.search(d.word)
        end = time.time() * 1000000000
        searches.append(end - start)
    return searches

def add_test(data: List[WordFrequency], dictionary: BaseDictionary):
    searches = []

    for d in data:
        start = time.time() * 1000000000
        dictionary.add_word_frequency(d)
        end = time.time() * 1000000000
        searches.append(end - start)
    return searches

def delete_test(data: List[WordFrequency], dictionary: BaseDictionary):
    searches = []

    for d in data:
        start = time.time() * 1000000000
        dictionary.delete_word(d.word)
        end = time.time() * 1000000000
        searches.append(end - start)
    return searches

def autocomplete_test(data: List[WordFrequency], dictionary: BaseDictionary):
    searches = []

    for d in data:
        for p in range(len(d.word)):
            start = time.time() * 1000000000
            dictionary.autocomplete(d.word[: len(d.word) - p])
            end = time.time() * 1000000000
            searches.append(end - start)
    return searches


if __name__ == "__main__":
    ## file names
    files = ["100", "500", "1000", "2500", "5000", "7500", "10000"]
    data = readWordList("", "sampleData200k.txt")
    linked = []
    arr_list = []
    trie_list = []

    for file in files: #benchmarn data is the folder the files are in
        word_list = readWordList("benchmark-data/", file)
        arrD = ArrayDictionary()
        llD = LinkedListDictionary()
        trieD = TrieDictionary()
        res = [arrD, trieD, llD]

        test_data = word_list
        random.shuffle(test_data)
        
        test_ammount = 100
        for i in res:
            i.build_dictionary(word_list)

            searches = search_test(test_data[:test_ammount], i)
            searches_res = int(math.fsum(searches) / len(searches))

            adds = add_test(test_data[:test_ammount], i)
            add_res = int(math.fsum(adds) / len(adds))

            deletes = delete_test(test_data[:test_ammount], i)
            deltes_res = int(math.fsum(deletes) / len(deletes))
            
            auto = autocomplete_test(test_data[:test_ammount], i)
            auto_res = int(math.fsum(auto) / len(auto))

            if type(i) == LinkedListDictionary:
                linked.append(auto_res)
            if type(i) == ArrayDictionary:
                arr_list.append(auto_res)
            if type(i) == TrieDictionary:
                trie_list.append(auto_res)