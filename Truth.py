'''
Huajie Shao @06/21/2016
Function: TruthFinding paper based EM algorithm
'''
import numpy as np
# from random import random


N = 20
NumV = 20 	# number of variables
flg = 1
link = N*2
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
ai = np.random.uniform(0.3,0.9,N)
bi = np.random.uniform(0.1,0.4,N)
d1, d0, dn1 = 0.5, 0.4, 0.1
Graph = np.zeros([N,N])

# ------------------------------------
# this function is to generate the graph
# ------------------------------------
while flg==1:
	i = np.random.randint(0,N-1)
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
	SC[j,:] = SC1|SC2

# print(SC)

nm = 3
first_user =[]
follower_id=np.empty([0, 2])   #define the empty array
for i in Cn1:
	User = np.random.randint(0,N,nm)
	SC[i,:] = 0
	for id in User:
		SC[i,id] = 1
	uid = np.array(User[1:nm])
	follower_id =np.append(follower_id,uid)
	first_user.append(User[0]) 		#get the first users to report

# print(first_user)

# print(SC[1,:])

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
fi = np.zeros(N)
gi = np.zeros(N)
# print(ai)
for key, val in ratio.items():
	parent_list = SD_ancestor[key]
	rebf, rebg = 0, 0
	for id in parent_list:
		rebf = ai[id] + rebf		# the reliability of the ancestors
		rebg = bi[id] + rebg
	rebf = rebf/len(parent_list)
	rebg = rebg/len(parent_list)
	fi[key] = ai[key]*(1-val) + val*rebf		# should find their ancestors, D=1, SC=1
	gi[key] = bi[key]*(1-val) + val*rebg

# get the first source of their reliability
qi = np.zeros(N)
hi = np.zeros(N)
# print(qi)
for id in first_user:
	qi[id] = ai[id]

# ---carefully----get the reliability of followers
for id in follower_id:
	if id in ratio.keys():
		hi[id] = ratio[id]*qi[id]
	else:
		hi[id] = ai[id]

deta = 0.2
PZ1 = 1	#SC=1 and D=0 independent
PZ0=1
PZn1 = 1
var_len = 2*parent_len + 3*child_len + 2
Store_Theta = np.zeros(var_len)  # Get the length of the variables
Z1 = np.zeros(NumV)
Z0  = np.zeros(NumV)
Zn1 = np.zeros(NumV)
while deta>0.1:
	for j in range(NumV):
		SCJ = SC[j,:]
		for i in range(N):
			if i in ratio.keys():
				D = 1
			else:
				D = 0
			if SCJ[i] ==1 and D == 0:
				PZ1 = PZ1*ai[i]
				PZ0= PZ0*bi[i]
				PZn1 = PZn1*qi[i]		# find the first source to make the claims
			elif SCJ[i] ==0 and D == 0:
				PZ1= PZ1*(1-ai[i])
				PZ0 = PZ0*(1-bi[i])
				PZn1= PZn1*(1-qi[i])
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

		fi[i] = Z1_SC1_D1/(Z1_SC1_D1+Z1_SC0_D1)
		gi[i] = Z0_SC1_D1/(Z0_SC1_D1+Z0_SC0_D1)
		hi[i] = (1-Z1_SC1_D1-Z0_SC1_D1)/(2-Z1_SC1_D1-Z0_SC1_D1-Z1_SC0_D1-Z0_SC0_D1)
		Lfi.append(fi[i])
		Lgi.append(gi[i])
		Lhi.append(hi[i])

	d1 = np.sum(Z1)/NumV  # when Zj=1
	d0 = np.sum(Z0)/NumV  # when Zj=0
	# below the list of all the variables
	Theta = np.hstack((Lai,Lbi,Lfi,Lgi,Lhi,d1,d0))
	Theta = np.array(Theta)
	print(Theta)
	deta = 	np.absolute(Theta - Store_Theta)  # get the abs
	deta = sum(deta/len(Theta))  # calculate the average error
	Store_Theta =Theta
	print("it is running")



# print(Theta)

	
