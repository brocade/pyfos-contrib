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

def buildMatchingview(vmax_api, targetSym):
	matchingviews = {}
	masks = vmax_api.get_slo_array_maskingviews(targetSym)
	print(masks)
	for j in range(len(masks['maskingViewId'])):
		mask = vmax_api.get_slo_arary_maskingview(targetSym, masks['maskingViewId'][j])
		for k in range(len(mask['maskingView'])):
			matchingId = mask['maskingView'][k]['maskingViewId']
			matchingviews[matchingId] = {}
			matchingviews[matchingId]['portGroup'] = mask['maskingView'][k]['portGroupId']
			if 'hostGroupId' in mask['maskingView'][k]:
				matchingviews[matchingId]['hostGroup'] = mask['maskingView'][k]['hostGroupId']
			elif 'hostId' in mask['maskingView'][k]:
				matchingviews[matchingId]['host'] = mask['maskingView'][k]['hostId']
			else:
				print("Neither host or hostgroup found.")
	return matchingviews

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
		print("Entering buildMatchingview")
		maskingviews = buildMatchingview(vmax_api, slo_array_ids[i])
		with open("maskingviews-" + slo_array_ids[i] + ".json", 'w') as f:
			json.dump(maskingviews, f)
		pprint.pprint(maskingviews)
		print("Leaving buildMatchingview")

if __name__ == "__main__":
	main()
