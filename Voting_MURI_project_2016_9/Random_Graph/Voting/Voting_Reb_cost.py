'''
Huajie Shao@09/20/2016
Fun: voting for MURI project about influence
graph in social sensing
'''

import numpy as np
# from math import factorial
from copy import deepcopy
import sys
import random


# cost = 50
M= 50		# Ma Carlo = 15
NumV = 60
p = 0.6
ratio = 0.7
w = 0.6
n = 80

#----define the huristic alg based on the reliability
# to choose the sources
def Get_graph(N,ratio):
	nr = int(N*(1-ratio))
	Graph = np.zeros([N,N])
	# for i in range(1,nr):  	# dependent sources
	# 	j = np.random.randint(0, i)
	# 	Graph[i][j] = 1		# column is the ancestor
	for i in range(nr+1,N):  	# dependent sources
		j = np.random.randint(0, i)
		Graph[i][j] = 1

	SD_ancestor = dict()   	# source graph dictionary	
	SD_successor = dict()
	for j in range(N):
		G_row = Graph[j,:]  # get the rows
		G_col = Graph[:,j]
		for i in range(N):
			if G_row[i]==1:		# get the column denote the ancestor
				SD_ancestor.setdefault(j, []).append(i)	 	# get the list of ancestors
			if G_col[i]==1:
				SD_successor.setdefault(j, []).append(i)	# get the list of successors

	return SD_ancestor,SD_successor


def Generate_SC(N,NumV,id_rank,SD_successor):   #sources'claims
	# print(N)
	t = int(NumV*p)
	SC = np.zeros([NumV,N])	#assertion and number of variables
	C0 = np.random.randint(0, 1, t)
	C1 = np.random.randint(1, 2, NumV-t)
	C = np.hstack((C1,C0))
	random.shuffle(C)
	top = int(N*0.3)
	Top_rank = id_rank[0:top]
	# print(Top_rank)
	# generate the claims of each observation
	for j in range(NumV):
		if C[j] ==1:
			t = np.random.uniform(0.3,0.9)
			numt = int(N*t)   # number of SC = 1
			SC1 = np.random.randint(1, 2, numt)	    # sc = 1
			SC0 = np.random.randint(0, 1, N-numt)   # sc = 0 
			SC01 = np.concatenate((SC0,SC1))
			random.shuffle(SC01)
			for k in Top_rank:
				cout = np.random.randint(0,100,1)
				if cout >= 30:
					SC01[k] = 1

			SC[j,:] = SC01
		else:
			# generate the false assertion and let SC=1
			tn =  np.random.uniform(0.2,0.8)
			nt = int(N*tn)
			SC3 = np.random.randint(1, 2, nt)
			SC4 = np.random.randint(0, 1, N-nt)
			SC34 = np.concatenate((SC4,SC3))
			random.shuffle(SC34)
			for kk in Top_rank:
				cout = np.random.randint(0,100,1)
				if cout >= 30:
					# SC01[k] = 1
					SC34[kk] = 0

			SC[j,:] = SC34

	for i in range(NumV):
		for j in range(n):
			if j in SD_successor.keys():
				child = SD_successor[j]
				for cd in child:
					cout = np.random.randint(0,100,1)
					if cout >= 30:  #control the prob of following ancestors
						SC[i,cd] = SC[i,j]

	return SC,C


##----voting based on the sorted reliability
def Fun_voting(st_num,SC,NumV,C):
	Claims = []
	num_src = len(st_num)
	# print(num_src)
	SC_new = []
	count = 0
	for j in st_num:
		SCJ = SC[:,j]
		lst = SCJ.tolist()
		SC_new.extend([lst])
		SC_arr = np.asarray(SC_new)
		SC_final = np.transpose(SC_arr)

	for i in range(NumV):
		SCi = SC_final[i,:]
		sum_sc = sum(SCi)
		if sum_sc > num_src/2:
			Claims.append(1)
		else:
			Claims.append(0)

	for j in range(NumV):
		if Claims[j] == C[j]:
			count += 1
	accy = count/NumV

	return accy
###-----huristic function----
def Hfun_reb(cost,new_price,n,C,ID_dict):
	st_num = []
	sum_fee = 0
	nums = []
	k = 0
	# print(new_price)
	while sum_fee <= cost:
		sum_fee = np.sum(new_price[0:k])
		k += 1
		if k >= n:
			break

	# st_num = list(range(0,k))
	nums = [ID_dict[i] for i in range(k)]
	# print()
	reb_accy = Fun_voting(nums,SC,NumV,C)

	return reb_accy


# define the random function
def rand_fun(NumV,SC,cost,prc,C,N):
	Psum = 0
	Num = []
	Rai = []
	Rbi = []
	while Psum<cost:
		ids = np.random.randint(0,N)
		if ids in Num:
			pass
		else:
			Psum += prc[ids]
			Num.append(ids)

	rand_accy = Fun_voting(Num,SC,NumV,C)

	return rand_accy


# define function: cost-only
# cost_only(ct,cost,SC)
def cost_only(SC,Fee,cost,C,prc_ids_dict):
	Psum = 0
	N = len(Fee)
	nums = []
	snums=[]
	for j in range(N):
		if Psum <= cost:
			Psum += Fee[j]
			nums.append(j)
		else:
			break

	snums = [prc_ids_dict[i] for i in nums]
	cost_accy = Fun_voting(snums,SC,NumV,C)

	return cost_accy

def Get_abi(SD_successor,n):
	Num = n
	ai = np.zeros(Num)
	bi = np.zeros(Num)
	pr = np.zeros(Num)
	for sd in range(n):
		if sd in SD_successor.keys():
			child = len(SD_successor[sd])
			if child >=6:
				ai[sd] = np.random.uniform(0.8,0.9)
				bi[sd] = np.random.uniform(0.1,0.2)
				pr[sd] = np.random.uniform(1.3,1.5)
			elif child >= 4 and child <=5:
				ai[sd] = np.random.uniform(0.7,0.8)
				bi[sd] = np.random.uniform(0.2,0.3)
				pr[sd] = np.random.uniform(1,1.4)
			elif child>=2 and child <=3:
				ai[sd] = np.random.uniform(0.6,0.7)
				bi[sd] = np.random.uniform(0.3,0.4)
				pr[sd] = np.random.uniform(0.8,1.2)
			else:
				ai[sd] = np.random.uniform(0.3,0.6)
				bi[sd] = np.random.uniform(0.4,0.5)
				pr[sd] = np.random.uniform(0.5,1)
		else:
			ai[sd] = np.random.uniform(0.3,0.6)
			bi[sd] = np.random.uniform(0.4,0.5)
			pr[sd] = np.random.uniform(0.5,1)

	pr = np.around(pr,decimals=3)
	ai = np.around(ai,decimals=3)
	bi = np.around(bi,decimals=3)
	return ai,bi,pr


##calculate the reb of sources based on their children
def Sort_abi(ai,bi):
	dict_ai = dict()
	id_list = []
	# dict_bi = dict()
	rk_ai = sorted(ai,reverse=True)
	# print(rk_ai)
	rk_bi = np.sort(bi)
	new_bi = np.zeros(len(bi))
	for i in range(n):
		dict_ai[ai[i]] = i
	for k in range(n):
		key = rk_ai[k]   # get the key of ai
		ids = dict_ai[key]
		new_bi[ids] = rk_bi[k]
		id_list.append(ids)

	return new_bi,id_list


#-----below is the main function to compare with the baselines
rst_err1 = []
rst_err2 = []
rst_err3 = []
# rst_err4 = []
for mt in range(0,M):
	print("running time is", mt)
	arr_err1 = []
	arr_err2 = []
	arr_err3 = []
	# arr_err4 = []
	# Assertion = np.random.uniform(0,2,)
	for cost in range(60,110,10):
		# ai = np.random.uniform(0.4,0.9,n)
		# bi = np.random.uniform(0.1,0.3,n)
		# ai = np.around(ai*1000)/1000
		# bi = np.around(bi*1000)/1000
		# pr = np.random.uniform(1,2, n)  # the prices for each source
		# pr = np.around(pr,decimals=3)
		SD_ancestor,SD_successor = Get_graph(n,ratio)
		ai,bi,pr = Get_abi(SD_successor,n)
		bi,id_rank = Sort_abi(ai,bi)

		# ---below fun: store the [ai, id]
		dict_ai = dict()
		dict_bi = dict()
		dict_pr = dict()
		for i in range(n):
			dict_pr[pr[i]] = i
			dict_ai[ai[i]] = i
			dict_bi[i] = bi[i]

		S_ai = deepcopy(ai)  # save the original reliability
		S_bi = deepcopy(bi)
		s_prc = deepcopy(pr)
		# -----------------------------------------------------
		# --make the ai and bi similar values after sorting ai, sort first
		# -----------------------------------------------------
		for k in range(n):
			key = ai[k]   # get the key of ai
			ids = dict_ai[key]
			S_bi[k] = dict_bi[ids]

		# --- the following is to save the original ai and bi
		# it could be used for Link ** changes and W changes---
		ai = S_ai
		bi = S_bi
		pr = s_prc
		Pa = ai
		Pb = bi
		# --#function is to generate the Matrix graph ------
		SC,C = Generate_SC(n,NumV,id_rank,SD_successor)
		#---------------------
		for s in range(n):
			if s in SD_ancestor.keys():
				parent = SD_ancestor[s]
				sum_ai_anct = 0
				sum_bi_anct = 0
				for v in parent:
					sum_ai_anct += ai[v]
					sum_bi_anct += bi[v]

				length = len(parent)
				Pa[s] = (1-w)*sum_ai_anct/length + w*ai[s]
				Pb[s] = (1-w)*sum_bi_anct/length + w*bi[s]

		#----below fun: sort the reliability of sources
		Hurist_rab = 1 + ai - bi
		rab_dict = dict()
		for i in range(n):
			h_rab = Hurist_rab[i]
			rab_dict[h_rab] = i

		Rab = np.sort(Hurist_rab)  # get the most reliable sources
		Rab = sorted(Rab, reverse=True)   #get the descending order
		ID_dict = dict()
		for rk in range(n):
			ids = rab_dict[Rab[rk]]
			ID_dict[rk] = ids

		# -------sort the reliability based on the hurisctic rab-----
		# then we get the highest reb to lowest in order
		# as input for the Hfun_reb
		new_Ra = np.zeros(n)
		new_Rb = np.zeros(n)
		new_price = np.zeros(n)
		for j in range(n):
			abi = Rab[j]
			ids = rab_dict[abi]
			new_price[j] = pr[ids]  #match the prices of org sources
			new_Ra[j] = ai[ids]
			new_Rb[j] = bi[ids]

		# --based on the prices, get the maxi number of sources chosen
		ct = np.sort(pr)  # sort prices for smallest to highest
		Ra_prc = np.zeros(n)
		Rb_prc = np.zeros(n)
		prc_ids_dict = dict()
		# this fun: sort the prices and its corrsponding reliability
		for i in range(n):
			srt_prc = ct[i]
			ids = dict_pr[srt_prc]  # find it in dict.
			Ra_prc[i] = ai[ids]
			Rb_prc[i] = bi[ids]
			prc_ids_dict[i] = ids

		psum = 0
		nm = 0
		# while psum <= cost:
		# 	nm += 1
		# 	psum += ct[nm]
		# 	if nm>n:
		# 		break

		# nm = nm-1   # get the max numbers of sources to report
		# min_err1 = 1
		#------------------------------------------------
		#  Here begin to calculate the error of our method
		#  -----------------------------------------------
		reb_accy = Hfun_reb(cost,new_price,n,C,ID_dict)

		# errors for the baselines
		rand_accy = rand_fun(NumV,SC,cost,s_prc,C,n)   #same as the RA,RB in the Matlab codes
		cost_accy = cost_only(SC,ct,cost,C,prc_ids_dict)

		arr_err1.append(reb_accy)
		arr_err2.append(rand_accy)
		arr_err3.append(cost_accy)

	rst_err1.append(arr_err1)
	rst_err2.append(arr_err2)
	rst_err3.append(arr_err3)

#-------------------------------------
# ----calculat the mean values---
# ------------------------------------
Reb_Accy1 = np.mean(rst_err1,axis=0)
Rand_Accy2 = np.mean(rst_err2,axis=0)
Cost_Accy3 = np.mean(rst_err3,axis=0)

print(Reb_Accy1)
print(Rand_Accy2)
print(Cost_Accy3)
