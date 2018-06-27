# Hanging Zone Cleanup

zoning_hanging_zone_find.py can be used to print or delete zones
that do not contain any online devices in the zone, thus refered as
"hanging zones". If any hanging zones are found, the script will
interactively accept "YES" to remove the zones and save the resulting
CFG or any other input, including non-uppercase "yes", to skip
making Zone DB changes.

CFG save phase will fail if any hanging zones are part of the current
effective cfg. The current effective CFG should be manually updated
to remove the zones from it before the script can be executed
successfully.
