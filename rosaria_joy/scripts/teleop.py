#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def callback(data):
    twist = Twist()
    # vertical left stick axis = linear rate
    twist.linear.x = 4*data.axes[1]
    # horizontal left stick axis = turn rate
    twist.angular.z = 4*data.axes[0]
    pub.publish(twist)

# Intializes everything
def listener():

    # starts the node
    rospy.init_node('listener', anonymous=True)
    
    # publishing to "RosAria/cmd_vel" to control turtle1
    global pub
    pub = rospy.Publisher('RosAria/cmd_vel', Twist)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber("joy", Joy, callback)
    
    # keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
