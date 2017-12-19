import cv2
import face_recognition
import time
import rospy
from std_msgs.msg import Int16

window_counter = 0

subject_counter = 1
training_encodings = []
subject_names = []
person = 0;

queue = []
temp_queue = []



def queue_member_collector(frame_names, queue_names):
    for nam in frame_names:
        if nam not in queue_names:
            queue_names.append(nam)
    return;

def queue_handler(new_names, queue_names):
    #remove patrons that weren't present for a majority of frames
    for nam in new_names:

        if new_names.count(nam) < 3:

            del(nam)

    #remove members of queue who were not consistently present for the capture
    for q in queue_names:
        if q not in new_names:
            queue_names.remove(q)
        else:
            break;

    # append new patrons waiting to the queue
    for nam in new_names:
        if nam not in queue_names:
            queue_names.append(nam)

    # take off the first queue member and return
    next_name = queue_names[0]
    #queue_names.remove(next_name)
    return next_name


def face_recogniser(subject_counter):
    global temp_queue
    global queue
    global window_counter
    temp_queue = queue

    s_counter = subject_counter
    face_locations = []
    face_encodings = []

    locs_and_names = []

    new_faces = []
    short_delay = 5

    ##start video feed
    video_feed = cv2.VideoCapture(0)

    ret, save_frame = video_feed.read()

    while(short_delay is not 0):
        ## find all faces in feed
        # Grab a single frame of video
        ret, frame = video_feed.read()

	locs_and_names = []

        frame = cv2.flip(frame, 1)
	#cv2.imshow('hi' ,frame)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
	#print('number of faces present: ', len(face_encodings))
        face_names = []
        for idx, face_encoding in enumerate(face_encodings):
            name = 0
            # See if the face is a match for the known face(s)
            if len(training_encodings) is not 0:
                match = face_recognition.compare_faces(training_encodings, face_encoding)
                for mat, subject in zip(match, subject_names):
                    if mat:
                        name = subject
			locs_and_names.append((subject, face_locations[idx]))
                        break;
                if name is 0:
		    #print('new face added')
                    name = s_counter
                    subject_names.append(name)
                    training_encodings.append(face_encoding)
                    s_counter += 1
            else:	# if training_encoding is none this is the first time this has been run and so there is no data to compare the faces against
		#print('first face added')
                name = s_counter
                subject_names.append(name)
                training_encodings.append(face_encoding)
                s_counter += 1

            face_names.append(name)

        # Display the resulting image
        #cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #queue_member_collector(face_names, queue)
        if(len(face_names) is not 0):
            new_faces += face_names
            short_delay -= 1

    
    next_patron = queue_handler(new_faces, temp_queue)
    top = 0
    right = 0
    left = 0
    bottom = 0
    print(locs_and_names)
    #print(subject_names.index(next_patron))
    for fred in locs_and_names:
	if next_patron is fred[0]:
		top, right, bottom, left = fred[1]
		break; #as in adem is about to break :/

    save_frame = cv2.flip(save_frame, 1)
    picture_out = cv2.rectangle(save_frame, (left, top), (right, bottom), (0, 0, 255), 2)
    #picture_out = cv2.flip(picture_out, -1)
    #picture_out = cv2.circle(save_frame, (50,50), 25, (0,0,255), 2)
    cv2.namedWindow(str(window_counter), cv2.WINDOW_NORMAL)
    cv2.imshow(str(window_counter), picture_out)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    window_counter += 1


    video_feed.release()
    video_feed.release()

    return next_patron, s_counter

pub = rospy.Publisher('face', Int16, queue_size=10)
rospy.init_node('face', anonymous=True)



def get_face(data):
    global queue
    global temp_queue
    global person;
    cv2.destroyAllWindows()
    global subject_counter
    if data.data == 100:
        print("Looking for face")
        person, subject_counter= face_recogniser(subject_counter)
	pub.publish(300)
        
#again or confirmed
    if data.data == 200: #confirm
	pub.publish(person)
	queue = temp_queue
	if len(queue) > 0:
	    queue.remove(queue[0])
 

rospy.Subscriber('face', Int16, get_face)


while not rospy.is_shutdown():
    time.sleep(5)
