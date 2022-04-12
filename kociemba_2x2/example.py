# ############################ Examples how to use the cube solver #####################################################

cubestring = 'FFBLBRDLDUBRRFDDLRLUUUFB'  # cube definition string of cube we want to solve
# See module enums.py for the format of the cube definition string

# ######################### Method 1: directly call the solve routine# #################################################
#  Uncomment this part if you want to use method 1

import solver as sv
a = sv.solve(cubestring)
print(a)
quit()

