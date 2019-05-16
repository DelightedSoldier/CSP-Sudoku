import sys
from sets import Set
import random
from collections import Counter
import math

import os,sys


# Define a main() function that prints a little greeting.
def main():
    i = 0
    list = []
    f = open("sudokus_finish.txt")
    list1 = []
    f2 = open("output.txt")
    i = 0
    for a in f.readlines():
        list.append(a)
    for a in f2.readlines():
        list1.append(a)
    for item in list:
        print item
        print list1[list.index(item)]
        if item == list1[list.index(item)]:
            i += 1
    print i    
    
        
    
        
if __name__ == '__main__':
    main()

    