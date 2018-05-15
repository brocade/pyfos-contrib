#!/usr/bin/env python
# Copyright 2018 Brocade Communications Systems, LLC.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may also obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import json
from pprint import pprint
import copy

def buildDupsDict(source, keyname):
	dupsDict = {}

	for k in source:
		if source[k][keyname] not in dupsDict:
			dupsDict[source[k][keyname]] = []
		dupsDict[source[k][keyname]].append(k)

	return dupsDict	

def findDupZones(masks):
	sortZones = buildDupsDict(masks, 'WWNsHash')
	dupZones = []
	for k in sortZones:
		if len(sortZones[k]) > 1:
			dupZones.append(sortZones[k])
	return dupZones

def findDupInits(masks):
	sortInits = buildDupsDict(masks, 'InitHash')
	dupInits = []
	for k in sortInits:
		if len(sortInits[k]) > 1:
			dupInits.append(sortInits[k])
	return dupInits

def findDupTargets(masks):
	sortTargets = buildDupsDict(masks, 'TargetHash')

	dupTargets = []
	for k in sortTargets:
		if len(sortTargets[k]) > 1:
			dupTargets.append(sortTargets[k])
	return dupTargets

def removeDupZones(masks, dupZones):
	newMasks = copy.deepcopy(masks)
	count = 0
	for i in range(len(dupZones)):
		for j in range(1, len(dupZones[i])):
			count += 1
			newMasks.pop(dupZones[i][j])
	return newMasks, count

def removeDupInits(masks, dupInits):
	newMasks = copy.deepcopy(masks)
	count = 0
	for i in range(len(dupInits)):
		for j in range(1, len(dupInits[i])):
			newMasks[dupInits[i][0]]['Targets'] = newMasks[dupInits[i][0]]['Targets'] + newMasks[dupInits[i][j]]['Targets']
			newMasks.pop(dupInits[i][j])
			count += 1
		newMasks[dupInits[i][0]]['Targets'] = sorted(list(set(newMasks[dupInits[i][0]]['Targets'])))		
	return newMasks, count

def removeDupTargets(masks, dupTargets):
	newMasks = copy.deepcopy(masks)
	count = 0
	for i in range(len(dupTargets)):
		for j in range(1, len(dupTargets[i])):
			newMasks[dupTargets[i][0]]['Initiators'] = newMasks[dupTargets[i][0]]['Initiators'] + newMasks[dupTargets[i][j]]['Initiators']
			newMasks.pop(dupTargets[i][j])
			count += 1
		newMasks[dupTargets[i][0]]['Initiators'] = sorted(list(set(newMasks[dupTargets[i][0]]['Initiators'])))		
	return newMasks, count

def main():

	with open("symList.json","r") as f:
		symList = json.load(f)

	for i in range(len(symList["symmetrixId"])):

		symID = symList["symmetrixId"][i]
		print
		print("ArraY ID:" + symID)

		with open("hashed-" + symID + ".json","r") as f:
			masks = json.load(f)

		with open("unopt-" + symID + ".json","w") as f:
			json.dump(masks, f)
		dupZones = findDupZones(masks)
		newDupZones, count = removeDupZones(masks, dupZones)
		print("Removed " + str(count) + " duplicated zone(s).")
		with open("dupsRemoved-" + symID + ".json","w") as f:
			json.dump(newDupZones, f)
		dupInits = findDupInits(masks)
		newDupInits, count = removeDupInits(masks, dupInits)
		print("Combined " + str(count) + " zone(s) with duplicate Initiators into " + str(len(dupInits)) + ".")
		with open("dupInitsRemoved-" + symID + ".json","w") as f:
			json.dump(newDupInits, f)
		print("Duplicate initiator sets:")
		pprint(dupInits)

		dupTargets = findDupTargets(masks)
		newDupTargets, count = removeDupTargets(masks, dupTargets)
		print("Combined " + str(count) + " zone(s) with duplicate Targets into " + str(len(dupTargets)) + ".")
		with open("dupTargetsRemoved-" + symID + ".json","w") as f:
			json.dump(newDupTargets, f)
		print("Duplicate target sets:")
		pprint(dupTargets)	



if __name__ == '__main__':
	main()
