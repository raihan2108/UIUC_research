'''
Huajie @ 2/2/2017
Fun: using cosine function to deal with the assertions
and the ids corresponding to the assertions
'''

import sys,os
import operator
import re
# import numpy as np


def intersect(lst_a, lst_b):
	return list(set(lst_a) & set(lst_b))

def union_set(lst_a,lst_b):
	return list(set(lst_a) | set(lst_b))

'''
def clean_http(texts):
	clean_text = []  # list of text
	text_spt = texts.split()
	for text in text_spt:
		plain_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
		if len(plain_text)>=1:
			clean_text.append(plain_text)

	return clean_text
'''

def title_prune():
	fr_tweet = open('User_assertion_time.txt','r')
	# fw_tweet = open("tweets_unique.txt",'w')
	raw_tweets =[]
	user_id_assertion = []
	for num,lines in enumerate(fr_tweet):
		line = lines.strip().split('\t')
		tweets = line[2]
		uid_ass =[line[0],line[1],line[2],line[3]]
		if tweets not in raw_tweets and len(tweets.split())>=1:
			raw_tweets.append(tweets)

		user_id_assertion.append(uid_ass)
			# fw_tweet.write(tweets + '\n')
	print(len(user_id_assertion))
	fr_tweet.close()
	# fw_tweet.close()
	return raw_tweets, user_id_assertion

def consine_sim(raw_tweets):
	# fw_tweets = open("tweets_text.txt",'w')
	tweet_title = []
	for num, lines in enumerate(raw_tweets):
		# print("It is running the program.",num)
		# print(texts)
		title_pure = lines.split()
		if not tweet_title:
			tweet_title.append(lines)
			# fw_tweets.write(texts+'\n')
		else:
			for title in tweet_title:
				save_title = title.split()  #get the words of the title
				inter_set = intersect(save_title,title_pure)
				uset = union_set(save_title,title_pure)
				if len(uset)>=1:
					if len(inter_set)/len(uset) >= 0.5:
						flag = 1
						break
					else:
						flag = 0
				else:
					flag = 1

			if flag == 0 and len(lines)>=1:
				tweet_title.append(lines)

	print("length",len(tweet_title))
	return tweet_title


def tweet_id_sort(unique_title,uid_assertion):
	num_id = []
	tweet_id_dict = dict()
	tweet_count_dict = dict()
	k = 0
	for utitle in unique_title:
		k += 1
		count = 0
		clean_txt = utitle.split()
		print('it is running',k)
		user_id_list = []
		for num,lines in enumerate(uid_assertion):
			if num not in num_id:
				tweets = lines[2]
				tid = lines[1]
				user_id = lines[0]
				timestamp = lines[3]
				timestamp = timestamp.replace('+0000 ','')
				clean_tweets = tweets.split()
				inter_set = intersect(clean_txt,clean_tweets)
				uset = union_set(clean_txt,clean_tweets)
				pr = len(inter_set)/len(uset)
				if pr >= 0.6 and len(uset)>=1:
					if user_id not in user_id_list:
						user_id_list.append(user_id)
						count += 1
						tid_uid_tm = [tid,user_id,timestamp]
						tweet_id_dict.setdefault(k,[]).append(tid_uid_tm)
						num_id.append(num)

		tweet_count_dict[k] = count
	
	#---write--sorted ids--
	fre_count = sorted(tweet_count_dict, key = tweet_count_dict.get, reverse= True)
	fw_tweets_id = open("Tweets_ids_new.txt",'w')
	fw_user_id = open("Source_ids_new.txt",'w')
	fw_src_time = open("Source_time_new.txt",'w')
	for ids in fre_count:
		values = tweet_id_dict[ids] #tid_uid_time
		for item in values: #tweets id 
			tid = item[0]
			uid = item[1]
			time = item[2]
			fw_tweets_id.write(tid+'\t')
			fw_user_id.write(uid+'\t')
			fw_src_time.write(time+'\t')

		fw_tweets_id.write('\n')
		fw_user_id.write('\n')
		fw_src_time.write('\n')

	fw_tweets_id.close()
	fw_user_id.close()
	fw_src_time.close()


def main():
	raw_tweets,user_id_assertion = title_prune()
	u_title = consine_sim(raw_tweets)
	# print(u_title)
	tweet_id_sort(u_title,user_id_assertion)
	print("well done")


if __name__ == '__main__':
	main()


