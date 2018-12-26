#!/usr/bin/env python
import rospy
import numpy as np
import math
import cv2
import os
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, LaserScan, CameraInfo
from std_msgs.msg import Bool, Int32, Float32
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import ColorRGBA
import image_geometry
import colorsys
camInfo = 0
distances = []


def find_object(r,g,b):


	print "find object"
   	imgdata=rospy.wait_for_message('usb_cam/image_raw',Image)
	if(imgdata is None):
		print "error reciving image from camera"
		return
	bridge = CvBridge()
	image = bridge.imgmsg_to_cv2(imgdata,"bgr8")
	print "we have image :)"
    	camInfodata=rospy.wait_for_message('usb_cam/camera_info',CameraInfo)
	if(camInfodata is None):
		print "error reciving caminfo"
		return
	camInfo=camInfodata
	print "camInfo:" +str(camInfo.K[0])+  str(camInfo.K[1])+ str(camInfo.K[2])
    	scannerdata=rospy.wait_for_message('scan',LaserScan)
	if(scannerdata is None):
		print "error getting scanner data"
		return
	distances=scannerdata
	if(camInfo!=0 and distances!=0 and len(image)!=0):
		camera = image_geometry.PinholeCameraModel()
		camera.fromCameraInfo(camInfo)
		
		Radius_center=(0,0)
	        Radius_center = findCenter(image,r,g,b)
		if(Radius_center==None):
			print "OBJECT NOT FOUND!"
			msg = Float32()
			msg.data =-1.0
			return  None
		else:
			ray = camera.projectPixelTo3dRay(camera.rectifyPoint(Radius_center))
			alpha = np.dot(ray[0],ray[2])
			if(alpha < 0):
				alpha = -alpha
			else:
				alpha = math.floor(math.pi * 2 - alpha)
		 	distance_index = int((alpha - distances.angle_min) / distances.angle_increment)
			actual_distance = distances.ranges[distance_index]
			print "the distance to the object is "+str(actual_distance)
			return actual_distance



def findCenter(cv_image,r,g,b):
  r1 ,g1,b1=colorsys.rgb_to_hsv(r,g,b)
  red = np.uint8([[[b,g,r ]]])
  redHSV = cv2.cvtColor(red, cv2.COLOR_BGR2HSV) 
  greenLower = (redHSV[0][0][0]-25, 80, 80)
  greenUpper = (redHSV[0][0][0]+25, 255, 255)
  
  height, width, channels = cv_image.shape
  blurred = cv2.GaussianBlur(cv_image, (11, 11), 0)
  hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, greenLower, greenUpper)
  mask = cv2.erode(mask, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=2)
  (_,cnts, _)  = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  center = None
  if len(cnts) > 0:
  	c = max(cnts, key=cv2.contourArea)
  	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return (x,y)
  else:
	return None

if __name__ == '__main__':
		red=int(input("insert red color\n"))
		green=int(input("insert green color\n"))
		blue=int(input("insert blue color\n"))	
	    	rospy.init_node('getDistance', anonymous=True)
  		find_object(red,green,blue)
