'''
Huajie Shao@2016/7/23
Function: get assertion Id(num) and get the corresponding tweets
'''

# -*- coding:utf-8 -*-
import ast
import operator


## we need to get the num ids of the assertions from the source claims
Num_id = []
f_read_ids = open("cluster_cred_temp.txt",'r')  #cluster_cred_temp.txt
for lines in f_read_ids.readlines():
	line = lines.split()
	Num_id.append(line[0]) # get the ids with string

# print(Num_id)

## -----read cluster_destination to get the Tweets Id
num_ids_dict = dict()
f_cluster_desc = open("cluster_desc.txt",'r')
for dest_id in f_cluster_desc.readlines():
	ids = dest_id.split()                          # num: ids string
	if ids[0] in Num_id:  #ids[0] = num 1,2,3
		num_ids_dict[str(ids[1])] = int(ids[0])

###-----it is better rank the dict------
sorted_num_id = sorted(num_ids_dict.items(), key=operator.itemgetter(1))

# #-----from the input2 documents
tweet_id_dict = dict()
with open("input2.txt") as tweets:
	for str_texts in tweets:
		dict_tweet = ast.literal_eval(str_texts)
		tweet_txt = dict_tweet['text'].replace('RT @','')
		tw_id = dict_tweet['id']
		# print(tw_id)
		tweet_id_dict[str(tw_id)] = str(tweet_txt)
		# break



## map the ids to tweets
f_get_tweets = open('Ids_tweets.txt','w')
for key,val in sorted_num_id:
	if key in num_ids_dict.keys():
		tweets = tweet_id_dict[key]
		str_tweet = tweets.encode('gbk','ignore').decode('gbk','ignore')  #decode
		new_tweet = str_tweet.replace('\n',' ')
		f_get_tweets.write(str(val)+'\t'+new_tweet+'\n')  #write to text
	else: 
		print("error",key)

f_get_tweets.close()

print("-----Congs, work done, good job----")


		