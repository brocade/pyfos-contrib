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


def buildPorts(vmax_api, targetSym):

	ports= {}

	array_directors = vmax_api.get_slo_array_directors(targetSym)
	for j in range(len(array_directors['directorId'])):
		if array_directors['directorId'][j][0:2] == 'FA':
			one_director_ports = vmax_api.get_slo_array_director_ports(targetSym, array_directors['directorId'][j])
			for k in range(len(one_director_ports['symmetrixPortKey'])):
				one_port = vmax_api.get_slo_array_port(targetSym, array_directors['directorId'][j], one_director_ports['symmetrixPortKey'][k]['portId'])
				for l in range(len(one_port['symmetrixPort'])):
					portName = one_port['symmetrixPort'][l]['symmetrixPortKey']['directorId'] + "-" + one_port['symmetrixPort'][l]['symmetrixPortKey']['portId']
					ports[portName] = {}
					ports[portName]['WWNs'] = {}
					ports[portName]['maskingviews'] = {}
					ports[portName]['WWNs'][one_port['symmetrixPort'][l]['identifier']] = 'Present'
					if 'maskingview' in one_port['symmetrixPort'][l].keys():
						for m in range(len(one_port['symmetrixPort'][l]['maskingview'])):
							ports[portName]['maskingviews'][one_port['symmetrixPort'][l]['maskingview'][m]] = 'Present'
	return ports


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
		thePorts = buildPorts(vmax_api, slo_array_ids['symmetrixId'][i])
		with open("ports-" + slo_array_ids['symmetrixId'][i] + ".json",'w') as f:
			json.dump(thePorts, f)
		pprint.pprint(thePorts)
		print("-------------------")

if __name__ == '__main__':
	main()
			
