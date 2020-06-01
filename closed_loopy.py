#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

pub = rospy.Publisher('/pioneer_1/RosAria/cmd_vel', Twist, queue_size=10)
goal = 0
eps = 0.01
flaga = 1

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
    global flaga
    druga_flaga = 0
    if flaga == 0:
        #print("do przodu")
        goal = 0
        err = data.pose.pose.position.x - goal
        #print(err)
        if math.fabs(err) < eps:
            stop()
            goal = 0
            flaga = 2
        set_velocity(-err, 0)
    if flaga == 1:
        #print("do tylu")
        goal = -2
        err = data.pose.pose.position.x - goal
        if math.fabs(err) < eps:
            stop()
            goal = math.pi/16
            flaga = 2
        set_velocity(-err, 0)
    if flaga == 2:
        err = quat2angle(data.pose.pose.orientation) - goal
    	if math.fabs(err) < eps:
	    stop()
            if goal == math.pi/16:
                flaga = 0
            if goal == 0:
                flaga = 1
        set_velocity(0.0,-err)
    #rospy.loginfo(data.pose.pose.position)
    #rospy.loginfo(data.pose.pose.orientation)
    #rospy.loginfo(quat2angle(data.pose.pose.orientation))
    
def control():
    global goal

    rospy.init_node('control', anonymous=True)
    rospy.Subscriber('/pioneer_1/RosAria/pose',Odometry,regulator)
        #rospy.sleep(2)
        #goal = math.pi/4
        #print("flaga = 2")
        #flaga = 2
        #rospy.sleep(2)
        #print("flaga = 0")
        #flaga = 0
        #rospy.sleep(2)
        #goal = 0
        #print("flaga = 2")
        #flaga = 2
        #rospy.sleep(2)
#	flaga = 0
#	goal = math.pi/2
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
