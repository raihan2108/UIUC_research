'''
Huajie Shao@2016/11/19
Fun: according to the time
'''

import numpy as np
import sys
from datetime import datetime
from datetime import timedelta
import operator
import matplotlib.pyplot as plt
# import matplotlib.pylab as pylab
import matplotlib as mpl


opinion_list = []
events_list = []
fr_opinion = open('truth-opinion.txt','r')
for num,lines in enumerate(fr_opinion):
	line = lines.split()
	if num+1 <= 25:  #control the readlines
		if int(line[0]) == 1:
			events_list.append(num+1)
		else:
			opinion_list.append(num+1)

fr_opinion.close()

# print(events_list)
# ------establish the dictionary for the assertion id and timestamp
opinion_time = dict()
event_time = dict()
fr_assertion = open('Tids_Sids_Aid_Tm.txt','r')
for lines in fr_assertion.readlines():
	line = lines.strip().split('\t',3)
	ids = int(line[2])
	times = line[3] #get the original time
	time = times.split(' ',1)
	timestamp = time[1]
	time_new = datetime.strptime(timestamp,"%b %d %H:%M:%S %Y")
	if ids in opinion_list:
		opinion_time.setdefault(ids,[]).append(time_new)
	elif ids in events_list:
		event_time.setdefault(ids,[]).append(time_new)
	else:
		pass

fr_assertion.close()


## use window = 8 hours to distribute the dataset
sort_opinion = sorted(opinion_time.items(), key=operator.itemgetter(0), reverse=False)
sort_event = sorted(event_time.items(), key=operator.itemgetter(0), reverse=False)

def Calculate_num_assertion(nums):
	window = 8
	Num_list = []
	for items in nums:
		val = items[1]
		i = 0
		num = 0
		vals = sorted(val)
		st_num = []
		for v in range(len(vals)):
			current = vals[v]
			if i == 0:
				first_time = current
				t2 = first_time+ timedelta(hours=window)
				i += 1

			if current <= t2:
				num += 1
			else:
				st_num.append(num)
				t2 = current + timedelta(hours=window)
				num = 0
			if v == len(vals)-1:
				if num > 0:
					st_num.append(num)
					num = 0

		Num_list.append(st_num)

	return Num_list


Opt_num = Calculate_num_assertion(sort_opinion)
Event_num = Calculate_num_assertion(sort_event)

print(Opt_num)
print(Event_num)
fw_opinion_dis = open('Opinion-dis.txt','w')
fw_event_dis = open('Event-dis.txt','w')

for num in Event_num:
	# pr = np.array(num)/sum(num)
	pr = np.array(num)
	for rst in pr:
		fw_event_dis.write('%.3f' %rst+'\t')
	fw_event_dis.write('\n')


print('--below is the opinion----')
for num in Opt_num:
	# opr = np.array(num)/sum(num)
	opr = np.array(num)
	for rst in opr:
		fw_opinion_dis.write('%.3f' %rst+'\t')
	fw_opinion_dis.write('\n')

fw_event_dis.close()
fw_opinion_dis.close()
print('---well done---')




