# VMax-Based Zoning

This sample code extracts information from EMC VMax arrays and uses that information to create zones for a Brocade Fibre Channel SAN.  A utility generates three different types of zone optimizations.  A simple tool is also included to apply the generated zones to a SAN fabric.

This code takes advantage of the PyFOS library located at _https://github.com/brocade/pyfos_ and the PyVMAX library located at _https://github.com/scottbri/PyVMAX_.

### Overview

VMax storage arrays use _masking views_ to determine which hosts or host groups can access logical volumes.  These views also determine which ports on the VMax can be used to present each volume.  Information about the masking views, hosts, host groups, port groups, and ports is kept in separate data structures on the VMax.  This program collects all of the required data structures, combines them, and then maps each view into the initiators and targets in the associated port groups, ports, hosts, and host groups.  Because the VMax array can support many different types of interfaces, only those views which contain Fibre Channel-mapped initiators __and__ targets are passed on to the next step.

In many cases, masking views differ only by the logical volume on the VMax.  The host/hostgroups and port/portgoups are exactly the same.  This means that optimization can be performed where either duplicate zones can be eliminated or, where safe, zones can be combined.  In doing so, the number of zones on the SAN can be drastically reduced making them easier to understand and causing them to consume fewer resources on the SAN fabric.

The optimizations take advantage of __Peer Zoning__ on the fabric.  For a complete discussion on Peer Zoning, please visit the Brocade website at _https://www.brocade.com_.

### Step for Running the Code

1.  Set the appropriate value for each of the following global environmental variables:
	* __MGMTPORT__ - URL for the Unisphere management port such as "https://10.xx.xx.xx:8443"
	* __SWITCHIP__ - IP address of a switch in the fabric
	* __VFID__ - Virtual fabric on the SAN in which to apply the zoning.  For environments without virtual fabrics, this variable should be set to -1.
2.  Run the script __buildProfile.bash__.
	This script will create a number of .json files that contain masking, host, and port information from the VMax.  It will also produce files with the zoning information generated for each VMax array.  The prefix of the file name indicates the type of optimization applied with the serial number of the VMax array following.  The files of interest are:
	* unopt-\<VMax-Serial\>.json - No optimization applied
	* dupsRemoved-\<VMax-Serial\>.json - exact duplicate zones removed
	* dupInitsRemoved-\<VMax-Serial\>.json - zones with duplicate initiators combined
	* dupTargetsRemoved-\<VMax-Serial\>.json - zones with duplicate targets combined

	_Note:  If one is not familiar with Peer Zoning introduced in FOS 7.4, the last two forms of optimization may be of concern because they would seemingly allow undesired communication between pairs of initiators and targets.  RSCNs may also be assumed to be an issue.  Those worried about these issues should consult the Brocade website as described above as Peer Zoning addresses these concerns._
	
3. For each VMax, select the approprpriate type of optimization and run the following commands:
	* __mergeToPZones.py \<optimization_type\>-\<VMax-Serial\>.json__
	* __pzoneLoadAndGo.py__

This sample code will change nothing on the VMax arrays and will only update the zoning on the SAN array if the script __pzoneLoadAndGo.py__ is executed.