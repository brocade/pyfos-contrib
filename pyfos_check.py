#!/usr/bin/python
# Copyright 2018 Brocade Storage Networking Division, Broadcom.  All rights reserved.
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

"""
:mod:`pyfos_check.py` - Reads and reports the version number of all the libraries in PyFOS.

Intended as a tool to validate that the PyFOS libraries were installed properly, are accessible, that any
libraries imported in by the PyFOS libraries are accessible, and that a supported version of Python is used.

* inputs:
    * None

* Outputs:
    * Writes a table with the module, import status, and version number to STD OUT

+------------+----------------+----------------------------------------------------------------------------------+
| Version    | Last Edit      | Description                                                                      |
+============+================+==================================================================================+
| 1.0.0      | 11 Dec 2018    | Initial release                                                                  |
+------------+----------------+----------------------------------------------------------------------------------+
"""

__author__ = 'Jack Consoli'
__copyright__ = 'Copyright 2018 Brocade Storage Networking Division, Broadcom'
__date__ = '11 Dec 2018'
__license__ = 'Apahche License, Version 2.0'
__email__ = 'jack.consoli@broadcom.com'
__maintainer__ = 'Jack Consoli'
__status__ = 'Submitted'
__version__ = '1.0.0'

import sys
import importlib

imports = [
    'pyfos.pyfos_auth',
    'pyfos.pyfos_brocade_access_gateway',
    'pyfos.pyfos_brocade_chassis',
    'pyfos.pyfos_brocade_extension_ipsec_policy',
    'pyfos.pyfos_brocade_extension_ip_interface',
    'pyfos.pyfos_brocade_extension_ip_route',
    'pyfos.pyfos_brocade_extension_tunnel',
    'pyfos.pyfos_brocade_fabric',
    'pyfos.pyfos_brocade_fdmi',
    'pyfos.pyfos_brocade_fibrechannel',
    'pyfos.pyfos_brocade_fibrechannel_configuration',
    'pyfos.pyfos_brocade_fibrechannel_diagnostics',
    'pyfos.pyfos_brocade_fibrechannel_logical_switch',
    'pyfos.pyfos_brocade_fibrechannel_switch',
    'pyfos.pyfos_brocade_fibrechannel_trunk',
    'pyfos.pyfos_brocade_fru',
    'pyfos.pyfos_brocade_gigabitethernet',
    'pyfos.pyfos_brocade_license',
    'pyfos.pyfos_brocade_logging',
    'pyfos.pyfos_brocade_maps',
    'pyfos.pyfos_brocade_media',
    'pyfos.pyfos_brocade_name_server',
    'pyfos.pyfos_brocade_operation_show_status',
    'pyfos.pyfos_brocade_operation_supportsave',
    'pyfos.pyfos_brocade_security',
    'pyfos.pyfos_brocade_time',
    'pyfos.pyfos_brocade_zone',
    'pyfos.pyfos_login',
    'pyfos.pyfos_rest_util',
    'pyfos.pyfos_type',
    'pyfos.pyfos_util',
    'pyfos.pyfos_version',
    'pyfos.pyfos_vobject',
    'pyfos.utils.brcd_cli',
    'pyfos.utils.brcd_util',
    'pyfos.utils.brcd_zone_util',
    'pyfos.utils.access_gateway.device_list_show',
    'pyfos.utils.access_gateway.fport_list_show',
    'pyfos.utils.access_gateway.nport_map_add',
    'pyfos.utils.access_gateway.nport_map_del',
    'pyfos.utils.access_gateway.nport_map_modify',
    'pyfos.utils.access_gateway.nport_map_show',
    'pyfos.utils.access_gateway.nport_settings_modify',
    'pyfos.utils.access_gateway.nport_settings_show',
    'pyfos.utils.access_gateway.policy_modify',
    'pyfos.utils.access_gateway.policy_show',
    'pyfos.utils.access_gateway.port_group_create_add',
    'pyfos.utils.access_gateway.port_group_del',
    'pyfos.utils.access_gateway.port_group_fport_add',
    'pyfos.utils.access_gateway.port_group_mode',
    'pyfos.utils.access_gateway.port_group_remove',
    'pyfos.utils.access_gateway.port_group_show',
    'pyfos.utils.chassis.chassis_name_set',
    'pyfos.utils.chassis.chassis_show',
    'pyfos.utils.chassis.chassis_vf_enabled_set',
    'pyfos.utils.chassis.ha_status_show',
    'pyfos.utils.config.switch_config_apply',
    'pyfos.utils.config.switch_config_diff',
    'pyfos.utils.config.switch_config_dump',
    'pyfos.utils.config.switch_config_obj',
    'pyfos.utils.config.switch_config_util',
    'pyfos.utils.configure.configure_dport_mode_modify',
    'pyfos.utils.configure.configure_fabric_modify',
    'pyfos.utils.configure.configure_fabric_show',
    'pyfos.utils.configure.configure_port_name_set',
    'pyfos.utils.configure.configure_port_show',
    'pyfos.utils.configure.configure_zone_show',
    'pyfos.utils.configure.f_port_login_settings_get',
    'pyfos.utils.configure.f_port_login_settings_modify',
    'pyfos.utils.configure.switch_configuration_get',
    'pyfos.utils.configure.switch_configuration_modify',
    'pyfos.utils.dns_config.dns_config_get',
    'pyfos.utils.dns_config.dns_config_modify',
    'pyfos.utils.extension.extensionShell',
    'pyfos.utils.extension.extension_circuit_create',
    'pyfos.utils.extension.extension_circuit_delete',
    'pyfos.utils.extension.extension_circuit_modify',
    'pyfos.utils.extension.extension_circuit_show',
    'pyfos.utils.extension.extension_circuit_statistics_pktloss_show',
    'pyfos.utils.extension.extension_circuit_statistics_show',
    'pyfos.utils.extension.extension_ipsec_policy_create',
    'pyfos.utils.extension.extension_ipsec_policy_delete',
    'pyfos.utils.extension.extension_ipsec_policy_modify',
    'pyfos.utils.extension.extension_ipsec_policy_show',
    'pyfos.utils.extension.extension_ip_interface_create',
    'pyfos.utils.extension.extension_ip_interface_delete',
    'pyfos.utils.extension.extension_ip_interface_modify',
    'pyfos.utils.extension.extension_ip_interface_show',
    'pyfos.utils.extension.extension_ip_route_create',
    'pyfos.utils.extension.extension_ip_route_delete',
    'pyfos.utils.extension.extension_ip_route_modify',
    'pyfos.utils.extension.extension_tunnel_create',
    'pyfos.utils.extension.extension_tunnel_delete',
    'pyfos.utils.extension.extension_tunnel_modify',
    'pyfos.utils.extension.extension_tunnel_show',
    'pyfos.utils.extension.extension_tunnel_statistics_show',
    'pyfos.utils.extension.gigabitethernet_enabled_state_set',
    'pyfos.utils.extension.gigabitethernet_show',
    'pyfos.utils.extension.gigabitethernet_speed_set',
    'pyfos.utils.extension.gigabitethernet_statistics_show',
    'pyfos.utils.fdmi.fdmi_show',
    'pyfos.utils.fru.blade_extncfg_set',
    'pyfos.utils.fru.blade_show',
    'pyfos.utils.fru.fan_show',
    'pyfos.utils.fru.powersupply_show',
    'pyfos.utils.license.license_show',
    'pyfos.utils.logging.audit_modify',
    'pyfos.utils.logging.audit_show',
    'pyfos.utils.logging.syslog_create',
    'pyfos.utils.logging.syslog_delete',
    'pyfos.utils.logging.syslog_facility_modify',
    'pyfos.utils.logging.syslog_facility_show',
    'pyfos.utils.logging.syslog_modify',
    'pyfos.utils.logging.syslog_show',
    'pyfos.utils.logical_switch.logical_switch_create',
    'pyfos.utils.logical_switch.logical_switch_delete',
    'pyfos.utils.logical_switch.logical_switch_modify',
    'pyfos.utils.logical_switch.logical_switch_show',
    'pyfos.utils.maps.maps_config_patch',
    'pyfos.utils.maps.maps_config_show',
    'pyfos.utils.maps.maps_dashboard_misc_patch',
    'pyfos.utils.maps.maps_dashboard_misc_show',
    'pyfos.utils.maps.maps_dashboard_rule_show',
    'pyfos.utils.maps.maps_get_ssp_report',
    'pyfos.utils.maps.maps_group_create',
    'pyfos.utils.maps.maps_group_delete',
    'pyfos.utils.maps.maps_group_patch',
    'pyfos.utils.maps.maps_group_show',
    'pyfos.utils.maps.maps_paused_cfg_delete',
    'pyfos.utils.maps.maps_paused_cfg_post',
    'pyfos.utils.maps.maps_paused_cfg_show',
    'pyfos.utils.maps.maps_policy_create',
    'pyfos.utils.maps.maps_policy_delete',
    'pyfos.utils.maps.maps_policy_enable',
    'pyfos.utils.maps.maps_policy_patch',
    'pyfos.utils.maps.maps_policy_show',
    'pyfos.utils.maps.maps_rule_create',
    'pyfos.utils.maps.maps_rule_delete',
    'pyfos.utils.maps.maps_rule_show',
    'pyfos.utils.maps.maps_rule_update',
    'pyfos.utils.maps.maps_system_resources_show',
    'pyfos.utils.maps.monitoring_system_matrix',
    'pyfos.utils.media.media_rdp_show',
    'pyfos.utils.misc.device_find',
    'pyfos.utils.misc.fabric_show',
    'pyfos.utils.name_server.name_server_show',
    'pyfos.utils.port.port_avail_show',
    'pyfos.utils.port.port_credit_recovery_state_set',
    'pyfos.utils.port.port_dport_run',
    'pyfos.utils.port.port_fault_delay_state_set',
    'pyfos.utils.port.port_isl_mode_state_set',
    'pyfos.utils.port.port_los_tov_state_set',
    'pyfos.utils.port.port_mirror_state_set',
    'pyfos.utils.port.port_name_set',
    'pyfos.utils.port.port_npiv_state_set',
    'pyfos.utils.port.port_resilience_set',
    'pyfos.utils.port.port_show',
    'pyfos.utils.port.port_sim_state_set',
    'pyfos.utils.port.port_state_set',
    'pyfos.utils.port.port_stats_show',
    'pyfos.utils.port.port_trunk_state_set',
    'pyfos.utils.rasadmin.log_quiet_control_get',
    'pyfos.utils.rasadmin.log_quiet_control_modify',
    'pyfos.utils.rasadmin.log_setting_keep_alive_period_get',
    'pyfos.utils.rasadmin.log_setting_keep_alive_period_set',
    'pyfos.utils.rasadmin.raslog_current_severity_set',
    'pyfos.utils.rasadmin.raslog_get',
    'pyfos.utils.rasadmin.raslog_message_enabled_set',
    'pyfos.utils.rasadmin.raslog_module_get',
    'pyfos.utils.rasadmin.raslog_module_set',
    'pyfos.utils.rasadmin.raslog_syslog_enabled_set',
    'pyfos.utils.supportsave.supportsave',
    'pyfos.utils.switch.switch_ag_mode_set',
    'pyfos.utils.switch.switch_banner_set',
    'pyfos.utils.switch.switch_name_set',
    'pyfos.utils.switch.switch_show',
    'pyfos.utils.switch_ip_config.switch_ip_config_get',
    'pyfos.utils.switch_ip_config.switch_ip_config_modify',
    'pyfos.utils.system_security.auth_spec_set',
    'pyfos.utils.system_security.auth_spec_show',
    'pyfos.utils.system_security.ipfilter_policy_activate_set',
    'pyfos.utils.system_security.ipfilter_policy_clone_set',
    'pyfos.utils.system_security.ipfilter_policy_create',
    'pyfos.utils.system_security.ipfilter_policy_delete',
    'pyfos.utils.system_security.ipfilter_policy_show',
    'pyfos.utils.system_security.ipfilter_rule_create',
    'pyfos.utils.system_security.ipfilter_rule_delete',
    'pyfos.utils.system_security.ipfilter_rule_show',
    'pyfos.utils.system_security.ldap_role_map_create',
    'pyfos.utils.system_security.ldap_role_map_delete',
    'pyfos.utils.system_security.ldap_role_map_set',
    'pyfos.utils.system_security.ldap_role_map_show',
    'pyfos.utils.system_security.ldap_server_create',
    'pyfos.utils.system_security.ldap_server_delete',
    'pyfos.utils.system_security.ldap_server_set',
    'pyfos.utils.system_security.ldap_server_show',
    'pyfos.utils.system_security.passwd_modify',
    'pyfos.utils.system_security.password_cfg_set',
    'pyfos.utils.system_security.password_cfg_show',
    'pyfos.utils.system_security.radius_server_create',
    'pyfos.utils.system_security.radius_server_delete',
    'pyfos.utils.system_security.radius_server_set',
    'pyfos.utils.system_security.radius_server_show',
    'pyfos.utils.system_security.seccertmgmt_action',
    'pyfos.utils.system_security.seccertmgmt_create',
    'pyfos.utils.system_security.seccertmgmt_delete',
    'pyfos.utils.system_security.seccertmgmt_show',
    'pyfos.utils.system_security.seccryptocfgtemplate_show',
    'pyfos.utils.system_security.seccryptocfg_apply_set',
    'pyfos.utils.system_security.seccryptocfg_delete',
    'pyfos.utils.system_security.seccryptocfg_export',
    'pyfos.utils.system_security.seccryptocfg_import',
    'pyfos.utils.system_security.seccryptocfg_show',
    'pyfos.utils.system_security.seccryptocfg_verify',
    'pyfos.utils.system_security.sshutil_key_create',
    'pyfos.utils.system_security.sshutil_key_delete',
    'pyfos.utils.system_security.sshutil_key_show',
    'pyfos.utils.system_security.sshutil_modify',
    'pyfos.utils.system_security.sshutil_public_key_delete',
    'pyfos.utils.system_security.sshutil_public_key_modify',
    'pyfos.utils.system_security.sshutil_public_key_show',
    'pyfos.utils.system_security.sshutil_show',
    'pyfos.utils.system_security.tacacs_server_create',
    'pyfos.utils.system_security.tacacs_server_delete',
    'pyfos.utils.system_security.tacacs_server_set',
    'pyfos.utils.system_security.tacacs_server_show',
    'pyfos.utils.system_security.user_config_create',
    'pyfos.utils.system_security.user_config_delete',
    'pyfos.utils.system_security.user_config_set',
    'pyfos.utils.system_security.user_config_show',
    'pyfos.utils.system_security.user_specific_password_cfg_create',
    'pyfos.utils.system_security.user_specific_password_cfg_delete',
    'pyfos.utils.system_security.user_specific_password_cfg_set',
    'pyfos.utils.system_security.user_specific_password_cfg_show',
    'pyfos.utils.time.clock_server_set',
    'pyfos.utils.time.clock_server_show',
    'pyfos.utils.time.time_zone_name_set',
    'pyfos.utils.time.time_zone_set',
    'pyfos.utils.time.time_zone_show',
    'pyfos.utils.trunk.port_trunk_area_create_add',
    'pyfos.utils.trunk.port_trunk_area_delete',
    'pyfos.utils.trunk.port_trunk_area_show',
    'pyfos.utils.trunk.port_trunk_area_show_all',
    'pyfos.utils.trunk.trunk_perf_show',
    'pyfos.utils.trunk.trunk_perf_show_all',
    'pyfos.utils.trunk.trunk_show',
    'pyfos.utils.trunk.trunk_show_all',
    'pyfos.utils.zoning.bulk_zoning',
    'pyfos.utils.zoning.zone_allow_pair',
    'pyfos.utils.zoning.zone_allow_pair_to_peer',
    'pyfos.utils.zoning.zoning_alias_create_add',
    'pyfos.utils.zoning.zoning_alias_delete',
    'pyfos.utils.zoning.zoning_alias_remove',
    'pyfos.utils.zoning.zoning_cfg_abort',
    'pyfos.utils.zoning.zoning_cfg_clear',
    'pyfos.utils.zoning.zoning_cfg_create_add',
    'pyfos.utils.zoning.zoning_cfg_delete',
    'pyfos.utils.zoning.zoning_cfg_disable',
    'pyfos.utils.zoning.zoning_cfg_enable',
    'pyfos.utils.zoning.zoning_cfg_remove',
    'pyfos.utils.zoning.zoning_cfg_save',
    'pyfos.utils.zoning.zoning_cfg_show',
    'pyfos.utils.zoning.zoning_def_zone',
    'pyfos.utils.zoning.zoning_hanging_zone_find',
    'pyfos.utils.zoning.zoning_pzone_create_add',
    'pyfos.utils.zoning.zoning_pzone_delete',
    'pyfos.utils.zoning.zoning_pzone_remove',
    'pyfos.utils.zoning.zoning_zone_create_add',
    'pyfos.utils.zoning.zoning_zone_delete',
    'pyfos.utils.zoning.zoning_zone_remove',

]
modules = {}
modules['Module'] = {'v': 'Version', 'i': 'Import'}
for buf in imports:
    try:
        mod = importlib.import_module(buf)
        try:
            ver = mod.__version__
        except:
            ver = 'Unknown'
        modules[buf] = {'v': ver, 'i': 'Success'}
    except ImportError:
        modules[buf] = {'v': '', 'i': 'Failed'}

_LEN_VER = 10  # Width of Version column
_LEN_STATUS = 10  # Width of Status column
_LEN_MOD = 70  # Width of Module column

# Check the Python version
msg = '\nPython Version: '
try:
    ver = sys.version
    msg += ver
    try:
        ver = ver.split(' ')[0]
        ol = ver.split('.')
        if int(ol[0]) != 3 or int(ol[1]) < 3:
            msg += '\nWARNING: Unsupported version  of Python. Python must be version  3.3 or higher.'
    except:
        msg += '\nInvalid version returned from sys.version'
except:
    msg += 'Unable to read sys.version'
print(msg)

# Print a description of what this module does.
msg = '\n\nThis is a simple pass/fail test to validate that PyFOS'
msg += '\nlibraries were installed properly, are accessible, and that'
msg += '\nall modules imported by the PyFOS libraries are installed'
msg += '\nand accessible. The list of libraries checked was complete'
msg += '\nfor PyFOS 1.1.0. A failure to import may be due to the'
msg += '\ninability to locate the module itself or to locate a module'
msg += '\nwithin the module being imported. A failure to import a'
msg += '\nmodule is only significant if you intend to use that module.\n'
msg += '\nVersion numbers for PyFOS modules were planned but not'
msg += '\navailable at the time this was written.\n'
print(msg)

# Now generate a simple report to STD_OUT
s = '-'
for i in range(0, _LEN_VER + _LEN_STATUS + _LEN_MOD):
    s = s + '-'
print(s)
ol = ['Module']
ol.extend(imports)
for mod in ol:
    mod_v = '| ' + mod
    space = ''
    for i in range(0, _LEN_MOD - len(mod_v) if _LEN_MOD - len(mod_v) > 0 else 0):
        space = space + ' '
    mod_v = mod_v + space
    import_v = '| ' + modules[mod]['i']
    space = ''
    for i in range(0, _LEN_STATUS - len(import_v) if _LEN_STATUS - len(import_v) > 0 else 0):
        space = space + ' '
    import_v = import_v + space
    ver_v = '| ' + modules[mod]['v']
    space = ''
    for i in range(0, _LEN_STATUS - len(ver_v) if _LEN_STATUS - len(ver_v) > 0 else 0):
        space = space + ' '
    ver_v = ver_v + space
    print(mod_v + import_v + ver_v + '|')
    print(s)

