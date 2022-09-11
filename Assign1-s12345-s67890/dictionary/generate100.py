
class WordFrequency:
    def __init__(self, word: str, frequency: int):
        self.word = word
        self.frequency = frequency


#opens the dataset file 
data_file = open("sampleData200k.txt", "r")
word_list = []

#for each data read from the large datasets, it splits the values by lines, and takes each word and its frequency then listed it out in each line
for line in data_file:
    values = line.split()
    frequency = int(values[1])
    word = values[0]
    word_frequency = WordFrequency(word, frequency)
    word_list.append(word_frequency)
    
   
#creates the text/file of the generated datasets based on the number of words u wanna list (100-15000)
f = open("dictionary/generation/" + "100", "w")
for w in word_list[:100]:
    f.write(w.word + " " + str(w.frequency) + "\n")

data_file.close()