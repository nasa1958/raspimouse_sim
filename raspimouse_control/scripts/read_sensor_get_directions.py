#!/usr/bin/env python
import sys, rospy
from raspimouse_ros.msg import LightSensorValues
from time import sleep
from geometry_msgs.msg import Twist
import subprocess
import requests
import json

if __name__ == '__main__':
    #freq = 10
    #if rospy.has_param('lightsensors_freq'):
    freq = rospy.get_param('lightsensors_freq',10)
    
    devfile = '/dev/rtlightsensor0'
    rospy.init_node('rtlightsensors')
    pub = rospy.Publisher('lightsensors', LightSensorValues, queue_size=1)
    rate = rospy.Rate(freq)

    SLACK_URL = "https://hooks.slack.com/services/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"

   
while not rospy.is_shutdown():
    #try:
        sleep(2)
        with open(devfile,'r') as f:
            data = f.readline().split()
            d = LightSensorValues()
            d.right_forward = int(data[0])
            d.right_side = int(data[1])
            d.left_side = int(data[2])
            d.left_forward = int(data[3])
            #pub.publish(d)
            """if d.right_side >= 80 and d.right_side <= 110 and d.left_side >= 80 and d.left_side <= 110:
                args = ['rosrun', 'raspimouse_control']
                res = subprocess.call(args)
                f = 'you can go right left'
                data = json.dumps(payload)
                requests.post(SLACK_URL, data)
                send_slack()

                break
            """
        if d.right_side >= 80 and d.right_side <= 110:
            f = 'you can go right'
            def send_slack():

                content = f

                payload = {
                    "text": content,
                    "icon_emoji": ':snake:',
                }
                data = json.dumps(payload)
                requests.post(SLACK_URL, data)
            send_slack()
            args = ['rosrun', 'raspimouse_control', 'motor_stop.py']
            res = subprocess.call(args)

            break

        if d.left_forward >= 80 and d.left_forward <= 110:
            f = 'you can go left'
            def send_slack():

                content = f

                payload = {
                    "text": content,
                    "icon_emoji": ':snake:',
                }
                data = json.dumps(payload)
                requests.post(SLACK_URL, data)
            send_slack()
            args = ['rosrun', 'raspimouse_control', 'motor_stop.py']
            res = subprocess.call(args)

            break

        if d.right_forward >= 300 and d.left_forward >=300:
            f = 'you can not go forward'
            def send_slack():

                content = f

                payload = {
                    "text": content,
                    "icon_emoji": ':snake:',
                }
                data = json.dumps(payload)
                requests.post(SLACK_URL, data)
            send_slack()
            args = ['rosrun', 'raspimouse_control', 'motor_stop.py']
            res = subprocess.call(args)
               
            break
            #sleep(15)
        
 
        #except:
        #rospy.logerr("cannot open " + devfile)

        #rate.sleep()

        


