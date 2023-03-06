# Pursuer-Evader Using ROS Environment

## Project Description

In this project, I have writen my own controller. The evader robot uses LiDAR to avoid obstacles and the Pursuer follows the evader. The evader publishes geometry msgs/twist using rostopic and subscribes to the laser output rostopic for obstacle avoidance. A controller node drives the evader robot at a constant speed of 2m/s. When
the evader robot is close to an obstacle, it stops, turn in a random new direction, and drive at the same speed. It publishes its coordinate frame with regards to the global frame using ROS-tf. The pursuer node subscribes to the tf messages from the evader, and follows the evader by going to the spot it was at from two second
before. Edit the existing pa2 pursuer.launch file so that your controller is launched.
