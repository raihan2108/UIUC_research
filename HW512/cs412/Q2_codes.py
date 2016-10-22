import numpy as np
import math
import sys


def Cal_data_cells(keys,Loc):
	unq =[]
	nums =[]
	sm = 0
	for ct in keys:
		vals = Loc[ct]
		# print(vals)
		unq =[]
		for v in vals:
			if v not in unq:
				unq.append(v)
		n = len(unq)
		sm += n

	return sm


###--main function----
city_list = []
states_list = []
price_list = []
rating_list = []
catogary_list = []
city_dict=dict()
new_city = dict()
states_dict={}
Level3=[]
fr_data = open('data.business','r')
for lines in fr_data.readlines():
	line = lines.strip().split('\t')
	# print(line)
	city=line[1]
	state=line[2]
	item=line[3]
	rate = line[4]
	prc = line[5]
	val= [item,rate,prc]
	city_dict.setdefault(city,[]).append(val)
	states_dict.setdefault(state,[]).append(val)
	if val not in Level3:
		Level3.append(val)
	# new_city[city] = [item,rate,prc]

	if city not in city_list:
		city_list.append(city)

	if state not in states_list:
		states_list.append(state)

	if item not in catogary_list:
		catogary_list.append(item)

	if prc not in price_list:
		price_list.append(prc)

	if rate not in rating_list:
		rating_list.append(rate)

# print(city_list)
num_city = Cal_data_cells(city_list,city_dict)
num_state = Cal_data_cells(states_list,states_dict)
print("the cells for city is",num_city,num_state)

print("the number of three is:",len(Level3))

###
x=0
Qe = states_dict['Illinois']
for val in Qe:
	if val[1] == '3' and val[2] == 'moderate':
		x +=1

y = 0
print("the number of IL",x)
qf = city_dict['Chicago']
print(qf)
for value in qf:
	print(value[0])
	if value[0] == "food":
		y +=1

print(y)










