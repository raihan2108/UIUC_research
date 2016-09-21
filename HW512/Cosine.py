'''Fun: Cosine function
   cos(t) = 向量a*向量b/(a的模*b的模)
'''

import numpy as np
from numpy import linalg as LA
import math

a = np.array([[1,0,1],[1,0,1],[0,0,1]])
b = np.array([[1,0,1],[0,0,0],[0,0,1]])
a_vect = np.hstack(a)   #turn the array to vector
b_vect = np.hstack(b)   #turn the array to vector

# print(a_vect)
# print(b_vect)
a_time_b = np.dot(a_vect,b_vect)  # the dot product of two vectors
# print(a_time_b)
a_mod = LA.norm(a_vect)  # get the mode of the a
b_mod = LA.norm(b_vect)  # get the mode of b vector

sim = a_time_b/(a_mod*b_mod)
print(math.exp(-1/2))

