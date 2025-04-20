import numpy as np

def vert_force_to_thrusters(force):
    ind_force = force/4
    
    command = np.zeros(8)
    command[0:4] = ind_force

    return command

def yaw_force_to_thrusters(force):
    ind_force = force/4
    
    command = np.zeros(8)
    command[4] = -1*ind_force
    command[5] = ind_force
    command[6] = ind_force
    command[7] = -1*ind_force

    return command
