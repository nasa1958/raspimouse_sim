#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, rospy
from raspimouse_ros.msg import LightSensorValues
from time import sleep
from geometry_msgs.msg import Twist
import math
import requests
import json

class WallAround():
	def __init__(self):
		self.cmd_vel = rospy.Publisher('/raspimouse_on_gazebo/diff_drive_controller/cmd_vel',Twist,queue_size=10)
		self.sensor_values = LightSensorValues()

	def wall_front(self,left_forward, right_forward):
		return left_forward > 550 and right_forward > 550

	def too_right(self,right_side):
		return right_side > 50

	def too_left(self,left_side):
		return left_side > 50

	def send_slack(self):
		content = f
		payload = {
                    	"text": content,
                    	"icon_emoji": ':snake:',
                	}
                data = json.dumps(payload)
                requests.post(SLACK_URL, data)
		return 1

	def set_position(self,left_forward, right_forward):
		vel = Twist()
		vel.linear.x = 0.0
		vel.angular.z = 0.0
		while(abs(left_forward - right_forward) < 50):
			if (left_forward - right_forward) > 50:
				vel.angular.z = 90*math.pi/180.0/10.0
			if (left_forward - right_forward) < -50:
				vel.angular.z = -90*math.pi/180.0/10.0
			self.cmd_vel.publish(vel)
			self.get_sensorsvalues()
		return 1

	def get_sensorsvalues(self):
		self.sensor_values = LightSensorValues()
		for num_2 in range(8):
			with open(devfile,'r') as f:
				data = f.readline().split()
				self.sensor_values.right_forward += int(data[0])
				self.sensor_values.right_side += int(data[1])
				self.sensor_values.left_forward += int(data[2])
				self.sensor_values.left_side += int(data[3])
		self.sensor_values.right_forward = self.sensor_values.right_forward / 8.0
		self.sensor_values.right_side = self.sensor_values.right_side / 8.0
		self.sensor_values.left_side = self.sensor_values.left_side / 8.0
		self.sensor_values.left_forward = self.sensor_values.left_forward / 8.0
		print self.sensor_values.right_forward
		print self.sensor_values.right_side
		print self.sensor_values.left_forward
		print self.sensor_values.left_side
		return 1
	
	def run(self):
		self.sensor_values = LightSensorValues()
		vel = Twist()
		num_1 = 0
		judge = []
		rate = rospy.Rate(20)
		for num_2 in range(8):
			with open(devfile,'r') as f:
				data = f.readline().split()
				self.sensor_values.right_forward += int(data[0])
				self.sensor_values.right_side += int(data[1])
				self.sensor_values.left_side += int(data[2])
				self.sensor_values.left_forward += int(data[3])
		self.sensor_values.right_forward = self.sensor_values.right_forward / 8.0
		self.sensor_values.right_side = self.sensor_values.right_side / 8.0
		self.sensor_values.left_side = self.sensor_values.left_side / 8.0
		self.sensor_values.left_forward = self.sensor_values.left_forward / 8.0

		print self.sensor_values.right_forward
		print self.sensor_values.right_side
		print self.sensor_values.left_side
		print self.sensor_values.left_forward

		self.set_position(self.sensor_values.left_forward, self.sensor_values.right_forward)
		
		while not rospy.is_shutdown():
			vel.angular.x = 0.18
			self.cmd_vel.publish(vel)
			vel.angular.x = 0.18
			self.cmd_vel.publish(vel)
			while(num_1 < 4):
				if (self.set_position(self.sensor_values.left_forward, self.sensor_values.right_forward)):
					vel.angular.z = -90*math.pi/180.0
					self.cmd_vel.publish(vel)
					vel.angular.z = -90*math.pi/180.0
					self.cmd_vel.publish(vel)
					self.get_sensorsvalues()
					if self.sensor_values.left_forward < 200 and self.sensor_values.right_forward < 200:
                				judge.append(1)
            				else:
                				judge.append(0)
				        num_1 = num_1 + 1

			a = ''
    			b = ''
    			c = ''
    			d = ''
    			e = 'に進めます'
    			if judge[0] == 1:
        			a = '右　'
    			if judge[1] == 1:
        			b = '後ろ　'
    			if judge[2] == 1:
        			c = '左　'
    			if judge[3] == 1:
     			   	d = '前　'
    			f = a + b + c + d + e

			if (judge[0] or judge[2]):
				self.send_slack()
				break

		rate.sleep()

if __name__ == '__main__':
	SLACK_URL = "https://hooks.slack.com/services/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"
	devfile = '/dev/rtlightsensor0'
	rospy.init_node('wallaround')
	WallAround().run()    

