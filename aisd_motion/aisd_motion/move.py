import rclpy
from rclpy.node import Node
from aisd_msgs.msg import Hand
from geometry_msgs.msg import Twist



class Move(Node):

    def __init__(self):
        super().__init__('Move_Node')

        # Subscribe to the 'cmd_hand' topic to receive hand gesture coordinates.
        self.subscription = self.create_subscription(
            Hand,
            'cmd_hand',
            self.listener_callback,
            10)
        
        # Create a publisher for the 'cmd_vel' topic to send velocity commands to the robot.
        self.vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        timer_period = 0.1  # seconds

        self.subscription  # prevent unused variable warning


    def listener_callback(self, msg):

        # Set the default angles.
        angle = 0.0
        linear = 0.0

        if msg.xindex > 0.55:
            self.get_logger().info('right')
            angle = -0.1
        elif msg.xindex < 0.45:
            self.get_logger().info('left')
            angle = 0.1
        else:
            angle = 0.0

        if msg.xindex > msg.xpinky:
            self.get_logger().info('come')
            linear = 0.5
        else:
            self.get_logger().info('stay')
            linear = 0.0

        # Initialize the Twist message.
        twist = Twist()

        # Set the linear and angular velocities based on the hand gesture.
        twist.linear.x = linear
        twist.angular.z = angle

        # Publish the Twist message to the 'cmd_vel' topic.
        if self.vel_publisher.get_subscription_count() > 0:
            self.vel_publisher.publish(twist)
        else:
            self.get_logger().info('waiting for subcriber')



def main(args=None):
    rclpy.init(args=args)

    move = Move()

    rclpy.spin(move)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    move.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
