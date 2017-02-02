'''
Huajie @ 2016/11/21
Function: code decision tree without other library
'''

import math
import sys,os
import operator
from copy import deepcopy
# import itertools

train_file = 'led.train.new'
test_file = 'led.test.new'

#--------
class Node:
	def __init__(self, attribute = None, attrVal = None, children = None, vote = None):
		self.attribute = attribute
		self.attrVal=attrVal
		self.children = []
		self.vote = vote
		if children is not None:
			for child in children:
				self.add_son(child)

	def __repr__(self):
		return self.attribute

	def add_son(self,son):
		assert isinstance(son, Node)
		self.children.append(son)

#------read train data----------
def read_train_file(train_file):
	fr_train = open(train_file,'r')
	data = []
	attributes_list = []
	for lines in fr_train.readlines():
		line = lines.split()
		data.append(line)

	first_line = data[0]
	for item in first_line[1:]:
		attribute = item.split(':')
		index = attribute[0]  # integer
		value = attribute[1]
		attributes_list.append(index)

	return data, attributes_list

## ----read the test files------
def read_test_file(test_file):
	fr_test = open(test_file,'r')
	test_label = []
	test_data = []
	for lines in fr_test.readlines():
		line = lines.split()
		test_label.append(line[0])
		attributes = line[1:]
		line_data = []
		for feature in attributes:
			values = feature.split(':')
			indx = values[0]
			val = values[1]
			line_data.append(val)
		test_data.append(line_data)

	return test_data, test_label

# Gini function to calculate the entropy
def compute_gini(label_di):
	label_subset = label_di
	label_dict = dict()
	count_lab = len(label_subset)  #the total number of labels
	sum_pi = 0
	# cal the number of labels of class
	for labs in label_subset:
		if labs in label_dict.keys():
			label_dict[labs] += 1
		else:
			label_dict[labs] = 1
	for key,val in label_dict.items():
		count = label_dict[key]
		p_j = float(count)/count_lab
		sum_pi += p_j**2

	gini_d = 1 - sum_pi

	return gini_d


# how to get the tuples of the corresponding attruibutes
def Convert_tuple_dict(data):
	attribute_dict = dict()
	for lines in data:
		att_line = lines[1:]
		label = lines[0]
		for feat in att_line:
			att = feat.split(":")
			index = att[0]  #string
			value = att[1]
			class_val = (value,label)
			attribute_dict.setdefault(index,[]).append(class_val)

	return attribute_dict

##-----split the feature------
def split_feature(att_tuple):
	Gini_index = dict()
	attri_class = att_tuple
	for keys in attri_class.keys():
		attribute = attri_class[keys]  # each attributes
		subset_dict = dict()  	   # for each attribute
		Di_set = dict()
		len_vals = len(attribute)  # get the lens of values
		for items in attribute:
			di = items[0]  	# the values of ith attributes
			di_class = items[1] 	# get the class of the ith attributes
			if di not in subset_dict.keys():
				subset_dict[di] = 1
			else:
				subset_dict[di] += 1

			Di_set.setdefault(di,[]).append(di_class)  #labels and value
		# print(Di_set)
		gini_sum = 0
		for di_key in Di_set.keys():
			di_vals = Di_set[di_key]  #for different vals
			gini_di = compute_gini(di_vals)
			wi = float(subset_dict[di_key])/len_vals
			gini_sum += wi*gini_di

		Gini_index[keys] = gini_sum
	sort_gini = sorted(Gini_index.items(),key=operator.itemgetter(1), reverse=False)
	# print('the gini index is', sort_gini)
	split_node = sort_gini[0][0]   # the node to split
	
	return split_node

##-----define majoity voting-----
def majority_voting(data):
	fre_count = dict()
	max_val = 0
	class_rst=0
	# print("majority data: ", data)
	for value in data:
		val = value[0]
		if val not in fre_count.keys():
			fre_count[val] = 1
		else:
			fre_count[val] += 1

	for k in fre_count.keys():
		if fre_count[k] > max_val:
			max_val = fre_count[k]
			class_rst = k
	print("callssss--", class_rst)
	return class_rst

# ---get node values of each attribute----
def Get_NodeValue(att_tuple,split_node):
	values = att_tuple[split_node]  #get the children of each attribute
	att_value_list = []
	for val in values:
		value = val[0]
		if value not in att_value_list:
			att_value_list.append(value)

	return att_value_list

#----node data-----
def Get_node_data(data, att_val, split_node):
	newdata = []
	node_num = []
	# print("data 0", data[0])
	line = data[0]
	attributes = line[1:]
	for att in attributes:
		indx_val = att.split(":")
		node_num.append(indx_val[0])  # store the index of attribute, id of attribute

	extract_att = deepcopy(node_num)
	extract_att.remove(split_node)
	if split_node in node_num:  #find the split node
		att_id = node_num.index(split_node) + 1
		for lines in data:
			feat = lines[att_id]  # get the feature of the data
			indx_val = feat.split(":")
			value = indx_val[1]
			if value == att_val:  # attribute value = org.data.value
				extract_line = []
				for t_id in extract_att:
					ids = extract_att.index(t_id) + 1
					extract_line.append(lines[ids])
				newdata.append(extract_line)

	return newdata

#------build tree-------
def BuildTree(data,attributes_list):

	labels = [line[0] for line in data]
	if len(attributes_list) <= 0:
		print("if enter: ",data)
		class_rst = majority_voting(data)
		# print('********-Finished************',class_rst)
		return Node(vote = class_rst)
	elif all(x==labels[0] for x in labels):
		print("if a: ",data)
		return Node(vote=labels[0])
	else:
		att_tuple = Convert_tuple_dict(data)  # conver the tabel to dictionary
		split_node = split_feature(att_tuple)  # the data of removed attributed
		Dtree = []
		attrVal=[]
		node_value = Get_NodeValue(att_tuple,split_node)  #children
		if len(node_value)<=0:
			print("split node:", split_node)
		# print("----node values---:", node_value)
		for val in node_value:
			new_data = Get_node_data(data,val,split_node)
			new_attributes = deepcopy(attributes_list)
			new_attributes.remove(split_node)
			# print("attributes list:", attributes_list, new_attributes)
			sub_tree = BuildTree(new_data, new_attributes)
			Dtree.append(sub_tree)
			attrVal.append(val)
		return Node(attribute = split_node, attrVal = attrVal, children = Dtree)

#-----predict label----
def predict_class(tree,row):
	# print("predict class")
	if tree.vote != None:
		return tree.vote
	val = row[int(tree.attribute)]
	for i in range(len(tree.attrVal)):
		if val == tree.attrVal[i]:
			return predict_class(tree.children[i],row)

#---print
def print_tree(tree,indent='  '):
	if tree.vote != None:
		print(" v = "+str(tree.vote))
	else:
		print(indent+str(tree.attribute) + ':')
		for i in range(len(tree.attrVal)):
			print(indent+indent+str(tree.attrVal[i])+ ' -> ')
			print_tree(tree.children[i],indent+indent + '  ')
#------the main function to get the data
def main():
	# if (len(sys.argv) <3):
	# 	sys.stderr.write("Input format: " + sys.argv[0] + " train_file " + " test_file \n" )
	# 	sys.stderr.flush()
	# 	sys.exit(1)
	# else:
	# 	train_file = sys.argv[1]
	# 	test_file = sys.argv[2]

	test_data, test_label = read_test_file(test_file)
	data, attributes_list = read_train_file(train_file) #read the train data and their attributes
	tree = BuildTree(data, attributes_list)
	# print("the tree root", tree)
	# print("true label of test data: ", test_label)
	# print(tree.keys())
	predict_rst = []
	for row in test_data:
		rst = predict_class(tree,row)
		predict_rst.append(rst[2])
		# print_tree(tree, indent = '  ')
		# print("the result is:",rst[2])

	sam_count = [i for i, j in zip(test_label, predict_rst) if i == j]
	accy = len(sam_count)/len(test_label)
	print(accy)


##the function to run main fun
if __name__ == "__main__":
	main()