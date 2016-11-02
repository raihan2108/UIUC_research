'''Huajie Shao@10/22 2016
Fun: assign the topics
'''

import numpy as np
import sys
# import os.path


fr_file = open('result/word-assignments.dat','r')
# filepath = "./top/"

fw_top0 = open("topic-0.txt",'w')
fw_top1 = open("topic-1.txt",'w')
fw_top2 = open("topic-2.txt",'w')
fw_top3 = open("topic-3.txt",'w')
fw_top4 = open("topic-4.txt",'w')

for lines in fr_file.readlines():
	eline = lines.split()
	top_list = eline[1:]
	# print(top_list)
	flg0,flg1,flg2,flg3,flg4 =0,0,0,0,0
	for item in top_list:
		item_num = item.split(':')
		index = item_num[0]
		num = item_num[1]
		# print(index,num)
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

fw_top0.close()
print("well done")
