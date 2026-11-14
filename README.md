<!-- ABOUT THE PROJECT -->
## About The Project

This project is for our Applied Machine Learning (CST8504) Assignment2 ROS2
hand gesture control of create3 robot.

<!-- REQUIREMENTS -->
## Requirements
In Linux, python (ROS2, opencv, mediapipe).

<!-- INSTALL -->
## Install
**Create your new workspace**

1) Create your new workspace directory

```
mkdir your_ws      
```
2) cd into your ws
```
cd your_ws
```

3) Create the src directory
```
mkdir src
```
4) Change dir to src
```
cd src
```
5) clone git repo here
```
git clone https://your_git_repo_url_here
```

**Now to install the python packages:**

1) Verify your are at the root of your workspace.
```
cd ~/your_ws
```
2) Install required packages
```
sudo apt update
pip3 install "numpy>=2"  
pip3 install opencv-python-headless  opencv-contrib-python
pip3 install mediapipe
sudo apt-get install libgles2   
```

3) Install dependencies.
```
rosdep install --from-paths src --ignore-src -y
```

4) Build the packages. It will create new directories under your ws directory
```
colcon build
```
5) Source the setup file.
```
source install/setup.py
```
6) Run the first node test
```
ros2 run aisd_vision py_node
```




<!-- DEPLOYMENT -->
## DEPLOYMENT

To deploy and run the project in a demonstration environment:

1. Ensure all requirements are installed and the workspace is built as described above.
2. Source your ROS2 workspace:
   ```
   source ~/your_ws/install/setup.bash
   ```
3. Connect your Create3 robot and ensure it is powered on and accessible.
4. Launch the gesture publisher node:
   ```
   ros2 run aisd_vision gesture_publisher
   ```
5. In another terminal:
   - Run step 2 above.
   - Launch the motion listener node:
   ```
   ros2 run aisd_vision motion_listener
   ```   



<!-- TEAM -->
## TEAM
    K. Tam
    G. Byron

<!-- ACKNOWLEDGEMENTS -->
## ACKNOWLEDGEMENTS
