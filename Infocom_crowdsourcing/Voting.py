'''
Huajie Shao@09/20/2016
Fun: voting for MURI project about influence
graph of social sensing
'''

import numpy as np
# from math import factorial
from copy import deepcopy
import sys


w1 = 0.3
w2 = 0.8
nk = 2
w = 0.8
cost = 60
M= 15		# Ma Carlo = 15
NumV = 60

#----define the huristic alg based on the reliability
# to choose the sources

def Get_graph(N):
	nr = int(N*0.25)
	Graph = np.zeros([N,N])
	for i in range(1,nr):  	# dependent sources
		j = np.random.randint(0, i)
		Graph[i][j] = 1		# column is the ancestor

	for i in range(nr+1,2*nr):  	# dependent sources
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
			# if G_col[i]==1:
			# 	SD_successor.setdefault(j, []).append(i)	# get the list of successors

	return SD_ancestor


def Generate_SC(N,NumV,id_rank):   #sources'claims
	t = NumV*pr
	SC = np.zeros([NumV,N])	#assertion and number of variables
	C0 = np.random.randint(0, 1, t)
	C1 = np.random.randint(1, 2, NumV-t)
	C = np.hstack((C1,C0))
	random.shuffle(C)
	top = int(N*0.3)
	Top_rank = id_rank[0:top]
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
				bull = np.around(np.random.random()+0.3)
				SC01[k] = int(bull)

			SC[j,:] = SC01
		else:
			# generate the false assertion and let SC=1
			tn =  np.random.uniform(0.2,0.7)
			nt = int(N*tn)
			SC3 = np.random.randint(1, 2, nt)
			SC4 = np.random.randint(0, 1, N-nt)
			SC34 = np.concatenate((SC4,SC3))
			random.shuffle(SC34)
			for kk in Top_rank:
				bull = np.around(np.random.random()-0.3)
				SC34[kk] = int(bull)

			SC[j,:] = SC34

	return SC,C


##----voting based on the sorted reliability
def Fun_voting(st_num,SC,NumV,C):
	Claims = []
	num_src = len(st_num)
	passvoting_reb(st_num,SC):
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

	for j in range(len(Claims)):
		if Claims[j] == C[j]:
			count += 1
	accy = count/NumV

	return accy
###-----huristic function----
def Hfun_reb(cost, new_price, n,C):
	st_num = []
	sum_fee = 0
	k = 5
	while sum_fee <= cost:
		sum_fee = np.sum(new_price[0:k])
		k += 1
		if k > n:
			break

	st_num = list(range(0,k))
	reb_accy= Fun_voting(st_num,SC,NumV,C)

	return reb_accy


# define the random function
def rand_fun(NumV,SC,cost,prc,C):
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
def cost_only(SC,Fee,cost,C):
	Psum = 0
	N = len(Fee)
	nums = []
	for j in range(N):
		if Psum <= cost:
			Psum += Fee[j]
			nums.append(j)
		else:
			break

	cost_accy = Fun_voting(nums,SC,NumV,C)

	return cost_accy



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
	for n in range(50,110,10):
		ai = np.random.uniform(0.4,0.9,n)
		bi = np.random.uniform(0.1,0.3,n)
		ai = np.around(ai*1000)/1000
		bi = np.around(bi*1000)/1000
		pr = np.random.uniform(1, 5, n)  # the prices for each source
		pr = np.around(pr,decimals=3)
		bi,id_rank = Sort_abi(ai,bi)

		# ---below fun: store the [ai, id]
		dict_ai = dict()
		dict_bi = dict()
		dict_pr = dict()
		for i in range(n):
			dict_pr[pr[i]] = i

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
		SD_ancestor = Get_graph(n)
		SC,C = Generate_SC(n,NumV,id_rank)
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

		# -------sort the reliability based on the hurisctic rab-----
		# then we get the highest reb to lowest in order
		# as input for the Hfun_reb
		new_Ra = np.zeros(n)
		new_Rb = np.zeros(n)
		new_price = np.zeros(n)
		for j in range(n):
			abi = Rab[j]
			ids = rab_dict[abi]
			new_price[j] = pr[ids]
			new_Ra[j] = ai[ids]
			new_Rb[j] = bi[ids]

		# --based on the prices, get the maxi number of sources chosen
		ct = np.sort(pr)  # sort prices for smallest to highest
		Ra_prc = np.zeros(n)
		Rb_prc = np.zeros(n)
		# this fun: sort the prices and its corrsponding reliability
		for i in range(n):
			srt_prc = ct[i]
			ids = dict_pr[srt_prc]  # find it in dict.
			Ra_prc[i] = ai[ids]
			Rb_prc[i] = bi[ids]

		psum = 0
		nm = 0
		while psum <= cost:
			nm += 1
			psum += ct[nm]
		nm = nm-1   # get the max numbers of sources to report
		min_err1 = 1


		#------------------------------------------------
		#  Here begin to calculate the error of our method
		#  -----------------------------------------------
		reb_accy = Hfun_reb(cost, new_price, n,C)

		# errors for the baselines
		rand_accy = rand_fun(NumV,SC,cost,prc,C)   #same as the RA,RB in the Matlab codes
		cost_accy = cost_only(SC,Fee,cost,C)

		arr_err1.append(min_err1)
		arr_err2.append(err2)
		arr_err3.append(err3)

	rst_err1.append(arr_err1)
	rst_err2.append(arr_err2)
	rst_err3.append(arr_err3)

#-------------------------------------
# ----calculat the mean values---
# ------------------------------------

Accy1 = np.mean(rst_err1,axis=0)
Accy2 = np.mean(rst_err2,axis=0)
Accy3 = np.mean(rst_err3,axis=0)

print(Err1)
print(Err2)
print(Err3)
