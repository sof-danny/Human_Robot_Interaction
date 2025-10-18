#!/usr/bin/env python3

import rospy
import cv2
import csv
import numpy as np
from datetime import datetime
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from ur3_driver.msg import position
from blob_search import blob_search
from std_msgs.msg import String

class ExperimentDataCollector:
    """
    Data collection node for MP1 vision safety experiments.
    Records timing, detection success, and robot position data.
    """
    
    def __init__(self):
        rospy.init_node('mp1_data_collector')
        
        self.bridge = CvBridge()
        
        # Trial state
        self.trial_active = False
        self.trial_number = 0
        self.entry_time = None
        self.detection_time = None
        self.stop_time = None
        self.detection_success = False
        self.human_detected = False
        self.human_detected_prev = False
        self.robot_stopped = False
        
        # Robot state
        self.thetas = [0, 0, 0, 0, 0, 0]
        self.prev_thetas = [0, 0, 0, 0, 0, 0]
        self.object_pos = []
        self.min_distance = float('inf')
        
        # Data storage
        self.results = []
        self.csv_filename = f"mp1_experiment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Velocity threshold for considering robot "stopped"
        self.STOP_VELOCITY_THRESHOLD = 0.001  # rad/s
        
        # Initialize CSV file
        self.init_csv()
        
        # Subscribe to topics
        rospy.Subscriber('ur3/position', position, self.position_callback)
        rospy.Subscriber("/cv_camera_node/image_raw", Image, self.image_callback)
        # Optional: subscribe to keyboard input topic to avoid OpenCV focus issues
        rospy.Subscriber('keyboard_input', String, self.keyboard_callback)
        
        rospy.loginfo("="*60)
        rospy.loginfo("MP1 Data Collector Initialized")
        rospy.loginfo(f"Data will be saved to: {self.csv_filename}")
        rospy.loginfo("="*60)
        rospy.loginfo("Press 's' to START a new trial")
        rospy.loginfo("Press 'r' to RESET current trial")
        rospy.loginfo("Press 'q' to QUIT and save data")
        rospy.loginfo("="*60)
        
    def init_csv(self):
        """Initialize CSV file with headers"""
        with open(self.csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Trial',
                'Entry_Time_s',
                'Detection_Time_s', 
                'Stop_Time_s',
                'Detection_Latency_ms',
                'Stop_Latency_ms',
                'Total_Response_ms',
                'Min_Distance_cm',
                'Detection_Success',
                'Notes'
            ])
        rospy.loginfo(f"CSV file created: {self.csv_filename}")
    
    def position_callback(self, msg):
        """Update robot joint positions"""
        self.prev_thetas = self.thetas.copy()
        self.thetas = [
            msg.position[0],
            msg.position[1],
            msg.position[2],
            msg.position[3],
            msg.position[4],
            msg.position[5]
        ]
        
        # Check if robot has stopped during active trial
        if self.trial_active and self.detection_time and not self.robot_stopped:
            velocity = self.calculate_joint_velocity()
            if velocity < self.STOP_VELOCITY_THRESHOLD:
                self.stop_time = rospy.get_time()
                self.robot_stopped = True
                rospy.loginfo(f"[DATA] Robot stopped at t={self.stop_time - self.entry_time:.3f}s")
    
    def calculate_joint_velocity(self):
        """Calculate approximate joint velocity magnitude"""
        velocity = 0
        for i in range(6):
            velocity += abs(self.thetas[i] - self.prev_thetas[i])
        return velocity
    
    def image_callback(self, data):
        """Process camera images for human detection"""
        try:
            raw_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return
        
        cv_image = cv2.flip(raw_image, -1)
        blob_image_center, im_with_keypoints = blob_search(cv_image, "green")
        self.object_pos = blob_image_center
        
        # Display image with trial info overlay
        if self.trial_active:
            status_text = f"Trial {self.trial_number} - ACTIVE"
            color = (0, 255, 0) if not self.human_detected else (0, 0, 255)
        else:
            status_text = "Press 's' to start trial"
            color = (255, 255, 255)
        
        cv2.putText(im_with_keypoints, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        if self.trial_active and self.entry_time:
            elapsed = rospy.get_time() - self.entry_time
            cv2.putText(im_with_keypoints, f"Time: {elapsed:.2f}s", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow("Data Collection", im_with_keypoints)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            self.start_trial()
        elif key == ord('r'):
            self.reset_trial()
        elif key == ord('q'):
            self.quit()
        elif key == ord('e'):
            # Manual entry time marker
            if self.trial_active and not self.entry_time:
                self.mark_entry()
        
        # Check for detection during trial
        if self.trial_active and self.entry_time:
            self.check_detection()

    def keyboard_callback(self, msg):
        """Handle keyboard commands published on 'keyboard_input' topic"""
        try:
            key_char = msg.data.strip().lower()
        except Exception:
            return
        if key_char == 's':
            self.start_trial()
        elif key_char == 'r':
            self.reset_trial()
        elif key_char == 'q':
            self.quit()
        elif key_char == 'e':
            if self.trial_active and not self.entry_time:
                self.mark_entry()
    
    def start_trial(self):
        """Start a new trial"""
        if self.trial_active:
            rospy.logwarn("Trial already active! Press 'r' to reset.")
            return
        
        self.trial_number += 1
        self.trial_active = True
        self.entry_time = None
        self.detection_time = None
        self.stop_time = None
        self.detection_success = False
        self.human_detected = False
        self.human_detected_prev = False
        self.robot_stopped = False
        self.min_distance = float('inf')
        
        rospy.loginfo("="*60)
        rospy.loginfo(f"TRIAL {self.trial_number} STARTED")
        rospy.loginfo("Press 'e' when object ENTERS the workspace")
        rospy.loginfo("Or entry time will be marked automatically on first detection")
        rospy.loginfo("="*60)
    
    def mark_entry(self):
        """Mark the entry time (called manually or automatically)"""
        if not self.trial_active or self.entry_time:
            return
        
        self.entry_time = rospy.get_time()
        rospy.loginfo(f"[DATA] Entry time marked: {self.entry_time}")
    
    def check_detection(self):
        """Check if human is detected"""
        human_detected = self.object_pos and len(self.object_pos) > 0
        
        # Auto-mark entry time on first detection if not already marked
        if human_detected and not self.entry_time:
            self.mark_entry()
            rospy.logwarn("Entry time auto-marked on first detection")
        
        # Record detection time on state change
        if human_detected and not self.human_detected_prev and not self.detection_time:
            self.detection_time = rospy.get_time()
            self.detection_success = True
            rospy.loginfo(f"[DATA] Detection at t={self.detection_time - self.entry_time:.3f}s")
        
        self.human_detected = human_detected
        self.human_detected_prev = human_detected
        
        # Calculate minimum distance (simplified - just tracks detection)
        # For actual distance, you'd need forward kinematics
        if human_detected and len(self.object_pos) > 0:
            # This is a placeholder - real implementation would need FK
            # For now, just use pixel distance as a proxy
            obj_x, obj_y = self.object_pos[0]
            # Assume center of image is robot base projection
            center_x, center_y = 320, 240  # typical camera resolution
            pixel_dist = np.sqrt((obj_x - center_x)**2 + (obj_y - center_y)**2)
            # Convert to approximate cm (this is rough - needs calibration)
            approx_dist_cm = pixel_dist * 0.1  # scaling factor
            if approx_dist_cm < self.min_distance:
                self.min_distance = approx_dist_cm
    
    def reset_trial(self):
        """Reset current trial without saving"""
        if not self.trial_active:
            rospy.logwarn("No active trial to reset")
            return
        
        rospy.logwarn(f"Trial {self.trial_number} RESET (data not saved)")
        self.trial_active = False
        rospy.loginfo("Press 's' to start new trial")
    
    def end_trial(self, notes=""):
        """End trial and save data"""
        if not self.trial_active:
            return
        
        # Wait a moment to ensure stop is detected
        rospy.sleep(0.5)
        
        # Calculate metrics
        detection_latency = None
        stop_latency = None
        total_response = None
        
        if self.entry_time and self.detection_time:
            detection_latency = (self.detection_time - self.entry_time) * 1000  # ms
        
        if self.detection_time and self.stop_time:
            stop_latency = (self.stop_time - self.detection_time) * 1000  # ms
        
        if self.entry_time and self.stop_time:
            total_response = (self.stop_time - self.entry_time) * 1000  # ms
        
        min_dist = self.min_distance if self.min_distance != float('inf') else None
        
        # Save to CSV
        with open(self.csv_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.trial_number,
                0.00 if self.entry_time else None,  # Relative to entry
                f"{detection_latency/1000:.2f}" if detection_latency else None,
                f"{total_response/1000:.2f}" if total_response else None,
                f"{detection_latency:.0f}" if detection_latency else None,
                f"{stop_latency:.0f}" if stop_latency else None,
                f"{total_response:.0f}" if total_response else None,
                f"{min_dist:.1f}" if min_dist else None,
                "✓" if self.detection_success else "✗",
                notes
            ])
        
        # Log summary
        rospy.loginfo("="*60)
        rospy.loginfo(f"TRIAL {self.trial_number} COMPLETE")
        rospy.loginfo(f"  Detection Success: {'YES' if self.detection_success else 'NO'}")
        if detection_latency:
            rospy.loginfo(f"  Detection Latency: {detection_latency:.0f} ms")
        if total_response:
            rospy.loginfo(f"  Total Response: {total_response:.0f} ms")
        if min_dist:
            rospy.loginfo(f"  Min Distance: {min_dist:.1f} cm (approximate)")
        rospy.loginfo("="*60)
        
        self.trial_active = False
        rospy.loginfo("Press 's' to start next trial")
    
    def quit(self):
        """Save data and exit"""
        if self.trial_active:
            user_input = input("Trial active. Save this trial? (y/n): ")
            if user_input.lower() == 'y':
                notes = input("Notes for this trial: ")
                self.end_trial(notes)
        
        rospy.loginfo("="*60)
        rospy.loginfo(f"Data saved to: {self.csv_filename}")
        rospy.loginfo(f"Total trials completed: {self.trial_number}")
        rospy.loginfo("="*60)
        rospy.signal_shutdown("User quit")
    
    def run(self):
        """Main loop"""
        rate = rospy.Rate(20)  # 20 Hz
        
        try:
            while not rospy.is_shutdown():
                # Auto-end trial if robot stopped and detection occurred
                if (self.trial_active and self.detection_success and 
                    self.robot_stopped and not self.human_detected):
                    rospy.loginfo("Trial conditions met. Ending trial...")
                    self.end_trial()
                
                # Manual trial end check
                if self.trial_active and self.entry_time:
                    elapsed = rospy.get_time() - self.entry_time
                    if elapsed > 10.0 and not self.detection_success:
                        rospy.logwarn("Trial exceeded 10s with no detection. Ending trial...")
                        self.end_trial("Timeout - no detection")
                
                rate.sleep()
                
        except KeyboardInterrupt:
            rospy.loginfo("Interrupted by user")
        finally:
            cv2.destroyAllWindows()

def main():
    try:
        collector = ExperimentDataCollector()
        collector.run()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

