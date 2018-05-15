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

def main():
	URL = os.getenv("MGMTPORT","NONE")
	if URL == "NONE":
		print("Environmental variable MGMTPORT is undefined.")
		exit()
	USER = "admin"
	PASSWORD = "password"
	vmax_api = pyvmax.connect(URL, USER, PASSWORD)
	slo_array_ids = vmax_api.get_slo_arrays()
	with open("symList.json", 'w') as f:
		json.dump(slo_array_ids, f)

if __name__ == '__main__':
	main()
			
