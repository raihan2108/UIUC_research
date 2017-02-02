'''
Huajie @ 2016/12/1 modified by huajie
Function: code decision tree without other library
'''

import math
import sys,os
import operator
from copy import deepcopy

train_file = 'nursery.data.train'
test_file = 'nursery.data.test'

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
		return str(self.attribute)

	def add_son(self,son):
		assert isinstance(son, Node)
		self.children.append(son)

#---------read train data-----------
def read_file(train_file):
	fr_train = open(train_file,'r')
	data = []
	attributes_list = []
	for lines in fr_train.readlines():
		line = lines.split()
		class_id = int(line[0])
		att_line = line[1:]
		att_value = [class_id]
		for attr in att_line:
			values = attr.split(":")
			val = int(values[1])
			att_value.append(val)
		data.append(att_value)

	first_line = data[0][1:]
	for i in range(len(first_line)):
		attributes_list.append(i+1)  # convert to integer

	return data, attributes_list

# Gini function to calculate the entropy
def compute_gini(label):
	label_subset = label
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

##-----split the feature------
def split_feature(data,att_list):
	Gini_index = dict()
	len_attr = len(att_list)
	for j in range(len_attr):  	   # colum j+1 is the values
		attr_vals = [line[j+1] for line in data]
		labels = [line[0] for line in data]
		subval_dict = dict()  	   # for each attribute
		attVal_set = dict()
		for n in range(len(attr_vals)):
			class_id = labels[n] 		# get the class of the ith attributes
			val = attr_vals[n]
			if val not in subval_dict.keys():
				subval_dict[val] = 1
			else:
				subval_dict[val] += 1

			attVal_set.setdefault(val,[]).append(class_id)  #labels and value

		gini_sum = 0
		for key in attVal_set.keys():
			label = attVal_set[key]  # label of values
			gini_di = compute_gini(label)
			wi = float(subval_dict[key])/len(attr_vals)
			gini_sum += wi*gini_di

		Gini_index[j] = gini_sum
	sort_gini = sorted(Gini_index.items(),key=operator.itemgetter(1), reverse=False)
	# print('the gini index is', sort_gini)
	split_node = att_list[sort_gini[0][0]]   # the node to split
	# print('split node', split_node)
	return split_node

##-----define majoity voting-----
def majority_voting(data):
	fre_count = dict()
	# print("majority data: ", data)
	for value in data:
		val = value[0]
		if val not in fre_count.keys():
			fre_count[val] = 1
		else:
			fre_count[val] += 1

	fre_class = sorted(fre_count, key = fre_count.get, reverse= True)
	class_rst = fre_class[0]

	return class_rst

# ---get node values of each attribute----
def Get_NodeValue(data,split_node,attributes_list):
	dx = attributes_list.index(split_node) + 1  #get the index
	indx_val = [line[dx] for line in data]
	att_value_list = []
	for val in indx_val:
		if val not in att_value_list:
			att_value_list.append(val)

	return att_value_list

#----node data-----
def get_attribute_data(data, att_val, split_node, attributes_list):
	newdata = []
	attr_id = attributes_list.index(split_node) + 1
	for line in data:
		value = line[attr_id]
		ext_data = []
		if value == att_val:  # attribute value = org.data.value
			ext_data = line[: attr_id] + line[attr_id+1 :]
			newdata.append(ext_data)

	return newdata

#------build tree-------
def BuildTree(data,attributes_list):

	labels = [line[0] for line in data]
	if len(attributes_list) <= 0:
		class_rst = majority_voting(data)
		# print('********-Finished************',class_rst)
		return Node(vote = class_rst)
	elif all(x==labels[0] for x in labels):
		# print("if a: ",data)
		return Node(vote=labels[0])
	else:
		split_node = split_feature(data,attributes_list)  # the data of removed attributed
		sub_tree = []
		attrVal=[]
		node_value = Get_NodeValue(data,split_node,attributes_list)  #children
		# print("----node values---:", node_value)
		for val in node_value:
			new_data = get_attribute_data(data,val,split_node,attributes_list)

			new_attributes = deepcopy(attributes_list)
			new_attributes.remove(split_node)
			# print("attributes list:", attributes_list, new_attributes)
			
			nodes = BuildTree(new_data, new_attributes)  #sub-sub_tree is the nodes
			sub_tree.append(nodes)
			attrVal.append(val)  #attribute value corresponding to the child node

		return Node(attribute = split_node, attrVal = attrVal, children = sub_tree)

#-----predict label----
def predict_class(tree,row):
	# print("predict class")
	if tree.vote != None:
		return tree.vote
	test_val = row[tree.attribute]  # get the testdata val
	for i in range(len(tree.attrVal)):
		if test_val == tree.attrVal[i]:
			return predict_class(tree.children[i],row)

#---print
def print_tree(tree,indent='  '):
	if tree.vote != None:
		print(" label = "+ str(tree.vote))
	else:
		print(indent + str(tree.attribute) + ':')
		for i in range(len(tree.attrVal)):
			print(indent +' ' + str(tree.attrVal[i])+ ' -> ')
			print_tree(tree.children[i],indent + '  ')

def confusion_matrix(predict_rst, test_label):
	true_prdt = zip(test_label,predict_rst)
	com_val = list(true_prdt)
	conf_dict =dict()
	for value in com_val:
		val = str(value)
		if val not in conf_dict.keys():
			conf_dict[val] = 1
		else:
			conf_dict[val] += 1

	print(conf_dict)
	sam_count = [i for i, j in zip(test_label,predict_rst) if i == j]
	accy = len(sam_count)/len(test_label)
	print("The predict accuracy is: ",accy)

#------the main function to get the data
def main():
	# if (len(sys.argv) <3):
	# 	sys.stderr.write("Input format: " + sys.argv[0] + " train_file " + " test_file \n" )
	# 	sys.stderr.flush()
	# 	sys.exit(1)
	# else:
	# 	train_file = sys.argv[1]
	# 	test_file = sys.argv[2]
	test_data, test_attr = read_file(test_file)
	test_label = [line[0] for line in test_data]
	data, attributes_list = read_file(train_file) #read the train data and their attributes
	
	#----below run the tree----------
	tree = BuildTree(data, attributes_list)
	# print_tree(tree, indent = '  ')

	print("the tree root", tree)
	predict_rst = []
	for row in test_data:
		rst = predict_class(tree,row)
		predict_rst.append(rst)
		# print("the result is:",rst)
		# break
	print(predict_rst.index(None))
	confusion_matrix(predict_rst,test_label)


##the function to run main fun
if __name__ == "__main__":
	main()