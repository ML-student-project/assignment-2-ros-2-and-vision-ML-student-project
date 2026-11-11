#!/usr/bin/env python3


import rclpy # import of the python interface with rosz 
from rclpy.node import Node # use the class called Node in rclpy


class MyNode (Node): # define the MyNode class
    def __init__(self): # initialize the class
        super().__init__("py_test") # call the parent class constructor from the Node class
        self.counter_  = 0 # initialize the counter value to be one
        self.get_logger().info("Py Node started") # initialize the log
        self.create_timer(0.5, self.timer_callback) # initialize a timer with 2 hertz to do timer_callback

    def timer_callback(self): # define the timer callback function
        self.counter_ += 1 # add +1 to the counter
        self.get_logger().info("Hello" + str(self.counter_)) # write Hello + new counter value

def main(args=None): # define the main function
    rclpy.init(args=args) # initialize the ros2 commuincation
    node = MyNode() # create an instance of the class called MyNode (we need to build it)
    rclpy.spin(node) # keep the node running untill we kill it
    rclpy.shutdown() # shutdown the ros2 commuincation

if __name__ == '__main__': # standard python line to execute the main function
    main()
