'''
Huajie Shao@2016/9/01
Function: check the opinion reported by sources
and If they are in the follower-followees trees
Input: tweets ids---->to--->social trees
'''

# -*- coding:utf-8 -*-
import ast
import operator


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
		tweet_time[str(tw_id)] = [src_ids,time]  #tweet, sourc and time
		fw_time.write(str(tw_id)+'\t'+str(src_ids)+'\t'+str(time)+'\n')

fw_time.close()


# #----Fun: get tweets_id and source_id_time_asstion ids
fw_all_info = open('Tids_Sids_Aid_Tm.txt','w')
fw_all_info.write('Source_ID'+'\t'+'Assertion_ID'+'\t'+'timestamp'+'\n')
fw_fst = open('First_sources.txt','w')
fw_src_claim = open('Source_claims.txt','w')
First_user = dict()
first_src_list=[]
Follow_count =dict()
f_tweet_ids = open("cluster_desc.txt",'r')   #tweets ids and sources ids
for tweet_id in f_tweet_ids.readlines()[0:100]:	# readline():[0:2]
	ids = tweet_id.split()
	for i in range(1,len(ids)):
		src_time = tweet_time[ids[i]]
		S_ids = src_time[0]
		timestamp = src_time[1]
		for j in range(i+1,len(ids)):
			source_next = tweet_time[ids[j]]
			next_sids = source_next[0]
			if S_ids != next_sids:
				src_pair = (S_ids,next_sids)
				if src_pair in Follow_count:
					Follow_count[src_pair] += 1
				else:
					Follow_count[src_pair] = 1
		
		if i == 1:
			First_user[ids[0]] = S_ids
			fw_fst.write(S_ids+'\n')
			first_src_list.append(S_ids)  #get the first sources

		fw_all_info.write(S_ids+'\t'+ids[0]+'\t'+timestamp+'\n')
		fw_src_claim.write(S_ids+'\t'+ids[0]+'\n')
		

fw_all_info.close()
fw_fst.close()

# print(Follow_count[('1','1')])
fw_graph = open('Ancestor-children.txt','w')
Rank_graph = sorted(Follow_count.items(), key=operator.itemgetter(1), reverse=True)
for elments in Rank_graph:
	if elments[1] >2:
		ancestor = elments[0][0]
		child = elments[0][1]
		fw_graph.write(ancestor+'\t'+child+'\n')
		# print(elments[0])

fw_graph.close()
print("good work, well done")
