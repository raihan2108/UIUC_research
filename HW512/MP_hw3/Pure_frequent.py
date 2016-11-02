'''Huajie Shao@10/27/2016
Fun: purity frequent pattern
'''
import numpy as np
import math
import sys
import os
import os.path
import operator

##------
def parse_data(str_data):
	id_list = str_data.strip('[]').split(',')
	new_ids = []
	for ta in id_list:
		ra = ta.strip('"\' ')
		ra = ra.replace("'",'')
		new_ids.append(ra)

	return new_ids
#----parse the string data--
def get_dtt_from_word(t,tp):
	fr_word = open('result/word-assignments.dat','r')
	t_tp = list([t,tp])
	common_num = 0
	for lines in fr_word.readlines():
		eline = lines.split()
		top_list = eline[1:]
		line_ttp = []
		for item in top_list:
			item_num = item.split(':')
			num = item_num[1]
			nm = int(num)
			line_ttp.append(nm)
		if set(t_tp).issubset(line_ttp)==True:
			common_num += 1
			# print(common_num, t_tp,top_list)

	fr_word.close()
	return common_num

#------
def len_topic():
	len_top = []
	for j in range(5):
		ft_read = open('topic-'+str(j)+'.txt','r')
		for nm,lines in enumerate(ft_read):
			pass
		len_top.append(nm+1)

	return len_top

def Cal_fp_dt(pattern,tp): #t and t' as t and tp
	fr_topic = open('topic-'+str(tp)+'.txt','r')
	fp_num = 0
	for num,lines in enumerate(fr_topic):
		t_pattern = lines.split()
		pat_other = t_pattern
		# print(tp,pat_other)
		if set(pattern).issubset(pat_other)==True:
			fp_num +=1

	fr_topic.close()
	return fp_num

#algorithm to cal purity
def purity_pattern(t,top_len,word_dict):
	File_name = os.path.join(os.getcwd()+"/purity","purity-"+str(t)+".txt")
	fw_purity = open(File_name, "w")
	File_purity = os.path.join(os.getcwd()+"/purity","purity-"+str(t)+".txt.phrase")
	fw_purity_phrase = open(File_purity, "w")
	other_topid = []
	Dt_list =[]
	for j in range(5):
		if j!=t:
			other_topid.append(j)
			Dt_list.append(top_len[j])
		else:
			Dt_now = top_len[j]

	Arr_dtp = np.asarray(Dt_list)
	Sum_Dtt = Arr_dtp + Dt_now
	# print(Arr_dtp,Dt_now, Sum_Dtt)
	fr_pattern = open('patterns/pattern-'+str(t)+'.txt','r')
	pattern_pur_dict=dict()
	for lines in fr_pattern.readlines():
		line = lines.split()
		FPnum = line[0]
		FP_now = int(FPnum)
		pattern = line[1:]
		FP_other =[]
		Com_num = []
		for tp in other_topid:
			num_fp = Cal_fp_dt(pattern,tp)
			fp_common_num = get_dtt_from_word(t,tp)
			FP_other.append(num_fp)
			Com_num.append(fp_common_num)  #cal the Dtt of top t and t'

		print(pattern,FP_other)
		Sum_fp =np.asarray(FP_other) + FP_now  #the sum of t and t'
		sumdtt = Sum_Dtt-Com_num
		max_ddt = max(Sum_fp/sumdtt)
		purity = math.log2(FP_now/Dt_now)-math.log2(max_ddt)
		pattern_pur_dict[str(pattern)] = purity

	sort_purity = sorted(pattern_pur_dict.items(),key=operator.itemgetter(1), reverse=True)
	for items in sort_purity:
		purity = items[1]
		patterns = items[0]
		newpat = parse_data(patterns)
		fw_purity.write("%.5f" %purity+' ')
		fw_purity_phrase.write("%.5f" %purity+' ')
		for pat in newpat:
			fw_purity.write(pat+' ')
			pat_phrase = word_dict[int(pat)]
			fw_purity_phrase.write(pat_phrase+' ')

		fw_purity.write('\n')
		fw_purity_phrase.write('\n')


	fr_pattern.close()
	fw_purity_phrase.close()


def main():
	if not os.path.exists("purity"):
		os.mkdir("purity")    # create a new folder
	top_len = len_topic()
	print('--It is beginning to run---')

	fr_word = open('vocab.txt','r')
	word_dict = dict()
	for num,lines in enumerate(fr_word):
		line = lines.split()
		word_dict[num] = line[0]
	fr_word.close()

	for t in range(1):
		print('---running topic:--',t)
		purity_pattern(t,top_len,word_dict)

	print('---well done----')

if __name__ == "__main__":
	main()
