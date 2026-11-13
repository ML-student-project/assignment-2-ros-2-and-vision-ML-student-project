import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import mediapipe as mp
mp_hands = mp.solutions.hands

from aisd_msgs.msg import Hand


class Hands(Node):

    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            'video_frames',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        # A converter between ROS and OpenCV images
        self.br = CvBridge()
        self.hand_publisher = self.create_publisher(Hand, 'cmd_hand', 10)


    def listener_callback(self, msg):
        image = self.br.imgmsg_to_cv2(msg)

        PINKY_FINGER_TIP = 20    # pinky tip landmark is index 20.
        INDEX_FINGER_TIP = 8     # Index tip landmark is index 8.
        # Analyse the image for hands
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as myhands:

          # To improve performance, optionally mark the image as not writeable to
          # pass by reference.
          image.flags.writeable = False

          #Convert image back to RGB for mediapipe.
          image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

          # Get the hand landmarks from the image.
          results = myhands.process(image)
          if results.multi_hand_landmarks:
              #publish the hand position in terms of index finger and pinky

              # Create new message of type Hand
              msg = Hand()
              
              # Assign the X- corrdinate value for both the pinky and index finger to the message.
              msg.xpinky = results.multi_hand_landmarks[0].landmark[PINKY_FINGER_TIP].x
              msg.xindex = results.multi_hand_landmarks[0].landmark[INDEX_FINGER_TIP].x

              # Check if there are any subscribers to hand_publisher.
              if self.hand_publisher.get_subscription_count() > 0:
                  self.hand_publisher.publish(msg)
              else:
                  self.get_logger().info('waiting for subcriber')



def main(args=None):
    rclpy.init(args=args)

    hands = Hands()

    rclpy.spin(hands)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    hands.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()