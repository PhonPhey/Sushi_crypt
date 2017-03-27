# -*- coding: utf-8 -*-

import os
import random
from sushi import libsushi

def main():
    '''Main Function'''
    os.system('clear')

    func = int(input("What want you do?\n\n0)Encrypt\n1)Decrypt\n\nYour answer: "))

    while func > 1 or func < 0:
        print("\n!!! Error input number 0 or 1 !!!\n")
        func = int(input("What want you do?\n0)Encrypt\n1)Decrypt\n\nYour answer:"))

    libsushi.sushi(func)

if __name__ == '__main__':
    main()
