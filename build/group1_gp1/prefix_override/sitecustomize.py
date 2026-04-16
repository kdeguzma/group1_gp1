import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/vboxuser/enpm605_projects/group1_gp1/install/group1_gp1'
