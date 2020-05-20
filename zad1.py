#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist

pub = rospy.Publisher('/pioneer_1/RosAria/cmd_vel', Twist, queue_size=10)

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
        
def talker():
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.sleep(1)
    set_velocity(1,0)
    rospy.sleep(1)
    set_velocity(0.5,0.5)
    rospy.sleep(3)
    set_velocity(1,0)
    rospy.sleep(1)
    set_velocity(0.5,0.5)
    rospy.sleep(3)
    stop()
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
