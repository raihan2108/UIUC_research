'''
Huajie Shao@2016/7/19
Functions: Evaluation based on Twitter data
Source selection problem in social networks and
expected error by changing the [N of sources]
'''

'''
Instructions:
[1] author_cluster.txt  lists the source to assertion relations, i.e. source_id, assertion_id
[2] ai_rst and bi_rst represent the reliability of sources
[3] social.rt.txt is the file that lists source relations
[4] cluster_cred_temp.txt lists the assertion credibilities
'''

import numpy as np
from math import factorial
from copy import deepcopy
# import math
# import random


# cost = 60
M = 2


#----define the huristic alg based on the reliability
# to choose the sources
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
	for pro_asst in C_credit:
		Sum = 0
		for n1 in range(L1+1):
			for n2 in range(L2+1):
				for n3 in range(L3+1):
					for n4 in range(L4+1):
						for n5 in range(L5+1):
							for n6 in range(L6+1):
								PCt =pro_asst*ST_all[0][n1]*ST_all[1][n2]*ST_all[2][n3]*ST_all[3][n4]*ST_all[4][n5]*ST_all[5][n6]
								PCf =(1-pro_asst)*SF_all[0][n1]*SF_all[1][n2]*SF_all[2][n3]*SF_all[3][n4]*SF_all[4][n5]*SF_all[5][n6]
								PErr = min(PCt,PCf)
								Sum += PErr

		Err += Sum

	return Err

# define the random function
def rand_fun(N,RA,RB,cost,prc,C_credit):
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

	for ids in Num:
		Rai.append(RA[ids])
		Rbi.append(RB[ids])

	rand_err = fun_window6(Rai,Rbi,C_credit)
	return rand_err


# define function: cost-only

def cost_only(Ra,Rb,Fee,cost,C_credit):
	Psum = 0
	N = len(Fee)
	nums = []
	for j in range(N):
		if Psum <= cost:
			Psum += Fee[j]
			nums.append(j)
		else:
			break

	Rai = []
	Rbi = []
	for ids in nums:
		Rai.append(Ra[ids])
		Rbi.append(Rb[ids])

	cost_err = fun_window6(Rai,Rbi,C_credit)
	return cost_err

# #the below is the crowdbudget algorithm---

def crowdbudget(prc,cost,R_ai,R_bi,C_credit):
	u1=np.mean(R_ai)
	u2=np.mean(R_bi)
	dm1=abs(u1-0.7)
	dm2=abs(u2-0.3)
	nm=np.mean(prc)
	N=round(cost/nm+1)
	crowd_err = 0
	# print(dm1,dm2)
	for pro_asst in C_credit:
		err=pro_asst*np.exp(-2*N*dm1**2)+(1-pro_asst)*np.exp(-2*N*dm2**2)
		crowd_err += err
	return crowd_err

def Generate_graph():
	SD_ancestor = dict()
	SD_successor = dict()
	file_graph = open('social.rt.txt', 'r')
	for rt in file_graph.readlines():
		rtn = rt.strip().split(',')
		SD_ancestor[rtn[0]] = rtn[1]

	file_graph.close()
	# print(SD_ancestor)
	return SD_ancestor

def Get_reb_abi():
	f_ai = open('ai_rst.txt','r')
	f_bi = open('bi_rst.txt','r')
	Ra = []
	Rb = []
	for ai in f_ai.readlines():
		rai = ai.split()
		int_ai = float(rai[0])
		Ra.append(int_ai)
	for bi in f_bi.readlines():
		rbi = bi.split()
		int_bi = float(rbi[0])
		Rb.append(int_bi)

	return Ra,Rb

def Pro_assertion():
	C_credit =[]
	credit_dict = dict()
	f_assertion = open('c_cred.txt','r')
	for credit in f_assertion.readlines():
		cdt = credit.split()
		cdt1 = float(cdt[1])
		C_credit.append(cdt1)
		cdt2 = float(cdt[0])
		credit_dict[cdt2] = cdt[1]

	return C_credit


#-----below is the main function to compare with the baselines
rst_err1 = []
rst_err2 = []
rst_err3 = []
rst_err4 = []
file_wt_ids = open("org_id.txt",'w')
for mt in range(0,M):
	print("running time is", mt)
	arr_err1 = []
	arr_err2 = []
	arr_err3 = []
	arr_err4 = []
	list_ids = []
	for cost in range(50,60,10):
		# flag = 1
		ai, bi = Get_reb_abi()		# get the ai and bi
		ai = np.array(ai)
		bi = np.array(bi)
		C_credit = Pro_assertion()
		C_credit = np.array(C_credit)
		n = len(ai)
		pr = np.random.uniform(0.5, 2, n)  # generate the prices for source
		pr = np.around(pr,decimals=3)
		# ---below fun: store the [ai, id]
		dict_ai = dict()
		dict_bi = dict()
		dict_pr = dict()
		for i in range(n):
			# dict_ai[ai[i]] = i
			# dict_bi[i] = bi[i]  	# store [id: bi]
			dict_pr[pr[i]] = i
		
		#----below fun: sort the reliability of sources
		Hurist_rab = 1 + ai - bi+np.random.randn(n)*0.001 #if ai and bi are the same, it is hard to find
		# print(Hurist_rab)
		rab_dict = dict()
		for i in range(n):
			h_rab = Hurist_rab[i]
			rab_dict[h_rab] = i

		Rab = np.sort(Hurist_rab)         # get the most reliable sources
		Rab = sorted(Rab, reverse=True)   # get the descending order

		# -------sort the reliability based on the hurisctic rab-----
		# then we get the highest reb to lowest in order
		new_Ra = np.zeros(n)
		new_Rb = np.zeros(n)
		new_price = np.zeros(n)
		ids_dict = dict()
		for j in range(n):
			abi = Rab[j]
			ids = rab_dict[abi]
			new_price[j] = pr[ids]
			new_Ra[j] = ai[ids]
			new_Rb[j] = bi[ids]
			ids_dict[j] = ids
		# print("the newprice",new_price)
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
		st_num=[]
		# print("nm is the number of",nm)
		#------------------------------------------------
		#  Here begin to calculate the error of our method
		#  -----------------------------------------------
		for k in range(2, nm):
			st_num = Hfun_reb(cost, new_price, k, n)
			Ran = []
			Rbn = []
			ppr = []
			if len(st_num) > 0:
				for j in range(len(st_num)):
					ids = st_num[j]
					Ran.append(new_Ra[ids])
					Rbn.append(new_Rb[ids])
					ppr.append(new_price[ids])

				# print(st_num)
				err1 = fun_window6(Ran,Rbn,C_credit)
				if err1 < min_err1:
					min_err1 = err1
					crowd_price = ppr
					crowd_ai = Ran
					crowd_bi = Rbn
					store_ids = deepcopy(st_num)

		# print("the final",crowd_price)
		org_id = []
		for snum in store_ids:
			myid = ids_dict[snum]
			org_id.append(myid)

		# errors for the baselines
		err2 = rand_fun(n,new_Ra,new_Rb,cost,new_price,C_credit)   #same as the RA,RB in the Matlab codes
		err3 = cost_only(Ra_prc,Rb_prc,ct,cost,C_credit)
		# print(len(crowd_ai))
		err4 = crowdbudget(crowd_price,cost,crowd_ai, crowd_bi,C_credit)

		arr_err1.append(min_err1)
		arr_err2.append(err2)
		arr_err3.append(err3)
		arr_err4.append(err4)
		list_ids.append(org_id)

	rst_err1.append(arr_err1)
	rst_err2.append(arr_err2)
	rst_err3.append(arr_err3)
	rst_err4.append(arr_err4)
	file_wt_ids.write(str(list_ids)+'\n')




file_wt_ids.close()
#-------------------------------------
# ----calculat the mean values---
# ------------------------------------

Err1 = np.mean(rst_err1,axis=0)
Err2 = np.mean(rst_err2,axis=0)
Err3 = np.mean(rst_err3,axis=0)
Err4 = np.mean(rst_err4,axis=0)
print(Err1)
print(Err2)
print(Err3)
print(Err4)












