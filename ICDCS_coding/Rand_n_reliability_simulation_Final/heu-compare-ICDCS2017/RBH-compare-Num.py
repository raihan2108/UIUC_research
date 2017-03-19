'''
Huajie Shao@2016/12/9
Version 2, Improved by Huajie,12/9/2016
Functions: Random Graph to calculate the expected error
Source selection problem in social networks and
we calculate the expected error by changing the [N and Cost of sources]
'''

import numpy as np
from math import factorial
from copy import deepcopy
import sys
# import math
# import random
# from subfun_test import test   this could import the function

# we can also run cost changes
nk = 1
w = 0.8
cost = 30
M= 30	# Ma Carlo
step = 10
n1 = 50
n2 = 110
num_assertion = 10

#----define the huristic alg based on the reliability
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
				Ran.append(S_ai[s]) ## I have a question of the result
				Rbn.append(S_ai[s])
		else:
			Ran.append(S_ai[s])
			Rbn.append(S_bi[s])

	return Ran,Rbn


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
								# print(PErr)
								Sum += PErr

		Err += Sum

	return Err/len(C_credit)

# define the random function
# reb based heuristic to choose the sources
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

#-----define RBH algorithm--------
def Reliability_cal_fun(S_ai,S_bi,cost,prc,C_credit,SD_ancestor):
	hrab = 1 + S_ai - S_bi
	rab_dict = dict()
	n = len(S_ai)
	for ids in range(n):
		rab_dict[ids] = hrab[ids]

	rank_ids = sorted(rab_dict, key = rab_dict.get, reverse=True)
	org_id_dict = dict()
	new_price = np.zeros(n)
	for t in range(n):
		ids = rank_ids[t]
		org_id_dict[t] = ids
		new_price[t] = prc[ids]

	sort_price = sorted(prc)  #sort the price to get the max num
	sum_prc = 0
	nm = 0
	while sum_prc<cost:
		sum_prc += prc[nm]
		nm += 1  #get the max number of sources

	min_err1 = 1
	for k in range(8,nm):
		Num = Hfun_reb(cost, new_price, k, n)
		if len(Num) >=1:
			Rai,Rbi = Get_source_reb(Num,SD_ancestor,org_id_dict,S_ai,S_bi)
			reb_err = fun_window6(Rai,Rbi,C_credit)
			if reb_err < min_err1:
				min_err1 = reb_err
				save_reb = Rai

	return min_err1

# define the random function
def reb_cost(S_ai,S_bi,cost,prc,C_credit,SD_ancestor):
	Rab = S_ai + 1 - S_bi
	N = len(Rab)
	ratio_id_dict = dict()
	for ids in range(N):
		ratio_id_dict[ids] = Rab[ids]/prc[ids]

	sort_ids = sorted(ratio_id_dict, key = ratio_id_dict.get, reverse= True)
	Psum = 0
	Num_list = []
	j1 = 0
	while Psum < cost:
		ids = sort_ids[j1]
		Psum += prc[ids]
		Num_list.append(ids)
		j1 += 1

	# print('num_list1',Num_list)

	ratio_id_org = dict()
	for nm in Num_list:
		ratio_id_org[nm] = nm

	Rai,Rbi = Get_source_reb(Num_list,SD_ancestor,ratio_id_org,S_ai,S_bi)
	rand_err = fun_window6(Rai,Rbi,C_credit)

	return rand_err


# define function: cost-only
def cost_only(S_ai,S_bi,cost, prc, C_credit,SD_ancestor):
	N = len(S_ai)
	prc_dict = dict()
	for ids in range(N):
		prc_dict[ids] = prc[ids]

	sort_prc_ids = sorted(prc_dict, key = prc_dict.get,  reverse= False)
	Psum = 0
	nm = 0
	nums_lst = []
	while Psum < cost:
		ids = sort_prc_ids[nm]
		Psum += prc[ids]
		nums_lst.append(ids)
		nm += 1

	nums_dict = dict()
	for nm in nums_lst:
		nums_dict[nm] = nm

	Rai,Rbi = Get_source_reb(nums_lst,SD_ancestor,nums_dict,S_ai,S_bi)
	cost_err = fun_window6(Rai,Rbi,C_credit)

	return cost_err

#---------------------------
#----sorted the sources with indepdent sources:
def indepent_reb(cost,ai,bi,s_prc,SD_ancestor,C_credit):
	children_reb = dict()
	parent_reb = dict()
	N = len(ai)
	for ids in range(N):
		if ids in SD_ancestor.keys():
			children_reb[ids] = ai[ids] + 1- bi[ids]
		else:
			parent_reb[ids] = ai[ids] + 1 - bi[ids]

	# father_rank = sorted(parent_reb.items(), key = operator.itemgetter(1),reverse=True)
	father_rank = sorted(parent_reb,  key = parent_reb.get,  reverse= True)
	child_rank = sorted(children_reb, key = children_reb.get, reverse=True)
	# print('father,',father_rank)
	# print('children',child_rank)
	Psum = 0
	num1 = 0
	ID_num = []
	while Psum < cost and num1< len(father_rank):
		ids = father_rank[num1]
		Psum += s_prc[ids]
		ID_num.append(ids)
		num1 += 1

	#use all the father sources
	num2 = 0
	while Psum < cost:
		ids = child_rank[num2]
		Psum += s_prc[ids]
		ID_num.append(ids)
		num2 += 1

	min_err4 = 1
	for k in range(10,len(ID_num)):
		ids_list =[ID_num[j] for j in range(k)]
		Rai = []
		Rbi = []
		for ids in ids_list:
			Rai.append(ai[ids])
			Rbi.append(bi[ids])
		reb_err = fun_window6(Rai,Rbi,C_credit)
		if reb_err<min_err4:
			min_err4 = reb_err
			reb2 = Rai
	return min_err4
## independent to choose father sources first
def indp_reb_cost(ai,bi,cost,prc,C_credit,SD_ancestor):
	children_reb = dict()
	parent_reb = dict()
	N = len(ai)
	for ids in range(N):
		if ids in SD_ancestor.keys():
			children_reb[ids] = (ai[ids] + 1- bi[ids])/prc[ids]
		else:
			parent_reb[ids] = (ai[ids] + 1 - bi[ids])/prc[ids]

	father_rank = sorted(parent_reb,  key = parent_reb.get,  reverse= True)
	child_rank = sorted(children_reb, key = children_reb.get,reverse= True)
	Psum = 0
	ID_num = []
	num1 = 0
	ID_num = []
	while Psum < cost and num1< len(father_rank):
		ids = father_rank[num1]
		Psum += s_prc[ids]
		ID_num.append(ids)
		num1 += 1

	#use all the father sources
	num2 = 0
	while Psum < cost:
		ids = child_rank[num2]
		Psum += s_prc[ids]
		ID_num.append(ids)
		num2 += 1
	# print("father_rank:",father_rank)
	# print("children",child_rank)
	# print("nums---:",ID_num)
	Rai = []
	Rbi = []
	for ids in ID_num:
		Rai.append(ai[ids])
		Rbi.append(bi[ids])

	reb_err = fun_window6(Rai,Rbi,C_credit)

	return reb_err

#----
def indp_cost(ai,bi,cost,prc,C_credit,SD_ancestor):
	children_prc = dict()
	parent_prc = dict()
	N = len(ai)
	for ids in range(N):
		if ids in SD_ancestor.keys():
			children_prc[ids] = prc[ids]
		else:
			parent_prc[ids] = prc[ids]

	father_rank = sorted(parent_prc,  key = parent_prc.get,  reverse = False)
	child_rank = sorted(children_prc, key = children_prc.get, reverse = False)
	Psum = 0
	num1 = 0
	ID_num = []
	while Psum < cost and num1< len(father_rank):
		ids = father_rank[num1]
		Psum += s_prc[ids]
		ID_num.append(ids)
		num1 += 1

	#use all the father sources
	num2 = 0
	while Psum < cost:
		ids = child_rank[num2]
		Psum += s_prc[ids]
		ID_num.append(ids)
		num2 += 1

	Rai = []
	Rbi = []
	for ids in ID_num:
		Rai.append(ai[ids])
		Rbi.append(bi[ids])

	cost_err = fun_window6(Rai,Rbi,C_credit)

	return cost_err

# the below is the crowdbudget algorithm---
def Generate_graph(n,nk):   # generate random graph!!
	flag = 1
	Amtx = np.zeros([n,n])
	links = nk*n
	while flag==1:
		i = np.random.randint(0,n-5)
		j = np.random.randint(i+1,n)
		ele = 1
		Amtx[i,j]=ele
		if np.sum(Amtx) <= links:
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

	return SD_ancestor

#------below is to calculat the reb-----
#------------------------------------------
def Sort_abi(ai,bi):
	dict_ai = dict()
	rk_ai = sorted(ai,reverse=True)
	rk_bi = np.sort(bi)
	new_bi = np.zeros(len(bi))
	for i in range(n):
		dict_ai[ai[i]] = i
	for k in range(n):
		key = rk_ai[k]   # get the key of ai
		ids = dict_ai[key]
		new_bi[ids] = rk_bi[k]

	return new_bi

#-----below is the main function to compare with the baselines
rst_err1 = []
rst_err2 = []
rst_err3 = []
rst_err4 = []
rst_err5 = []
rst_err6 = []
for mt in range(0,M):
	print("running time is", mt)
	arr_err1 = []
	arr_err2 = []
	arr_err3 = []
	arr_err4 = []
	arr_err5 = []
	arr_err6 = []
	for n in range(n1,n2,step):
		# flag = 1
		ai = np.random.uniform(0.3,0.9,n)
		bi = np.random.uniform(0.1,0.5,n)
		ai = np.around(ai*1000)/1000
		bi = np.around(bi*1000)/1000
		bi = Sort_abi(ai,bi)
		pr = np.random.uniform(0.5, 1.5, n)  # the prices for each source
		pr = np.around(pr,decimals =3)
		C_credit = np.random.uniform(0.4,0.6,num_assertion)
		
		S_ai = deepcopy(ai)  # save the original reliability
		S_bi = deepcopy(bi)
		s_prc = deepcopy(pr)
		# --- the following is to save the original ai and bi
		# it could be used for Link ** changes and W changes---
		ai = S_ai
		bi = S_bi
		pr = s_prc
		# --#function is to generate the Matrix graph ------
		SD_ancestor = Generate_graph(n,nk)
		print(len(SD_ancestor.keys()))
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
		
		##-------calculate the error of each heuristic method-----
		err1 = Reliability_cal_fun(S_ai,S_bi,cost,s_prc,C_credit,SD_ancestor)

		err2 = reb_cost(S_ai,S_bi,cost,s_prc,C_credit,SD_ancestor)

		err3 = cost_only(S_ai,S_bi,cost,s_prc, C_credit,SD_ancestor)

		err4 = indepent_reb(cost,ai,bi,s_prc,SD_ancestor,C_credit)

		err5 = indp_reb_cost(ai,bi,cost,s_prc,C_credit,SD_ancestor)

		err6 = indp_cost(ai,bi,cost,s_prc,C_credit,SD_ancestor)
		# print(min_err1)
		arr_err1.append(err1)
		arr_err2.append(err2)
		arr_err3.append(err3)
		arr_err4.append(err4)
		arr_err5.append(err5)
		arr_err6.append(err6)

	rst_err1.append(arr_err1)
	rst_err2.append(arr_err2)
	rst_err3.append(arr_err3)
	rst_err4.append(arr_err4)
	rst_err5.append(arr_err5)
	rst_err6.append(arr_err6)

#-------------------------------------
# ----calculat the mean values---
# ------------------------------------
Err1 = np.mean(rst_err1,axis=0)
Err2 = np.mean(rst_err2,axis=0)
Err3 = np.mean(rst_err3,axis=0)
Err4 = np.mean(rst_err4,axis=0)
Err5 = np.mean(rst_err5,axis=0)
Err6 = np.mean(rst_err6,axis=0)

fw_err = open('Num_error_rand.txt','w')
fw_err.write(str(Err1)+'\n'+str(Err2)+'\n'+str(Err3)+'\n'+str(Err4)+'\n'+str(Err5)+'\n'+str(Err6)+'\n')
fw_err.close()

print("as the number of sources changes:")
print(Err1)
print(Err2)
print(Err3)
print(Err4)
print(Err5)
print(Err6)












