# Bulk Zoning Demo

Although the bulk zoning utility is included in the PyFOS distribution, it may not be possible for you to run it in your environment.

This branch contains the output of the bulk_zoning.py command when run against a switch with no other configurations.

Files:

check.txt - contains the output of the utility when the following command is run:

bulk_zoning.py -i 10.XX.XX.XX --filename=bulk_zoning.xlsx --xlscheck="Ex DC1 Fabric A" -f -1

apply.txt - contains the output of the utility when the following command is run:

bulk_zoning.py -i 10.XX.XX.XX --filename=bulk_zoning.xlsx --xlsapply="Ex DC1 Fabric A" -f -1

cfgshowBefore.txt - shows the results of running the command cfgshow on the switch before the spreadsheet is applied

cfgshowAfter.txt - shows the results of running the command cfgshow on the switch after the spreadsheet is applied

Note: The files check.txt and apply.txt contain escape sequences intended to highlight certain lines in the output.  If you notice strange characters at the beginning of lines without seeing the text change colors, your terminal shell may not be interpreting these VT100 control sequences.

