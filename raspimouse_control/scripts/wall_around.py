#!/usr/bin/env python
import sys, rospy
from raspimouse_ros.msg import LightSensorValues
from time import sleep
from geometry_msgs.msg import Twist
import math

class WallAround():
	def __init__(self):
		self.cmd_vel = rospy.Publisher('/raspimouse_on_gazebo/diff_drive_controller/cmd_vel',Twist,queue_size=10)
		self.sensor_values = LightSensorValues()

	def wall_front(self,left_forward, right_forward):
		return left_forward > 50 or right_forward > 50

	def too_right(self,right_side):
		return right_side > 50

	def too_left(self,left_side):
		return left_side > 50

	def run(self):
		rate = rospy.Rate(20)
		vel = Twist()

		vel.linear.x = 0.05
		vel.angular.z = 0.0
		while not rospy.is_shutdown():
			with open(devfile,'r') as f:
				data = f.readline().split()
				self.sensor_values.right_forward = int(data[0])
				self.sensor_values.right_side = int(data[1])
				self.sensor_values.left_side = int(data[2])
				self.sensor_values.left_forward = int(data[3])
				print data[0]
				print data[1]
				print data[2]
				print data[3]

			if self.wall_front(self.sensor_values.right_forward, self.sensor_values.left_forward):
                                vel.angular.z = -math.pi
			elif self.too_right(self.sensor_values.right_side):
				vel.angular.z  = math.pi
			elif self.too_left(self.sensor_values.left_side):
				vel.angular.z = -math.pi
			else:
				e = 50 - self.sensor_values.left_side
				vel.angular.z = e * math.pi / 180.0

			self.cmd_vel.publish(vel)
			rate.sleep()

if __name__ == '__main__':
	devfile = '/dev/rtlightsensor0'
	rospy.init_node('wallaround')
	WallAround().run()    


   

