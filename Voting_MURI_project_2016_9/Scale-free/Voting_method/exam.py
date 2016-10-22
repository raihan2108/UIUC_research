import math
import numpy as np

# a = (499/500)**3
# Pb = 1-a
# Pd = Pb**4
# print(10/7)

#3# schedule--

P1=9
C1=4
P2=100
C2=14
P3 = 10
C3 = 6
P4 = 20
# C4 = 1

# # P = [9,100,10,20]
# P_arr = np.array([30,40])
# C = np.array([10,4])
# print(sum(C/P_arr))


Pa = 1/250
PBA = 0.5
PB_a=1/500
PB = Pa*PBA + PB_a*(1-Pa)
t = (1-PB)**3

print((1-t)**4)
print(math.log(2))
