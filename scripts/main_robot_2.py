# ENPM605 Project GP1 - Scenario 2
# Group 1
# main_robot_2.py - Initiates a Robot 2 Node.

import rclpy

# Import the RobotTwo class from the node itself.
from group1_gp1.robot_2 import RobotTwo


def main(args=None) -> None:
    """Main function to spin the robot_2 node."""
    # Initialize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = RobotTwo("robot_2")
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
