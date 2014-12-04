#!/usr/bin/python
import csv

f = open('LoggedIn.csv', 'rt')
lines = f.readlines()
for line in lines:
	print line

f.close()
