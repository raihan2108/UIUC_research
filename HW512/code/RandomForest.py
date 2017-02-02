'''
Huajie @16/11/25
fun: random forests
'''

import random
import math
import operator


train_file = 'train.txt'
def read_train_file(train_file):
	fr_train = open(train_file,'r')
	data = []
	attributes_list = []
	N = 0
	for lines in fr_train.readlines():
		line = lines.split()
		data.append(line)
		N += 1
	first_line = data[0]
	for item in first_line[1:]:
		attribute = item.split(':')
		index = attribute[0]
		value = attribute[1]
		attributes_list.append(index)

	return data, attributes_list, N


def sample_attributes(data,attributes_list,N):
	att_len = len(attributes_list)
	m = 2.0/3 * math.sqrt(att_len)
	f_num = math.ceil(m)  # the number of attributed to be chosen
	rand_num = random.sample(range(0, att_len),f_num) #sample the attributes
	rand_num = sorted(rand_num)
	# print(attributes_list)
	sel_att = []
	for k in rand_num:
		order = int(attributes_list[k])
		sel_att.append(order)

	# print(sel_att)
	samp_data = []
	for i in range(N):
		di = random.randint(0,N-1)
		dataline = data[di]
		di_data = [dataline[j] for j in sel_att]
		samp_data.append(di_data)

	# print(samp_data)
	return samp_data

		
## get the label
def predict_class(tree,test_data):


def main():
	# if (len(sys.argv) <3):
	# 	sys.stderr.write("Input format: " + sys.argv[0] + " train_file " + " test_file \n" )
	# 	sys.stderr.flush()
	# 	sys.exit(1)
	# else:
	# 	train_file = sys.argv[1]
	# 	test_file = sys.argv[2]
	data, attributes_list, N = read_train_file(train_file)
	Num = 100
	est_rst = []
	for t in range(Num):  #the  t time of random forest
		samp_data = sample_attributes(data,attributes_list,N)
		tree = BuildTree(data,attributes_list)
		rst_i = predict_class(tree,test_data)
		est_rst.append(rst_i)

	forest_rst = []
	for t in range(N):
		ct = [est_rst[j][t] for j in range(Num)]  #num of trees
		clls_dict = dict()
		for vi in ct:
			if vi not in clls_dict:
				clls_dict[vi] = 1
			else:
				clls_dict[vi] += 1
		ci = sorted(clls_dict.items(),key=operator.itemgetter(1), reverse=True)
		forest_rst.append(ci)


##the function to run main fun
if __name__ == "__main__":
	main()

