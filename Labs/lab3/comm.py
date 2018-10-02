#!/usr/bin/python

# take and read two files: file1 and file2
# produce three text columns as output: lines only in file1, lines only in file2, and lines in both files.

import sys, sys
from optparse import OptionParser

# create a class called comm which will hold the arguments (i.e. the files) and the lines

class comm:

# initialize the class with the arguments (files) given
    def __init__(self, args, options):
        if args[0] == "-":
            self.lines1 = sys.stdin.readlines()
        else:
            file1 = open(args[0], 'r')
            self.lines1 = file1.readlines()
            file1.close()

        if args[1] == "-":
            self.lines2 = sys.stdin.readlines()
        else:
            file2 = open(args[1], 'r')
            self.lines2 = file2.readlines()
            file2.close()

        if "\n" not in self.lines1[len(self.lines1) - 1]:
            self.lines1[len(self.lines1) - 1] += "\n"
        
        if "\n" not in self.lines2[len(self.lines2) - 1]:
            self.lines2[len(self.lines2) - 1] += "\n"

        self.column1 = ""
        self.column2 = ""
        self.column3 = ""

        self.options = options

# check to see if the files are sorted beforehand (if -u is not used)
    def sort(self):
        self.sort_1 = sorted(self.lines1)
        self.sort_2 = sorted(self.lines2)
        if self.options.optu == 1:
            return 0
        elif (self.sort_1 != self.lines1) and (self.sort_2 != self.lines2):
            return -3
        elif (self.sort_2 != self.lines2):
            return -2
        elif (self.sort_1 != self.lines1):
            return -1
        else:
            return 0

# compare function to compare lines between the files
    def compare(self):
        for line in self.lines1:
            if line not in self.lines2:
                if self.options.opt1 == 1 and line not in self.column1:
                    self.column1 += line #if line from file1 is not in file2, write to first column.
            else:
                if self.options.opt3 == 1 and line not in self.column3:
                    self.column3 += "                " 
                    self.column3 += line #if line from file1 is in file2, write to third column.

        for line in self.lines2:
            if (line not in self.lines1) and (self.options.opt2 == 1) and (line not in self.column2):
                self.column2 += "        " 
                self.column2 += line #if line from file2 is not in file1, write to second column.

# output the lines
    def output(self):
        allcolumns = self.column1 + self.column2 + self.column3
        allcolumns = allcolumns.splitlines()
        sortedcolumns = sorted(allcolumns, key=lambda x: ''.join(x.split()))
        print("\n".join(sortedcolumns))

def main():

# define format of command (flags, operands)
    version_msg = "%prog 2.0"
    usage_msg = "%prog [-123u] FILE1 FILE2"
    parser = OptionParser(version=version_msg, usage=usage_msg)  
    parser.add_option("-u", "--unsorted", action="store_true", dest="optu", default=0)
    parser.add_option("-1", "--surpressfile1", action="store_false", dest="opt1", default=1)
    parser.add_option("-2", "--surpressfile2", action="store_false", dest="opt2", default=1)
    parser.add_option("-3", "--surpressfile3", action="store_false", dest="opt3", default=1)
    options, args = parser.parse_args(sys.argv[1:])

# must have two operands (i.e. two files)
    if len(args) != 2:
        parser.error("missing operand")

# call compare function in comm class, and then suppress columns as specified

    run = comm(args, options)
    checksort = run.sort()

    if checksort == -3:
        print("comm: file 1 is not in sorted order \ncomm: file 2 is not in sorted order")
        return -1
    if checksort == -2:
        print("comm: file 2 is not in sorted order")
        return -1
    if checksort == -1:
        print("comm: file 1 is not in sorted order")
        return -1

    run.compare()
    run.output()

if __name__ == "__main__":
    main()
