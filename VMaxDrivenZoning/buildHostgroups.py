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
import argparse
import os
import sys
import logging
sys.path.insert(0, os.path.abspath('..'))

import pyvmax
import pprint
import json

def buildHostgroupTable(vmax_api, targetSym):

	hostgroups = {}
	groups = vmax_api.get_slo_array_hostgroups(targetSym)
	for i in range(len(groups['hostGroupId'])):
		group = vmax_api.get_slo_array_hostgroup(targetSym, groups['hostGroupId'][i])
		for j in range(len(group['hostGroup'])):
			hostgroups[group['hostGroup'][j]['hostGroupId']] = {}
			for k in range(len(group['hostGroup'][j]['host'])):
				initiator = group['hostGroup'][j]['host'][k]['initiator']
				for l in range(len(initiator)):
					hostgroups[group['hostGroup'][j]['hostGroupId']][initiator[l]] = 'Present'
	return hostgroups

def main():

	URL = os.getenv("MGMTPORT","NONE")
	if URL == "NONE":
		print("Environmental variable MGMTPORT is undefined.")
		exit()
	USER = "admin"
	PASSWORD = "password"
	vmax_api = pyvmax.connect(URL, USER, PASSWORD)
	print(vmax_api.rest.json_to_str(vmax_api.get_version()))
	with open('symList.json') as f:
		symList = json.load(f)
	slo_array_ids = symList['symmetrixId']
	print(slo_array_ids)
	for i in range(len(slo_array_ids)):
		print("Entering buildHostgroupTable")
		hostgroupTable = buildHostgroupTable(vmax_api, slo_array_ids[i])
		with open("hostgroups-" + slo_array_ids[i] + ".json",'w') as f:
			json.dump(hostgroupTable, f)
		pprint.pprint(hostgroupTable)
		print("Leaving buildHostgroupTable")

if __name__ == "__main__":
	main()
