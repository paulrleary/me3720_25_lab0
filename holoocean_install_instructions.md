# Re-Clone the lab0 repo from github onto the Desktop

In AWS open a terminal window and cd to the desktop:
```
cd ~/Desktop
```

Then use the tool git to clone this repo:
```
git clone https://github.com/paulrleary/me3720_25_lab0.git lab_0
```

# Copy the required source code from the root folder onto the desktop.
## This is a "hack" of sorts, to get past the HoloOcean install troubles.  You now have a new AWS VM which contains the source code to install in the folder root, or '/'

```
cp -r /me3720_src/ ~/Desktop
```

# Copy the holoocean installation script into the me3720_src folder and cd into it

```
cp ./lab_0/install_holoocean.bash ./me3720_src/
cd me3720_src
```
The install script is written to work only within the folder containing the source code directories, that is me3720_src should now contain install_holoocean.bash, posix-ipc, HoloOcean, and me3720_lab25_init, and you should be in this folder in the terminal.

# Run the installation 
Install should take less than 10 minutes to complete with a fairly obvious success message, and your user prompt will be returned when done.
```
source install_holoocean.bash
```

# Test the installation
Running the initial lab example should open holoocean as intended.

cd back into the lab folder
```
cd ../lab_0
```
or
```
cd ~/Desktop/lab_0
```

For good measure, let's make sure the lab required python libraries are installed
```
pip install -r requirements.txt
```

And finally, run the lab example.  You should be able to drive the vehicle using the keys W,A,S,D and I,J,K,L 

```
python hoveringauv_interface_init.py
```