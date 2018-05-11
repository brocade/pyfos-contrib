# Bulk Zoning Demo

Although the bulk zoning utility is included in the PyFOS distribution, it may not be possible for you to run it in your environment.

This branch contains the output of the bulk_zoning.py command when run against a switch with no other configuration loaded.

The **bulk_zoning.py** script can be found in the directory **pyfos/utils/zoning** along with the sample configuration file **bulk_zoning.xlsx**.  The utility can be run in two different modes - *check* and *apply*.  The *check* mode allows you to see what changes will be made.  The *apply* mode then allows you to make those changes.

The following command runs the utility in *check* mode:

`bulk_zoning.py -L username -P password -i IP_address --filename=bulk_zoning.xlsx --xlscheck="Ex DC1 Fabric A" -f -1`

*(For details on the command line parameters, consult the comments in the program bulk_zoning.py)*

The file **check.txt** contains the output when this command is run.

The following command runs the utility in *apply* mode:

`bulk_zoning.py -L username -P password -i IP_address --filename=bulk_zoning.xlsx --xlsapply="Ex DC1 Fabric A" -f -1`

The file **apply.txt** contains the output of the utility when this command is run.

# Additional Files:

**cfgshowBefore.txt** - shows the results of running the command `cfgshow` on the switch before the spreadsheet is applied

**cfgshowAfter.txt** - shows the results of running the command `cfgshow` on the switch after the spreadsheet is applied

Note: The files **check.txt** and **apply.txt** contain escape sequences intended to highlight certain lines in the output.  If you notice strange characters at the beginning of lines without seeing the text change colors, your terminal shell may not be interpreting these VT100 control sequences.

