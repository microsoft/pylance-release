import sys
print(sys.version)
import os
print(os.getcwd())

from test_another_module import print_stuff
print_stuff()