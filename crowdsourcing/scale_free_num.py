'''
Huajie Shao@2016/7/14
Functions: Source selection problem in social networks and
we calculate the expected error by changing the N of sources
'''

import numpy as np
from math import factorial 
import math
# import random
# from subfun_test import test   this could import the function


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
def fun_window6(Rai,Rbi):
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
	# print("the L is",L)
	# mc = [mc1,mc2,mc3,mc4,mc5,mc6]
	# mb = [mb1,mb2,mb3,mb4,mb5,mb6]
	# ST1,ST2,ST3,ST4,ST5,ST6 = [],[],[],[],[],[]
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
	for n1 in range(L1+1):
		for n2 in range(L2+1):
			for n3 in range(L3+1):
				for n4 in range(L4+1):
					for n5 in range(L5+1):
						for n6 in range(L6+1):
							PCt =ST_all[0][n1]*ST_all[1][n2]*ST_all[2][n3]*ST_all[3][n4]*ST_all[4][n5]*ST_all[5][n6]
							PCf =SF_all[0][n1]*SF_all[1][n2]*SF_all[2][n3]*SF_all[3][n4]*SF_all[4][n5]*SF_all[5][n6]
							PErr = min(PCt,PCf)
							Sum += PErr

	Err = 0.5*Sum
	return Err

# define the random function
def rand_fun(N,RA,RB,cost,prc):
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

	rand_err = fun_window6(Rai,Rbi)
	return rand_err


# define function: cost-only

def cost_only(Ra,Rb,Fee,cost):
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

	cost_err = fun_window6(Rai,Rbi)
	return cost_err

# #the below is the crowdbudget algorithm---

def crowdbudget(prc,cost,R_ai,R_bi):
	u1=np.mean(R_ai)
	u2=np.mean(R_bi)
	dm1=abs(u1-0.5)
	dm2=abs(0.5-u2)
	mc=np.mean(prc)
	N=round(cost/mc+1)
	crowd_err=0.5*exp(-2*N*dm2**2)+0.5*exp(-2*N*dm2**2)
	return crowd_err


#-----below is the main function to compare with the baselines
nk = 2
w = 0.8
cost = 50
M= 15	# Ma Carlo
rst_err1 = []
rst_err2 = []
rst_err3 = []
rst_err4 = []
for mt in range(0,M):
	# kw = 1
	print("the running is", mt)
	arr_err1 = []
	arr_err2 = []
	arr_err3 = []
	arr_err4 = []
	for n in range(40,70,5):
		flag = 0
		# Sji = np.empty(n)
		ai = np.random.uniform(0.4,0.9,n)
		bi = np.random.uniform(0.1,0.5,n)
		ai = np.around(ai*1000)/1000
		bi = np.around(bi*1000)/1000
		s_prc = np.random.uniform(1, 5, n)  # the prices for each source

		# ---below fun: store the [ai, id]
		dict_ai = dict()
		dict_bi = dict()
		dict_pr = dict()
		for i in range(n):
			dict_ai[ai[i]] = i
			dict_bi[i] = bi[i]  	# store [id: bi]
			dict_pr[s_prc[i]] = i
		S_ai = ai  # save the original reliability
		S_bi = bi
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
		# ---the following is to generate the graph and its Matrix---
		Amtx = np.zeros([n,n])
		# print(Amtx[0:2,:])
		links = nk*n
		while flag==1:
			if np.sum(Amtx[0:3]) < np.around(links*0.75):
				i = np.random.randint(0,3)
				j = np.random.randint(i+1, n)
			else:
				i = np.random.randint(0,n-1)
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
			ai = Pa
			bi = Pb

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
		# print("the nm is the",nm)
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

				# print(Ran, Rbn)
				err1 = fun_window6(Ran,Rbn)
				if err1 < min_err1:
					min_err1 = err1
					crowd_price = ppr
					crowd_ai = Ran
					crowd_bi = Rbn

		# errors for the baselines
		err2 = rand_fun(n,new_Ra,new_Rb,cost,new_price)   #same as the RA,RB in the Matlab codes
		err3 = cost_only(Ra_prc,Rb_prc,ct,cost)
		# err4 = crowdbudget(crowd_price,cost,crowd_ai, crowd_bi)

		arr_err1.append(err1)
		# arr_err2.append(err2)
		# arr_err3.append(err3)
		# arr_err4.append(err4)

	rst_err1.append(arr_err1)
	# rst_err2.append(arr_err2)
	# rst_err3.append(arr_err3)
	# rst_err4.append(arr_err4)

#---------------------------------
# calculat the mean values
# --------------------------------
rst1 = np.asarray(rst_err1)
# rst2 = np.asarray(rst_err2)
# rst3 = np.asarray(rst_err3)
# rst4 = np.asarray(rst_err4)
# 

Err1 = np.mean(rst1,axis=0)
print(Err1)












