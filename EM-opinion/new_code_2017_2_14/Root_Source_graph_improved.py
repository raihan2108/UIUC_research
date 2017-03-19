'''
Huajie @ 2/7/2017
Fun: for a certain tweet and find the social graph
to track the opinion
'''


import os,sys
import numpy as np


#read the sources:
fr_sources = open('Source_ids_new.txt','r')
source_ids =[]
for num,lines in enumerate(fr_sources):
	line = lines.strip().split('\t')
	source_ids.append(line)

fr_sources.close()


#read the counts of the followrs:
fr_counts = open('Follower_counts.txt','r')
follower_count = []
for num, lines in enumerate(fr_counts):
	line = lines.strip().split('\t')
	follower_count.append(line)

fr_counts.close()

# hash the ids and follower counts:
tid_fcount_dict = dict()
for m in range(len(follower_count)):
	src_ids = source_ids[m]
	count = follower_count[m]
	for j in range(len(count)):
		ids = src_ids[j]
		numbers = count[j]
		tid_fcount_dict[ids] = numbers
#---tweet ids
#read tweets ids------
fr_tweet_id = open('Tweets_ids_new.txt','r')
tweet_id_list =[]
for num,lines in enumerate(fr_tweet_id):
	line = lines.strip().split('\t')
	tweet_id_list.append(line)

fr_tweet_id.close()
# print(tweet_id_list)
# print(follower_count)
# print('----------')
# 

fr_graph = open("Follow_graph.txt",'r')
tweet_src_id = dict()
for num,lines in enumerate(fr_graph):
	line = lines.split()
	tids = line[0]  #tweets ids
	parent_children = (line[1],line[2])
	for k, tweets in enumerate(tweet_id_list): #tweets id list
		if tids in tweets:
			tweet_src_id.setdefault(k,[]).append(parent_children)  #the kth assertion

fr_graph.close()

fw_follower = open('Ancestor_children.txt','w')
for key,val in tweet_src_id.items():  #parent and children
	for v in val:
		fw_follower.write(str(v)+'\t')
	fw_follower.write('\n')

fw_follower.close()

# print(tweet_src_id)

fw_root_src = open('Root_source.txt','w')
for key in range(len(tweet_id_list)): #key denote the No. of assertion
	root_src = []
	dependent = []
	if key in tweet_src_id:  #follower and followees
		values = tweet_src_id[key]
		for v1,v2 in values:
			root_src.append(v1)
			dependent.append(v2)  #get the dependent sources
		for src in set(root_src):
			fcounts = tid_fcount_dict[src]
			fw_root_src.write(src+':'+ fcounts+'\t')

		line_srcs = source_ids[key] #each assertion source
		for ids in line_srcs:
			if ids not in dependent and ids not in root_src:
				fcounts = tid_fcount_dict[ids]
				fw_root_src.write(ids+':'+ fcounts+'\t')

		fw_root_src.write('\n')
	else:
		line_srcs = source_ids[key] #each assertion source
		fw_root_src.write('Independent'+'\n')

	print("The number is: ",key)
	# if key>=2:
		# break

fw_root_src.close()

print('ok, well done')





