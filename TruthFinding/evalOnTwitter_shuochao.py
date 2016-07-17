import sys
import os
import numpy as np
from copy import deepcopy
import warnings

def abpEMatInit(sourceNum, depDefault, indepDefault):
	defaultA = indepDefault
	defaultB = indepDefault*0.5
	defaultPT = depDefault
	defaultPF = depDefault
	aEMat= np.ones(sourceNum)*defaultA
	bEMat = np.ones(sourceNum)*defaultB
	pTEMat = np.ones(sourceNum)*defaultPT
	pFEMat = np.ones(sourceNum)*defaultPF
	return [aEMat,bEMat,pTEMat,pFEMat]

def probCMatInit(assertionNum):
	probCMat = 0.5*np.ones(assertionNum)
	return probCMat

def estimate(n,m,aEMat,bEMat,pTEMat,pFEMat,cMat,depMat,probCMat,totalProb):
	pCTMat = np.zeros(m)#np.ones(m)
	pCFMat = np.zeros(m)#np.ones(m)
	for j in xrange(m):
		# pCTMat[j] = 1.
		# pCFMat[j] = 1.
		for i in xrange(n):
			if cMat[i][j] == 1:
				if depMat[i][j] == 1:
					pCTMat[j] += np.log(pTEMat[i]/pFEMat[i]) #*= pTEMat[i]/pFEMat[i]
					# pCFMat[j] += 0.0#*= 1.0#pFEMat[i]
				else:
					# if bEMat[i] == 0.0:
					# 	print aEMat[i], aEMat[i], i
					# try:
						# pCTMat[j] *= (aEMat[i]*1000000.)/(bEMat[i]*1000000.)
					pCTMat[j] += np.log(aEMat[i]/bEMat[i])
					# except RuntimeWarning:
					# 	print aEMat[i], bEMat[i], i
					# 	print (aEMat[i]*1000000.)/(bEMat[i]*1000000.)
					# 	print pCTMat[j]
					# else:
					# 	print aEMat[i], bEMat[i], i
					# pCFMat[j] *= 1.0#bEMat[i]
			else:
				if depMat[i][j] == 1:
					# pCTMat[j] *= (1. - pTEMat[i])/(1. - pFEMat[i])
					pCTMat[j] += np.log((1. - pTEMat[i])/(1. - pFEMat[i]))
					# pCFMat[j] *= 1.0#(1. - pFEMat[i])
				else:
					pCTMat[j] += np.log((1. - aEMat[i])/(1. - bEMat[i]))
					# pCTMat[j] *= ((1. - aEMat[i])*1000000.)/((1. - bEMat[i])*1000000.)
					# pCFMat[j] *= 1.0#(1. - bEMat[i])

	for j in xrange(m):
		try:
			probCMat[j] = np.exp(pCTMat[j])*totalProb/(np.exp(pCTMat[j])*totalProb + np.exp(pCFMat[j])*(1-totalProb))
		except RuntimeWarning:
			# print 'pCTMat[j]', pCTMat[j]
			# print 'pCFMat[j]', pCFMat[j]
			probCMat[j] = 0.999
		if probCMat[j]>0.999:
			probCMat[j]=0.999
		elif probCMat[j]<0.001:
			probCMat[j]=0.001
	return probCMat

def estimate_Social(n,m,aEMat,bEMat,cMat,depMat,probCMat,totalProb):
	pCTMat = np.zeros(m) #np.ones(m)
	pCFMat = np.zeros(m) #np.ones(m)
	for j in xrange(m):
		# pCTMat[j] = 1.
		# pCFMat[j] = 1.
		for i in xrange(n):
			if cMat[i][j] == 1:
				if depMat[i][j] == 0:
					pCTMat[j] += np.log(aEMat[i]/bEMat[i])
					# pCTMat[j] *= (aEMat[i]/aEMat[i]*1000000.)/(bEMat[i]*1000000.)
					# pCFMat[j] *= 1.0#bEMat[i]
			else:
				if depMat[i][j] == 0:
					pCTMat[j] += np.log((1. - aEMat[i])/(1. - bEMat[i]))
					# pCTMat[j] *= ((1. - aEMat[i])*1000000.)/((1. - bEMat[i])*1000000.)
					# pCFMat[j] *= 1.0#(1. - bEMat[i])

	for j in xrange(m):
		try:
			probCMat[j] = np.exp(pCTMat[j])*totalProb/(np.exp(pCTMat[j])*totalProb + np.exp(pCFMat[j])*(1-totalProb))
		except RuntimeWarning:
			probCMat[j] = 0.999
		if probCMat[j]>0.999:
			probCMat[j]=0.999
		elif probCMat[j]<0.001:
			probCMat[j]=0.001
	return probCMat

def estimate_EM(n,m,aEMat,bEMat,cMat,depMat,probCMat,totalProb):
	pCTMat = np.zeros(m) #np.ones(m)
	pCFMat = np.zeros(m) #np.ones(m)
	for j in xrange(m):
		# pCTMat[j] = 1.
		# pCFMat[j] = 1.
		for i in xrange(n):
			if cMat[i][j] == 1:
				pCTMat[j] += np.log(aEMat[i]/bEMat[i])
				# pCTMat[j] *= (aEMat[i]*1000000.)/(bEMat[i]*1000000.)
				# pCFMat[j] *= 1.0#bEMat[i]
			else:
				pCTMat[j] += np.log((1. - aEMat[i])/(1. - bEMat[i]))
				# pCTMat[j] *= ((1. - aEMat[i])*1000000.)/((1. - bEMat[i])*1000000.)
				# pCFMat[j] *= 1.0#(1. - bEMat[i])

	for j in xrange(m):
		try:
			probCMat[j] = np.exp(pCTMat[j])*totalProb/(np.exp(pCTMat[j])*totalProb + np.exp(pCFMat[j])*(1-totalProb))
		except RuntimeWarning:
			probCMat[j] = 0.999
		if probCMat[j]>0.999:
			probCMat[j]=0.999
		elif probCMat[j]<0.001:
			probCMat[j]=0.001
	return probCMat

def paraEstimate(n,m,aEMat,bEMat,pTEMat,pFEMat,cMat,depMat,probCMat):

	aLast = deepcopy(aEMat)
	bLast = deepcopy(bEMat)
	pTLast = deepcopy(pTEMat)
	pFLast = deepcopy(pFEMat)

	for i in xrange(n):
		aUp = 0.
		aDown = 0.
		bUp = 0.
		bDown = 0.
		pCTUp = 0.
		pCTDown = 0.
		pCFUp = 0.
		pCFDown = 0.
		for j in xrange(m):
			if depMat[i][j] == 1:
				pCTDown += probCMat[j]
				pCFDown += 1. - probCMat[j]
				if cMat[i][j] == 1:
					pCTUp += probCMat[j]
					pCFUp += 1. -probCMat[j]
			# elif depMat[i][j] == 0:
			else:
				aDown += probCMat[j]
				bDown += 1. - probCMat[j]
				if cMat[i][j] == 1:
					aUp += probCMat[j]
					bUp += 1. - probCMat[j]

		if aDown > 0:
			aEMat[i] = aUp/aDown
		if bDown > 0:
			bEMat[i] = bUp/bDown
		if pCTDown > 0:
			pTEMat[i] = pCTUp/pCTDown
		if pCFDown > 0:
			pFEMat[i] = pCFUp/pCFDown

		if pFEMat[i] > pTEMat[i]:
			tmp = pFEMat[i]
			pFEMat[i] = pTEMat[i]
			pTEMat[i] = tmp

	totalProb = 0.0

	for j in xrange(m):
		totalProb += probCMat[j]
	totalProb /= m

	count = 0.
	sumAll = 0.
	for i in xrange(n):
		count += 1.
		sumAll = aEMat[i] - aLast[i] + bEMat[i] - bLast[i] + pTEMat[i] - pTLast[i] + pFEMat[i] - pFLast[i]

	return [aEMat, bEMat, pTEMat, pFEMat, sumAll/count, totalProb]

def paraEstimate_Social(n,m,aEMat,bEMat,cMat,depMat,probCMat):

	aLast = deepcopy(aEMat)
	bLast = deepcopy(bEMat)

	for i in xrange(n):
		aUp = 0.
		aDown = 0.
		bUp = 0.
		bDown = 0.
		for j in xrange(m):
			if depMat[i][j] == 0:
				aDown += probCMat[j]
				bDown += 1. - probCMat[j]
				if cMat[i][j] == 1:
					aUp += probCMat[j]
					bUp += 1. - probCMat[j]

		if aDown > 0:
			aEMat[i] = aUp/aDown
		if bDown > 0:
			bEMat[i] = bUp/bDown
		# if pCTDown > 0:
		# 	pTEMat[i] = pCTUp/pCTDown
		# if pCFDown > 0:
		# 	pFEMat[i] = pCFUp/pCFDown

	totalProb = 0.0

	for j in xrange(m):
		totalProb += probCMat[j]
	totalProb /= m

	count = 0.
	sumAll = 0.
	for i in xrange(n):
		count += 1.
		sumAll = aEMat[i] - aLast[i] + bEMat[i] - bLast[i]

	return [aEMat, bEMat, sumAll/count, totalProb]

def paraEstimate_EM(n,m,aEMat,bEMat,cMat,depMat,probCMat):

	aLast = deepcopy(aEMat)
	bLast = deepcopy(bEMat)

	for i in xrange(n):
		aUp = 0.
		aDown = 0.
		bUp = 0.
		bDown = 0.
		for j in xrange(m):
			aDown += probCMat[j]
			bDown += (1. - probCMat[j])
			if cMat[i][j] == 1:
				aUp += probCMat[j]
				bUp += (1. - probCMat[j])

		if aDown > 0:
			aEMat[i] = aUp/aDown
		if bDown > 0:
			bEMat[i] = bUp/bDown
		# if pCTDown > 0:
		# 	pTEMat[i] = pCTUp/pCTDown
		# if pCFDown > 0:
		# 	pFEMat[i] = pCFUp/pCFDown

	totalProb = 0.0

	for j in xrange(m):
		totalProb += probCMat[j]
	totalProb /= m

	count = 0.
	sumAll = 0.
	for i in xrange(n):
		count += 1.
		sumAll = aEMat[i] - aLast[i] + bEMat[i] - bLast[i]

	return [aEMat, bEMat, sumAll/count, totalProb]



inputFolder = sys.argv[1]
sourceClaimFile = sys.argv[2]
rtFile = sys.argv[3]
numBound = 999999999999999
if len(sys.argv) > 4:
	numBound = int(sys.argv[4])
warnings.filterwarnings("error")
# np.seterr(all='warn')

print 'Obtain Source Assertion #'
fileIn = open(os.path.join(inputFolder, sourceClaimFile))
line = fileIn.readline()
count = 0
sourceDict = {}
idxSourceDict = {}
assertionList = []
maxAssertionID = -1
while len(line) > 0:
	elems = line.split('\t')
	curSource = int(elems[0])
	curAssertion = int(elems[1])
	if not sourceDict.has_key(curSource):
		curID = len(sourceDict)
		sourceDict[curSource] = curID
		idxSourceDict[curID] = curSource
	assertionList.append(curAssertion)
	if curAssertion > maxAssertionID:
		maxAssertionID = curAssertion
	count += 1
	line = fileIn.readline()
	print '\r', count,
	if count >= numBound:
		break
print ''
fileIn.close()

# sourceList = list(set(sourceList))
assertionList = list(set(assertionList))
sourceNum = len(sourceDict)
assertionNum = len(assertionList)

if len(assertionList) != maxAssertionID:
	print 'maxAssertionID', maxAssertionID
	print 'len(assertionList)', len(assertionList)
print 'sourceNum', sourceNum
print 'assertionNum', assertionNum

print 'Gen sourceClaimMat'
sourceClaimMat = np.zeros((sourceNum, assertionNum))
fileIn = open(os.path.join(inputFolder, sourceClaimFile))
line = fileIn.readline()
count = 0
while len(line) > 0:
	elems = line.split('\t')
	curSource = int(elems[0])
	curAssertion = int(elems[1])
	sourceClaimMat[sourceDict[curSource]][curAssertion-1] = 1.
	line = fileIn.readline()
	count += 1
	print '\r', count,
	sys.stdout.flush()
	if count >= numBound:
		break
totalSourceClaim = count
print ''

print 'Gen rtList'
# rtMat = np.zeros((sourceNum, sourceNum))
rtList = [[] for i in xrange(sourceNum)]
fileIn = open(os.path.join(inputFolder, rtFile))
line = fileIn.readline()
count = 0
while len(line) > 0:
	elems = line.split(',')
	if sourceDict.has_key(int(elems[0])) and sourceDict.has_key(int(elems[1])):
	# 	folID = sourceDict[int(elems[0])]
	# 	masID = sourceDict[int(elems[1])]
		rtList[sourceDict[int(elems[0])]].append(sourceDict[int(elems[1])])
	# else:
	# 	print elems
	# rtMat[folID][masID] = 1.0
	line = fileIn.readline()
	count += 1
	print '\r', count,
	sys.stdout.flush()
print ''
fileIn.close()

print 'Gen depMat'
depMat = np.zeros((sourceNum, assertionNum))
# Dierctly serach for sourceNum*assertionNum is too large takes too much time
# But this old setting seems wrong
depSourceClaim = 0
count = 0
print 'sourceNum * assertionNum', sourceNum*assertionNum
for idx1 in xrange(sourceNum):
	for idx2 in xrange(assertionNum):
		for masID in rtList[idx1]:
			if sourceClaimMat[masID][idx2] == 1:
				depMat[idx1][idx2] = 1
				depSourceClaim += 1
				break
		count += 1
		print '\r', count,
		sys.stdout.flush()
print ''
# fileIn = open(os.path.join(inputFolder, sourceClaimFile))
# line = fileIn.readline()
# count = 0
# depSourceClaim = 0
# while len(line) > 0:
# 	elems = line.split('\t')
# 	curSource = sourceDict[int(elems[0])]
# 	curAssertion = int(elems[1]) - 1
# 	for masID in rtList[curSource]:
# 		if sourceClaimMat[masID][curAssertion] == 1:
# 			depMat[curSource][curAssertion] = 1.
# 			if sourceClaimMat[curSource][curAssertion] == 1:
# 				depSourceClaim += 1
# 			else:
# 				print 'wanted!\nwanted!\nwanted!\n'
# 			break
# 	line = fileIn.readline()
# 	count += 1
# 	print '\r', count,
# 	sys.stdout.flush()
# print ''
# fileIn.close()

print 'totalSourceClaim', totalSourceClaim
print 'depSourceClaim', depSourceClaim

indepSoceClaim = totalSourceClaim - depSourceClaim
depDefault = float(depSourceClaim)/(sourceNum*assertionNum)
indepDefault = float(indepSoceClaim)/(sourceNum*assertionNum)
print "depDefault", depDefault
print 'indepDefault', indepDefault

[aEMat_Ext,bEMat_Ext,pTEMat_Ext,pFEMat_Ext] = abpEMatInit(sourceNum, depDefault, indepDefault)
probCMat_Ext = probCMatInit(assertionNum)
[aEMat_Social,bEMat_Social,pTEMat_Social,pFEMat_Social] = abpEMatInit(sourceNum, depDefault, indepDefault)
probCMat_Social = probCMatInit(assertionNum)
[aEMat_EM,bEMat_EM,pTEMat_EM,pFEMat_EM] = abpEMatInit(sourceNum, depDefault, indepDefault)
probCMat_EM = probCMatInit(assertionNum)

print 'aEMat_Ext.dtype', aEMat_Ext.dtype
print 'bEMat_Ext.dtype', bEMat_Ext.dtype

totalProb_Ext = 0.5
totalProb_Social = 0.5
totalProb_EM = 0.5

for idx in xrange(8):
	print '\r', idx+1,
	sys.stdout.flush()
	probCMat_Ext = estimate(sourceNum,assertionNum,aEMat_Ext,bEMat_Ext,pTEMat_Ext,pFEMat_Ext,sourceClaimMat,depMat,probCMat_Ext,totalProb_Ext)
	[aEMat_Ext, bEMat_Ext, pTEMat_Ext, pFEMat_Ext, diff_Ext, totalProb_Ext] = paraEstimate(sourceNum,assertionNum,aEMat_Ext,bEMat_Ext,pTEMat_Ext,pFEMat_Ext,sourceClaimMat,depMat,probCMat_Ext)

	probCMat_Social = estimate_Social(sourceNum,assertionNum,aEMat_Social,bEMat_Social,sourceClaimMat,depMat,probCMat_Social,totalProb_Social)
	[aEMat_Social, bEMat_Social, diff_Social, totalProb_Social] = paraEstimate_Social(sourceNum,assertionNum,aEMat_Social,bEMat_Social,sourceClaimMat,depMat,probCMat_Social)

	probCMat_EM = estimate_EM(sourceNum,assertionNum,aEMat_EM,bEMat_EM,sourceClaimMat,depMat,probCMat_EM,totalProb_EM)
	[aEMat_EM, bEMat_EM, diff_EM, totalProb_EM] = paraEstimate_EM(sourceNum,assertionNum,aEMat_EM,bEMat_EM,sourceClaimMat,depMat,probCMat_EM)

addName = ''
if numBound < 999999999999999:
	addName = str(numBound)

res_Ext = []
for idx in xrange(assertionNum):
	res_Ext.append([idx, probCMat_Ext[idx]])
res_Ext = sorted(res_Ext, key = lambda x: -x[1])
fileOut = open(os.path.join(inputFolder, 'res_Ext_'+addName+'.out'), 'w')
for idx in xrange(len(res_Ext)):
	fileOut.write(str(res_Ext[idx][0])+'\t'+str(res_Ext[idx][1])+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'aEMat_Ext_'+addName+'.out'), 'w')
for idx in xrange(len(aEMat_Ext)):
	fileOut.write(str(aEMat_Ext[idx])+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'bEMat_Ext_'+addName+'.out'), 'w')
for idx in xrange(len(bEMat_Ext)):
	fileOut.write(str(bEMat_Ext[idx])+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'pTEMat_Ext_'+addName+'.out'), 'w')
for idx in xrange(len(pTEMat_Ext)):
	fileOut.write(str(pTEMat_Ext[idx])+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'pFEMat_Ext_'+addName+'.out'), 'w')
for idx in xrange(len(pFEMat_Ext)):
	fileOut.write(str(pFEMat_Ext[idx])+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'sourceDict_'+addName+'.out'), 'w')
# for idx in xrange(len(pFEMat_Ext)):
fileOut.write(str(sourceDict)+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'totalProb_Ext_'+addName+'.out'), 'w')
# for idx in xrange(len(pFEMat_Ext)):
fileOut.write(str(totalProb_Ext)+'\n')
fileOut.close()

# depMat
fileOut = open(os.path.join(inputFolder, 'depMat_'+addName+'.out'), 'w')
for idx in xrange(sourceNum):
	curDep = depMat[idx]
	curDepNum = np.sum(curDep)
	fileOut.write(str(curDepNum/float(assertionNum))+'\n')
fileOut.close()

fileOut = open(os.path.join(inputFolder, 'sourceClaimMat_'+addName+'.out'), 'w')
for idx in xrange(sourceNum):
	curDep = sourceClaimMat[idx]
	curDepNum = np.sum(curDep)
	fileOut.write(str(curDepNum/float(assertionNum))+'\n')
fileOut.close()


res_Social = []
for idx in xrange(assertionNum):
	res_Social.append([idx, probCMat_Social[idx]])
res_Social = sorted(res_Social, key = lambda x: -x[1])
fileOut = open(os.path.join(inputFolder, 'res_Social_'+addName+'.out'), 'w')
for idx in xrange(len(res_Social)):
	fileOut.write(str(res_Social[idx][0])+'\t'+str(res_Social[idx][1])+'\n')
fileOut.close()

res_EM = []
for idx in xrange(assertionNum):
	res_EM.append([idx, probCMat_EM[idx]])
res_EM = sorted(res_EM, key = lambda x: -x[1])
fileOut = open(os.path.join(inputFolder, 'res_EM_'+addName+'.out'), 'w')
for idx in xrange(len(res_EM)):
	fileOut.write(str(res_EM[idx][0])+'\t'+str(res_EM[idx][1])+'\n')
fileOut.close()














