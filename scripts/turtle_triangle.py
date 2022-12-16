#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x=0
y=0
z=0 
yaw=0

def poseCallback(pose_message):
    global x, y, yaw
    x=pose_message.x
    y=pose_message.y
    yaw=pose_message.theta

def move(speed,distance, is_foward):
    velocity_message = Twist()
    global x, y
    x0=x
    y0=y

    if (is_foward):
        velocity_message.linear.x=abs(speed)
    else:
        velocity_message.linear.x=-abs(speed)
    distance_moved = 0.0
    loop_rate = rospy.Rate(10)
    cmd_vel_topic ='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)

        loop_rate.sleep()
        distance_moved = distance_moved+abs(0.5 * math.sqrt(((x-x0)*(x-x0)) + ((y-y0)*(y-y0))))
        print(distance_moved)
        if not (distance_moved<distance):
            rospy.loginfo("Distance reached")
            break
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)

def rotate(angular_speed_degree, relative_angle_degree, clockwise):
    global yaw
    velocity_message = Twist()
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0
    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    theta0=yaw
    angular_speed = math.radians(abs(angular_speed_degree))

    if (clockwise):
        velocity_message.angular.z = abs(angular_speed)
    else:
        velocity_message.angular.z = -abs(angular_speed)
    
    angle_moved = 0.0
    loop_rate = rospy.Rate(10)
    cmd_vel_topic='turtle1/cmd_vel'
    velocity_publisher=rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True:
        rospy.loginfo("Turtlesim rotates")
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()

        if (current_angle_degree>relative_angle_degree):
            rospy.loginfo("Angle reached")
            break
    velocity_message.angular.z=0
    velocity_publisher.publish(velocity_message)

def square():
    for i in range(4):
        move(3, 2, True)
        rotate(20,88,True)

def triangle():
    for i in range(3):
        move(3, 2, True)
        rotate(20,118,True)

def star():
    for i in range(5):
        move(3, 2, True)
        rotate(20,142,True)


if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose_TRIANGLE', anonymous=True)
        #Declare velocity publisher
        cmd_vel_topic ='/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic="/turtle1/pose"
        pose_subscriber=rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)

        triangle()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")