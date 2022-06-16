"""
Checking Python Version
"""

import sys
py_v = sys.version_info[0:3];
print("Python working via reticulate. Version: {}".format(py_v));
if py_v[0] != 3:
  raise ValueError("Not correct Python Version, must be at least 3.! Please download python from https://www.python.org/ or using the reticulate package in R before continuing!")
else:
    print("Correct Python Version! Ready to GO!")
