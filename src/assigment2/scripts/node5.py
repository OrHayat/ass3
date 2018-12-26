#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import sys
import os
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, LaserScan, CameraInfo
import random
from std_msgs.msg import Bool, Int32, Float32
import numpy as np
import math
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from node3 import find_object
PI = 3.1415926535897
import image_geometry
import colorsys

def rotate(angle):
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)	
	current_dis=0
	t1=0
	t0=0
	vel_msg= Twist()
	angle = abs(angle)
	if(angle>10):
		angle=angle+5
	print("Let's rotate your robot!! angle: "+str(angle))
	speed = angle/7
	angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360
	#We wont use linear components
        vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
       	vel_msg.angular.z = abs(angular_speed)
    	t0 = rospy.Time.now().to_sec()
    	current_angle = 0
	r=rospy.Rate(40)
	print "turning"
    	while(  current_angle < relative_angle and (not rospy.is_shutdown())):
        	velocity_publisher.publish(vel_msg)
        	t1 = rospy.Time.now().to_sec()
		r.sleep()
        	current_angle = angular_speed*(t1-t0)
        vel_msg.angular.z = abs(0)
        velocity_publisher.publish(vel_msg)
	rospy.sleep(1)

def move_forward():
	data=rospy.wait_for_message("/scan", LaserScan)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)	
	current_dis=0
	t1=0
	t0=0
	print (data.angle_min)
	center=data.ranges[0]
	rospy.loginfo(center)
	msg= Twist()
	if( center>0.7):
		msg.linear.x= 0.1
	else:
		msg.linear.x= 0.0
		pub.publish(msg)
		return False
	t0=rospy.Time.now().to_sec()
	r=rospy.Rate(40)
	while((not rospy.is_shutdown()) and current_dis<0.3):
		pub.publish(msg)
		t1=rospy.Time.now().to_sec()
		r.sleep()
		current_dis=msg.linear.x*(t1-t0)
			
	print "current dis"+str(current_dis)
	msg.linear.x= 0.0	
	pub.publish(msg)
	return True

def find_object(r,g,b):


	print "find object"
   	imgdata=rospy.wait_for_message('usb_cam/image_raw',Image)
	if(imgdata is None):
		print "error reciving image from camera"
		return None,None
	bridge = CvBridge()
	image = bridge.imgmsg_to_cv2(imgdata,"bgr8")
	print "we have image :)"
    	camInfodata=rospy.wait_for_message('usb_cam/camera_info',CameraInfo)
	if(camInfodata is None):
		print "error reciving caminfo"
		return None,None
	camInfo=camInfodata
	print "camInfo:" +str(camInfo.K[0])+  str(camInfo.K[1])+ str(camInfo.K[2])
    	scannerdata=rospy.wait_for_message('scan',LaserScan)
	if(scannerdata is None):
		print "error getting scanner data"
		return None,None
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
			return  None,None
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
			return actual_distance ,alpha

def find_angle(r,g,b):


	print "find angle"
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
	#print "camInfo:" +str(camInfo.K[0])+  str(camInfo.K[1])+ str(camInfo.K[2])
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
			print "alpha = "+str(distance_index)			
			return distance_index

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
def move_to_object():
	data=rospy.wait_for_message("/scan", LaserScan)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)	
	current_dis=0
	t1=0
	t0=0
	
	center=data.ranges[0]
	print "Range[0] "+str(center)
	msg= Twist()
	if( center>0.5):
		msg.linear.x= 0.1
	else:
		msg.linear.x= 0.0
		pub.publish(msg)
		return False
	t0=rospy.Time.now().to_sec()
	r=rospy.Rate(40)
	
	while((not rospy.is_shutdown()) and current_dis<(center-0.6)):
		pub.publish(msg)
		t1=rospy.Time.now().to_sec()
		r.sleep()
		current_dis=msg.linear.x*(t1-t0)
			
	print "current dis"+str(current_dis)
	msg.linear.x= 0.0	
	pub.publish(msg)
	return True

def move ():
	global r
	global g
	global b
	r=input("insert red\n")
	g=input ("insert green\n")
	b=input("insert blue\n")
	found=False
	print "move function"
	len, ang=find_object(r,g,b)
	i=0
	while(len is None or (not i==13) ):
		#moved = move_forward()
		#print "moved: "+str(moved)
		rotate(30)
		i+=1
	        len, ang=find_object(r,g,b) 
	print "ang main" +str(ang)
	#rotate(ang*180/(2*PI))
	print "Rotated"
	move_to_object()
	print "moved to object"

		

if __name__ == '__main__':
     try:
	 rospy.init_node('move', anonymous=True)
         move()
     except rospy.ROSInterruptException: pass
