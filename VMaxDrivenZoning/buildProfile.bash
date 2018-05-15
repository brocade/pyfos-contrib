#!/usr/bin/env bash

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

(set -o igncr) 2>/dev/null && set -o igncr; # this comment is needed for Cygwin

# Gather needed information from VMax creating a separate data file for each

echo "Building Sym List"
./buildSyms.py
echo "Building Masking Views"
./buildMaskingviews.py
echo "Building Host lists"
./buildHost.py
echo "Building Host Groups"
./buildHostgroups.py
echo "Building Ports"
./buildPorts.py
echo "Building Port Groups"
./buildPortGroups.py


# Merge the information into Initiator/Target groupings
echo "Combining information into zoning data"
./buildZones.py 


# In order to detect duplicate Initiators, Targets, or both, a hash is created
echo "Preparing for zone analysis"
./addHash.py

# Once hashes are in place, look for different types of duplicates and combine
echo "Creating zoning alternatives"
./optimize.py

# This batch file does not make the selection of the optimization method if any
# to be used.  Once the desired optimization has been determined, run
#./mergeToPZones.py
# to create the final pzones.json with the proper format and then run
# pzoneLoadAndGo.py pzones.json
# to install the zones on the fabric.

