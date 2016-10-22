import numpy as np
import ast
import json

def Get_candidate(i,j):
	Alpha = []
	a1=i.replace('"','').strip('[ ]').split(',')
	b1=j.replace('"','').strip('[ ]').split(',')
	for ta in a1:
		ra = ta.strip('"\'')
		Alpha.append(ra)
	for ta in b1:
		ra = ta.strip('"\'')
		if ra not in Alpha:
			Alpha.append(ra)

	return Alpha


B = ["['a','c']"]
C = ['c','b']
A = ["['a','b']"]
D =['c']
for i in A:
	for j in D:
		rst = Get_candidate(i,j)
		print(rst)