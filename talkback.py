#!/usr/bin/env python
import rospy, os, sys
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from opencv_apps.msg import FaceArrayStamped
from opencv_apps.msg import Face
class TalkBack:
     def __init__(self, script_path):
         rospy.init_node('talkback')

         rospy.on_shutdown(self.cleanup)

         # Create the sound client object
         #self.soundhandle = SoundClient()
         self.soundhandle = SoundClient(blocking=True)

         # Wait a moment to let the client connect to the sound_play server
         rospy.sleep(1)

         # Make sure any lingering sound_play processes are stopped.
         self.soundhandle.stopAll()

         
         #Announce that we are ready
        
         rospy.loginfo("Say one of the navigation commands...")

         # Subscribe to the recognizer output and set the callback function
         rospy.Subscriber('/lm_data', String, self.talkback)

	 #Publish to go_to_the_location
         self.go = rospy.Publisher("/go_to_the_location", String, queue_size=10) 
             
     def face_back(self,face_data):
         pos = face_data.faces
         if pos:
             self.face_x=pos[0].face.x
             self.face_y=pos[0].face.y

     def talkback(self, msg):
         #Print the recognized words on the screen
         rospy.loginfo(msg.data)

         if msg.data.find('IS YOUR NAME')>-1:
		self.soundhandle.say("My name is Jack. I am your personal robot, sir")
		#rospy.sleep(10) 
	 elif msg.data.find('OLD ARE YOU')>-1:
		self.soundhandle.say("Two years old, sir.")
		#rospy.sleep(5) 
	 elif msg.data.find('ARE YOU FROM')>-1:
        	#rospy.sleep(1)
		self.soundhandle.say("I am from China, sir.")
		#rospy.sleep(5)
	 elif msg.data.find('DO FOR ME')>-1:
        	#rospy.sleep(1)
		self.soundhandle.say("I can talk with you and do some housework,sir .")
		#rospy.sleep(5)
         elif msg.data.find('THANK YOU')>-1:
        	#rospy.sleep(1)
		self.soundhandle.say("My pleasure, sir.")
		#rospy.sleep(5)
         #elif msg.data.find('TAKE A PHOTO')>-1:
         #      self.soundhandle.say("It is a piece of cake for me.")
                #rospy.sleep(1)
         #      while(True):
	#		if self.face_x<180 and self.face_x>0:
	#			self.soundhandle.say("A little to the left, please.")
	#			self.face_x=0
	#			rospy.sleep(1)
	#		elif self.face_x>460 and self.face_x<640:
	#			self.soundhandle.say("A little to the right, please.")
	#			self.face_x=0
	#			rospy.sleep(1)
	#		elif self.face_x>=180 and self.face_x<=460:
	#			self.soundhandle.say("Perfect.")
	#			break
	#	self.soundhandle.say("3! 2! 1!")
	#	self.take_photo.publish('take photo')
	#	self.soundhandle.say("Got it,sir.")
         elif msg.data.find('GO TO THE CUBE')>-1:
        	#rospy.sleep(1)
		self.soundhandle.say("I am going to the cube.")
		self.go.publish('go to the cube')
         elif msg.data.find('GO TO THE GARBAGE')>-1:
        	#rospy.sleep(1)
		self.soundhandle.say("I am going to the garbage.")
		self.go.publish('go to the garbage')
         elif msg.data.find('GO TO THE BOOKSHELF')>-1:
        	#rospy.sleep(1)
		self.soundhandle.say("I am going to the bookshelf.")
		self.go.publish('go to the bookshelf')
         elif msg.data=='':
             rospy.sleep(1)

     def cleanup(self):
         self.soundhandle.stopAll()
         rospy.loginfo("Shutting down talkbot node...")

if __name__=="__main__":
    try:
        TalkBack(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Talkback node terminated.")
