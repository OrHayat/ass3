#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
def stop():
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)	
	msg=Twist()
	msg.linear.x=0.08
	pub.publish(msg)
	rospy.sleep(0.5)

	msg.linear.x=0.06
	pub.publish(msg)
	rospy.sleep(0.5)

	msg.linear.x=0.04
	pub.publish(msg)
	rospy.sleep(0.5)

	msg.linear.x=0.02
	pub.publish(msg)
	rospy.sleep(0.5)

	msg.linear.x=0
	pub.publish(msg)
	rospy.sleep(0.2)
	
		

def move():
	data=rospy.wait_for_message("/scan", LaserScan)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)	
	current_dis=0
	t1=0
	t0=0
	print (data.angle_min)
	center=data.ranges[0]
	rospy.loginfo(center)
	msg= Twist()
	if( center>0.5):
		msg.linear.x= 0.1
	else:
		msg.linear.x= 0.0
		pub.publish(msg)
		return
	t0=rospy.Time.now().to_sec()
	r=rospy.Rate(40)
	while(current_dis<0.4 and (not rospy.is_shutdown())):
		pub.publish(msg)
		t1=rospy.Time.now().to_sec()
		r.sleep()
		current_dis=msg.linear.x*(t1-t0)
	print current_dis
	stop()	

	
if __name__ == '__main__':
	rospy.init_node('checkObstacle', anonymous=True)
	move()

