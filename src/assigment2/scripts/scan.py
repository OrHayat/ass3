#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Quaternion
from image_geometry import PinholeCameraModel
from sensor_msgs.msg import CameraInfo
import numpy as np
import cv2
import math
import image_geometry
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()
PI = 3.1415926535897
def printCommands():
	rospy.init_node('turtle_script')
    	#pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	while(1):
		commandNum = raw_input("Enter Command Number: \n0.Exit\n1.Move Forward\n2.Turn Around\n3.Distance to object with color X\n4.Find object with color X\n ")
		while((commandNum!='1') & (commandNum!='2') & (commandNum!='3') & (commandNum!='4') & (commandNum!='5') & (commandNum!='0')):
			commandNum = raw_input("You entered wrong command number")
		if commandNum=='1':
			moveForward()
		elif commandNum=='2':
			turnAround()
		elif commandNum=='3':
			distanceObject()
		elif commandNum=='4':
			findObject()
		#elif commandNum=='5':
			#IMAGE = rospy.wait_for_message('/camera/image_raw',Image)
			#cv_image = bridge.imgmsg_to_cv2(IMAGE,'bgr8')
			#cv2.imshow("CheckColor", cv_image)
			#cv2.waitKey(0);
		elif commandNum=='0':
			break
		

def moveForward():
	#rospy.init_node('scan_values')
	msg = rospy.wait_for_message('/scan',LaserScan)
	#print msg
	print msg.ranges[0]
	if (msg.ranges[0]>0.5):
		velpub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
		move = Twist()
		move.linear.x=0.05
		move.linear.y=0
		move.linear.z=0
		move.angular.x=0
		move.angular.y=0
		move.angular.z=0
		while not rospy.is_shutdown():
			t0=rospy.Time.now().to_sec()
			current_distance =0
			while(current_distance < 0.5):
				velpub.publish(move)
				t1=rospy.Time.now().to_sec()
				current_distance = 0.1*(t1-t0)

			move.linear.x=0
			velpub.publish(move)
			break
	else:
		print "too close to obstacle"
		return None
	return 1

def moveForwardAuto():
	#rospy.init_node('scan_values')
	msg = rospy.wait_for_message('/scan',LaserScan)
	#print msg
	print msg.ranges[0]
	if (msg.ranges[0]>0.6):
		velpub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
		move = Twist()
		move.linear.x=0.15
		move.linear.y=0
		move.linear.z=0
		move.angular.x=0
		move.angular.y=0
		move.angular.z=0
		while not rospy.is_shutdown():
			t0=rospy.Time.now().to_sec()
			current_distance =0
			while(current_distance < 0.3):
				velpub.publish(move)
				t1=rospy.Time.now().to_sec()
				current_distance = 0.1*(t1-t0)
			print "Moved forward"

			move.linear.x=0
			velpub.publish(move)
			return 1
			break
	else:
		print "too close to obstacle"
		return None
	return 1
def rotate(alpha):
	global PI
	#rospy.init_node('rotate_turtle',anonymous=True)
	velpub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
	rotate = Twist()
	#Converting from angles to radians
	speed = alpha
	angular_speed = speed*2*PI/360
	print angular_speed
	relative_angle = alpha*2*PI/360
	print "relative angle: "
	print relative_angle
	rotate.linear.x=0
	rotate.linear.y=0
	rotate.linear.z=0
	rotate.angular.x = 0
	rotate.angular.y = 0
	rotate.angular.z=-abs(angular_speed) #clockwise 
	
	t0 = rospy.Time.now().to_sec()
	current_angle=0
	while(current_angle < relative_angle):
		velpub.publish(rotate)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)

	rotate.angular.z=0
	velpub.publish(rotate)

def turnAround():
	alpha = input("Enter alpha angle to rotate alpha degrees clockwise: ")
	global PI
	#rospy.init_node('rotate_turtle',anonymous=True)
	velpub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
	rotate = Twist()
	#Converting from angles to radians
	speed = alpha/5
	angular_speed = speed*2*PI/360
	print angular_speed
	relative_angle = alpha*2*PI/360
	print "relative angle: "
	print relative_angle
	rotate.linear.x=0
	rotate.linear.y=0
	rotate.linear.z=0
	rotate.angular.x = 0
	rotate.angular.y = 0
	rotate.angular.z=-abs(angular_speed) #clockwise 
	
	t0 = rospy.Time.now().to_sec()
	current_angle=0
	while(current_angle < relative_angle):
		velpub.publish(rotate)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)

	rotate.angular.z=0
	velpub.publish(rotate)
	#rospy.spin()
	
def distance(color):
	IMAGE = rospy.wait_for_message('/camera/image_raw',Image)
	camera_info = rospy.wait_for_message('/camera/camera_info',CameraInfo)
	scan = rospy.wait_for_message('/scan',LaserScan)
	cv_image = bridge.imgmsg_to_cv2(IMAGE,'bgr8')
	#cv2.imwrite("FirstPhoto.jpg", cv_image)
	color_boundaries = [
	([0,0,100],[97,105,255]),
	([100, 0, 0], [255, 204, 70]),
	([0,70,0], [93,236,178]),
	([19,230,240], [40,255,255]),
	([95, 45, 120], [130, 70, 150])]
	if(color == "red"):
		numColor = 0;
	elif(color == "blue"):
		numColor = 1;
	elif(color == "green"):
		numColor = 2;
	elif(color == "yellow"):
		numColor = 3;
	elif(color == "purple"):
		numColor = 4;
	else:
		return
	boundaries_chosen = color_boundaries[numColor]
	lower = np.array(boundaries_chosen[0],dtype="uint8")
	upper = np.array(boundaries_chosen[1],dtype="uint8")
	mask_image = cv2.inRange(cv_image, lower, upper)
	#cv2.imwrite("MaskPhoto.jpg", mask_image)
	if(camera_info != 0 and scan!=0 and IMAGE != 0):
		camera = image_geometry.PinholeCameraModel()
		camera.fromCameraInfo(camera_info)
		#gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(mask_image, (5, 5), 0)
		#cv2.imwrite("BlurrePhoto.jpg", blurred)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1] 
		#cv2.imwrite("BlurredAfterPhoto.jpg", thresh)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts1 = cnts[1]
		cXreal = None
		cYreal = None
		perimeterMax = 0
		print len(cnts1)
		for c in cnts1:
			# compute the center of the contour
			M = cv2.moments(c)
			if M["m00"] != 0:
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				perimeter = cv2.arcLength(c,True)
				if(perimeter > perimeterMax):
					cXreal = cX
					cYreal = cY
					perimeterMax = perimeter
				
				print "perimeter is: "+str(perimeter)
				print "radius is: "+str(cX)+" , "+str(cY)
				# draw the contour and center of the shape on the image
				cv2.drawContours(cv_image, [c], -1, (0, 255, 0), 2)
				cv2.circle(cv_image, (cX, cY), 7, (255, 255, 255), -1)

		radius_center= (cXreal,cYreal)
		#cv2.imwrite("NewPhoto.jpg",cv_image)
		#print "radius center = "+str(radius_center)
		if(perimeterMax <350):
			print "Color not found"
		else:
			ray = camera.projectPixelTo3dRay(camera.rectifyPoint(radius_center))
			#print ("x = "+str(ray[0])+" y = "+str(ray[1])+" z = "+str(ray[2]))
			alpha = np.dot(ray[0],ray[2])
			#print ("alpha = "+str(math.degrees(alpha)))
			if(alpha<0):
				alpha = -alpha
			alpha = math.floor(math.pi*2 - alpha)
			#print "min = "+str(scan.angle_min)
			#print "increment = "+str(scan.angle_increment)
			scan_index = int((alpha - scan.angle_min) / scan.angle_increment)
			#print "index = "+str(scan_index)
			real_distance = scan.ranges[scan_index]
			print "real distance: " +str(real_distance)
			if(real_distance< 10):
				return real_distance
			else:
				return None

	else: 
		print "NULL"
		return None
def distanceObject():
	color = raw_input("Enter color to get distance to object with that color: ")
	IMAGE = rospy.wait_for_message('/camera/image_raw',Image)
	camera_info = rospy.wait_for_message('/camera/camera_info',CameraInfo)
	scan = rospy.wait_for_message('/scan',LaserScan)
	cv_image = bridge.imgmsg_to_cv2(IMAGE,'bgr8')
	#cv2.imwrite("FirstPhoto.jpg", cv_image)
	color_boundaries = [
	([0,0,100],[97,105,255]),
	([128, 0, 0], [255, 70, 70]),
	([0,70,0], [93,236,178]),
	([19,230,240], [40,255,255]),
	([95, 45, 120], [130, 70, 150])]
	if(color == "red"):
		numColor = 0;
	elif(color == "blue"):
		numColor = 1;
	elif(color == "green"):
		numColor = 2;
	elif(color == "yellow"):
		numColor = 3;
	elif(color == "purple"):
		numColor = 4;
	else:
		return
	boundaries_chosen = color_boundaries[numColor]
	lower = np.array(boundaries_chosen[0],dtype="uint8")
	upper = np.array(boundaries_chosen[1],dtype="uint8")
	mask_image = cv2.inRange(cv_image, lower, upper)
	#cv2.imwrite("MaskPhoto.jpg", mask_image)
	if(camera_info != 0 and scan!=0 and IMAGE != 0):
		camera = image_geometry.PinholeCameraModel()
		camera.fromCameraInfo(camera_info)
		#gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(mask_image, (5, 5), 0)
		#cv2.imwrite("BlurrePhoto.jpg", blurred)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1] 
		#cv2.imwrite("BlurredAfterPhoto.jpg", thresh)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts1 = cnts[1]
		cXreal = None
		cYreal = None
		perimeterMax = 0
		print len(cnts1)
		for c in cnts1:
			# compute the center of the contour
			M = cv2.moments(c)
			if M["m00"] != 0:
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				perimeter = cv2.arcLength(c,True)
				if(perimeter > perimeterMax):
					cXreal = cX
					cYreal = cY
					perimeterMax = perimeter
				
				print "perimeter is: "+str(perimeter)
				print "radius is: "+str(cX)+" , "+str(cY)
				# draw the contour and center of the shape on the image
				cv2.drawContours(cv_image, [c], -1, (0, 255, 0), 2)
				cv2.circle(cv_image, (cX, cY), 7, (255, 255, 255), -1)

		radius_center= (cXreal,cYreal)
		#cv2.imwrite("NewPhoto.jpg",cv_image)
		#print "radius center = "+str(radius_center)
		if(perimeterMax <350):
			print "Color not found"
		else:
			ray = camera.projectPixelTo3dRay(camera.rectifyPoint(radius_center))
			#print ("x = "+str(ray[0])+" y = "+str(ray[1])+" z = "+str(ray[2]))
			alpha = np.dot(ray[0],ray[2])
			#print ("alpha = "+str(math.degrees(alpha)))
			if(alpha<0):
				alpha = -alpha
			alpha = math.floor(math.pi*2 - alpha)
			#print "min = "+str(scan.angle_min)
			#print "increment = "+str(scan.angle_increment)
			scan_index = int((alpha - scan.angle_min) / scan.angle_increment)
			#print "index = "+str(scan_index)
			real_distance = scan.ranges[scan_index]
			print "real distance: " +str(real_distance)
			return real_distance

	else: 
		print "NULL"
		return None


def findObject():
	color = raw_input("Enter color to find object with that color: ")	
	while(distance(color) is None):
		moved = moveForwardAuto()
		if(moved is None):
			rotate(40)
			
				
		
		
		
		

if __name__ == '__main__':
    try:
        printCommands()
    except rospy.ROSInterruptException:
        passen
