#!/usr/bin/env python

"""

    RoboCup@Home Education | oc@robocupathomeedu.org
    navi.py - enable turtlebot to navigate to predefined waypoint location

"""

import rospy

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler


class NavToPoint:
    def __init__(self):
        
        
        rospy.on_shutdown(self.cleanup)
        
	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")
            
        rospy.loginfo("Ready to go")

	rospy.sleep(1)

	self.locations = dict()

	rospy.Subscriber('/go_to_the_location', String, self.to)

	# Location Cube
	A_x = 0.6
	A_y = 0.0444
	A_theta = 0

	quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
	locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	# Location Garbage
	B_x = -0.602
	B_y = -3.44
	B_theta = 0

	quaternion = quaternion_from_euler(0.0, 0.0, B_theta)
	locations['B'] = Pose(Point(B_x, B_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	# Location Bookshelf
	C_x = -1.17
	C_y = 1.37
	C_theta = 0

	quaternion = quaternion_from_euler(0.0, 0.0, C_theta)
	locations['C'] = Pose(Point(C_x, C_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	self.goal = MoveBaseGoal()
        rospy.loginfo("Starting navigation test")

    def to(self,data):
	self.goal.target_pose.header.frame_id = 'map'
	self.goal.target_pose.header.stamp = rospy.Time.now()
	# Cube
	if data.data == "go to the cube":
	    rospy.sleep(2)
	    self.goal.target_pose.pose = self.locations['A']
	    self.move_base.send_goal(self.goal)
	    waiting = self.move_base.wait_for_result(rospy.Duration(300))
            if waiting == 1:
		rospy.loginfo("Reached the Cube")
	#Garbage
	elif data.data == "go to the garbage":
            rospy.sleep(2)
	    self.goal.target_pose.pose = self.locations['B']
	    self.move_base.send_goal(self.goal)
	    waiting = self.move_base.wait_for_result(rospy.Duration(300))
            if waiting == 1:
		rospy.loginfo("Reached the Garbage")
	#Bookshelf
	elif data.data == "go to the bookshelf":
            rospy.sleep(2)
	    self.goal.target_pose.pose = self.locations['C']
	    self.move_base.send_goal(self.goal)
	    waiting = self.move_base.wait_for_result(rospy.Duration(300))
            if waiting == 1:
		rospy.loginfo("Reached the Bookshelf")

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
	self.move_base.cancel_goal()

if __name__=="__main__":
    rospy.init_node('navi_point')
    try:
        NavToPoint()
        rospy.spin()
    except:
        pass

