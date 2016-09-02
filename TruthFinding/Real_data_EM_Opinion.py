''' 
Huajie Shao@08/31/2016
Fun: use the real data to check the new EM-opinion algorithm
'''

import sys
import numpy as np
import random
import math


#---this function is to get the reb of first sources to tweet
def Get_qi(NumV,N,st_fst_id,ai):
	qi = np.zeros([NumV,N])+0.01
	all_fst_ids=[]  #for all the claims and assertions
	for j in range(NumV):
		ids = st_fst_id[j]
		qi[j,ids] = ai[ids]
		all_fst_ids.append(ids)

	return qi, all_fst_ids


def Get_graph(sc_rt):
	SD_ancestor = []
	SD_successor =[]


	return SD_successor,SD_ancestor,st_fst_id

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
		if ik>=50:
			break
			print("it is terminated by k")


	return Z1, Z0, Zn1


## ---------main_fun-----------
accuray_EM =[]
accuray_vote=[]
accuray_social=[]
itera = 50
fr = open('.txt','r')
for num,data in enumerate(fr):
	pass

fr.close()


for Nt in range(60, 70, 20):
	rpt_EM = []
	rpt_vote = []
	rpt_social =[]
	for mt in range(itera):  # the number of iteration
		NumV = 50 	# number of variables
		N = len(Source_ids)
		#initialize the parameters------
		ai = np.random.uniform(0.5,0.9,N)
		bi = np.random.uniform(0.2,0.6,N)
		ai = np.round(ai*100)/100
		bi = np.round(bi*100)/100
		sfi = np.random.uniform(0.5,0.8,N)
		sgi = np.random.uniform(0.2,0.6,N)
		fi = np.round(sfi*100)/100
		gi = np.round(sgi*100)/100

		# we need to get the independent sources
		SD_successor,SD_ancestor = Get_graph(social_relation)
		st_fst_id = Get_TimeStamp()
		Ind_Source =[]
		Dep_Source =[]
		for i in range(N):
			if i in SD_ancestor.keys():		# child: [list of parents]
				Dep_Source.append(i)
			else:
				Ind_Source.append(i)	# get the independent sources

		parent_len = len(Ind_Source)
		child_len = len(Dep_Source)
		
		qi, all_fst_ids = Get_qi(NumV,N,st_fst_id,ai)
		hi = np.random.uniform(0.6,0.8,N)
		hi = np.round(hi,decimals=3)
		Parameter = np.vstack((ai,bi,fi,gi))  # parameters for EM algorithm
		# --------Function:EM algorithm-------
		# -------EM algorithm-----------
		var_len = 2*parent_len + 3*child_len + 2
		Z1, Z0, Zn1 = New_fun_EM(var_len,NumV,Ind_Source,Dep_Source,SC,Parameter,qi,hi,st_fst_id) #new EM algorithms
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



# if __name__ == '__main__':
# 	Fun_main()
