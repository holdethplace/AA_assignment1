import sys
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.array_dictionary import ArrayDictionary
from dictionary.linkedlist_dictionary import LinkedListDictionary
from dictionary.trie_dictionary import TrieDictionary


# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# This is the entry point to run the program in file-based mode.
# It uses the data file to initialise the set of words & frequencies.
# It takes a command file as input and output into the output file.
# Refer to usage() for exact format of input expected to the program.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# -------------------------------------------------------------------

def usage():
    """
    Print help/usage message.
    """
    # On Teaching servers, use 'python3'
    # On Windows, you may need to use 'python' instead of 'python3'
    print('python3 dictionary_file_based.py', '<approach> <data fileName> <command fileName> <output fileName>')
    print('<approach> = <array | linkedlist | trie>')
    sys.exit(1)


if __name__ == '__main__':
    # Fetch the command line arguments
    args = sys.argv

    if len(args) != 5:
        print('Incorrect number of arguments.')
        usage()

    # initialise search agent
    agent: BaseDictionary = None
    if args[1] == 'array':
        agent = ArrayDictionary()
    elif args[1] == 'linkedlist':
        agent = LinkedListDictionary()
    elif args[1] == 'trie':
        agent = TrieDictionary()
    else:
        print('Incorrect argument value.')
        usage()

    # read from data file to populate the initial set of points
    data_filename = args[2]
    words_frequencies_from_file = []
    try:
        data_file = open(data_filename, 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            frequency = int(values[1])
            word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
            words_frequencies_from_file.append(word_frequency)
        data_file.close()
        agent.build_dictionary(words_frequencies_from_file)
    except FileNotFoundError as e:
        print("Data file doesn't exist.")
        usage()

    command_filename = args[3]
    output_filename = args[4]
    # Parse the commands in command file
    try:
        command_file = open(command_filename, 'r')
        output_file = open(output_filename, 'w')

        for line in command_file:
            command_values = line.split()
            command = command_values[0]
            # search
            if command == 'S':
                word = command_values[1]
                search_result = agent.search(word)
                if search_result > 0:
                    output_file.write(f"Found '{word}' with frequency {search_result}\n")
                else:
                    output_file.write(f"NOT Found '{word}'\n")

            # add
            elif command == 'A':
                word = command_values[1]
                frequency = int(command_values[2])
                word_frequency = WordFrequency(word, frequency)
                if not agent.add_word_frequency(word_frequency):
                    output_file.write(f"Add '{word}' failed\n")
                else:
                    output_file.write(f"Add '{word}' succeeded\n")

            # delete
            elif command == 'D':
                word = command_values[1]
                if not agent.delete_word(word):
                    output_file.write(f"Delete '{word}' failed\n")
                else:
                    output_file.write(f"Delete '{word}' succeeded\n")

            # check
            elif command == 'AC':
                word = command_values[1]
                list_words = agent.autocomplete(word)
                line = "Autocomplete for '" + word + "': [ "
                for item in list_words:
                    line = line + item.word + ": " + str(item.frequency) + "  "
                output_file.write(line + ']\n')

            else:
                print('Unknown command.')
                print(line)

        output_file.close()
        command_file.close()
    except FileNotFoundError as e:
        print("Command file doesn't exist.")
        usage()
