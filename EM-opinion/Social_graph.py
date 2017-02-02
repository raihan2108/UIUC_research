'''
Huajie Shao@ 2/1/2017
Fun: from the raw data of input to get the social graph
in order to find which sources follow the original ones

'''


# import sys,os
import operator
# import pprint as pp
import ast


fw_user_tweet = open('User_assertion_time.txt','w')
fw_graph = open('Follow_graph.txt','w')
num = 0
with open("input2.txt") as tweets:
	for str_texts in tweets:
		num += 1
		dict_tweet = ast.literal_eval(str_texts)
		# pp.pprint(dict_tweet)
		key = 'retweeted_status'
		if key in dict_tweet:
			retweet = dict_tweet['retweeted_status']
			root_src_dict = retweet['user']  #get the dict orginal sources
			org_sid = root_src_dict['id']
			text_org = retweet['text']
			text_org = text_org.encode('gbk','ignore').decode('gbk','ignore')
			text_org = text_org.replace('\n','\t')
			# text_org = text_org.strip()
			time_org = retweet['created_at']
			time_org = time_org.replace("+0000 ",'') #delete the "0000"
			org_aid = retweet['id']  #assertion id
			fw_user_tweet.write(str(org_sid) +'\t'+ str(org_aid)+'\t'+ str(text_org) +'\t' + time_org + '\n')
			# print('org time:',time_org)
			#--------the current tweet made by users------
			current_user = dict_tweet['user']
			user_id = current_user['id'] #user id
			if str(user_id).isspace():
				print('lost the id of user')
			assertion_id = dict_tweet['id']  #assertion id
			current_time = dict_tweet['created_at']
			current_time = current_time.replace("+0000 ",'')
			fw_user_tweet.write(str(user_id) +'\t'+ str(assertion_id)+'\t'+ str(text_org) +'\t' + current_time + '\n')
			fw_graph.write(str(org_sid) +'\t'+ str(user_id)+'\n')  #follower and followee
			# print('current_time:',current_time)
		else:
			print("it is independent source")
			indp_user = dict_tweet['user']
			indp_uid = indp_user['id']
			assertion_id = dict_tweet['id']
			text = dict_tweet['text']
			text_new = text.encode('gbk','ignore').decode('gbk','ignore')
			text_new = text_new.replace('\n','\t')
			current_time = dict_tweet['created_at']
			current_time.replace("+0000 ",'\t')
			fw_user_tweet.write(str(indp_uid) +'\t'+ str(assertion_id)+'\t'+ text_new +'\t' + current_time + '\n')
		# print(root_src)
		# pp.pprint(retweet)
		print(num)
		if num>=10:
			break
