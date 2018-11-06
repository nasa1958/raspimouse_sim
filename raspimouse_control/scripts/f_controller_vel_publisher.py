#!/usr/bin/env python

import rospy
import requests
import json
from geometry_msgs.msg import Twist
from time import sleep
import subprocess



if __name__ == '__main__':

	rospy.init_node('vel_publisher1')
        pub = rospy.Publisher('/raspimouse_on_gazebo/diff_drive_controller/cmd_vel', Twist, queue_size=10)
	try:
            while not rospy.is_shutdown():
                sleep(0.4)
                vel = Twist()
                vel.linear.x = 0.35
                print vel
                pub.publish(vel)

                args = ['rosrun', 'raspimouse_control', 'suggest_directions.py']
                res = subprocess.call(args)

                break
        except rospy.ROSInterruptException:
	        pass
