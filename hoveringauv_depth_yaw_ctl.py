import holoocean
import numpy as np
from pynput import keyboard
import matplotlib.pyplot as plt
import time

from helper_functions import vert_force_to_thrusters, yaw_force_to_thrusters

scenario = {
    "name": "depth_yaw_ctl",
    "world": "PierHarbor",
    "package_name": "Ocean",
    "main_agent": "auv0",
    "ticks_per_sec": 10,
    "agents": [
        {
            "agent_name": "auv0",
            "agent_type": "HoveringAUV",
            "sensors": [
                {
                    "sensor_type": "RGBCamera",
                    "socket": "CameraSocket",
                    "configuration": {
                        "CaptureWidth": 512,
                        "CaptureHeight": 512
                    }
                },
                {
                    "sensor_type": "DynamicsSensor",
                    # "configuration":{
                    #     "UseRPY": False # Use quaternion
                    # }
                },
            ],
            "control_scheme": 0,
            "location": [-43,112,-5],
            "rotation": [0, 0, 0]
        }
    ]
}


depth_command = -100
heading_command = 146

pressed_keys = list()
force = 25

def on_press(key):
    global pressed_keys
    if hasattr(key, 'char'):
        pressed_keys.append(key.char)
        pressed_keys = list(set(pressed_keys))

def on_release(key):
    global pressed_keys
    if hasattr(key, 'char'):
        pressed_keys.remove(key.char)

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

def parse_keys(keys, val):
    command = np.zeros(8)
    if 'i' in keys:
        command[0:4] += val
    if 'k' in keys:
        command[0:4] -= val
    if 'j' in keys:
        command[[4,7]] += val
        command[[5,6]] -= val
    if 'l' in keys:
        command[[4,7]] -= val
        command[[5,6]] += val

    if 'w' in keys:
        command[4:8] += val
    if 's' in keys:
        command[4:8] -= val
    if 'a' in keys:
        command[[4,6]] += val
        command[[5,7]] -= val
    if 'd' in keys:
        command[[4,6]] -= val
        command[[5,7]] += val

    return command

start_time = time.time()
def get_states_6dof(dynamics_sensor_output_rpy):
    x = dynamics_sensor_output_rpy
    
    a = x[:3]
    v = x[3:6]
    p = x[6:9]
    alpha = x[9:12]
    omega = x[12:15]
    theta = x[15:18]

    pos = np.concatenate((p,theta))
    vel = np.concatenate((v,omega))
    acc = np.concatenate((a,alpha))
    t = time.time() - start_time

    state_6dof = dict(pose=pos, velocity=vel,acceleration=acc, time=t)

    return state_6dof

plt.ion()
x_data = []
y1_ctl_data = []
y1_set_data = []
y2_ctl_data = []
y2_set_data = []


''
fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10, 5))
line1_ctl, = ax1.plot(x_data, y1_ctl_data,color='blue')
line1_set, = ax1.plot(x_data, y1_set_data,color='black')
line2_ctl, = ax2.plot(x_data, y2_ctl_data,color='red')
line2_set, = ax2.plot(x_data, y2_set_data,color='black')

# ax1.set_xlabel("time (s)")
ax1.set_ylabel("Depth (m)")
ax1.set_title("Depth/Heading Control Plots")

ax2.set_xlabel("time (s)")
ax2.set_ylabel("Heading")
# ax2.set_title("Heading Plot")

z_force = 0
psi_force = 0
with holoocean.make(scenario_cfg=scenario) as env:
    while True:
        if 'q' in pressed_keys:
            break
        
        # # KEY PRESS DRIVE CAN BE UNCOMMENTED FOR TROUBLESHOOTING, BUT MAY CAUSE CONFUSION WITH OTHER COMMANDS
        # command = parse_keys(pressed_keys, force) # command is a numpy array of length 8, corresponding to the vehicle's 8 thrusters.  thruster values are in Newtons
        # print(command)

        

        # INSERT HERE: command vehicle to drive to depth = depth_command and yaw = heading_command, by updating z_force and psi_force.
        
        # Goal is to get to desired depth and heading as rapidly as possible, but also without colliding with bottom
        # x_force_to_thrusters commands serve to distribute commanded force amongst four relevant thrusters. Familiarize yourself with the import structure which allows definition of these functions in a separate file.
        # Note: check on sign of psi force.  if yaw_thruster_cmd appears to drive yaw in opposite of intended direction, multiply psi_force by -1, but also discuss/share
        
        # Warning: uncommenting these values may make you seasick.
        # z_force = -160
        # psi_force = 40

        depth_thruster_cmd = vert_force_to_thrusters(z_force)
        yaw_thruster_cmd = yaw_force_to_thrusters(psi_force)
        command = depth_thruster_cmd+yaw_thruster_cmd
        # print(command)

        #send to holoocean
        env.act("auv0", command)
        simul_state = env.tick()
        
        auv_state = get_states_6dof(simul_state["DynamicsSensor"])
        
        st = auv_state["pose"] # auv_state is a python dictionary with pose velocity and acceleration in 6DOF, as well as a timestamp in seconds since the beginning of execution.  right now, all states are in global coordinates
        # print(st) #uncomment to view the states of the vehicle
        t = auv_state["time"]

        depth = st[2] #note that python uses "0 indexing"
        yaw = st[5]

        
        
        x_data.append(t)
        y1_ctl_data.append(depth)
        y1_set_data.append(depth_command)
        y2_ctl_data.append(yaw)
        y2_set_data.append(heading_command)

        line1_ctl.set_xdata(x_data)
        line1_ctl.set_ydata(y1_ctl_data)
        line1_set.set_xdata(x_data)
        line1_set.set_ydata(y1_set_data)

        line2_ctl.set_xdata(x_data)
        line2_ctl.set_ydata(y2_ctl_data)
        line2_set.set_xdata(x_data)
        line2_set.set_ydata(y2_set_data)


        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()





