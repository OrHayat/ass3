#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import sys
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import ColorRGBA

def publisher():
    pub = rospy.Publisher('/ledscape_ros/array', ColorRGBA, queue_size=10)
    rospy.init_node('userstracker_vectors', anonymous=True)
    rate=rospy.Rate(0.2)
    msg = ColorRGBA()
    msg.r = int(sys.argv[1])
    msg.g = int(sys.argv[2])
    msg.b = int(sys.argv[3])
    while not rospy.is_shutdown():
        rospy.loginfo('Publishing color = '+str(msg.r)+" "+ str(msg.g)+" "+str(msg.b))
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
	pass
