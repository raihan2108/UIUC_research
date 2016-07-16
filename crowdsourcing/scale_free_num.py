'''
Huajie Shao@2016/7/14
Functions: Source selection problem in social networks and
we calculate the expected error by changing the N of sources
'''

import numpy as np
# import random
# from subfun_test import test   this could import the function

nk = 2
w = 0.8
cost = 60
M= 1 	# Ma Carlo
dict_ai = dict()
dict_bi = dict()
for mt in range(0,M):
	kw = 1
	for n in range(30,45,10):
		flag = 0
		Sji = np.empty(n)
		ai = np.random.uniform(0.4,0.9,n)
		bi = np.random.uniform(0.1,0.5,n)
		ai = np.around(ai*1000)/1000
		bi = np.around(bi*1000)/1000
		s_prc = np.random.randint(1, 5, n)  # the prices for each source

		# ---below fun: store the [ai, id]
		for i in range(n):
			dict_ai[i] = ai[i] 
			dict_bi[i] = bi[i]  	# store [id: bi]
		S_ai = ai  # save the original reliability
		S_bi = bi
		# make the ai and bi similar values
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
			if np.sum(np.sum(Amtx[0:2,:])) < np.around(links*0.75):
				i = np.random.randint(0,3)
				j = np.random.randint(i+1, n)
			else:
				i = np.random.randint(0,n)
				j = np.random.randint(i+1,n)
			ele = 1
			Amtx[i,j]=ele
			if np.sum(sum(Amtx))<=links:
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
					SD_successor.setdefault(i, []).append(j)	# get the list of children
				if G_col[j]==1:
					SD_ancestor.setdefault(j, []).append(i)	# get the list of ancestors
		for s in range(n):
			if s in SD_ancestor.keys():
				val = SD_ancestor[s]
				sum_ai_anct = 0
				sum_bi_anct = 0
				for v in val:
					sum_ai_anct += dict_ai[v]
					sum_bi_anct += dict_bi[v]

				length = len(val)
				Pa[s] = (1-w)/length*sum_ai_anct + w*ai[s]
				Pb[s] = (1-w)/length*sum_bi_anct + w*bi[s]
			ai = Pa
			bi = Pb

		#----below fun: sort the reliability of sources
		Hurist_rab = 1 + ai - bi
		rab_dict = dict()
		for i in range(n):
			h_rab = Hurist_rab[i]
			rab_dict[h_rab] = i

		Rab = np.sort(Hurist_rab)  # get the most reliable sources
		Rab = [: : -1]
		for ab in Rab:
			ids = rab_dict[ab]


		price = np.sort(pr)  # sort prices for smallest to highest






