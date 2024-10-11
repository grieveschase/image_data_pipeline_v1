import sys

min_major_version = 3
min_minor_version = 9

if (sys.version_info[0] < min_major_version) or (sys.version_info[1] < 9):
    print('Bad Python Version')
    sys.exit("Requires Python Version 3.9 or higher")

sys.exit(0)