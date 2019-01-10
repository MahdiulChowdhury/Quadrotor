import rospy
import math
import numpy as np
import mavros_msgs
from geometry_msgs.msg import PoseStamped, TwistStamped
import mavros
from mavros import command
from mavros_msgs.srv import CommandBool, ParamGet, SetMode
from mavros_msgs.msg import State
import rospy
import states  ##script
import inspect
from std_msgs.msg import String



class StateMachine():


	def __init__(self):

		self.current_state=0; #this should be the "idle=not armed" state
		self.new_state = rospy.Subscriber('state_machine/command',String,self.command_callback)
		self.states_list=[states.IdleNotArmed(),states.Arming(),states.Takeoff(),states.Grounded()] #this list should be automatically generated by introspection
		#print "length"+str(len(self.states_list))
	def state_name_to_index(self, state_name):
		''' Converts a string with a state name to the index in states[] corresponding to the class with that name'''
		for idx,state in enumerate(self.states_list):
			if state.__class__.__name__ == state_name:
				idx_selected=idx
				break

		return idx_selected


	def command_callback(self, msg):
		print "Received ", msg.data
		state_name=msg.data;
		state_index=self.state_name_to_index(state_name)
		print  "new state", state_index
		self.current_state=state_index



	def run(self):
##"""Polls the current state every 100ms to run"""
		self.rate = rospy.Rate(10)
        	while not rospy.is_shutdown():
            		#if self.current_state in self.states_list:
			#print "current state:", self.current_state
                	self.states_list[self.current_state].run() ##run.Arming()
            		#else:
                		#rospy.logerr("State %s not in dictionary" % self.current_state)
                		#self._add_state(self.current_state)
         	self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('state_machine', anonymous=True) #initializing the node
	sm = StateMachine()
	sm.run()