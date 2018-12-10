

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
import inspect
from std_msgs.msg import String
import rospy
import potential_path_vel as pp
import controller
from std_msgs.msg import Header
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry as Odom

current_pose = PoseStamped()
set_vel = TwistStamped()
current_state = State()

def state_callback(state_data):
	global current_state
	current_state = state_data

class base_state:
	def __init__(): 
		rospy.init_node('Controller', anonymous='True')
		self.my_state = rospy.Subscriber('/mavros/state',State,state_callback) #subscribing to local state 
		##vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size = 1) #publishing the velocity 
		#local_position_subscribe = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, pos_sub_callback) #updating the local position
		self.service_timeout = 30
	        rospy.loginfo("waiting for ROS services")
	    #Publisher to send commands to the state machine
	    self.state_machine_command=rospy.Publisher('state_machine/command',std_msgs::String)


class IdleNotArmed(base_state):
	''' Do not do anything with the quadrotor'''
	def run():
		pass



class Arming (base_state):
	''' This state tries to arm the motors. If they are armed, transition to "Grounded" '''

	def __init__():
		super().__init__():

	def run(): 
		# Ensure all services are running, and switch Quad to offboard
		#while current_state.mode != "OFFBOARD" or not current_state.armed:
		#If it is not armed, try to arm, otherwise tell the state machine to switch to armed
		if current_state.mode != "OFFBOARD" or not current_state.armed:

			arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
	        arm(True)
	        set_mode = rospy.ServiceProxy('/mavros/set_mode',SetMode)
	        mode = set_mode(custom_mode='OFFBOARD')
	    else:
	    	self.state_machine_command.publish('Grounded')
		rospy.wait_for_service('mavros/set_mode', service_timeout)
		rospy.loginfo("ROS services are up")
		if not mode.mode_sent:
				rospy.logerr("failed to send mode command")


class Grounded():
	''' When in this state, the quadrotor is on the ground, or, it is not, it is landing '''

	def run():
		if not mavros_is_landed():
			mavros.land()
		else:
			pass
	
class Waypoint: 





class Search: 





class Inactive:




class Landed:






class Hover: 






class Potential_Avoidance: 







