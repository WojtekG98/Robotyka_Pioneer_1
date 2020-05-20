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

def set_speedLP(lewe,prawe):
    global pub
    # cos(theta)*lewe + cos(theta)*prawe = q1'
    # sin(theta)*lewe + sin(theta)*prawe = q2'
    # -1/d*lewe + 1/d*prawe = q3'
    #set_velocity(0,-lewe)
    #set_velocity(0,prawe)
    # G = |cos(theta) 0|
    #     |sin(theta) 0|
    #     |0          1|
    # cos(theta)*u1 = cos(theta)*lewe + cos(theta)*prawe
    # sin(theta)*u1  = sin(theta)*lewe + sin(theta)*prawe
    # u2            = -1/d*lewe + 1/d*prawe
    d = 0.163
    #cr_vel_msg(math.cos(90)*lewe + math.cos(90)*prawe, math.sin(90)*lewe + math.sin(90)*prawe, 0.0, 0.0, 0.0, -1/d*lewe + 1/d*prawe)
    set_velocity(-1*(lewe+prawe), (-1/d*lewe +1/d*prawe))
    
def talker():
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.sleep(1)
    for i in range(0,4):
        set_speedLP(0.5, 0.5)
        rospy.sleep(1)
        set_speedLP(0.0, 0.0)
        rospy.sleep(1)
        set_speedLP(0.15, 0.0)
        rospy.sleep(1)
        set_speedLP(0.0, 0.0)
        rospy.sleep(1)
    stop()
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
