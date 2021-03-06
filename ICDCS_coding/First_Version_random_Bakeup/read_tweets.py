'''
Huajie Shao@2016/7/23
Function: assertion Id and get the tweets
'''

# -*- coding:utf-8 -*-
import ast
import operator


file_name = "Rand_"
## we need to get the num ids of the assertions
Num_id = []
f_read_ids = open(file_name+"claim_100.txt",'r')
for lines in f_read_ids.readlines():
	line = lines.split()
	Num_id.append(line[0])   # get the ids with string

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
		tweet_txt = dict_tweet['text']
		tw_id = dict_tweet['id']
		tweet_id_dict[str(tw_id)] = str(tweet_txt)



## map the ids to tweets
f_get_tweets = open(file_name+'Ids_tweets_100.txt','w')
for key,val in sorted_num_id:
	if key in num_ids_dict.keys():
		tweets = tweet_id_dict[key]
		str_tweet = tweets.encode('gbk','ignore').decode('gbk','ignore')  #decode
		new_tweet = str_tweet.replace('\n',' ')
		f_get_tweets.write(str(val)+'\t'+new_tweet+'\n')  #write to text
	else: 
		print("error",key)

f_get_tweets.close()

print("work done, good job")


		