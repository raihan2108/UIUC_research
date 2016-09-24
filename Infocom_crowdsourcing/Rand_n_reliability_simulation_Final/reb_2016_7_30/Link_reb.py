'''
Huajie Shao@2016/7/26: [[Good to run]]
Version 2, Improved by Huajie, 7/26/2016
Functions: Random Graph to calculate the expected error
Source selection problem in social networks and
we calculate the expected error by changing the [Change the links among sources]
'''

import numpy as np
from math import factorial
from copy import deepcopy
import sys
# import math
# import random
# from subfun_test import test   this could import the function


link1 = 1	# link
link2 = 4
w = 0.8
cost = 40
M= 30	# Ma Carlo
step=0.5
n = 80
# n2 = 70
num_assertion = 20


#----define the huristic alg based on the reliability
# to choose the sources
# #------below is to calculat the reb-----
#------------------------------------------
def Get_source_reb(st_num,SD_ancestor,org_id_dict,S_ai,S_bi):
	indpt_src = []
	Org_ids = []
	Ran = []
	Rbn = []
	for m in st_num:
		ids = org_id_dict[m]
		Org_ids.append(ids)

	for s in Org_ids:
		sum_ai_anct = 0
		sum_bi_anct = 0
		if s in SD_ancestor.keys():
			ancestor = SD_ancestor[s]
			s_ids = set(Org_ids).intersection(ancestor) # if they has a father?
			father = list(s_ids)  # get the same number
			if len(father) > 0:
				for f in father:
					sum_ai_anct += S_ai[f]
					sum_bi_anct += S_bi[f]

				ai_s = (1-w)*sum_ai_anct/len(father) + w*S_ai[s]
				bi_s = (1-w)*sum_bi_anct/len(father) + w*S_bi[s]
				Ran.append(ai_s)
				Rbn.append(bi_s)
			else:
				Ran.append(w*S_ai[s])
				Rbn.append(w*S_ai[s])
		else:
			Ran.append(S_ai[s])
			Rbn.append(S_bi[s])
	return Ran,Rbn

#---------------------
def Hfun_reb(cost, new_price, k, n):
	st_num = []
	if np.sum(new_price[0:k+1]) <= cost:  # e.g k=3 there are 4 numbers
		st_num = list(range(0,k+1))
	elif np.sum(new_price[0:k]) <= cost:
		for j in range(k+1, n):
			Sum_cost = np.sum(new_price[0:k]) + new_price[j]
			if Sum_cost <= cost:
				st_num = list(range(0,k))
				st_num.append(j)
			else:
				if j < n-1:
					Sum_cost = np.sum(new_price[0:k-1]) + new_price[j] + new_price[j+1]
					if Sum_cost<cost:
						st_num = list(range(0,k-1))
						st_num.extend([j, j+1])
					else:
						st_num = list(range(0,k-1))
	return st_num


# define the combinations
def n_choose_k(n,r):
	return factorial(n) / factorial(r) / factorial(n-r)


#--function: similarity based lossy estimation algorithm, expected error
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
			st = 1.0
			sf = 1.0
			ST_list.append(st)
			SF_list.append(sf)
		t += 1

		ST_all.extend([ST_list])
		SF_all.extend([SF_list])
	#---##calculate the expected error
	Err = 0
	# print(ST_all)
	# print(C_credit)
	print("----it is running--:links changes",len(Rai))
	# Pro = 0.5
	for Pro in C_credit:
		Sum = 0
		for n1 in range(L1+1):
			for n2 in range(L2+1):
				for n3 in range(L3+1):
					for n4 in range(L4+1):
						for n5 in range(L5+1):
							for n6 in range(L6+1):
								PCt =Pro*ST_all[0][n1]*ST_all[1][n2]*ST_all[2][n3]*ST_all[3][n4]*ST_all[4][n5]*ST_all[5][n6]
								PCf =(1-Pro)*SF_all[0][n1]*SF_all[1][n2]*SF_all[2][n3]*SF_all[3][n4]*SF_all[4][n5]*SF_all[5][n6]
								PErr = min(PCt,PCf)
								# print(PErr)
								Sum += PErr

		Err += Sum
	return Err/len(C_credit)

# define the random function
# define the random function
def rand_fun(N,RA,RB,cost,prc,C_credit,SD_ancestor):
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

	rand_id_dict = dict()
	for nm in Num:
		rand_id_dict[nm]=nm
	# for ids in Num:
	# 	Rai.append(RA[ids])
	# 	Rbi.append(RB[ids])
	S_ai = RA
	S_bi = RB
	Rai,Rbi = Get_source_reb(Num,SD_ancestor,rand_id_dict,S_ai,S_bi)
	rand_err = fun_window6(Rai,Rbi,C_credit)
	return rand_err


# define function: cost-only

def cost_only(S_ai,S_bi,ct,cost,C_credit,prc_ids_dict,SD_ancestor):
	Psum = 0
	N = len(S_ai)
	nums = []
	for j in range(N):
		if Psum <= cost:
			Psum += ct[j]
			nums.append(j)
		else:
			break
	Rai,Rbi = Get_source_reb(nums,SD_ancestor,prc_ids_dict,S_ai,S_bi)
	cost_err = fun_window6(Rai,Rbi,C_credit)
	return cost_err


# #the below is the crowdbudget algorithm---

def crowdbudget(cost,R_ai,R_bi,C_credit):
	u1=np.mean(R_ai)
	u2=np.mean(R_bi)
	dm1=abs(u1-0.4)
	dm2=abs(u2-0.5)
	# nm=np.mean(prc)
	# N=round(cost/nm+1)
	N = len(R_ai)
	crowd_err = 0
	for pro_asst in C_credit:
		err=pro_asst*np.exp(-2*N*dm1**2)+(1-pro_asst)*np.exp(-2*N*dm2**2)
		crowd_err += err
	return crowd_err/len(C_credit)

def Generate_graph(n,nk):   # generate random graph!!
	flag = 1
	Amtx = np.zeros([n,n])
	links = nk*n
	while flag==1:
		i = np.random.randint(0,n-5)
		j = np.random.randint(i+1,n)
		ele = 1
		Amtx[i,j]=ele
		if np.sum(Amtx)<=links:
			flag = 1
		else:
			flag = 0

	# establish the dict to find the dependency graph
	SD_ancestor = dict()
	SD_successor = dict()
	for i in range(n):
		G_row = Amtx[i,:]  # get the rows
		G_col = Amtx[:,i]
		for j in range(n):
			if G_row[j]==1:		# get the column denote the ancestor
				SD_successor.setdefault(i, []).append(j)	# list of children [id:children]]
			if G_col[j]==1:
				SD_ancestor.setdefault(i, []).append(j)	# list of ancestors [id: ancestors]

	return SD_ancestor, SD_successor


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
				pr[sd] = np.random.uniform(1,1.2)
			elif child>=2 and child <=3:
				ai[sd] = np.random.uniform(0.6,0.7)
				bi[sd] = np.random.uniform(0.3,0.4)
				pr[sd] = np.random.uniform(0.8,1)
			else:
				ai[sd] = np.random.uniform(0.3,0.6)
				bi[sd] = np.random.uniform(0.4,0.5)
				pr[sd] = np.random.uniform(0.5,0.8)
		else:
			ai[sd] = np.random.uniform(0.3,0.4)
			bi[sd] = np.random.uniform(0.4,0.5)
			pr[sd] = np.random.uniform(0.5,0.8)

	pr = np.around(pr,decimals=3)
	return ai,bi,pr


#-----below is the main function to compare with the baselines

rst_err1 = []
rst_err2 = []
rst_err3 = []
rst_err4 = []
for mt in range(0,M):
	print("running time is", mt)
	arr_err1 = []
	arr_err2 = []
	arr_err3 = []
	arr_err4 = []
	# ai = np.random.uniform(0.3,0.8,n)
	# bi = np.random.uniform(0.1,0.5,n)
	# pr = np.random.uniform(0.5, 1.5, n)  # the prices for each source
	# pr = np.around(pr,decimals=3)
	C_credit = np.random.uniform(0.4,0.6,num_assertion)
	for nk in np.arange(link1,link2,step):

		# we first generate the graph and get the reb
		SD_ancestor,SD_successor = Generate_graph(n,nk)
		ai,bi,pr = Get_abi(SD_successor,n)
		#------------------------------------S
		S_ai = deepcopy(ai)  			# save the original reliability
		S_bi = deepcopy(bi)
		s_prc = deepcopy(pr)
		dict_pr = dict()
		for i in range(n):
			dict_pr[pr[i]] = i
		
		# ai = S_ai
		# bi = S_bi
		# pr = s_prc
		#---------------------
		for s in range(n):
			if s in SD_ancestor.keys():  #calculate the prob of successors 
				parent = SD_ancestor[s]
				sum_ai_anct = 0
				sum_bi_anct = 0
				for v in parent:
					sum_ai_anct += S_ai[v]
					sum_bi_anct += S_bi[v]

				length = len(parent)
				ai[s] = (1-w)*sum_ai_anct/length + w*ai[s]
				bi[s] = (1-w)*sum_bi_anct/length + w*bi[s]

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
		new_price = np.zeros(n)
		org_id_dict=dict()
		for j in range(n):
			abi = Rab[j]
			ids = rab_dict[abi]
			org_id_dict[j] = ids
			new_price[j] = pr[ids]  # save----used for rand function
			# new_Ra[j] = ai[ids]
			# new_Rb[j] = bi[ids]

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
		while psum <= cost:
			nm += 1
			psum += ct[nm]
		nm = nm-1   # get the max numbers of sources to report
		min_err1 = 1
		# print("nm is the number of",nm)
		#------------------------------------------------
		#  Here begin to calculate the error of our method
		#  -----------------------------------------------
		for k in range(10, nm):
			st_num = Hfun_reb(cost, new_price, k, n)

			if len(st_num) > 0:
				Ran, Rbn = Get_source_reb(st_num,SD_ancestor,org_id_dict,S_ai,S_bi)
				# print(Ran)
				# for j in range(len(st_num)):
					# ids = st_num[j]

				err1 = fun_window6(Ran,Rbn,C_credit)
				# print(err1)
				if err1 < min_err1:
					min_err1 = err1
					# crowd_price = ppr
					crowd_ai = Ran
					crowd_bi = Rbn

		# errors for the baselines
		err2 = rand_fun(n,S_ai,S_bi,cost,pr,C_credit,SD_ancestor)   #same as the RA,RB in the Matlab codes
		err3 = cost_only(S_ai,S_bi,ct,cost,C_credit,prc_ids_dict,SD_ancestor)
		# print(crowd_bi)
		# print(len(crowd_ai))
		err4 = crowdbudget(cost,crowd_ai, crowd_bi,C_credit)
		# print(min_err1)
		arr_err1.append(min_err1)
		arr_err2.append(err2)
		arr_err3.append(err3)
		arr_err4.append(err4)

	rst_err1.append(arr_err1)
	rst_err2.append(arr_err2)
	rst_err3.append(arr_err3)
	rst_err4.append(arr_err4)

#-------------------------------------
# ----calculat the mean values---
# ------------------------------------
Err1 = np.mean(rst_err1,axis=0)
Err2 = np.mean(rst_err2,axis=0)
Err3 = np.mean(rst_err3,axis=0)
Err4 = np.mean(rst_err4,axis=0)


fw_err = open('Link_error_Reb.txt','w')
fw_err.write(str(Err1)+'\n'+str(Err2)+'\n'+str(Err3)+'\n'+str(Err4)+'\n')
fw_err.write("ratio change from 1 to 4 ")
fw_err.close()

print("when the links ratio changes from 1 to 4:")
print(Err1)
print(Err2)
print(Err3)
print(Err4)












