
'''
Huajie: fun: test code
'''


import math
import random


class Tree():
	def __init__(self, name = None, node = None):
		self.name = name
		self.node = node

class Node:
	def __init__(self, label=None, children=None):
		self.label = label
		self.children =[]
		if children is not None:
			for child in children:
				self.children.append(child)

	def __repr__(self):
		return self.label

# print(math.sqrt(3))
rand_num = random.randint(0, 3)
rand_num = rand_num
print(rand_num)

'''
class Tree(object):
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

t = Tree('*', [Tree('1'),
               Tree('2'),
               Tree('+', [Tree('3'),
                          Tree('4')])])

print(t)
'''