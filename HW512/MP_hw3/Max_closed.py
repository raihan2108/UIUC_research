'''Huajie Shao@2016/10/21
Fun: frequent patterns
'''

import numpy as np
import sys
import os
import operator
import ast
# import os.path

def Get_candidate(ai,aj):
	Alpha = []
	a1=ai.strip('[]').split(',')
	b1=aj.strip('[]').split(',')
	# print("the fist time deal with",a1)
	for ta in a1:
		ra = ta.strip('"\' ')
		ra = ra.replace("'",'')
		Alpha.append(ra)
	for ta in b1:
		ra = ta.strip('"\' ')
		ra = ra.replace("'",'')
		if ra not in Alpha:
			Alpha.append(ra)
	return Alpha

##---the subfuns-----
def fun_aprior_loop(item_count,min_sup,items_list):
	Fk = item_count
	# print("the init Fk",Fk)
	ri= 1
	topic_list =[]
	pattern_dict=dict()
	print("min_support:",min_sup)
	while bool(Fk):
		ri += 1
		print("---it is running Aprior:\n")
		for key in Fk.keys():
			val = Fk[key]
			if val>=min_sup:
				topic_list.append(key)
				pattern_dict[key] = val
		
		topic_list=sorted(topic_list)
		Ck = []
		K_max = len(topic_list)
		Fk = dict()
		for j in range(K_max):
			for t in range(j+1,K_max):
				# print("it is to Ck")
				A = topic_list[j]
				B = topic_list[t]
				rst=Get_candidate(A,B)
				rst = sorted(rst)
				# print("the length",len(rst))
				if rst not in Ck and len(rst) == ri:
					Ck.append(rst)
		# print(Ck)
		for val in Ck:
			for items in items_list:
				flag = 0
				# print("it is running")
				for v in val:
					if v not in items:
						flag = 1

				if flag ==0:
					sval = str(val)
					if sval not in Fk:
						Fk[sval] = 1
					else:
						Fk[sval] += 1

	return pattern_dict

##----define the parse function-----
def parse_data(str_data):
	id_list = str_data.strip('[]').split(',')
	new_ids = []
	for ta in id_list:
		ra = ta.strip('"\' ')
		ra = ra.replace("'",'')
		new_ids.append(ra)

	return new_ids

##---the Aprior algorithm---
def Fun_FP_Aprior(i,min_sup,word_dict):
	item_count ={}
	items_list =[]
	Read_Topic = open('topic-'+str(i)+'.txt','r')
	for lines in Read_Topic.readlines():
		eline = lines.split()
		for item in eline:
			if item not in item_count:
				item_count[item] = 1
			else:
				item_count[item] +=1
		items_list.extend([eline])

	File_name = os.path.join(os.getcwd()+"/patterns","pattern-"+str(i)+".txt")
	fw_pi = open(File_name, "w")
	phrase_name = os.path.join(os.getcwd()+"/patterns","pattern-"+str(i)+".txt.phrase")
	fw_phrase = open(phrase_name, "w")

	fre_pattern = fun_aprior_loop(item_count,min_sup,items_list)
	Rank_dict = dict()
	for key,value in fre_pattern.items():
		Rank_dict.setdefault(value,[]).append(key)
		# num_set.add(value)

	fp_rst = sorted(Rank_dict.items(), key=operator.itemgetter(0), reverse=True)

	for kv in fp_rst:
		sup = kv[0]
		val = kv[1]
		for ids in val:
			new_ids = parse_data(ids) #parse the data
			# t_ids = set(new_ids)
			fw_pi.write(str(sup)+' ')
			fw_phrase.write(str(sup)+' ')
			for t_ids in new_ids:
				fw_pi.write(str(t_ids) +' ')
				phrase = word_dict[int(t_ids)]
				# print(phrase)
				fw_phrase.write(phrase+' ')
			fw_pi.write('\n')
			fw_phrase.write('\n')

	Read_Topic.close()
	fw_pi.close()
	fw_phrase.close()

	return fp_rst,fre_pattern

# below the max pattern function
def max_pattern(fre_kv,i,word_dict):
	Item_lists = []
	max_set =[]
	Fname = os.path.join(os.getcwd()+"/max","max-"+str(i)+".txt")
	fw_max = open(Fname, "w")
	max_name = os.path.join(os.getcwd()+"/max","max-"+str(i)+".txt.phrase")
	fw_phrase_max = open(max_name, "w")
	for lines in fre_kv:
		values = lines[1]
		for val in values:
			str_item = parse_data(val) #parse the string data
			Item_lists.append(str_item)

	for lines in fre_kv:
		num = lines[0]
		values = lines[1]
		# write_flg = 0
		for v in values:
			ki = parse_data(v)
			flag = 0
			for kj in Item_lists:
				if set(ki).issubset(kj) == True and ki!=kj:
					flag = 0
					break
				else:
					flag = 1
			if flag == 1:
				fw_max.write(str(num)+' ')
				fw_phrase_max.write(str(num)+' ')
				for tup_max in ki:
					fw_max.write(tup_max+' ')
					phrase_max = word_dict[int(tup_max)]
					fw_phrase_max.write(phrase_max+' ')
				fw_max.write('\n')
				fw_phrase_max.write('\n')

	fw_max.close()
	fw_phrase_max.close()

#-----closed pattern----
def closed_pattern(FP_rst,i,word_dict):
	fname = os.path.join(os.getcwd()+"/closed","closed-"+str(i)+".txt")
	fw_closed = open(fname, "w")
	fname_close = os.path.join(os.getcwd()+"/closed","closed-"+str(i)+".txt.phrase")
	fw_close_phrase = open(fname_close, "w")
	closed_set = []
	for kv in FP_rst:  # it is the tuple
		key = kv[0]
		values = kv[1]
		val_list =[]
		for v in values:
			val = parse_data(v)
			val_list.append(val)

		for ki in val_list:
			flag = 0
			for kj in val_list:
				if set(ki).issubset(kj) == True and ki!=kj:
					flag = 0
					break
				else:
					flag = 1
			if flag == 1:
				fw_closed.write(str(key) + ' ')
				fw_close_phrase.write(str(key) + ' ')
				for S_item in ki: 
					fw_closed.write(str(S_item)+' ')
					phrase_item = word_dict[int(S_item)]
					fw_close_phrase.write(phrase_item + ' ')
				fw_closed.write('\n')
				fw_close_phrase.write('\n')

	fw_closed.close()
	fw_close_phrase.close()

#------Main function-----------
def main():
	if not os.path.exists("patterns"):
		os.mkdir("patterns")   #create a new folder

	if not os.path.exists("max"):
		os.mkdir("max")   #create a new folder

	if not os.path.exists("closed"):
		os.mkdir("closed")   #create a new folder

	fr_word = open('vocab.txt','r')
	word_dict = dict()
	for num,lines in enumerate(fr_word):
		line = lines.split()
		word_dict[num] = line[0]
	fr_word.close()
	#-------run all the files
	for i in range(5):
		fr_Topic = open('topic-'+str(i)+'.txt','r')
		for num, lines in enumerate(fr_Topic):
			pass
		lenght = num + 1
		min_sup = int(lenght*0.01)
		fr_Topic.close()
		# min_sup = 3
		FP_rst,fre_pattern = Fun_FP_Aprior(i,min_sup,word_dict)
		max_pattern(FP_rst,i,word_dict)  	#get the max pattern
		closed_pattern(FP_rst,i,word_dict) 	#get the closed pattern
		print('--it is runing file----',i)
	print("----Congs---the work is done")

if __name__ == "__main__":
	main()

