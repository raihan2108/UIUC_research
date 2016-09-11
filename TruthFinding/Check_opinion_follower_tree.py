'''
Huajie Shao@2016/9/01
Function: check the opinion reported by sources
and If they are in the follower-followees trees
Input: tweets ids---->to--->social trees
'''

# -*- coding:utf-8 -*-
import ast
import operator



##--Function: get the sources for a specific assertion
ass_src_dict = dict()
src_assertion = dict()
src_id = []
fr_assertion = open('author_cluster.txt','r')
for line in fr_assertion.readlines():
	lines = line.split()
	src = lines[0]
	ass_id = int(lines[1])
	# src_id.append(src_id)
	ass_src_dict.setdefault(ass_id,[]).append(src)
	src_assertion.setdefault(src,[]).append(ass_id)


# print(len(src_id),len(Tweet_ids_list))

###--Fun:get the timestamp tweet_ids and sourc_ids from the tweets
fw_time = open('Tids_Sid_time.txt','w') # record the Tw_ids and src_ids
tweet_time = dict()
with open("input2.txt") as tweets:
	for str_texts in tweets:
		dict_tweet = ast.literal_eval(str_texts)
		time = dict_tweet['created_at'].replace('+0000 ','')
		users= dict_tweet['user']		#get the information of users
		src_ids = users['id_str']
		tw_id = dict_tweet['id']
		tweet_time[str(tw_id)] = [src_ids,time]
		fw_time.write(str(tw_id)+'\t'+str(src_ids)+'\t'+str(time)+'\n')

fw_time.close()

# print(tweet_time)

# #----Fun: get tweets_id and source_id_time_asstion ids
fw_all_info = open('Tids_Sids_Aid_Tm.txt','w')
First_user = dict()
f_tweet_ids = open("cluster_desc.txt",'r')   #tweets ids and sources ids
for tweet_id in f_tweet_ids.readlines():	# readline():[0:2]
	ids = tweet_id.split()
	for i in range(1,len(ids)):
		src_time = tweet_time[ids[i]]
		S_ids = src_time[0]
		timestamp = src_time[1]
		if i == 1:
			First_user[ids[0]] = S_ids
		fw_all_info.write(ids[i]+'\t'+S_ids+'\t'+ids[0]+'\t'+timestamp+'\n')
		

fw_all_info.close()

# print(First_user['5'])
'''
k = 9
## -----read tweets ids to look for sources ids
num_ids_dict = dict()
f_cluster_desc = open("cluster_desc.txt",'r')   #tweets ids and sources ids
for dest_id in f_cluster_desc.readlines():
	ids = dest_id.split()
	t = int(ids[0])
	for i in range(1,len(ids)):
		num_ids_dict.setdefault(t, []).append(ids[i])


f_cluster_desc.close()
# print(num_ids_dict)

##get the sources ids
Source_ids = num_ids_dict[k]   #get the list of source who report assertion k
print(Source_ids)
# #-----from the input2 documents
depdent_source = []
with open("social_rt.txt") as graphs:
	for uid in graphs:
		sid = uid.strip().split(',')
		# print(sid)
		depdent_source.append(sid[0])


# print (depdent_source)
##---get the followers and indepdent sources
Successors =[]
Ind_sources =[]
for ids in Source_ids:
	if ids in depdent_source:
		Successors.append(ids)
	else:
		Ind_sources.append(ids)

print(Successors)
print("-----Congs, work done, good job----")
'''

		