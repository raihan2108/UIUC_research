'''Huajie Shao@10/22 2016
Fun: assign the topics
'''

import numpy as np
import sys
# import os.path


fr_file = open('word-assignments.dat')
# filepath = "./top/"

fw_top0 = open('top-0.txt','w')
fw_top1 = open('top-1.txt','w')
fw_top2 = open('top-2.txt','w')
fw_top3 = open('top-3.txt','w')
fw_top4 = open('top-4.txt','w')

for lines in fr_file.readlines():
	eline = lines.split()
	top_list = eline[1:]
	# print(top_list)
	flg0,flg1,flg2,flg3,flg4 =0,0,0,0,0
	for k in range(len(top_list)):
		num = top_list[k][5:]
		index = top_list[k][:4]
		# print(index)
		if num == '00':
			fw_top0.write(index +' ')
			flg0 = 1
		if num =='01':
			fw_top1.write(index +' ')
			flg1 = 1
		if num =='02':
			fw_top2.write(index +' ')
			flg2 = 1
		if num =='03':
			fw_top3.write(index +' ')
			flg3 = 1
		if num =='04':
			fw_top4.write(index +' ')
			flg4 = 1

	if flg0 == 1:
		fw_top0.write('\n')
	if flg1 == 1:
		fw_top1.write('\n')
	if flg2 == 1:
		fw_top2.write('\n')
	if flg3 == 1:
		fw_top3.write('\n')
	if flg4 == 1:
		fw_top4.write('\n')
