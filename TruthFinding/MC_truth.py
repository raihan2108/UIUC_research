'''
Huajie Shao @06/30/2016 new
Function: TruthFinding paper based EM algorithm for Man claro
'''
import numpy as np
import random

# ------generate the graph-------
# ------Fun: different graph--------
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
	for j in range(N):
		G_row = Graph[j,:]  # get the rows
		G_col = Graph[:,j]
		for i in range(N):
			if G_row[i]==1:		# get the column denote the ancestor
				SD_ancestor.setdefault(j, []).append(i)	 	# get the list of ancestors
			if G_col[i]==1:
				SD_successor.setdefault(j, []).append(i)	# get the list of successors

	return SD_successor,SD_ancestor


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
					if k2 in SD_successor:
						child3 = SD_successor[k2]
						for k3 in child3:
							dep_ids.append(k3)
							if k3 in SD_successor:
								child4 = SD_successor[k3]
								for k4 in child4:
									dep_ids.append(k4)
	print(dep_ids)
	return dep_ids



def Generate_SC(N,NumV,SD_successor,pct):   #sources'claims
	SC = np.zeros([NumV,N])	#assertion and number of variables
	Cn = np.random.randint(-1, 0, NumV*0.3)
	C0 = np.random.randint(0, 1, NumV*0.2)
	C1 = np.random.randint(1, 2, NumV*0.5)
	C = np.hstack((C1,Cn,C0))
	random.shuffle(C)
	# generate the claims of each observation
	for j in range(NumV):
		if C[j] > 0:
			t = np.random.uniform(0.5,0.9)
			numt = int(N*t)   # number of SC = 1
			SC1 = np.random.randint(1, 2, numt)	    # sc = 1
			SC0 = np.random.randint(0, 1, N-numt)   # sc = 0 
			SC01 = np.concatenate((SC0,SC1))
			random.shuffle(SC01)
			SC[j,:] = SC01
		elif C[j] == 0:
			# generate the false assertion and let SC=1
			tn =  np.random.uniform(0.2,0.6)
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
		first_user = np.random.randint(0,15)
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
	for i in range(NumV):
		if i in Cn1:
			ids = st_fst_id[t]
			qi[i,ids] = ai[ids]
			t += 1
		else:
			Sclaim = SC[i,:]
			for k in range(N):
				if Sclaim[k] == 1:
					qi[i,k] = ai[k]
					break
	# print(qi)
	return qi

#----------------EM-social algorithm IPSN2014-----
def Fun_EM_Social(NumV,Ind_Source,Dep_Source,SC,Parameter):
	ai,bi,fi,gi = Parameter[0],Parameter[1],Parameter[2],Parameter[3]
	ln = 2*len(ai) + 1
	Store_Theta = np.zeros(ln)  # Get the length of the variables
	Z1 = np.zeros(NumV)
	Z0  = np.zeros(NumV)
	# Zn1 = np.zeros(NumV)
	d1 = 0.5
	d0 = 0.5
	ik = 0
	deta = 1
	while deta>0.0000001:
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
			Z1[j] = PZ1*d1/(PZ1*d1 + PZ0*d0)  # calculate the Zj for all the independent sources SC=1
			if Z1[j] <0.000001:
				Z1[j] = 0.0001
			if Z1[j] >0.999:
				Z1[j] = 0.999
			Z0[j] = PZ0*d0/(PZ1*d1 + PZ0*d0)
			if Z0[j]<0.000001:
				Z0[j] = 0.0001
			if Z0[j] >0.999:
				Z0[j] = 0.999

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
		d1 = np.sum(Z1)/NumV  # when Zj=1
		d0 = 1 - d1 			# when Zj=0
		# below the list of all the variables
		Theta = np.hstack((Lai,Lbi,Lfi,Lgi,d1))
		Theta = np.array(Theta)
		deta = 	np.absolute(Theta - Store_Theta)  # get the abs
		deta = sum(deta/len(Theta))  # calculate the average error
		Store_Theta =Theta
		print("----it is running---")
		if ik>=50:
			break
			print("it is terminated by k=50")

	return Z1


#-----below is the new algorithms for opinion
def New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id):
	ai,bi,fi,gi = Parameter[0],Parameter[1],Parameter[2],Parameter[3]
	Store_Theta = np.zeros(var_len)  # Get the length of the variables
	Z1 = np.zeros(NumV)
	Z0  = np.zeros(NumV)
	Zn1 = np.zeros(NumV)
	d1, d0, dn1 = 0.5, 0.1, 0.4
	ik = 0
	deta = 1
	while deta>np.exp(-20):
		ik += 1
		for j in range(NumV):
			SCJ = SC[j,:]
			PZ1 = 1		# SC=1 and D=0 independent
			PZ0=1
			PZn1 = 1
			for i in range(N):
				if i in Dep_Source:
					D = 1
				else:
					D = 0
				if SCJ[i] ==1 and D == 0:
					PZ1 = PZ1*ai[i]
					PZ0= PZ0*bi[i]
					PZn1 = PZn1*qi[j,i]		# find the first source to make the claims
				elif SCJ[i] ==0 and D == 0:
					PZ1= PZ1*(1-ai[i])
					PZ0 = PZ0*(1-bi[i])
					PZn1= PZn1*(1-qi[j,i])
				elif SCJ[i] ==1 and D == 1:
					PZ1 = PZ1*fi[i]
					PZ0 = PZ0*gi[i]
					PZn1 = PZn1*hi[i]
				elif SCJ[i] ==0 and D == 1:
					PZ1 = PZ1*(1-fi[i])
					PZ0 = PZ0*(1-gi[i])
					PZn1 = PZn1*(1-hi[i])
				else:
					print("there is an error")
			# print((PZ1*d1 + PZ0*d0+ PZn1*dn1))
			# print(PZn1,PZ1,PZ0)
			Z1[j] = PZ1*d1/(PZ1*d1 + PZ0*d0 + PZn1*dn1)  # calculate the Zj for all the independent sources SC=1
			if Z1[j] <0.000001:
				Z1[j] = 0.001
			if Z1[j] >0.999:
				Z1[j] = 0.999
			Z0[j] = PZ0*d0/(PZ1*d1 + PZ0*d0 + PZn1*dn1)
			if Z0[j]<0.000001:
				Z0[j] = 0.001
			if Z0[j] >0.999:
				Z0[j] = 0.999
			Zn1[j] = PZn1*dn1/(PZ1*d1 + PZ0*d0 + PZn1*dn1)
			if Zn1[j]<0.000001:
				Zn1[j] = 0.001
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
		qi = Get_qi(SC,NumV,N,Cn1,st_fst_id,ai)
		d1 = np.sum(Z1)/NumV  # when Zj=1
		d0 = np.sum(Z0)/NumV  # when Zj=0
		dn1= 1-d1-d0
		# below the list of all the variables
		Theta = np.hstack((Lai,Lbi,Lfi,Lgi,Lhi,d1,d0))
		Theta = np.array(Theta)
		deta = 	np.absolute(Theta - Store_Theta)  # get the abs
		deta = sum(deta/len(Theta))  # calculate the average error
		Store_Theta =Theta
		print("----it is running---")
		if ik>=50:
			break
			print("it is terminated by k")

	return Z1, Z0, Zn1


#-------below is the main function------
# --------Main Function-------------
accuray_EM =[]
accuray_vote=[]
itera = 1
for N in range(120, 130, 10):
	rpt_EM = []
	rpt_vote = []
	for mt in range(itera):  # the number of iteration
		NumV = 60 	# number of variables
		link = int(N*1)
		pct = 0.7
		ratio = 0.5  #dependent ratio
		ai = np.random.uniform(0.3,0.9,N)
		bi = np.random.uniform(0.1,0.5,N)
		ai = np.round(ai*100)/100
		bi = np.round(bi*100)/100
		sfi = np.random.uniform(0.3,0.8,N)
		sgi = np.random.uniform(0.1,0.5,N)
		fi = np.round(sfi*100)/100
		gi = np.round(sgi*100)/100

		# we need to get the independent sources
		SD_successor,SD_ancestor = Get_graph(N, ratio)
		Ind_Source =[]
		Dep_Source =[]
		for i in range(N):
			if i in SD_ancestor.keys():		# child: [list of parents]
				Dep_Source.append(i)
			else:
				Ind_Source.append(i)	# get the independent sources

		parent_len = len(Ind_Source)
		child_len = len(Dep_Source)
		# we get the claims of sources
		SC,C,st_fst_id,Cn1 = Generate_SC(N,NumV,SD_successor,pct)
		# get the first source of their reliability
		# ---we need to find the first users of each events
		
		qi = Get_qi(SC,NumV,N,Cn1,st_fst_id,ai)
		hi = np.random.uniform(0.5,0.9,N)
		Parameter = np.vstack((ai,bi,fi,gi))  # parameters for EM algorithm
		# --------Function:EM algorithm-------
		# -------EM algorithm-----------
		var_len = 2*parent_len + 3*child_len + 2
		Z1, Z0, Zn1 = New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id) #new EM algorithms
		EM_z1 = Fun_EM_Social(NumV,Ind_Source,Dep_Source,SC,Parameter)
		print(EM_z1)
		# ------statistic for true or false report---
		Z_rst = np.zeros(NumV)-1
		Vote = np.zeros(NumV)
		##---!!!notice, how to know the opinion?!!!-----
		for j in range(NumV):
			if Z1[j]>=0.5:
				Z_rst[j] = 1
			elif Z1[j]<0.5 and Z0[j] >= 0.5:
				Z_rst[j] = 0


		print("-----Z0 below is the prob of Z0----")
		print(Z0)
		print(C)
		# print("-----Z1 below is the prob of Z1----")
		print(Z1)
		# print("-----below is the prob of opinion----")
		# print(Zn1)
		for k in range(NumV):
			if np.sum(SC[k,:])>N/2:
				Vote[k] = 1
			elif np.sum(SC[k,:])<=N/2 and np.sum(SC[k,:])>10:
				Vote[k] = 0
			else:
				Vote[k] = -1

		ML_num = 0
		vote_num =0
		for j in range(NumV):
			if Z_rst[j] == C[j]:
				ML_num += 1
			if Vote[j] == C[j]:
				vote_num += 1
		rpt_EM.append(ML_num/NumV)
		rpt_vote.append(vote_num/NumV)

	mean_vote = np.mean(rpt_vote)
	mean_EM = np.mean(rpt_EM)
	accuray_vote.append(mean_vote)
	accuray_EM.append(mean_EM)

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


