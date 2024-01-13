#!/bin/python3
import logging
logging.basicConfig(level=logging.DEBUG, format="line : %(lineno)d, message : %(message)s")
f = open("./usernames.txt", 'r')

for username in enumerate(f):
    print(type(username[1]), username[1][:-1])

f.close()