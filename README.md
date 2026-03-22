---

# AutoBot — Autonomous Mobile Robot in ROS2

A fully autonomous differential drive robot built from scratch in ROS2 Humble. The robot is capable of mapping unknown environments, localizing itself within a saved map, planning paths, and navigating autonomously while avoiding dynamic obstacles in real time.

Built entirely in simulation using Gazebo, with a modular URDF/Xacro model, LiDAR-based SLAM, and the Nav2 navigation stack.

---

## Demo

> *"Go there." — me*
> *"Say less." — the robot*

Setting a goal pose in RViz:

![Setting the navigation goal](assets/navigation1.jpeg)

The robot actually doing it:

![Robot following the planned path](assets/navigation2.jpeg)

---

## Capabilities

- **Environment Mapping** — builds a 2D occupancy grid map using LiDAR SLAM via slam_toolbox
- **Localization** — determines its position on a saved map using AMCL particle filter
- **Autonomous Navigation** — plans and executes paths to goal poses using the Nav2 stack
- **Real-time Obstacle Avoidance** — detects and navigates around dynamic obstacles not present in the original map. Tested by throwing barrels at it. It was not impressed.
- **Manual Control** — PS3 DualShock controller support via teleop_twist_joy
- **Depth Camera** — onboard RGB-D sensor streaming to ROS2 image topics

---

## Tech Stack

| Component | Role |
|---|---|
| ROS2 Humble | Middleware and communication framework |
| Gazebo | Physics simulation environment |
| URDF / Xacro | Robot model definition |
| slam_toolbox | Online asynchronous LiDAR SLAM |
| Nav2 | Full autonomous navigation stack |
| AMCL | Monte Carlo localization |
| Regulated Pure Pursuit | Local path controller |
| NavFn | Global path planner |
| diff_drive plugin | Wheel control and odometry |

---

## System Architecture

```
PS3 Controller ──► /cmd_vel ──► diff_drive ──► robot moves
                                    │
                                    ▼
LiDAR ──► /scan ──► slam_toolbox ──► /map
                         │
                         ▼
              AMCL (localization) ──► /amcl_pose
                         │
                         ▼
Goal Pose ──► bt_navigator ──► planner ──► controller ──► /cmd_vel
```

---

## Getting Started

**Prerequisites:**
- ROS2 Humble
- Gazebo
- nav2_bringup, slam_toolbox, teleop_twist_joy

**Clone and build:**
```bash
git clone git@github.com:yourusername/ros2-autonomous-bot.git
cd ros2-autonomous-bot
colcon build --symlink-install
source install/setup.bash
```

**Launch simulation:**
```bash
ros2 launch my_bot launch_sim.launch.py
```

**Map the environment:**
```bash
ros2 launch my_bot slam.launch.py
```
Drive around with the controller until satisfied with the map, then save:
```bash
cd src/my_bot/maps
ros2 run nav2_map_server map_saver_cli -f map
```

**Autonomous navigation:**
```bash
ros2 launch my_bot navigation.launch.py
```
In RViz, set a **2D Pose Estimate** to initialize localization, then set a **2D Goal Pose** and watch the robot handle the rest.

---

## Package Structure

```
src/my_bot/
├── config/
│   ├── mapper_params_online_async.yaml
│   ├── nav2_params.yaml
│   └── ps3_custom.yaml
├── description/
│   ├── robot.urdf.xacro
│   ├── robot_core.xacro
│   ├── lidar.xacro
│   ├── camera.xacro
│   ├── gazebo_control.xacro
│   └── inertial_macros.xacro
├── launch/
│   ├── launch_sim.launch.py
│   ├── rsp.launch.py
│   ├── slam.launch.py
│   └── navigation.launch.py
└── maps/
    ├── map.pgm
    └── map.yaml
```

---

## What's Next

- Integrating object detection via the depth camera
- Multi-waypoint navigation
- Exploring Nav2 behaviour trees for more complex navigation logic

---

## Contact

Open to collaborations and discussions around robotics and autonomous systems. Feel free to open an issue or reach out directly.

---

*Tested on ROS2 Humble. Number of `colcon build` commands executed during development: too many to count.*
