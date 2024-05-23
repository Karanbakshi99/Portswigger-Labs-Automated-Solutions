#!/bin/python3

fd = open('./username.txt', 'r')

lines = fd.readlines()
print(lines)

fd.close()