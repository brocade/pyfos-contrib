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
import hashlib

def makeMd5(array):
	tmp = hashlib.md5()
	for i in range(len(array)):
		tmp.update(array[i])
	return tmp.hexdigest()

def main():

	with open("symList.json","r") as f:
		symList = json.load(f)

	for i in range(len(symList["symmetrixId"])):

		symID = symList["symmetrixId"][i]

		newZones = {}

		with open("merged-" + symID + ".json", 'r') as f:
			zoneFile = json.load(f)

		for k in zoneFile:
			if (len(zoneFile[k]['Initiators']) > 0) and (len(zoneFile[k]['Targets']) > 0):
				sortedInits = sorted(zoneFile[k]['Initiators'])
				sortedTargets = sorted(zoneFile[k]['Targets'])
				sortedWWNs = sorted(sortedInits + sortedTargets)
				sortedWWNs = sorted((sortedInits + sortedTargets))
				zoneFile[k]['InitHash'] = makeMd5(sortedInits)
				zoneFile[k]['TargetHash'] = makeMd5(sortedTargets)
				zoneFile[k]['WWNsHash'] = makeMd5(sortedWWNs)
				newZones[k] = zoneFile[k]
			else:
				pass

		with open("hashed-" + symID + ".json",'w') as f:
			json.dump(newZones, f)

if __name__ == "__main__":
	main()
