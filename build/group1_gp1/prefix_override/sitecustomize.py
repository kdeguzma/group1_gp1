import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/kdeguzma/Documents/group1_gp1/install/group1_gp1'
