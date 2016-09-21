'''
Huajie Shao @05/03/2016
fun: CS525 project: get the parameters of servers, database and cache
'''

import numpy as np
from numpy.linalg import inv


real_time = np.array([])

for i in range(4, 16, 2):
	file_time = open("power"+str(i)+"-t14.log","r")
	time = []  # list of times
	for num, line in enumerate(file_time):
		line=line.split()
		time.append(line[0])
	t = float(time[-1])-float(time[0])
	real_time = np.append(real_time, t)  # get the time begining and end
	
	file_time.close()

# c= np.array([[1, 2], [3, 4]])
# print(real_time)

# this fun is to get the cache and database, web using the standard files
sum_db = np.array([])
sum_cache = np.array([])
sum_web = np.array([])

for j in range(4, 16, 2):
	file_std = open("res-q"+str(j)+"-stat-t21.txt",'r')	# standard file
	for num, line in enumerate(file_std):
		line = line.split()
		cache = int(line[0]) + int(line[1])
		web = cache/20.0
		cache = cache/4.0
		db = float(line[2])
	sum_db = np.append(sum_db, db)  #only one row for this file
	sum_cache = np.append(sum_cache, cache)  #requests of cache
	sum_web = np.append(sum_web, web)
	file_std.close()

# request of per second
cache_request = np.divide(sum_cache, real_time)
db_request = np.divide(sum_db, real_time)
web_request = np.divide(sum_web, real_time)

# print("Database request:\n", db_request)
# print("Cache request:\n", cache_request)
# print("Web request:\n", web_request)

# get the mean of delay for web, cache and database
arr_cache_delay = np.array([])
arr_db_delay = np.array([])
arr_web_delay = np.array([])

for k in range(4, 16, 2):
	sum_cache_delay = 0.0
	sum_db_delay = 0.0
	sum_web_delay = 0.0
	file_cache_delay = open("res-q"+str(k)+"-cn-t21.txt",'r')
	file_db_delay = open("res-q"+str(k)+"-dn-t21.txt",'r')
	file_web_delay = open("res-q"+str(k)+"-wn-t21.txt",'r')
	for num, line in enumerate(file_cache_delay):
		line = line.split()
		cache_delay = float(line[0])
		sum_cache_delay += cache_delay   #1000 rows for this file
	avg_cache_delay = sum_cache_delay/(num+1)
	arr_cache_delay = np.append(arr_cache_delay, avg_cache_delay)

#	db delay
	for num, line in enumerate(file_db_delay):
		line = line.split()
		db_delay = float(line[0])
		sum_db_delay = sum_db_delay + db_delay
	avg_db_delay = sum_db_delay/(num+1)
	arr_db_delay = np.append(arr_db_delay, avg_db_delay)

	for num, line in enumerate(file_web_delay):
		line = line.split()
		web_delay = float(line[0])
		sum_web_delay = sum_web_delay + web_delay
	avg_web_delay = sum_web_delay/(num+1)
	arr_web_delay = np.append(arr_web_delay, avg_web_delay)


	file_cache_delay.close()
	file_db_delay.close()
	file_web_delay.close()


# solve the equation of M*delay-C=lamda*delay, where M and C are variables
# solve the cache parameters:
b1 = web_request*arr_web_delay
b2 = cache_request*arr_cache_delay
b3 = db_request*arr_db_delay
arr_one = -np.ones(6)   		# get six ones array
a1 = np.concatenate(([arr_web_delay], [arr_one]))
a2 = np.concatenate(([arr_cache_delay], [arr_one]))
a3 = np.concatenate(([arr_db_delay], [arr_one]))

# using least squares to solve the equations for web, cache and database
x1 = np.linalg.lstsq(a1.T, b1)[0]
x2 = np.linalg.lstsq(a2.T, b2)[0]
x3 = np.linalg.lstsq(a2.T, b3)[0]

print("For web_server whose parameters M and C are below:")
print(x1)
print("For cache whose parameters M and C is below:")
print(x2)
print("For database whose parameters M and C is below:")
print(x3)






