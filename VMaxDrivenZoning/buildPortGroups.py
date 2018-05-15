#!/usr/bin/python
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
import pyvmax
import pprint
import json
import os

def buildPortgroups(vmax_api, targetSym):

	portgroups = {}
	groups = vmax_api.get_slo_array_portgroups(targetSym)
	for i in range(len(groups['portGroupId'])):
		group = vmax_api.get_slo_array_portgroup(targetSym, groups['portGroupId'][i])
		for j in range(len(group['portGroup'])):
			gelement = group['portGroup'][j]
			portgroups[gelement['portGroupId']] = {}
			for k in range(len(gelement['symmetrixPortKey'])):
				portgroups[gelement['portGroupId']][gelement['symmetrixPortKey'][k]['directorId'] + '-' + gelement['symmetrixPortKey'][k]['portId']] = "Present"
	return portgroups

def main():
	URL = os.getenv("MGMTPORT","NONE")
	if URL == "NONE":
		print("Environmental variable MGMTPORT is undefined.")
		exit()
	USER = "admin"
	PASSWORD = "password"
	vmax_api = pyvmax.connect(URL, USER, PASSWORD)
	with open('symList.json') as f:
		slo_array_ids = json.load(f)
	for i in range(len(slo_array_ids['symmetrixId'])):
		thePortgroups = buildPortgroups(vmax_api, slo_array_ids['symmetrixId'][i])
		with open("portgroups-" + slo_array_ids['symmetrixId'][i] + ".json",'w') as f:
			json.dump(thePortgroups, f)
		pprint.pprint(thePortgroups)
		print("-------------------")

if __name__ == '__main__':
	main()
			
