#!/usr/bin/python3
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import random
import tf
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime

pub = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=2)
start_time = datetime.now()
def callback_func(msg):

    #waiting for pursuer to come near evader, giving a 15 sec time delay.
    cur_time = datetime.now()
    delta = cur_time - start_time
    delta_sec = delta.total_seconds()
    if delta_sec <= 10.0:
        return 

    #checking if robot is close to a obstacle
    # Intention is to monitor the fron view of the robot. the min_angle and max_angle of laser beam is -2.35, 2.35 hence if we convert it to angle it is a 270 degree, so beams are covering a 270 degree view. The ranges arr consisit of 720 values and the front center of the robot is observed at 360th idx. hence I have taked 180-360 as front right view and 360-540 as front left view of the robot.
    #for i in range(len(msg.ranges)):
    #    if msg.ranges[i] < 1.5:
    #        print(i, end=" ")
    #print()


    if min(msg.ranges[0:45]) < 1.75 or min(msg.ranges[315:360]) < 1.75:
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
    #rate.sleep()

def callback_gtr0(msg):
    br1= tf.TransformBroadcaster()
    br1.sendTransform((msg.pose.pose.position.x, msg.pose.pose.position.y, 0), (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w), rospy.Time.now(), '/tb3_0/odom',"world")


def callback_gtr1(msg):
    br2 = tf.TransformBroadcaster()
    br2.sendTransform((msg.pose.pose.position.x, msg.pose.pose.position.y, 0), (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w), rospy.Time.now(), '/tb3_1/odom',"world")


def evader():
    #creating node
    rospy.init_node('evader_part2')
    rate = rospy.Rate(2)

    # initializing tf broadcaster
    broad = tf.TransformBroadcaster()
    broad.sendTransform((0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0), rospy.Time.now(), 'world', '/tb3_1/odom')

    # next we subscribe to tb3_0/scan to get its scan readings with a callback func
    cmd_vel = rospy.Subscriber('/tb3_0/scan', LaserScan, callback_func, queue_size= 20)

    # subscribing to tb3_0/odom to get its odometry
    gtr0 = rospy.Subscriber('/tb3_0/odom', Odometry, callback_gtr0, queue_size=20)

    #subscribing to tb3_1/odom to get its odometry
    gtr1 = rospy.Subscriber('/tb3_1/odom', Odometry, callback_gtr1, queue_size=20)


    rospy.spin()



def main():
    try:
        evader()
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()

