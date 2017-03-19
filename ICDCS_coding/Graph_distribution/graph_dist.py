''' Huajie @3/19/2017
Fun: to distribute the graph to see if 
it is heavy tailed graph or random graph distribution
'''


import sys,os
import random
import matplotlib.pyplot as plt
from math import log
# from pylab import figure


def intersection(a,b):
	return list(set(a)&set(b))


# read the ancestor and children
print('----start running----')
source_total = []
file_input = open('follow_graph.txt','r')
parent_children= dict()
anc_child = []
for num, lines in enumerate(file_input):
	line = lines.split()
	ancestor = line[1]
	children = line[2]
	parent_children.setdefault(ancestor,[]).append(children)
	pair = [ancestor,children]
	if pair not in anc_child:
		anc_child.append(pair)
	# add ancestor and children to source_total
	if ancestor not in source_total:
		source_total.append(ancestor)
	if children not in source_total:
		source_total.append(children)

	# if num>=100:
	# 	print(anc_child)
	# 	break


# plot the distribution of grapg
n1 = 200
n2 = len(source_total)
print(n2)
step = 400
edgeNum = []
node_num =[]
for k in range(n1,n2+1,step):
	rst = random.sample(source_total,k)
	num = 0
	for src in rst:
		if src in parent_children:
			child = parent_children[src]
			intsect = intersection(child,rst)
			if len(intsect) >=1:
				num += 1
	edgeNum.append(num)
	node_num.append(k)

print(edgeNum)
# print(node_num)
xmax = max(node_num)
ymax = max(edgeNum)

# #---plot ---orignal coordinate
# plt.plot(node_num, edgeNum, 'ro')
# plt.axis([0, xmax, 0, ymax])
# plt.show()

#log-log plot:
logEdge = [log(y,10) for y in edgeNum]
logNode = [log(x,10) for x in node_num]
lxmax = max(logNode)
lymax = max(logEdge)
plt.plot(logNode, logEdge, 'bo')
plt.axis([1, lxmax, 0, lymax])
plt.xlabel('# of sources (log)')
plt.ylabel('# of Edges (log)')
plt.savefig('graph_dis.jpg')
print('done well')
# plt.show()
# print(logEdge)
# print(logNode)

