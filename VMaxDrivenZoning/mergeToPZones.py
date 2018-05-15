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
from __future__ import print_function
import sys
import pprint
import json

def createPZoneDefn(name, members, pmembers):

	zone = {
				"zone-name": name,
				"zone-type": 1,
				"member-entry":
					{
						"entry-name": members,
						"principal-entry-name": pmembers
					}
			}

	return zone

def convertWWNS(WWNList):
	converted = []
	for i in range(len(WWNList)):
		converted.append(addColons(WWNList[i]))
	return converted

def addColons(WWN):
	tmp = WWN[0:2] + ":" + WWN[2:4] + ":" + WWN[4:6] + ":" + WWN[6:8] + ":" + WWN[8:10] + ":" + WWN[10:12] + ":" + WWN[12:14] + ":" + WWN[14:16]
	return(tmp)

def main():
	zones = []

	with open(sys.argv[1], 'r') as f:
		masks = json.load(f)

	for key in masks:
		if (len(masks[key]['Initiators']) > 0 and len(masks[key]['Targets']) > 0):
			convertedInitiators = convertWWNS(masks[key]['Initiators'])
			convertedTargets = convertWWNS(masks[key]['Targets'])
			zoneDefn = createPZoneDefn(key, convertedInitiators,convertedTargets)
			zones.append(zoneDefn)
	pprint.pprint(zones)
	with open("pzones.json","w") as f:
		json.dump(zones, f)


if __name__ == "__main__":
	main()