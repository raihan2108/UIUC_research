''' 
Huajie Shao@2016/7/20
Get data from Twitter
function: selected source to EM to calculate the estimation error
'''

import numpy as np
import ast

file_name="Opt_org"
# ---func:read the author ids from author_credit.txt
def Get_author_id():
	author_id = dict()
	a_id = []
	fr_author = open('source-prob.txt','r')  #authors should be the same as following
	for num, names in enumerate(fr_author):
		nm_id = names.split()
		if nm_id in a_id:
			pass
		else:
			a_id.append(int(nm_id[0]))  # ID is a string
	author_order = np.sort(a_id)
	for i in range(len(author_order)):
		author_id[i] = str(author_order[i])

	fr_author.close()
	return author_id
	# print(author_id)

# Get_author_id()


##-----get the author and its assertions
def Get_author_assertion():
	author_claim = dict()
	f_author_claim = open('author_cluster.txt','r')
	for lines in f_author_claim.readlines():
		SC = lines.split()
		author_claim.setdefault(SC[0], []).append(SC[1])  #string 
		# print(author_claim)
	f_author_claim.close()
	return author_claim



# ------below is init the paramters---
author_id = Get_author_id()
# print(author_id)
a_claim = Get_author_assertion()
# print(author_claim)
# SD_ancestor = Generate_graph()


# ---------------- the main function----------------------
#  -choose data for a given cost rather than multiple costs
#  -------------------------------------------------------
fread_ids = open(file_name+'_ids.txt','r')  # notice the order of the sources
i = 0
for ids in fread_ids.readlines():
	org_id = []
	i +=1
	fw_author_claim = open(str(i)+'sel_author_claim.txt','w')
	vid = ids.strip()  # delete '\r\t\n'
	vid = ast.literal_eval(vid)  #get the list of selcted sources
	for org_id in vid:
		num_id = org_id  # the list of sources for each cost
		for nums in num_id:
			src_id = author_id[nums]   #get the ids of selected sources
			# get the assertions made by the selected sources
			Assertion = a_claim[src_id]
			for la in Assertion:
				fw_author_claim.write(str(src_id)+'\t'+la+'\n')
			

	fw_author_claim.close()

fread_ids.close()

##----sort the author and claims--------
num_txt = i+1
for j in range(1,num_txt):
	claim_order=[]
	claim_dict = dict()
	read_author_claim = open(str(j)+'sel_author_claim.txt','r')
	for clm in read_author_claim.readlines():
		scm = clm.split()
		# print (scm)
		if int(scm[1]) in claim_order:
			pass
		else:
			claim_order.append(int(scm[1]))  #get the all the claims
			
		claim_dict.setdefault(scm[1], []).append(scm[0])

	assertion_order = np.sort(claim_order)  #get the new order
	# print(assertion_order)
	fw_user_claim = open(str(j)+file_name+'choose_sources.txt','w')
	for k in range(len(assertion_order)):
		asst_id = str(assertion_order[k])   # the id of assertion
		user_ids = claim_dict[asst_id]    	# get the id of users
		for user in user_ids:
			fw_user_claim.write(user+'\t'+asst_id+'\n')


	fw_user_claim.close()

print("congratulations, work done and then input to EM algorithm")





		


