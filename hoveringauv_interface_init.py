import holoocean
import numpy as np
from pynput import keyboard
import matplotlib.pyplot as plt
import time

scenario = {
    "name": "test_rgb_camera",
    "world": "SimpleUnderwater",
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
            "location": [10, -30, -10],
            "rotation": [0, 0, 90]
        }
    ]
}


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
y_data = []
''
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_title("Real-time Plot")

with holoocean.make(scenario_cfg=scenario) as env:
    simul_state = env.tick()
    while True:
        if 'q' in pressed_keys:
            break

        # probably best to comment out the parse_keys call when running your own code, or you may find confusing behavior.
        command = parse_keys(pressed_keys, force) # command is a numpy array of length 8, corresponding to the vehicle's 8 thrusters.  thruster values are in Newtons
        print(command)
        
        auv_state = get_states_6dof(simul_state["DynamicsSensor"])
        
        st = auv_state["pose"] # auv_state is a python dictionary with pose velocity and acceleration in 6DOF, as well as a timestamp in seconds since the beginning of execution.  right now, all states are in global coordinates
        # print(st) #uncomment to view the states of the vehicle

        #INSERT HERE:
        # try driving the vehicle forward 30 meters, then backward 30 meters, by "hard coding" the thruster command here, using information from the vehicle state. 
        # you will probably need a set of conditional statements, like if, elif, else, or switch case.

        #looking at the plots, and your starting position and orientation, in what directions does do the positive axes of this coordinate system point?

        #send to holoocean
        env.act("auv0", command)
        simul_state = env.tick()
        x_data.append(st[0])
        y_data.append(st[1])

        line.set_xdata(x_data)
        line.set_ydata(y_data)

        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()





