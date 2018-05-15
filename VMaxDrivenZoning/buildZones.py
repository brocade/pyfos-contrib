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
import json
from pprint import pprint

def getPortsforPortgroup(portgroups, ports, portgroup):
	results = []
	for k in portgroups[portgroup]:
		if k[0:2] == "FA":
			WWNArray = getWWNsforDirectorPort(ports, k)
			for i in range(len(WWNArray)):
				results.append(WWNArray[i])
	return results

def getWWNsforDirectorPort(ports, port):
	results = []
	for key in ports[port]['WWNs']:
		results.append(key)
	return results

def getWWNsForHostgroup(hostgroups, hosts, key):
	results = []
	if key in hostgroups:
		for k in hostgroups[key]:
			results.append(k)
	if key in hosts:
		for k in hosts[key]:
			results.append(k)
	return results

def getPrincipalWWNs(maskingviews, portgroups, ports, key):
	return getPortsforPortgroup(portgroups, ports, maskingviews[key]['portGroup'])


def main():
	with open("symList.json", 'r') as f:
		symList = json.load(f)

	for i in range(len(symList['symmetrixId'])):
		symID = symList['symmetrixId'][i]

		print(symID)
		with open('hostgroups-' + symID + '.json') as f:
			hostgroups = json.load(f)
		with open('hosts-' + symID + '.json') as f:
			hosts = json.load(f)
		with open('maskingviews-' + symID + '.json') as f:
			maskingviews = json.load(f)
		with open('ports-' + symID + '.json') as f:
			ports = json.load(f)
		with open('portgroups-' + symID + '.json') as f:
			portgroups = json.load(f)

		print(hosts)
		print('=========================')
		print(hostgroups)
		print('=========================')
		print(maskingviews)
		print('=========================') 
		print(portgroups)
		print('=========================')
		print(ports)
		print("+++++++++++++++++++++++++")

		for key in ports:
			print(getWWNsforDirectorPort(ports, key))

		for key in portgroups:
			print(key, getPortsforPortgroup(portgroups, ports, key))

		print('///////////////////////')

		for key in hostgroups:
			print(key, getWWNsForHostgroup(hostgroups,hosts, key))

		print('\\\\\\\\\\\\\\\\\\\\\\\'')

		for key in maskingviews:
			maskingviews[key]['Targets'] = getPrincipalWWNs(maskingviews, portgroups, ports, key)
			print(key, getPrincipalWWNs(maskingviews, portgroups, ports, key))

		print('<><><><><><><><><><><><><><>')

		for key in maskingviews:
			if 'host' in maskingviews[key]:
				maskingviews[key]['Initiators'] = getWWNsForHostgroup(hostgroups, hosts, maskingviews[key]['host'])
				print('host ',key, getWWNsForHostgroup(hostgroups, hosts, maskingviews[key]['host']))
			elif 'hostGroup' in maskingviews[key]:
				maskingviews[key]['Initiators'] = getWWNsForHostgroup(hostgroups, hosts, maskingviews[key]['hostGroup'])
				print('hostGroup ', key, getWWNsForHostgroup(hostgroups, hosts, maskingviews[key]['hostGroup']))

		with open("merged-" + symID + ".json", 'w') as f:
			json.dump(maskingviews, f)


if __name__ == '__main__':
	main()
