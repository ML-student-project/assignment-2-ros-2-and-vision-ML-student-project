#!/usr/bin/env python3

import os
from tokenize import String

import rclpy # import of the python interface with rosz 
from rclpy.node import Node # use the class called Node in rclpy
import cv2
import mediapipe as mp
import time
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory

# Get the path to the package share directory
package_directory = get_package_share_directory('aisd_vision')

# Path to the downloaded MediaPipe model
MODEL_PATH = os.path.join(package_directory, 'resource', 'data', 'hand_landmarker.task')

# MediaPipe Tasks API
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

# Configure the hand detector model options.
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)




class GesturePublisher (Node): # define the MyNode class
    def __init__(self): # initialize the class
        
        # call the parent class constructor from the Node class
        super().__init__("gesture_publisher") 
        
        # initialize the log
        self.get_logger().info("gesture_publisher started") 

        # Initialize OpenCV VideoCapture (0 is usually the default webcam)
        self.cap = cv2.VideoCapture(0)

        # Create publisher for sensor_msgs/Image
        self.publisher_ = self.create_publisher(
            String, 'gesture', 10
            )

        # initialize a timer to do timer_callback
        self.create_timer(0.3, self.timer_callback) 

        # initialize the model.
        self.landmarker = HandLandmarker.create_from_options(options)

    def find_pinkie_position(self,landmarks, handedness):
        """Determine pinkie position as Vertical, Horizontal."""
        if landmarks[20].y < landmarks[18].y :    # Pinky tip is above pinky PIP joint.
            return "Vertical"    
        else:   # Thumb tip is above pinky tip.
            return "Horizontal"
 

    def gesture_stop_forward(self,landmarks, handedness):
        """Determine if the hand gesture indicates a 'Stop' or 'Forward' command."""
        match handedness:
            case "Left":
                # Check if the thumb is to the right of the pinky for a left hand
                if landmarks[4].x < landmarks[20].x:
                    return "Forward"
                else:
                    return "Stop"
            case "Right":
                # Check if the thumb is to the left of the pinky for a right hand
                if landmarks[4].x < landmarks[20].x:
                    return "Stop"
                else:
                    return "Forward"        
            case _:
                return "Unknown"

    def gesture_left_right(self,landmarks, handedness):
        """Determine if the hand gesture indicates a 'Left' or 'Right' command."""
        match handedness:
            case "Left":
                # Check if the thumb is above the pinky for a left hand
                if landmarks[2].x < landmarks[20].x:
                    return "Right"
                else:
                    return "Left"
            case "Right":
                # Check if the thumb is above the pinky for a right hand
                if landmarks[2].x > landmarks[20].x:
                    return "Left"
                else:
                    return "Right"
            case _:
                return "Unknown"
            
    def kt_classify_gesture(self,landmarks, handedness):
        """Classify hand gesture based on palm, back of hand, left, or right."""
        pinkie_position = self.find_pinkie_position(landmarks, handedness)

        # Classify gesture based on pinkie position.
        match pinkie_position:
            case "Vertical":
                return self.gesture_stop_forward(landmarks, handedness)
            case "Horizontal":
                return self.gesture_left_right(landmarks, handedness)
            case _:
                return "Unknown"
            
    def timer_callback(self): # define the timer callback function

        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().error("Failed to grab frame")
            return

        # Mirror the webcam image
        img = cv2.flip(frame, 1)
    
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
        # Create a MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=img_rgb
        )
    
        # Timestamp in milliseconds
        timestamp_ms = time.monotonic_ns() // 1_000_000
    
        # Detect hand landmarks
        results = self.landmarker.detect_for_video(
                    mp_image,
                    timestamp_ms
                )

        # Process detected hands
        if results.hand_landmarks:
            for i, handedness_list in enumerate(results.handedness):
                for category in handedness_list:
                    handedness = category.category_name

            for hand_landmarks in results.hand_landmarks:
                                    
                if handedness == "Right" : handedness = "Left"
                else: handedness = "Right"

                # Determine the hand gesture. 
                gesture = self.kt_classify_gesture(landmarks=hand_landmarks, handedness=handedness)

                self.get_logger().info(f"Gesture: {gesture}, Handedness: {handedness}")
        
                # Publish the message
                msg = String()
                msg.data = gesture
                self.publisher_.publish(msg)
        


def main(args=None): # define the main function
    
    # initialize the ros2 commuincation
    rclpy.init(args=args) 

    # create an instance of the class called MyNode (we need to build it)
    node = GesturePublisher() 

    # keep the node running untill we kill it
    rclpy.spin(node) 

    # shutdown the ros2 commuincation
    rclpy.shutdown() 

if __name__ == '__main__': # standard python line to execute the main function
    main()