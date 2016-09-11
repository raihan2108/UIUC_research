''' 
Huajie Shao@08/31/2016
Fun: use the real data to check the new EM-opinion algorithm
'''

import sys
import numpy as np
import random
import math



r0 = 0.1
rn1 = 0.05
r1 = 0.85
#---this function is to get the reb of first sources to tweet
def Get_qi(NumV,N,st_fst_id,ai):
	qi = np.zeros([NumV,N])+0.01
	# all_fst_ids=[]  #for all the assertions
	for j in range(NumV):
		sids = st_fst_id[j]
		qi[j,sids] = ai[sids]
		# all_fst_ids.append(sids)
	return qi


def Get_graph(Src_num_dict):
	fr_graph = open('Ancestor-children.txt','r')
	fr_first = open('First_sources.txt','r')
	SD_ancestor = dict()
	# SD_successor =dict()
	First_src = []
	for lines in fr_graph.readlines():
		par_child = lines.split()
		father = Src_num_dict[par_child[0]]
		child = Src_num_dict[par_child[1]]
		# print(Src_num_dict['1'])
		# SD_successor.setdefault(father,[]).append(child)
		SD_ancestor.setdefault(child,[]).append(father)  #child:ancestors

	for sources in fr_first.readlines():
		ids = sources.split()
		fid = Src_num_dict[ids[0]]
		First_src.append(fid)

	fr_graph.close()
	fr_first.close()
	# print(First_src)
	return SD_ancestor,First_src

def Get_Source_Claims():
	uniq_src = []
	Src_num_dict = dict()
	Ass_src_dict = dict()
	fr_SC = open('Source_claims.txt','r')
	for line in fr_SC.readlines():
		SClaim = line.split()
		source = SClaim[0]
		ass = SClaim[1]
		Ass_src_dict.setdefault(ass,[]).append(source)
		if source not in uniq_src:
			uniq_src.append(source)

	for j in range(len(uniq_src)):
		Src_num_dict[uniq_src[j]] = j

	V_num = len(Ass_src_dict.keys())
	N = len(uniq_src)
	SC = np.zeros([V_num,N])
	for k in range(V_num):
		nm = k+1
		S_ids = Ass_src_dict[str(nm)]
		for ids in S_ids:
			num = Src_num_dict[ids]
			SC[k,num] = 1
			# print(k+1,num)
	return SC,N,V_num,Src_num_dict

#---EM-social algorithm-----
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
		if ik>=20:
			print("it is terminated by k=50")
			break

	return Z1


#-----below is the new algorithms for opinion
def New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id):
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
				if i == st_fst_id[j]:
					PZn1 = PZn1*qi[j,i]
					flag = 1
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
		qi = Get_qi(NumV,N,st_fst_id,ai)
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
		if ik>=20:
			break
			print("it is terminated by k")


	return Z1, Z0, Zn1


## ---------main_fun-----------
EM_opinion =[]
Voting=[]
EM_social=[]
itera = 1

SC, N, NumV,Src_num_dict = Get_Source_Claims()
SD_ancestor,st_fst_id = Get_graph(Src_num_dict)

# print(SD_ancestor)
fr_voting = open('Voting_rst.txt','w')
fr_EMsocial = open('EM_social_rst.txt','w')
fr_opinionEM = open('EM_opinion_rst.txt','w')
for Nt in range(1, 2, 2):
	for mt in range(itera):  # the number of iteration
		#initialize the parameters------
		ai = np.random.uniform(0.1,0.5,N)
		bi = np.random.uniform(0.1,0.6,N)
		ai = np.round(ai*100)/100
		bi = np.round(bi*100)/100
		sfi = np.random.uniform(0.7,0.95,N)
		sgi = np.random.uniform(0.2,0.6,N)
		fi = np.round(sfi*100)/100
		gi = np.round(sgi*100)/100

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
		
		qi = Get_qi(NumV,N,st_fst_id,ai)
		hi = np.random.uniform(0.6,0.8,N)
		hi = np.round(hi,decimals=3)
		Parameter = np.vstack((ai,bi,fi,gi))  # parameters for EM algorithm
		# --------Function:EM algorithm-------
		# -------EM algorithm-----------
		var_len = 2*parent_len + 3*child_len + 2
		Z1, Z0, Zn1 = New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id) #new EM algorithms
		EM_z1 = Fun_EM_Social(NumV,Ind_Source,Dep_Source,SC,Parameter)
		# print(EM_z1)
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
		print(Z0)
		# print(C)
		# print(np.sum(SC,axis=1))  #calculate the rows
		print("-----Z1 below is the prob of Z1----")
		print(Z1)
		# print("-----below is the prob of opinion----")
		print(Z_rst)
		for k in range(NumV):
			if np.sum(SC[k,:])>N/10:
				Vote[k] = 1
			elif np.sum(SC[k,:])<=N/10 and np.sum(SC[k,:])>=N*0.005:
				Vote[k] = 0
			else:
				Vote[k] = -1

	# -----get the iteration results-------
		fr_EMsocial.write(str(EM_SC)+'\n')
		fr_voting.write(str(Vote)+'\n')
		fr_opinionEM.write(str(Z_rst)+'\n')

# if __name__ == '__main__':
# 	Fun_main()

fr_voting.close()
fr_EMsocial.close()
fr_opinionEM.close()
print("Congratulations, work is done")