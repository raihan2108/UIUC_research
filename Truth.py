'''
Huajie Shao @06/21/2016
Function: TruthFinding paper based EM algorithm
'''
import numpy as np
# from random import random


N = 70
NumV = 50 	# number of variables
flg = 1
link = N*3
SD_ancestor = dict()   	# source graph dictionary	
SD_successor = dict()
Cn = np.random.randint(-1, 0, NumV*0.1)
C0 = np.random.randint(0, 1, NumV*0.2)
C1 = np.random.randint(1, 2, NumV*0.7)		# the claims of sources
C2 = np.concatenate((C1, C0), axis=0)
C =  np.concatenate((C2, Cn), axis=0)   	# assertion
Cn1 =[]   # store the negative one
for i in range(NumV):
	if C[i] == -1:
		Cn1.append(i)

# print(Cn1,C)
ai = np.random.uniform(0.1,0.9,N)
bi = np.random.uniform(0.1,0.6,N)
d1, d0, dn1 = 0.7, 0.2, 0.1
Graph = np.zeros([N,N])

# ------------------------------------
# this function is to generate the graph
# ------------------------------------
while flg==1:
	i = np.random.randint(0,N-2)
	j = np.random.randint(i+1, N)
	ele = 1
	Graph[j][i] = ele		# column is the ancestor
	if np.sum(sum(Graph))<link:
		flg = 1
	else:
		flg = 0

# establish the dict to find the dependency graph
# print(Graph)
for j in range(N):
	G_row = Graph[j,:]  # get the rows
	G_col = Graph[:,j]
	for i in range(N):
		if G_row[i]==1:		# get the column denote the ancestor
			SD_ancestor.setdefault(j, []).append(i)	 	# get the list of ancestors
		if G_col[i]==1:
			SD_successor.setdefault(i, []).append(j)	# get the list of successors

# print(SD_ancestor)
# calculate the results
SC = np.zeros([NumV,N])

# generate the claims of each observation
for j in range(NumV):
	SC1 = np.random.randint(0, 2, N)
	SC2 = np.random.randint(0, 2, N)
	SC3 = np.random.randint(0, 2, N)
	if j >=NumV*0.55 and j<=NumV*0.9:
		SC[j,:] = SC1
	else:
		SC[j,:] = SC2|SC3

nm = 3
follower_id=np.empty([0, 2])   #define the empty array
for i in Cn1:
	User = np.random.randint(0,N,nm)
	SC[i,:] = 0
	for id in User:
		SC[i,id] = 1

print(SC)

# -----Calculate the ratio of dependent sources---
ratio = dict()
for key, val in SD_ancestor.items():
	child = key
	parent = val
	num_same = 0.0
	num_par = 0.0
	for k in parent:
		Sg = SC[:,child]
		Sp = SC[:,k]
		num_bit = Sg.astype(int) & Sp.astype(int)  #convert to int for matrix
		num_same = np.sum(num_bit) + num_same
		num_par = np.sum(Sp) + num_par

	ratio[key] = num_same/num_par	# the ratio is right

# we need to get the independent sources
Ind_Source =[]
Dep_Source =[]
for i in range(N):
	if i in SD_ancestor.keys():		# child: [list of parents]
		Dep_Source.append(i)
	else:
		Ind_Source.append(i)	# get the independent sources

parent_len = len(Ind_Source)
child_len = len(Dep_Source)

# print(ratio)
fi = np.random.uniform(0.2,0.7,N)
gi = np.random.uniform(0.2,0.4,N)

# get the first source of their reliability
# ---we need to find the first users of each events
qi = np.zeros([NumV,N])
for k in range(NumV): # each event has a first user
	qi[k,:] = np.random.uniform(0.1,0.2,N)
	SC_k = SC[k,:]
	for i in range(N):
		if SC_k[i] == 1:
			fst_id = i
			break
	qi[k,fst_id] = ai[fst_id]

hi = np.random.uniform(0.1,0.4,N)


deta = 0.1
var_len = 2*parent_len + 3*child_len + 2
Store_Theta = np.zeros(var_len)  # Get the length of the variables
Z1 = np.zeros(NumV)
Z0  = np.zeros(NumV)
Zn1 = np.zeros(NumV)
while deta>0.005:
	for j in range(NumV):
		SCJ = SC[j,:]
		PZ1 = 1	#SC=1 and D=0 independent
		PZ0=1
		PZn1 = 1
		for i in range(N):
			if i in ratio.keys():
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
				Pt = SD_ancestor[i]
				for val in Pt:
					if SCJ[val] ==1:
						fi[i] = ratio[i]*ai[val] + (1-ratio[i])*fi[i]
						gi[i] = ratio[i]*bi[val] + (1-ratio[i])*gi[i]
						# fi[i] = ratio[i]*ai[val] 
						# gi[i] = ratio[i]*bi[val]
						break
				PZ1 = PZ1*fi[i]
				PZ0 = PZ0*gi[i]
				PZn1 = PZn1*hi[i]
			elif SCJ[i] ==0 and D == 1:
				PZ1 = PZ1*(1-fi[i])
				PZ0 = PZ0*(1-gi[i])
				PZn1 = PZn1*(1-hi[i])
			else:
				print("there is an error")
		Z1[j] = PZ1*d1/(PZ1*d1 + PZ0*d0+ PZn1*dn1)   # calculate the Zj for all the independent sources SC=1
		Z0[j] = PZ0*d0/(PZ1*d1 + PZ0*d0+ PZn1*dn1)
		Zn1[j] = 1-Z1[j]-Z0[j]

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

		fi[i] = Z1_SC1_D1/(Z1_SC1_D1+Z1_SC0_D1)*ratio[i]
		gi[i] = Z0_SC1_D1/(Z0_SC1_D1+Z0_SC0_D1)*(1-ratio[i])
		hi[i] = (1-Z1_SC1_D1-Z0_SC1_D1)/(2-Z1_SC1_D1-Z0_SC1_D1-Z1_SC0_D1-Z0_SC0_D1)
		Lfi.append(fi[i])
		Lgi.append(gi[i])
		Lhi.append(hi[i])
	# print(ai)
	d1 = np.sum(Z1)/NumV  # when Zj=1
	d0 = np.sum(Z0)/NumV  # when Zj=0
	# below the list of all the variables
	Theta = np.hstack((Lai,Lbi,Lfi,Lgi,Lhi,d1,d0))
	Theta = np.array(Theta)
	deta = 	np.absolute(Theta - Store_Theta)  # get the abs
	deta = sum(deta/len(Theta))  # calculate the average error
	Store_Theta =Theta
	print("----it is running---")
	# deta = 0.001


# print(Theta)
print(Z1)
for k in range(1,45):
	print(np.sum(SC[k,:]))
