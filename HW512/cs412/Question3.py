'''
Huajie @10/1/2016
fun:frequent pattern
'''

import numpy as np
import math
import sys
# import ast

def Get_candidate(ai,aj):
	Alpha = []
	# print("this is ai",ai)
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
	# print(Alpha)
	return Alpha
# test = ast.literal_eval("['a','b']")

items_dict=dict()  #use dict to statistic numbers
items_list =[]
fr_data = open('data.transaction')
for num,val in enumerate(fr_data):
	vals = val.split()
	for i in vals:
		if i not in items_dict:
			items_dict[i] = 1
		else:
			items_dict[i] +=1

	# val = val.strip()
	items_list.extend([vals])

# print(items_list)
# print("the single alphabet is:",len(items_dict))

Fk = items_dict  #get the frequent items
# Ck = items_dict.keys()
minsup = 10
item = []
Snums = []
t = 1
store_v3=[]
History=[]
while bool(Fk):
	t +=1
	item=[]
	for key in Fk.keys():
		v = Fk[key]
		if v >=minsup:
			item.append(key)
			# print(key)
	Snums.append(len(item))  # np.sum([],element)
	item=sorted(item)
	# print(item)
	Ck =[]
	Three_item=[]
	# print(Ck)
	Fk = dict()
	for i in range(len(item)):
		for j in range(i+1,len(item)):
			A = item[i]
			B = item[j]
			rst=Get_candidate(A,B)
			rst = sorted(rst)
			if rst not in Ck and len(rst) == t:
				Ck.append(rst)
			if len(rst) == 3 and rst not in Three_item:
				Three_item.append(rst)
	# print(Ck)
	for val in Ck:
		for items in items_list:
			flag = 0
			for v in val:
				if v in items:
					pass
				else:
					flag = 1

			if flag ==0:
				# val = sorted(val)
				sval = str(val)
				if sval not in Fk:
					Fk[sval] = 1
				else:
					Fk[sval] += 1
	# print('the following is fk:')
	# print(Fk)
	if len(Three_item)>=1:
		# print(Three_item)
		# print(Fk)
		for z in Three_item:
			strz = str(z)
			if strz in Fk:
				v3= Fk[strz]
				if v3>=minsup:
					store_v3.append(v3)
					print(strz,v3)
	# print("---------------")
	sce = str(['C', 'E'])
	SCEA =str(['A','C', 'E'])
	str_abc = str(['A','B', 'C'])
	str_abce = str(['A','B', 'C','E'])
	if str_abc in Fk:
		abc = Fk[str_abc]
		print("abc",abc)
	if str_abce in Fk:
		abce = Fk[str_abce]
		print("abce",abce)
	# confidence measurement
	# print('--the next confidence')
	if sce in Fk:
		CE = Fk[sce]
		# print("the CE is",CE)
	if SCEA in Fk:
		ACE = Fk[SCEA]
		# print("scea",ACE)

print(Snums)
print('Total:',sum(Snums))
print(len(store_v3))
# print("the total number is:",sum(Snums))

#confidence:  C E--->A

print("the CE is",CE)
print("ACE",ACE)
print("ac--e:\n",ACE/CE)
# A,B,C--->E
print("abc--e\n:",abce/abc,23/31)