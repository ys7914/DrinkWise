import rospy
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

rospy.init_node('say',anonymous = True)
soundhandle = SoundClient()
rospy.sleep(3)

voice = 'voice_kal_diphone'
volume = 1.0

def callback(data):
	soundhandle.say(data.data, voice, volume)
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
	rospy.Subscriber("chatter", String, callback)
	rospy.spin()

listener()
