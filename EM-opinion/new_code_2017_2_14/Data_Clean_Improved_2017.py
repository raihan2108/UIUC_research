'''
Huajie Shao@ 2/1/2017
Fun: from the raw data of input to clean the data

'''

# import sys,os
import operator
import pprint as pp
import ast


fw_user_tweet = open('User_assertion_time.txt','w')
fw_graph = open('Follow_graph.txt','w')
num = 0
with open("input.txt") as tweets:
	for str_texts in tweets:
		num += 1
		dict_tweet = ast.literal_eval(str_texts)
		pp.pprint(dict_tweet)
		key = 'retweeted_status'
		if key in dict_tweet: #dependent sources
			retweet = dict_tweet['retweeted_status']
			root_src_dict = retweet['user']  #get the dict orginal sources
			if 'id' in root_src_dict:
				flag = 1
				org_sid = root_src_dict['id']
				count_follower = root_src_dict['followers_count']
				text_org = retweet['text']
				text_org = text_org.encode('gbk','ignore').decode('gbk','ignore')
				# text_org = text_org.encode('utf-8')
				text_org = text_org.replace('\n',' ')
				text_org = text_org.replace('\r',' ')
				time_org = retweet['created_at']
				org_aid = retweet['id']  #assertion id
				if len(text_org.split())>=1:
					fw_user_tweet.write(str(org_sid) +'\t'+ str(org_aid)+'\t'+ str(text_org) +'\t' + time_org + '\t'+ str(count_follower)+'\n')
			else:
				flag = 0
			# print('org time:',time_org)
			#--------the current tweet made by users------
			current_user = dict_tweet['user']
			if 'id' in current_user and flag == 1:
				user_id = current_user['id'] #user id
				follower_current = current_user['followers_count']
				assertion_id = dict_tweet['id']  #assertion id
				current_time = dict_tweet['created_at']
				# current_time = current_time.replace("+0000",'')
				if len(text_org.split())>=1:
					fw_user_tweet.write(str(user_id) +'\t'+ str(assertion_id)+'\t'+ str(text_org) +'\t' + current_time + '\t'+ str(follower_current)+'\n')
					fw_graph.write(str(assertion_id) +'\t'+str(org_sid) +'\t'+ str(user_id)+'\n')  #follower and followee
		else:
			# print("it is independent source")
			indp_user = dict_tweet['user']
			if 'id' in indp_user:
				indp_uid = indp_user['id']
				assertion_id = dict_tweet['id']
				follower_indp = indp_user['followers_count']
				text = dict_tweet['text']
				text_new = text.encode('gbk','ignore').decode('gbk','ignore')
				# text_new = text.encode("utf-8")
				text_new = text_new.replace('\n',' ')
				text_new = text_new.replace('\r',' ')
				current_time = dict_tweet['created_at']
				if len(text_new.split())>=1:
					fw_user_tweet.write(str(indp_uid) +'\t'+ str(assertion_id)+'\t'+ text_new +'\t' + current_time+'\t'+ str(follower_indp) + '\n')
		
		print('---Number is-----: ',num)
		if num >=698:
			break

fw_user_tweet.close()
fw_graph.close()

