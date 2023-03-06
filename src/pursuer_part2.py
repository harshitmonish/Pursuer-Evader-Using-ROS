#!/usr/bin/python3
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import random
import tf
import warnings
warnings.filterwarnings("ignore")

#initialization of the publisher to /tb3_1/cmd_vel to publish new Twist messages to tb3_1
pub = rospy.Publisher('/tb3_1/cmd_vel', Twist, queue_size=20)

def callback_func(msg):

    #checking if robot is close to a obstacle
    # Intention is to monitor the fron view of the robot. the min_angle and max_angle of laser beam is -2.35, 2.35 hence if we convert it to angle it is a 270 degree, so beams are covering a 270 degree view. The ranges arr consisit of 720 values and the front center of the robot is observed at 360th idx. hence I have taked 180-360 as front right view and 360-540 as front left view of the robot.
    #for i in range(len(msg.ranges)):
    #    if msg.ranges[i] < 1.5:
    #        print(i, end=" ")
    #print()
    if min(msg.ranges[0:45]) < 1.5 or min(msg.ranges[315:360]) < 1.5:
        cmd_vel = Twist()
        #stopping the robot
        cmd_vel.linear.x = 0
        # Rotating the bot in random direction
        ang = random.uniform(0.1, 0.35)
        cmd_vel.angular.z = ang
        pub.publish(cmd_vel)

    #Driving the robot at constant speed 2m/s
    else:
        cmd_vel = Twist()
        cmd_vel.linear.x = 1
        pub.publish(cmd_vel)

def pursuer():
    # initializing the pursuer node
    rospy.init_node('pursuer')

    rate = rospy.Rate(2)

    #initializing listener
    listener = tf.TransformListener()

    # next we subscribe to tb3_0/scan to get its scan readings with a callback func
    cmd_vel = rospy.Subscriber('/tb3_1/scan', LaserScan, callback_func, queue_size= 20)


    while not rospy.is_shutdown():
        try:
            # let's first get the current timestamp 
            curr_time = rospy.Time.now()

            # next we will fetch older timestamp
            old_time = rospy.Time.now() - rospy.Duration(2.0)

            listener.waitForTransformFull('/tb3_1/odom', curr_time, '/tb3_0/odom', old_time, 'world', rospy.Duration(1.0))
            # get transform with frames and time
            (t, r) = listener.lookupTransformFull('/tb3_1/odom', curr_time, '/tb3_0/odom', old_time, 'world')

            cmd_vel = Twist()

            # calculating linear and angular velocity for tb3_1
            cmd_vel.angular.z = 4*math.atan2(t[1], t[0])
            cmd_vel.linear.x = (0.5*math.sqrt(t[0] ** 2 + t[1]**2))/2

            # robots collision avoidance, stop tb3_1
            if 0.5*math.sqrt(t[0]**2 + t[1]**2) < 1.25:
                cmd_linear.x=0.0

            #publish new cmdd
            pub.publish(cmd_vel)
            rate.sleep()

        except:
            pass


def main():
    try:
        pursuer()
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()
