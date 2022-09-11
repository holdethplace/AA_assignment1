import math
import time
import random
import matplotlib.pyplot as plt



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
    files = ["100", "700", "1500", "2750", "5000", "8000", "15000"]
    data = readWordList("", "sampleData200k.txt")
    linked = []
    arr_list = []
    trie_list = []

    for file in files: #benchmark data is the folder the files are in
        word_list = readWordList("dictionary/generation/", file)
        arrD = ArrayDictionary()
        llD = LinkedListDictionary()
        trieD = TrieDictionary()
        result = [arrD, trieD, llD]

        test_data = word_list
        random.shuffle(test_data)
        
        test_ammount = 100
        for i in result:
            i.build_dictionary(word_list)

            searches = search_test(test_data[:test_ammount], i)
            searches_result = int(math.fsum(searches) / len(searches))

            adds = add_test(test_data[:test_ammount], i)
            add_result = int(math.fsum(adds) / len(adds))

            deletes = delete_test(test_data[:test_ammount], i)
            deletes_result = int(math.fsum(deletes) / len(deletes))
            
            auto = autocomplete_test(test_data[:test_ammount], i)
            auto_result = int(math.fsum(auto) / len(auto))

            if type(i) == LinkedListDictionary:
                linked.append(auto_result)
            if type(i) == ArrayDictionary:
                arr_list.append(auto_result)
            if type(i) == TrieDictionary:
                trie_list.append(auto_result)



print(f" array add: {arr_list}")
print(f" linked add: {linked}")
print(f" trie add: {trie_list}")
plt.plot(files, linked, label="linked list")
plt.plot(files, arr_list, label="array")
plt.plot(files, trie_list, label="trie")
plt.legend()
plt.show()

    
 