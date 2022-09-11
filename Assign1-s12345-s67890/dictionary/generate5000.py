
class WordFrequency:
    def __init__(self, word: str, frequency: int):
        self.word = word
        self.frequency = frequency



data_file = open("sampleData200k.txt", "r")
word_list = []

for line in data_file:
    values = line.split()
    frequency = int(values[1])
    word = values[0]
    word_frequency = WordFrequency(word, frequency)
    word_list.append(word_frequency)


f = open("dictionary/generation/" + "5000", "w")
for w in word_list[:5000]:
    f.write(w.word + " " + str(w.frequency) + "\n")

data_file.close()