#!/usr/bin/env python
import rospy
PI = 3.1415926535897
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def stop(rotate_last):
	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)	
    	current_angle = 0	
	vel_msg= Twist()
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)		
	print "stop  fun"
	speed=(rotate_last/2)
	angular_speed = speed*2
       	vel_msg.angular.z = abs(angular_speed)
        velocity_publisher.publish(vel_msg)
	rospy.sleep(0.5)

	speed=(rotate_last/3)
	angular_speed = speed*2
       	vel_msg.angular.z = abs(angular_speed)
        velocity_publisher.publish(vel_msg)
	rospy.sleep(0.5)
	
	speed=(rotate_last/6)
	angular_speed = speed*2
       	vel_msg.angular.z = abs(angular_speed)
        velocity_publisher.publish(vel_msg)
	rospy.sleep(0.5)
	
	print 

	speed=0
	angular_speed = 0
       	vel_msg.angular.z = abs(angular_speed)
        velocity_publisher.publish(vel_msg)
	rospy.sleep(0.5)






def rotate():

	velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)	
	current_dis=0
	t1=0
	t0=0
	vel_msg= Twist()
	print("Let's rotate your robot")
	angle = input("Type your distance (degrees):")
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
    	while(  current_angle < relative_angle and (not rospy.is_shutdown())):
        	velocity_publisher.publish(vel_msg)
        	t1 = rospy.Time.now().to_sec()
		r.sleep()
        	current_angle = angular_speed*(t1-t0)
        vel_msg.angular.z = abs(0)
        velocity_publisher.publish(vel_msg)
	rospy.sleep(1)
#stop(relative_angle/5)        



if __name__ == '__main__':
	rospy.init_node('checkObstacle', anonymous=True)
	rotate()

