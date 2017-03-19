'''
Huajie Shao @12/11/2016
Fun: compare the SLE algorithm with global poptimization
'''

import os,sys
import numpy as np
import random

nk = 1
w = 0.8
cost = 30
M= 3	# Ma Carlo
step = 10
n1 = 50
n2 = 110
num_assertion = 1

#window of 6
def fun_window6(Rai,Rbi,C_credit):
	C1, C2, C3, C4, C5, C6= [],[],[],[],[],[]
	B1, B2, B3, B4, B5, B6= [],[],[],[],[],[]
	Sum=0
	# print(Rai)
	md = np.median(Rai)
	mxu = max(Rai) - md
	mx = md - min(Rai)
	delta = 6  # divided into 6 groups
	T = delta/2
	for i in range(len(Rai)):
		if Rai[i]>=md + 2*mxu/T:
			C1.append(Rai[i])
			B1.append(Rbi[i])
		elif Rai[i] < md + 2*mxu/T and Rai[i] >= md + mxu/T:
			C2.append(Rai[i])
			B2.append(Rbi[i])
		elif Rai[i] < md + mxu/T and Rai[i] >= md:
			C3.append(Rai[i])
			B3.append(Rbi[i])
		elif Rai[i] < md and Rai[i] >= md -mx/T:
			C4.append(Rai[i])
			B4.append(Rbi[i])
		elif Rai[i] < md-mx/T and Rai[i] >= md -2*mx/T:
			C5.append(Rai[i])
			B5.append(Rbi[i])
		else:
			C6.append(Rai[i])
			B6.append(Rbi[i])

	# get the mean val of each group
	C=[C1, C2, C3, C4, C5, C6]
	B=[B1, B2, B3, B4, B5, B6]
	mc = np.zeros(delta)
	mb = np.zeros(delta)
	for i in range(delta):
		arr_c = C[i]
		arr_b = B[i]
		if len(arr_c)>=1:
			mc[i] = np.mean(arr_c)
			mb[i] = np.mean(arr_b)

	L1,L2,L3,L4,L5,L6 = len(C1), len(C2),len(C3),len(C4),len(C5),len(C6)
	L = [L1,L2,L3,L4,L5,L6]
	ST_all, SF_all = [], []
	t = 0
	for Ls in L:
		ST_list, SF_list = [], []
		if Ls >= 1:
			for d in range(Ls+1):
				st = n_choose_k(Ls,d)*mc[t]**d*(1-mc[t])**(Ls-d)
				sf = n_choose_k(Ls,d)*mb[t]**d*(1-mb[t])**(Ls-d)
				ST_list.append(st)
				SF_list.append(sf)
		else:
			ST_list.append(1.0)
			SF_list.append(1.0)
		t += 1

		ST_all.extend([ST_list])
		SF_all.extend([SF_list])
	#---##calculate the expected error
	Err = 0
	# print(ST_all)
	# print(C_credit)
	print("----it is running---",len(Rai))
	for Pro in C_credit:
		Sum = 0
		for n1 in range(L1+1):
			for n2 in range(L2+1):
				for n3 in range(L3+1):
					for n4 in range(L4+1):
						for n5 in range(L5+1):
							for n6 in range(L6+1):
								# Pro = 0.5
								PCt =Pro*ST_all[0][n1]*ST_all[1][n2]*ST_all[2][n3]*ST_all[3][n4]*ST_all[4][n5]*ST_all[5][n6]
								PCf =(1-Pro)*SF_all[0][n1]*SF_all[1][n2]*SF_all[2][n3]*SF_all[3][n4]*SF_all[4][n5]*SF_all[5][n6]
								PErr = min(PCt,PCf)
								Sum += PErr

		Err += Sum

	return Err/len(C_credit)

# windows of 4 ---
def fun_window4(Rai,Rbi,C_credit):
	C1, C2, C3, C4= [],[],[],[],[]
	B1, B2, B3, B4= [],[],[],[],[]
	Sum=0
	# print(Rai)
	md = np.median(Rai)
	mxu = max(Rai) - md
	mx = md - min(Rai)
	delta = 4  # divided into 6 groups
	T = delta/2
	for i in range(len(Rai)):
		if Rai[i]>=md + mxu/T:
			C1.append(Rai[i])
			B1.append(Rbi[i])
		elif Rai[i] < md + mxu/T and Rai[i] >= md:
			C2.append(Rai[i])
			B2.append(Rbi[i])
		elif Rai[i] < md and Rai[i] >= md - mx/T:
			C3.append(Rai[i])
			B3.append(Rbi[i])
		else:
			C4.append(Rai[i])
			B4.append(Rbi[i])

	# get the mean val of each group
	C=[C1, C2, C3, C4]
	B=[B1, B2, B3, B4]
	mc = np.zeros(delta)
	mb = np.zeros(delta)
	for i in range(delta):
		arr_c = C[i]
		arr_b = B[i]
		if len(arr_c)>=1:
			mc[i] = np.mean(arr_c)
			mb[i] = np.mean(arr_b)

	L1,L2,L3,L4 = len(C1), len(C2),len(C3),len(C4)
	L = [L1,L2,L3,L4]
	ST_all, SF_all = [], []
	t = 0
	for Ls in L:
		ST_list, SF_list = [], []
		if Ls >= 1:
			for d in range(Ls+1):
				st = n_choose_k(Ls,d)*mc[t]**d*(1-mc[t])**(Ls-d)
				sf = n_choose_k(Ls,d)*mb[t]**d*(1-mb[t])**(Ls-d)
				ST_list.append(st)
				SF_list.append(sf)
		else:
			ST_list.append(1.0)
			SF_list.append(1.0)

		t += 1

		ST_all.extend([ST_list])
		SF_all.extend([SF_list])
	#---##calculate the expected error
	Err = 0
	# print(ST_all)
	# print(C_credit)
	print("----it is running---",len(Rai))
	for Pro in C_credit:
		Sum = 0
		for n1 in range(L1+1):
			for n2 in range(L2+1):
				for n3 in range(L3+1):
					for n4 in range(L4+1):
						PCt =Pro*ST_all[0][n1]*ST_all[1][n2]*ST_all[2][n3]*ST_all[3][n4]
						PCf =(1-Pro)*SF_all[0][n1]*SF_all[1][n2]*SF_all[2][n3]*SF_all[3][n4]
						PErr = min(PCt,PCf)
						Sum += PErr

		Err += Sum

	return Err/len(C_credit)



