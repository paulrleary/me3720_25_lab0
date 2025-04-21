# Lab 0

The goal of this lab is to familiarize yourself with the Holoocean simulator, the basics of python programming, and basic actuator-level control of the vehicle.  There are three main tasks, wrapped into two scripts:

1.  hoveringauv_interface_init.py is a basic simulation of the AUV in a contained environment.  It contains a simple keypress functionality to drive the vehicle and explore how the vehicle responds to thruster command structure.  Your task is to implement a short block of code, driving the vehicle 30m forward, then back to its starting position (roughly).

The other tasks are within the script hoveringauv_depth_yaw_ctl.py, and are done essentially at the same time.

2. Implement a "hard-coded" depth control block which drives the vehicle to the depth setting, without colliding with the bottom.  

3. While descending to the bottom implement a similar yaw control, which drives the vehicle to the desired yaw setting.

The end state should be the vehicle hovering in place at the desired depth and heading.

For the tasks above, when you feel you have a solution, please save your plots, and hand them in with your inserted control block.  

# Getting started.

First clone this repo.  in AWS open a terminal window and cd to the desktop:
'''
cd ~/Desktop
'''

Then use the tool git to clone this repo:
'''
git clone https://github.com/paulrleary/me3720_25_lab0.git
'''

Then cd into the the cloned folder:
'''
cd me3720_25_lab0
'''

And finally launch VSCode:
'''
code .
'''