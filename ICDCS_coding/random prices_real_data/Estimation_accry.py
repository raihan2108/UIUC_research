import sys
import numpy as np


filename=['Opt','Cost','Rand']
j = 0
Accy = np.zeros(3)
for f_name in filename:
	fr_claim = open(f_name+'_claim_140_rst.txt','r')
	nm = 0
	snum = 0
	for lines in fr_claim.readlines():
		val = lines.split()
		v1,v2 = float(val[1]), float(val[2])
		snum += 1
		if abs(v1-v2)<0.49:
			nm += 1

	Accy[j] = nm/snum
	j += 1

print(Accy)
