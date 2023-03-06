#!/usr/bin/python3
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import random

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def callback_func(msg):
    #pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=20)

    #a = min(msg.ranges[180:360])
    #h = min(msg.ranges[360:540])
    #print("180-360 Front Right min : %f, 360-540 Front Left min : %f "%(a, h ))
    #checking if robot is close to a obstacle
    # Intention is to monitor the fron view of the robot. the min_angle and max_angle of laser beam is -2.35, 2.35 hence if we convert it to angle it is a 270 degree, so beams are covering a 270 degree view. The ranges arr consisit of 720 values. hence I have taked 200-450 as front view of the robot.
    #print()
    if min(msg.ranges[200:450]) < 1.5:
        cmd_vel = Twist()
        #stopping the robot
        cmd_vel.linear.x = 0
        # Rotating the bot in random direction
        ang = random.uniform(0, 0.5)
        cmd_vel.angular.z = ang
        pub.publish(cmd_vel)

    #Driving the robot at constant speed 2m/s
    else:
        cmd_vel = Twist()
        cmd_vel.linear.x = 2
        pub.publish(cmd_vel)

def evader():
    #creating node
    rospy.init_node('lab2_evader')
    rate = rospy.Rate(10)

    command_velocity = rospy.Subscriber('/front/scan', LaserScan, callback_func, queue_size=10)
    rospy.spin()



def main():
    try:
        evader()
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()

