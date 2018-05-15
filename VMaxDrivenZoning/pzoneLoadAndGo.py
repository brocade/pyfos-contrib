#!/usr/bin/env python3
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

# This program is a hacked version of the utility pzonecreate.py that is 
# included in the standard distribution of PyFOS.  

import pyfos.pyfos_auth as pyfos_auth
import pyfos.pyfos_zone as pyfos_zone
import sys
import pyfos.utils.brcd_zone_util as brcd_zone_util
import pyfos.utils.brcd_util as brcd_util
import json
import os

isHttps = "0"

# The utility function needed this function defined.
def usage():
    pass

def pzonecreate(session, zones):

    new_defined = pyfos_zone.defined_configuration()
    new_defined.set_zone(zones)
    result = new_defined.post(session)
    return result


def __pzonecreate(session, name, members, pmembers):

    with open('pzones.json','r') as f:
        zones = json.load(f)
    return pzonecreate(session, zones)


def main(argv):
    switchIP = os.getenv("SWITCHIP","NONE")
    vfid = os.getenv("VFID","NONE")
    if switchIP == "NONE" or vfid == "NONE":
        print("Environmental variables SWITCHIP and/or VFID are not set")
        exit()
    # Bogus arguments included here to get past forced argument checking.
    # Actual values are read from the data file.
    inputs = {'vfid': -1, 'members': ['1234567890abcdef'], 'pmembers': ['1234567887654321'], 'login': 'admin', 'name': 'test1', 'ipaddr': switchIP, 'password': 'password'}
    
    session = pyfos_auth.login(inputs["login"], inputs["password"],
                               inputs["ipaddr"], isHttps)
    if pyfos_auth.is_failed_login(session):
        print("login failed because",
              session.get(pyfos_auth.CREDENTIAL_KEY)
              [pyfos_auth.LOGIN_ERROR_KEY])
        sys.exit()

    brcd_util.exit_register(session)

    vfid = None
    if 'vfid' in inputs:
        vfid = inputs['vfid']

    if vfid is not None:
        pyfos_auth.vfid_set(session, vfid)

    brcd_zone_util.zone_name_members_pmembers_func(
            session, inputs, usage, __pzonecreate)

    pyfos_auth.logout(session)


if __name__ == "__main__":
    main(sys.argv[1:])
