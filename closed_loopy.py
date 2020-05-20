#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

pub = rospy.Publisher('/pioneer_1/RosAria/cmd_vel', Twist, queue_size=10)
goal = [0]
eps = 0.00001
flaga = 0

def quat2angle(quat):
    ang = 2 * math.acos(quat.w)
    if quat.z > 0:
        return ang
    else:
       return 2*math.pi - ang

def cr_vel_msg(lx,ly,lz,ax,ay,az):
    global pub
    vel_msg=Twist()
    vel_msg.linear.x = lx
    vel_msg.linear.y = ly
    vel_msg.linear.z = lz
    vel_msg.angular.x = ax 
    vel_msg.angular.y = ay
    vel_msg.angular.z = az
    pub.publish(vel_msg)

def set_velocity(linear,angular):
    cr_vel_msg(linear,0,0,0,0,-angular)

def stop():
    cr_vel_msg(0,0,0,0,0,0)

def regulator(data):
    global goal
    global eps

    #err = data.pose.pose.position.x - goal
    #rospy.loginfo(err)
    if flaga == 0:
    	err = quat2angle(data.pose.pose.orientation) - goal[0]
    	if math.fabs(err) < eps:
		stop()
    	set_velocity(0.0,0.1*-err)
    if flaga == 1:
	err = data.pose.pose.position.x - goal[0]
	if math.fabs(err) < eps:
		stop()
	set_velocity(1.0, 0.0)
    if flaga == 2:
	err = data.pose.pose.position.y - goal[1]
	if math.fabs(err) < eps:
		stop()
	set_velocity(1.0, 0.0)
    rospy.loginfo(data.pose.pose.position)
    #rospy.loginfo(data.pose.pose.orientation)
    #rospy.loginfo(quat2angle(data.pose.pose.orientation))
    
def control():
    global goal

    rospy.init_node('control', anonymous=True)
    rospy.Subscriber('/pioneer_1/RosAria/pose',Odometry,regulator)
    while True:
	flaga = 0
	goal = [math.pi/2]
	flaga = 1
	goal = [5, 0]
        #key = raw_input()
    	#if key == 'a':
	#    goal = input()
	#    goal = (goal*2*math.pi)/360
    rospy.spin()
    
if __name__ == '__main__':
    try:
        control()
    except rospy.ROSInterruptException:
        pass
