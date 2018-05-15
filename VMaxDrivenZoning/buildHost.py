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

def reorgHostTable(hostTable):
	hosts = {}
	for host in hostTable:
		if host not in hosts:
			hosts[host] = {}
		for initiator in hostTable[host]['initiators']:
			hosts[host][initiator] = 'Present'
	return hosts

def buildHostTable(vmax_api, targetSym):
	hostTable = {}
	array_hosts = vmax_api.get_slo_array_hosts(targetSym)
	for j in range(len(array_hosts)):
		next_host = vmax_api.get_slo_array_host(targetSym, array_hosts['hostId'][j])
		print(next_host)
		for k in range(len(next_host['host'])):
			initiators = []
			maskingviews = []
			for l in range(len(next_host['host'][k]['initiator'])):
				initiators.append(next_host['host'][k]['initiator'][l])
			for l in range(len(next_host['host'][k]['maskingview'])):
				maskingviews.append(next_host['host'][k]['maskingview'][l])
			hostTable[array_hosts['hostId'][j]] = {}
			hostTable[array_hosts['hostId'][j]]['initiators'] = initiators
			hostTable[array_hosts['hostId'][j]]['maskingviews'] = maskingviews
	pprint.pprint(hostTable)
	return hostTable

def main():

	URL = os.getenv("MGMTPORT","NONE")
	if URL == "NONE":
		print("Environmental variable MGMTPORT is undefined.")
		exit()
	USER = "admin"
	PASSWORD = "password"
	vmax_api = pyvmax.connect(URL, USER, PASSWORD)
	print(vmax_api.rest.json_to_str(vmax_api.get_version()))
	with open("symList.json") as f:
		symList = json.load(f)
	slo_array_ids = symList['symmetrixId']
	print(slo_array_ids)
	for i in range(len(slo_array_ids)):
		print("Entering buildHostTable")
		hostTable = buildHostTable(vmax_api, slo_array_ids[i])
		maskTable = reorgHostTable(hostTable)
		with open("hosts-" + slo_array_ids[i] + ".json",'w') as f:
			json.dump(maskTable, f)
		pprint.pprint(maskTable)
		print("Leaving buildHostTable")



if __name__ == "__main__":
	main()
