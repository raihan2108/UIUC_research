'''
Huajie Shao @05/06/2016
fun: CS525 project: optimization model
'''

import numpy as np
from scipy.optimize import linprog

def OptMain(Request, delay, M, C):	#C: constant
	Pw = [70, 2, 0, 0]	# power energy for x1 = large server, x2 = small
	rqst = Request
	cnt = np.asarray(C)
	dly =  np.asarray(delay)
	Mp = np.asarray(M)
	par = delay*Mp - cnt
	Aeq = [[0, 0, 1, 1],[par[0], 0, -delay[0], 0], [0, par[1], 0, -delay[1]]]		# requests balance
	beq = [rqst, 0, 0]
	x1_bounds = (0, 35)
	x2_bounds = (0, 35)
	x3_bounds = (0, None)
	x4_bounds = (0, None)
	res = linprog(Pw, A_ub=None, b_ub=None, A_eq=Aeq, b_eq=beq, bounds=(x1_bounds, x2_bounds, x3_bounds, x4_bounds), options={"disp": True})
	return res.x


# dell:
# wpara=[ 17.5217   0.78363531];
# edison:
# ewpara=[ 2.88375094  0.91995302];
fw = open('result_delay_0.3.txt','w')

for Request in range(5,101,5):
	delay = [0.3, 0.3]
	M = [17.5217,  2.88375094]
	C = [0.78363531, 0.91995302]
	x = OptMain(Request, delay, M, C)
	xst = str(x).strip('[]')
	fw.write(xst+"\n")

fw.close()