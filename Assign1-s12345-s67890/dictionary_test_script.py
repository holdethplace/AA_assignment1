#
# Script to perform automated testing for Assignment 1 of Algorithms & Analysis class, 2022 Semester 2
# The script is designed to be ran
#
# The provided Python script will be the same one used to test your implementation. The script runs one of the three
# implementations then runs a series of test. Each test consists of sequence of operations to execute, whose results
# will be saved to file, then compared against the expected output.  If output from the tested implementation is the
# same as expected (script is tolerant for some formatting differences but if you don't change the IO functionality
# of the supplied files, you'll be fine), then you'll pass that test. Otherwise, difference will be printed (
# if in verbose mode, see below).
#
# Usage, assuming you are in the directory where the test script "dictionary_test_script.py" is located.
#
# > python dictionary_test_script.py [-v] <codeDirectory> <name of implementation to test> <data filename> <list of input files to test on>
#
# options:
#
#    -v : verbose mode
#
# Input:
#
#   code directory : directory where the python files reside.  E.g., if directory specified is Assign1-s1234,
#       then Assign1-s1234/dictionary_file_based.py should exist.
#   name of implementation to test: This is the name of the implementation to test.  The names
#       should be the same as specified in the script or in dictionary_file_based.py. E.g.- "list", or "hashtable", or "tst"
#   data filename: This is the input data file consists of a list of point information.
#       NOTE- the script expects the data file to be in the same directory as the script.
#       E.g. if the script is in the directory path /home/s1234/dictionary_test_script.py and
#       the data file name is sampleData.txt then the code will search the data file as
#       /home/s1234/sampleData.txt
#   input files: these are the input command files, where each file is a list of commands to execute.
#       NOTE- the script expects the input files to be in the same directory as the script (just like the data file).
#       IMPORTANT, the expected output file must be in the same directory
#       as the input files, and the should have the same basename - e.g., if we have input operation
#       file of "test1.in", then we should have expected files "test1.out".
#
#
# As an example, I can run the code as follows when testing code directory "Assign1-s1234",
# the data file is named "sampleData.txt",
# all my input command and expected files are located in the same folder,
# and named "test1.in" and testing for "list" implementation:
#
# > python assign1TestScript.py -v   Assign1-s1234    list    sampleData.txt    test1.in
#
# Note that for each tests, the output will be stored within the code directory.  For example, above
# that would mean test1-list.out will be created in Assign1-s1234.
#
#
#
# @Son Hoang Dau, 2022
#

import string
import csv
import getopt
import os
import os.path
import re
import sys
import subprocess as sp
import difflib


def main():
    # process command line arguments
    try:
        # option list
        sOptions = "v"
        # get options
        optList, remainArgs = getopt.gnu_getopt(sys.argv[1:], sOptions)
    except getopt.GetoptError as err:
        print(str(err))
        usage(sys.argv[0])

    bVerbose = False

    for opt, arg in optList:
        if opt == "-v":
            bVerbose = True
        else:
            usage(sys.argv[0])

    if len(remainArgs) < 4:
        usage(sys.argv[0])

    sOrigPath = os.getcwd()

    # code directory
    sCodeDir = os.path.abspath(remainArgs[0])
    # which implementation to test (see NearestNeighFileBased.java for the implementation strings)
    sImpl = remainArgs[1]
    # data file name
    sDataFile = os.path.join(sOrigPath, remainArgs[2])
    # set of input files that contains the operation commands
    lsInFile = remainArgs[3:]

    # check implementation
    setValidImpl = set(["array", "linkedlist", "trie"])
    if sImpl not in setValidImpl:
        print(sImpl + " is not a valid implementation name.")
        sys.exit(1)

    # python file to run
    sExec = "dictionary_file_based.py"

    os.chdir(sCodeDir)

    # variable to store the number of tests passed
    passedNum = 0
    failedNum = 0
    lsTestPassed = []
    lsTestFailed = []
    print('')

    # check if python file exists
    if not os.path.isfile(sExec):
        print(sExec + " does not exists in directory.")
    else:
        # loop through each input test file
        for (j, sInLoopFile) in enumerate(lsInFile):
            sInFile = os.path.join(sOrigPath, sInLoopFile)
            sTestName = os.path.splitext(os.path.basename(sInFile))[0]
            sOutputFile = os.path.join(sCodeDir, sTestName + "-" + sImpl + ".out")
            sExpectedFile = os.path.splitext(sInFile)[0] + ".exp"

            # check if expected files exist
            if not os.path.isfile(sExpectedFile):
                print(sExpectedFile + " is missing.")
                continue

            sCommand = 'python {sExec} {sImpl} "{sDataFile}" "{sInFile}" "{sOutputFile}"'.format(sExec=sExec,
                                                                                                 sImpl=sImpl,
                                                                                                 sDataFile=sDataFile,
                                                                                                 sInFile=sInFile,
                                                                                                 sOutputFile=sOutputFile)
            # print(sCommand)

            if bVerbose:
                print("Testing: " + sCommand)
            proc = sp.Popen(sCommand, shell=True, stderr=sp.PIPE)

            (sStdout, sStderr) = proc.communicate()

            if bVerbose and len(sStderr) > 0:
                print("\nWarnings and error messages from running python program:\n" + sStderr)

            # compare expected with output
            bPassed, bFailedOutput = evaluate(sExpectedFile, sOutputFile)
            if bPassed:
                passedNum += 1
                lsTestPassed.append(sTestName)
            else:
                # print difference if failed
                failedNum += 1
                lsTestFailed.append(sTestName)
                if bVerbose:
                    if bFailedOutput:
                        for line in bFailedOutput:
                            print(line)

    # change back to original path
    os.chdir(sOrigPath)

    print("\nSUMMARY: " + sExec + " has passed " + str(passedNum) + " out of " + str(len(lsInFile)) + " tests.")
    print("PASSED: " + ", ".join(lsTestPassed))
    print("FAILED: " + ", ".join(lsTestFailed) + "\n")

    # print out the mark
    # if sImpl in ["array", "linkedlist"]:
    #    print(str(0.4 * passedNum) + " marks\n\n")
    # if sImpl == "trie":
    #    print(str(passedNum) + " marks\n\n")


########################################################################################################################

def evaluate(sExpectedFile, sOutputFile):
    """
    Evaluate if the output is the same as expected input for the vertices operation.
    """
    test_passed = True
    test_failed_output = []
    expected_results = []
    output_results = []
    with open(sExpectedFile, "r") as fExpected:

        for line in fExpected:
            # Fetch expected results. Remove any empty lines
            if not len(line.strip()) == 0:
                expected_results.append(line.strip().lower())

    with open(sOutputFile, "r") as fOut:
        for line in fOut:
            # Fetch output results. Remove any empty lines
            if not len(line.strip()) == 0:
                output_results.append(line.strip().lower())

    for index, line in enumerate(expected_results):
        # Check if EOF reached for output results
        if index > len(output_results) - 1:
            test_passed = False
            test_failed_output.append(
                "At line {index} expected : {expected} actual: End of File".format(index=str(index + 1), expected=line))
            break

        if line != output_results[index]:
            test_passed = False
            test_failed_output.append(
                ("At line {index} expected : {expected} actual: {output}").format(index=str(index + 1), expected=line,
                                                                                  output=output_results[index]))
    return test_passed, test_failed_output


def usage(sProg):
    print(
        sProg + " [-v] <code directory> <name of implementation to test> <input data file> <list of test command files>")
    sys.exit(1)


if __name__ == "__main__":
    main()
