#!/usr/bin/env python
import sys, rospy
from raspimouse_ros.msg import LightSensorValues
from time import sleep
from geometry_msgs.msg import Twist
import requests
import json

if __name__ == '__main__':
    devfile = '/dev/rtlightsensor0' 
    rospy.init_node('vel_publisher')
    pub = rospy.Publisher('/raspimouse_on_gazebo/diff_drive_controller/cmd_vel', Twist, queue_size=10)
    
    SLACK_URL = "https://hooks.slack.com/services/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"
   
try:
    judge = []
    for num in range(4):
        vel = Twist()
        vel.angular.z = -3.2999
        sleep(0.3)
        pub.publish(vel)
        sleep(1.4)
        with open(devfile,'r') as f:
            data = f.readline().split()
            d = LightSensorValues()
            d.right_forward = int(data[0])
            d.left_forward = int(data[3])
            print data[0]
            print data[1]
            print data[2]
            print data[3]
            if d.right_forward < 200 and d.left_forward < 200:
                judge.append(1)
            else:
                judge.append(0)
    a = ''
    b = ''
    c = ''
    d = ''
    e = 'raspimouse can go'
    if judge[0] == 1:
        a = ' right'
    if judge[1] == 1:
        b = ' backward'
    if judge[2] == 1:
        c = ' left'
    if judge[3] == 1:
        d = ' forward'
    f = e + a + b + c + d 
    print f
except rospy.ROSInterruptException:
    pass


def send_slack():

    content = f

    payload = {
        "text": content,
        "icon_emoji": ':snake:',
    }

    data = json.dumps(payload)

    requests.post(SLACK_URL, data)

send_slack()


        










        
