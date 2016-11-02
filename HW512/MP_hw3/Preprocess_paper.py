'''Huajie shao@16/10/20
Fun: frequent patterns MP 
CS 412
'''

import numpy as np
import sys
import math
import ast


fr_paper = open('paper.txt','r')
fnew_voc = open('vocab.txt','w')
f_title = open('title.txt','w')


## the first step is to get the unique vacabularies
vac_list = []

for line in fr_paper.readlines():
	vals = line.split()
	for num, item in enumerate(vals[1 :]):
		if item not in vac_list:
			vac_list.append(item)

##----Step 1: get the unique vocal
for val in vac_list:
	fnew_voc.write(val + '\n')

fnew_voc.close()
fr_paper.close()

# print(word_dict)
##------step 2: the tokens dictionary------
fr_paper = open('paper.txt','r')
vac_index = dict()
for index,item in enumerate(vac_list):  #generate the dict
	vac_index[item] = index

for lines in fr_paper.readlines():
	vals = lines.split()
	each_line_list = []
	word_dict = dict()
	for item in vals[1 :]:
		if item not in each_line_list:
			each_line_list.append(item)

		if item in word_dict:
			word_dict[item] +=1  #counts of same words
		else:
			word_dict[item] = 1
	M = len(each_line_list)
	# if M <1:
		# print('error')
	if M >0:
		f_title.write(str(M))
		for item in each_line_list:
			value = word_dict[item]
			dx = vac_index[item]
			f_title.write(' '+ '%d' %dx +':'+str(value))

		f_title.write('\n')


f_title.close()

