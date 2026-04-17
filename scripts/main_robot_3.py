# ENPM605 Project GP1 - Scenario 2
# Group 1
# main_robot_3.py - Initiates a Robot 3 Node.

import rclpy

# Import the RobotThree class from the node itself.
from group1_gp1.robot_3 import RobotThree


def main(args=None) -> None:
    """Main function to spin the robot_3 node."""
    # Initialize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = RobotThree("robot_3")
    # Spin the node.
    try:
        rclpy.spin(node)
    # Ctrl+C stops the node.
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down.")
    # Clean up and shut down the node when done.
    finally:
        node.destroy_node()
        # Account for ROS 2 already shutting down.
        if rclpy.ok():
            rclpy.shutdown()
