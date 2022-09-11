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


#reads the word frequency of each word

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

#tests our the operation of each approach by using time.time function and then substract the end - start time of each operation then appending into the list 
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
    ## file names of each generated datasets that was generated from the large sampleData200k.txt file
    files = ["100", "700", "1500", "2750", "5000", "8000", "15000"]
    data = readWordList("", "sampleData200k.txt")
    linked = []
    arr_list = []
    trie_list = []

    for file in files: #reads the files/ generated datasets from the generation folder inside the dictionary directory
        word_list = readWordList("dictionary/generation/", file)
        arrD = ArrayDictionary()
        llD = LinkedListDictionary()
        trieD = TrieDictionary()
        result = [arrD, llD, trieD]

        test_data = word_list
        random.shuffle(test_data)
        #amounts of test did
        test_ammount = 100
        for i in result:
            i.build_dictionary(word_list)
            
            searches = search_test(test_data[:test_ammount], i)
            searches_result = int(math.fsum(searches) / len(searches))

            adds = add_test(test_data[:test_ammount], i)
            add_result = int(math.fsum(adds) / len(adds))


            
            auto = autocomplete_test(test_data[:test_ammount], i)
            auto_result = int(math.fsum(auto) / len(auto))
            #appending each operations and adding all the running time into 1 list
            if type(i) == LinkedListDictionary:
                linked.append(auto_result)
            if type(i) == ArrayDictionary:
                arr_list.append(auto_result)
            if type(i) == TrieDictionary:
                trie_list.append(auto_result)


#prints the running time
print(f" array : {arr_list}")
print(f" linked : {linked}")
print(f" trie : {trie_list}")

#creates the graph for comparing the amount of datasets to the running time of each approach/ dictionaries
plt.plot(files, linked, label="linked list")
plt.plot(files, arr_list, label="array")
plt.plot(files, trie_list, label="trie")
plt.legend()
plt.show()

    
 