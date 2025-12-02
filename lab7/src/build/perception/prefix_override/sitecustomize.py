import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cc/ee106a/fa25/class/ee106a-add/106A-CATCH/lab7/src/install/perception'
