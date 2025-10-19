#!/usr/bin/env python3

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

from blob_search import blob_search
from ur3_driver.msg import command
from ur3_driver.msg import position

PI = 3.1415926535

class VisionSafety:

    def __init__(
        self,
        vel,
        accel,
    ):
        if vel > 2 or accel > 2:
            raise RuntimeError('vel and accel cannot be set larger than 2.')
        self.vel = vel
        self.accel = accel
        self.bridge = CvBridge()
        self.SPIN_RATE = 20
        self.loop_rate = rospy.Rate(self.SPIN_RATE)
        self.thetas = [0,0,0,0,0,0]
        self.object_pos = []  # Initialize object position
        self.human_detected_prev = False  # Track previous detection state
        
        # Define safety region (adjust these coordinates to cover robot motion range)
        # Format: (x_min, y_min, x_max, y_max) - adjust based on your camera view
        # You may need to tune these values based on your camera setup
        self.safety_region = (100, 100, 540, 380)  # Rectangle covering robot workspace
        
        self.dest1 = [270*PI/180.0, -90*PI/180.0, 90*PI/180.0, -90*PI/180.0, -90*PI/180.0, 135*PI/180.0]
        self.dest2 = [90*PI/180.0, -90*PI/180.0, 90*PI/180.0, -90*PI/180.0, -90*PI/180.0, 135*PI/180.0]
        self.goal_index = 2
        self.break_flag = False
        self.curr_dest = self.dest2
        self.at_goal = 0
        self.command_pub = rospy.Publisher('ur3/command', command, queue_size=10)
        rospy.Subscriber('ur3/position', position, self.position_callback)
        rospy.Subscriber("/cv_camera_node/image_raw", Image, self.image_callback)
        rospy.sleep(1)
        rospy.loginfo("Vision safety initialized.")
 
    def image_callback(self, data):
        # ****************************************
        # *** You may modify this part of code ***
        try:
            raw_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.loginfo(e)
        cv_image = cv2.flip(raw_image, -1)
        blob_image_center, im_with_keypoints = blob_search(cv_image, "green") # * you may need to modify blob_search function.
        self.object_pos = blob_image_center
        
        # Draw safety region on visualization
        x_min, y_min, x_max, y_max = self.safety_region
        cv2.rectangle(im_with_keypoints, (x_min, y_min), (x_max, y_max), (0, 0, 255), 3)  # Red rectangle
        
        # Add text label for safety region
        cv2.putText(im_with_keypoints, "SAFETY REGION", (x_min, y_min - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Draw detected objects and check if they're in safety region
        for obj_pos in blob_image_center:
            obj_x, obj_y = int(obj_pos[0]), int(obj_pos[1])
            # Check if object is in safety region
            if x_min <= obj_x <= x_max and y_min <= obj_y <= y_max:
                # Object in safety region - draw red circle
                cv2.circle(im_with_keypoints, (obj_x, obj_y), 15, (0, 0, 255), 3)
                cv2.putText(im_with_keypoints, "IN SAFETY ZONE", (obj_x - 50, obj_y - 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                # Object outside safety region - draw green circle
                cv2.circle(im_with_keypoints, (obj_x, obj_y), 15, (0, 255, 0), 3)
                cv2.putText(im_with_keypoints, "OUTSIDE", (obj_x - 30, obj_y - 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Vision Safety", im_with_keypoints)
        cv2.waitKey(2)    
        self.break_flag = self.safety_function()
        # ****************************************

    def position_callback(self, msg):
        self.thetas[0] = msg.position[0]
        self.thetas[1] = msg.position[1]
        self.thetas[2] = msg.position[2]
        self.thetas[3] = msg.position[3]
        self.thetas[4] = msg.position[4]
        self.thetas[5] = msg.position[5]
        
    def safety_function(self):
        # ****************************************
        # *** You may modify this part of code ***
        # Check if ANY green object (human) is detected in the safety region
        human_in_safety_region = False
        objects_in_region = 0
        total_objects = len(self.object_pos)
        
        if self.object_pos:
            x_min, y_min, x_max, y_max = self.safety_region
            for obj_pos in self.object_pos:
                obj_x, obj_y = obj_pos[0], obj_pos[1]
                # Check if this object is within the safety region
                if x_min <= obj_x <= x_max and y_min <= obj_y <= y_max:
                    human_in_safety_region = True
                    objects_in_region += 1
        
        # Only log when detection state changes
        if human_in_safety_region and not self.human_detected_prev:
            rospy.logwarn(f"SAFETY VIOLATION: {objects_in_region}/{total_objects} object(s) in safety region! Stopping robot.")
        elif not human_in_safety_region and self.human_detected_prev:
            if total_objects > 0:
                rospy.loginfo(f"Safety region clear. {total_objects} object(s) detected outside region. Robot can resume.")
            else:
                rospy.loginfo("No objects detected. Robot can resume.")
        
        self.human_detected_prev = human_in_safety_region
        return human_in_safety_region  # Stop robot if ANY object is in safety region
        # ****************************************
        
    def move_arm(self, goal_index):
        driver_msg = command()
        if goal_index == 1:
            driver_msg.destination = self.dest1
            self.curr_dest = self.dest1
        elif goal_index == 2:
            driver_msg.destination = self.dest2
            self.curr_dest = self.dest2
        else:
            raise RuntimeError
        driver_msg.v = self.vel
        driver_msg.a = self.accel
        self.command_pub.publish(driver_msg)
        self.loop_rate.sleep()
        while self.at_goal==0:
            if self.break_flag:
                break
            if  abs(self.thetas[0]-self.curr_dest[0]) < 0.0005 and \
                abs(self.thetas[1]-self.curr_dest[1]) < 0.0005 and \
                abs(self.thetas[2]-self.curr_dest[2]) < 0.0005 and \
                abs(self.thetas[3]-self.curr_dest[3]) < 0.0005 and \
                abs(self.thetas[4]-self.curr_dest[4]) < 0.0005 and \
                abs(self.thetas[5]-self.curr_dest[5]) < 0.0005:
                self.at_goal = 1
                return 1
            self.loop_rate.sleep()
        return 0

    def run(self, goal_index):
        while self.at_goal != 1 and not rospy.is_shutdown():
            self.move_arm(goal_index)
            self.loop_rate.sleep()
        self.at_goal = 0

def main():
    rospy.init_node('mp1_node')
    # ****************************************
    # *** You may modify this part of code ***
    vel = 0.25 # set a value between 0 and 2
    accel = 0.25 # set a value between 0 and 2
    # ****************************************
    vs = VisionSafety(vel, accel)
    while(not rospy.is_shutdown()):
        rospy.loginfo("go to goal 2")
        vs.run(2)
        rospy.loginfo("go to goal 1")
        vs.run(1)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass