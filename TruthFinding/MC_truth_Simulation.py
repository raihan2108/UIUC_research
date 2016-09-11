'''
Huajie Shao @06/30/2016 new
Function: TruthFinding paper based EM algorithm for Man claro
It is a simulation program
'''
import numpy as np
import random
import math
import sys

# ------generate the graph-------
# ------Fun: different graph--------
r0 = 0.1
rn1 = 0.4
r1 = 0.5
itera = 50
def Get_graph(N,ratio):
	nr = int(N*0.2)
	Graph = np.zeros([N,N])
	for i in range(1,nr):  	# dependent sources
		j = np.random.randint(0, i)
		Graph[i][j] = 1		# column is the ancestor

	for i in range(nr+1,2*nr):  	# dependent sources
		j = np.random.randint(0, i)
		Graph[i][j] = 1		

	SD_ancestor = dict()   	# source graph dictionary	
	SD_successor = dict()
	Parents = []
	Children =[]
	for j in range(N):
		G_row = Graph[j,:]  # get the rows
		G_col = Graph[:,j]
		for i in range(N):
			if G_row[i]==1:		# get the column denote the ancestor
				SD_ancestor.setdefault(j, []).append(i)	 	# get the list of ancestors
				Parents.append(i)
			if G_col[i]==1:
				SD_successor.setdefault(j, []).append(i)	# get the list of successors
				Children.append(i)

	return SD_successor,SD_ancestor,Parents,Children


def Fun_get_opinions(first_user, SD_successor):
	fst_id = first_user
	dep_ids = []   # list of the dependent sources
	if fst_id in SD_successor.keys():
		child1= SD_successor[fst_id]
		dep_ids.append(fst_id)
		for k1 in child1:
			dep_ids.append(k1)
			if k1 in SD_successor.keys():
				child2 = SD_successor[k1]
				for k2 in child2:
					dep_ids.append(k2)
					if k2 in SD_successor.keys():
						child3 = SD_successor[k2]
						for k3 in child3:
							dep_ids.append(k3)
							if k3 in SD_successor.keys():
								child4 = SD_successor[k3]
								for k4 in child4:
									dep_ids.append(k4)
									# if k4 in SD_successor.keys():
									# 	child5 = SD_successor[k4]
									# 	for k5 in child5:
									# 		dep_ids.append(k5)

	# print(dep_ids):
	return dep_ids



def Generate_SC(N,NumV,SD_successor,pct):   #sources'claims
	SC = np.zeros([NumV,N])	#assertion and number of variables
	Cn = np.random.randint(-1, 0, NumV*rn1)
	C0 = np.random.randint(0, 1, NumV*r0)
	C1 = np.random.randint(1, 2, NumV*r1)
	C = np.hstack((C1,Cn,C0))
	random.shuffle(C)
	Nuser = 15
	# generate the claims of each observation
	for j in range(NumV):
		if C[j] > 0:
			t = np.random.uniform(0.4,0.9)
			numt = int(N*t)   # number of SC = 1
			SC1 = np.random.randint(1, 2, numt)	    # sc = 1
			SC0 = np.random.randint(0, 1, N-numt)   # sc = 0 
			SC01 = np.concatenate((SC0,SC1))
			random.shuffle(SC01)
			SC[j,:] = SC01
		elif C[j] == 0:
			# generate the false assertion and let SC=1
			tn =  np.random.uniform(0.1,0.7)
			nt = int(N*tn)
			SC3 = np.random.randint(1, 2, nt)
			SC4 = np.random.randint(0, 1, N-nt)
			SC34 = np.concatenate((SC4,SC3))
			random.shuffle(SC34)
			SC[j,:] = SC34

	Cn1 =[]   # store the negative one
	st_fst_id = []
	for i in range(NumV):
		if C[i] == -1:
			Cn1.append(i)

	for i in Cn1:
		SC[i,:] = 0
		first_user = np.random.randint(0,Nuser)
		SC[i,first_user] = 1
		st_fst_id.append(first_user)   #store the first author
		dep_ids = Fun_get_opinions(first_user, SD_successor)
		# print(dep_ids)
		for j in dep_ids:
			SC[i,j] = 1

		Noise = np.random.randint(0,N,1)
		for t in Noise:
			SC[i,t] = 1

	return SC, C, st_fst_id,Cn1


def Get_qi(SC,NumV,N,Cn1,st_fst_id,ai):
	qi = np.zeros([NumV,N])+0.01
	t = 0
	all_fst_ids=[]  #for all the claims and assertions
	for i in range(NumV):
		if i in Cn1:
			ids = st_fst_id[t]
			qi[i,ids] = ai[ids]
			all_fst_ids.append(ids)
			t = t+1
		else:
			Sclaim = SC[i,:]
			for k in range(N):
				if Sclaim[k] == 1:
					qi[i,k] = ai[k]
					break
			all_fst_ids.append(k)

	return qi, all_fst_ids

#----------------EM-social algorithm IPSN2014-----
def Fun_EM_Social(NumV,Ind_Source,Dep_Source,SC,Parameter):
	ai,bi,fi,gi = Parameter[0],Parameter[1],Parameter[2],Parameter[3]
	ln = 2*len(ai) + 1
	Store_Theta = np.zeros(ln)  # Get the length of the variables
	Z1 = np.zeros(NumV)
	Z0  = np.zeros(NumV)
	# Zn1 = np.zeros(NumV)
	dc1 = 0.5
	dc0 = 0.5
	ik = 0
	deta = 1
	while deta>math.pow(10,-8):
		ik += 1
		for j in range(NumV):
			SCJ = SC[j,:]
			PZ1 = 1		# SC=1 and D=0 independent
			PZ0 = 1
			for i in range(N):
				if i in Dep_Source:
					D = 1
				else:
					D = 0
				if SCJ[i] ==1 and D == 0:
					PZ1 = PZ1*ai[i]
					PZ0= PZ0*bi[i]
				elif SCJ[i] ==0 and D == 0:
					PZ1= PZ1*(1-ai[i])
					PZ0 = PZ0*(1-bi[i])
				elif SCJ[i] ==1 and D == 1:
					PZ1 = PZ1*fi[i]
					PZ0 = PZ0*gi[i]
				elif SCJ[i] ==0 and D == 1:
					PZ1 = PZ1*(1-fi[i])
					PZ0 = PZ0*(1-gi[i])
				else:
					print("there is an error")
			# print((PZ1*d1 + PZ0*d0+ PZn1*dn1))
			# print(PZ1,PZ0)
			Z1[j] = PZ1*dc1/(PZ1*dc1 + PZ0*dc0)  # calculate the Zj for all the independent sources SC=1
			if Z1[j] <0.000001:
				Z1[j] = 0.0001
			if Z1[j] >0.999:
				Z1[j] = 0.999
			Z0[j] = 1-Z1[j]
			# if Z0[j]<0.000001:
			# 	Z0[j] = 0.0001
			# if Z0[j] >0.999:
			# 	Z0[j] = 0.999

		Z1_SC1_D0 = 0
		Z0_SC1_D0 = 0
		Z1_SC0_D0 = 0
		Z0_SC0_D0 = 0
		Z1_SC1_D1 = 0
		Z0_SC1_D1 = 0
		Z1_SC0_D1 = 0
		Z0_SC0_D1 = 0
		Lai = []
		Lbi = []
		Lfi = []
		Lgi = []

		for i in Ind_Source:	# independent sources
			for j in range(NumV):
				if SC[j,i] == 1:
					Z1_SC1_D0 += Z1[j]
					Z0_SC1_D0 += Z0[j]
				else:
					Z1_SC0_D0 += Z1[j]
					Z0_SC0_D0 += Z0[j]

			ai[i] = Z1_SC1_D0/(Z1_SC1_D0 + Z1_SC0_D0)
			bi[i] = Z0_SC1_D0/(Z0_SC1_D0 + Z0_SC0_D0)

			Lai.append(ai[i])
			Lbi.append(bi[i])
			# Q[i] = qi[i]
		for i in Dep_Source:	#dependent sources
			for j in range(NumV):
				if SC[j,i] == 1:
					Z1_SC1_D1 += Z1[j]
					Z0_SC1_D1 += Z0[j]
				else:
					Z1_SC0_D1 += Z1[j]
					Z0_SC0_D1 += Z0[j]

			fi[i] = Z1_SC1_D1/(Z1_SC1_D1+Z1_SC0_D1)
			gi[i] = Z0_SC1_D1/(Z0_SC1_D1+Z0_SC0_D1)
			Lfi.append(fi[i])
			Lgi.append(gi[i])
		# print(ai)
		dc1 = np.sum(Z1)/NumV  # when Zj=1
		dc0 = 1 - dc1 			# when Zj=0
		# below the list of all the variables
		Theta=np.zeros(ln)
		Theta = np.hstack((Lai,Lbi,Lfi,Lgi,dc1))
		Theta = np.array(Theta)
		deta = 	np.absolute(Theta - Store_Theta)  # get the abs
		deta = sum(deta/len(Theta))  # calculate the average error
		Store_Theta =Theta
		print("----it is running---")
		if ik>=50:
			print("it is terminated by k=50")
			break

	return Z1


#-----below is the new algorithms for opinion
def New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id,all_fst_ids):
	ai,bi,fi,gi = Parameter[0],Parameter[1],Parameter[2],Parameter[3]
	Store_Theta = np.zeros(var_len)  # Get the length of the variables
	Z1 = np.zeros(NumV)
	Z0  = np.zeros(NumV)
	Zn1 = np.zeros(NumV)
	d1, d0, dn1 = r1, r0, rn1
	ik = 0
	deta = 1
	# print(Dep_Source)
	while deta>math.pow(10,-8):
		ik += 1
		for j in range(NumV):
			SCJ = SC[j,:]
			PZ1 = 1		# SC=1 and D=0 independent
			PZ0=1
			PZn1 = 1
			eps1=0.0001
			flag=0
			for i in range(N):
				if i in Dep_Source:
					D = 1
				else:
					D = 0
				if i == all_fst_ids[j]:
					PZn1 = PZn1*qi[j,i]
					flag = 1
					# print(all_fst_ids)
					# print("the number is ",j,i)
				else:
					flag = 0

				if abs(SCJ[i] -1) < eps1 and abs(D)<eps1:
					# print("ok")
					PZ1 = PZ1*ai[i]
					PZ0 = PZ0*bi[i]
					if flag < 1:
						PZn1 = PZn1*qi[j,i]		# find the first source to make the claims
					
				elif SCJ[i] ==0 and D == 0:
					PZ1= PZ1*(1-ai[i])
					PZ0 = PZ0*(1-bi[i])
					PZn1= PZn1*(1-qi[j,i])
					# print("ok")
				elif SCJ[i] ==1 and D == 1:
					PZ1 = PZ1*fi[i]
					PZ0 = PZ0*gi[i]
					if flag<1:
						PZn1 = PZn1*hi[i]

				elif SCJ[i] == 0 and D == 1:
					PZ1 = PZ1*(1-fi[i])
					PZ0 = PZ0*(1-gi[i])
					PZn1 = PZn1*(1-hi[i])
					# print("ok")
				else:
					print("there is an error")
					
			# print(PZn1,PZ0)
			Z1[j] = PZ1*d1/(PZ1*d1 + PZ0*d0 + PZn1*dn1)  # calculate the Zj for all the independent sources SC=1
			if Z1[j] <0.000001:
				Z1[j] = 0.00001
			if Z1[j] >0.999:
				Z1[j] = 0.999
			Z0[j] = PZ0*d0/(PZ1*d1 + PZ0*d0 + PZn1*dn1)
			if Z0[j]<0.000001:
				Z0[j] = 0.00001
			if Z0[j] >0.999:
				Z0[j] = 0.999
			Zn1[j] = PZn1*dn1/(PZ1*d1 + PZ0*d0 + PZn1*dn1)
			if Zn1[j]<0.000001:
				Zn1[j] = 0.00001
			if Zn1[j] >0.999:
				Zn1[j] = 0.999

		Z1_SC1_D0 = 0
		Z0_SC1_D0 = 0
		Z1_SC0_D0 = 0
		Z0_SC0_D0 = 0
		Z1_SC1_D1 = 0
		Z0_SC1_D1 = 0
		Z1_SC0_D1 = 0
		Z0_SC0_D1 = 0
		Lai = []
		Lbi = []
		Lfi = []
		Lgi = []
		Lhi = []

		for i in Ind_Source:	# independent sources
			for j in range(NumV):
				if SC[j,i] == 1:
					Z1_SC1_D0 += Z1[j]
					Z0_SC1_D0 += Z0[j]
				else:
					Z1_SC0_D0 += Z1[j]
					Z0_SC0_D0 += Z0[j]

			ai[i] = Z1_SC1_D0/(Z1_SC1_D0+Z1_SC0_D0)
			bi[i] = Z0_SC1_D0/(Z0_SC1_D0+Z0_SC0_D0)

			Lai.append(ai[i])
			Lbi.append(bi[i])
			# Q[i] = qi[i]
		for i in Dep_Source:	#dependent sources
			for j in range(NumV):
				if SC[j,i] == 1:
					Z1_SC1_D1 += Z1[j]
					Z0_SC1_D1 += Z0[j]
				else:
					Z1_SC0_D1 += Z1[j]
					Z0_SC0_D1 += Z0[j]

			fi[i] = Z1_SC1_D1/(Z1_SC1_D1+Z1_SC0_D1)
			gi[i] = Z0_SC1_D1/(Z0_SC1_D1+Z0_SC0_D1)
			hi[i] = (1-Z1_SC1_D1-Z0_SC1_D1)/(2-Z1_SC1_D1-Z0_SC1_D1-Z1_SC0_D1-Z0_SC0_D1)
			Lfi.append(fi[i])
			Lgi.append(gi[i])
			Lhi.append(hi[i])
		# print(ai)
		qi,all_fst_ids = Get_qi(SC,NumV,N,Cn1,st_fst_id,ai)
		d1 = np.sum(Z1)/NumV  # when Zj=1
		d0 = np.sum(Z0)/NumV  # when Zj=0
		dn1= 1-d1-d0
		# below the list of all the variables
		Theta = np.zeros(var_len)
		Theta = np.hstack((Lai,Lbi,Lfi,Lgi,Lhi,d1,d0))
		Theta = np.array(Theta)
		deta = 	np.absolute(Theta - Store_Theta)  # get the abs
		deta = sum(deta/len(Theta))  # calculate the average error
		Store_Theta =Theta
		print("----it is running---")
		if ik>=50:
			break
			print("it is terminated by k")

		# print(ai)

	return Z1, Z0, Zn1

#-------below is the main function------
# ----------Main Function----------------
accuray_EM =[]
accuray_vote=[]
accuray_social=[]
for N in range(60, 150, 20):
	rpt_EM = []
	rpt_vote = []
	rpt_social =[]
	for mt in range(itera):  # the number of iteration
		NumV = 50 	# number of variables
		link = int(N*1)
		pct = 0.7
		ratio = 0.5  #dependent ratio
		ai = np.random.uniform(0.5,0.9,N)
		bi = np.random.uniform(0.2,0.6,N)
		ai = np.round(ai*100)/100
		bi = np.round(bi*100)/100
		sfi = np.random.uniform(0.5,0.8,N)
		sgi = np.random.uniform(0.2,0.6,N)
		fi = np.round(sfi*100)/100
		gi = np.round(sgi*100)/100

		# we need to get the independent sources
		SD_successor,SD_ancestor,Parents,Children = Get_graph(N, ratio)
		Ind_Source =[]
		Dep_Source =[]
		for i in range(N):
			if i in SD_ancestor.keys():		# child: [list of parents]
				Dep_Source.append(i)
			else:
				Ind_Source.append(i)	# get the independent sources

		# print(Children)
		parent_len = len(Ind_Source)
		child_len = len(Dep_Source)
		# we get the claims of sources
		SC,C,st_fst_id,Cn1 = Generate_SC(N,NumV,SD_successor,pct)
		# get the first source of their reliability
		# ---we need to find the first users of each events
		
		qi, all_fst_ids = Get_qi(SC,NumV,N,Cn1,st_fst_id,ai)
		hi = np.random.uniform(0.6,0.8,N)
		hi = np.round(hi,decimals=3)
		Parameter = np.vstack((ai,bi,fi,gi))  # parameters for EM algorithm
		# --------Function:EM algorithm-------
		# -------EM algorithm-----------
		var_len = 2*parent_len + 3*child_len + 2
		Z1, Z0, Zn1 = New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id,all_fst_ids) #new EM algorithms
		EM_z1 = Fun_EM_Social(NumV,Ind_Source,Dep_Source,SC,Parameter)
		print(EM_z1)
		EM_SC = np.zeros(NumV)
		for j in range(NumV):
			if EM_z1[j] >= 0.5:
				EM_SC[j] = 1
			else:
				EM_SC[j] = np.random.randint(-1,1)
		# ------statistic for true or false report---
		Z_rst = np.zeros(NumV)
		Vote = np.zeros(NumV)
		##---!!!notice, how to know the opinion?!!!-----
		for j in range(NumV):
			if Z1[j]>=0.5:
				Z_rst[j] = 1
			if Zn1[j] >= 0.5:
				Z_rst[j] = -1
			if Z0[j]>=0.5:
				Z_rst[j] = 0

		# print("-----Z0 below is the prob of Z0----")
		# print(Z0)
		print(C)
		# print(np.sum(SC,axis=1))  #calculate the rows
		# print("-----Z1 below is the prob of Z1----")
		# print(Z1)
		# print("-----below is the prob of opinion----")
		# print(Zn1)
		for k in range(NumV):
			if np.sum(SC[k,:])>N/2:
				Vote[k] = 1
			elif np.sum(SC[k,:])<=N/2 and np.sum(SC[k,:])>=N*0.05:
				Vote[k] = 0
			else:
				Vote[k] = -1

		ML_num = 0
		vote_num =0
		socail_num = 0
		for j in range(NumV):
			if Z_rst[j] == C[j]:
				ML_num += 1
			if Vote[j] == C[j]:
				vote_num += 1
			if EM_SC[j] == C[j]:
				socail_num += 1
		rpt_EM.append(ML_num/NumV)
		rpt_vote.append(vote_num/NumV)
		rpt_social.append(socail_num/NumV)

	mean_vote = np.mean(rpt_vote)
	mean_EM = np.mean(rpt_EM)
	mean_social = np.mean(rpt_social)
	mean_vote=np.round(mean_vote,decimals=3)
	mean_EM=np.round(mean_EM,decimals=3)
	mean_social = np.round(mean_social,decimals=3)


	accuray_vote.append(mean_vote)
	accuray_EM.append(mean_EM)
	accuray_social.append(mean_social)


	print(accuray_social,accuray_vote,accuray_EM)


# fw = open('vote_accy_N.txt', 'w')
# fw.write(str(accuray_vote))
# fw.close()

# fp = open('SC.txt', 'w')
# fp.write(str(SC))
# fp.close()
# print(accuray_vote)
# print(accuray_EM)
# for i in range(NumV):
# 	print(SC[i,:])
