'''
Huajie Shao@2016/7/25
fun: find the nums and the corresponding truth or false
'''

import sys
import numpy as np

filename=['Opt','Cost','Rand']
truth_dict = dict()
for f_name in filename:
	fr_claim = open(f_name+'_claim_100.txt','r')
	for lines in fr_claim.readlines():
		val = lines.split()
		truth_dict[val[0]] = val[2]

for f_name2 in filename:
	fr_claim = open(f_name2+'_claim_140_rst.txt','r')
	for lines in fr_claim.readlines():
		val = lines.split()
		truth_dict[val[0]] = val[2]

# after we get the dict., we can calculate the other files
fname = 'Rand'

fr_source_claims = open(fname+'_claim_140.txt','r')
fw_truth = open(fname+'_claim_140_rst.txt','w')
for line in fr_source_claims.readlines():
	key = line.split()
	if key[0] in truth_dict.keys():
		val = truth_dict[key[0]]
		fw_truth.write(key[0]+'\t'+key[1]+'\t'+str(val)+'\n')
	else:
		fw_truth.write(key[0]+'\t'+key[1]+'\t'+'\n')


print("-----good work, work done----")
