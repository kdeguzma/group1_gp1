# ENPM605 Project GP1 - Scenario 2
# Group 1
# Mismatched Subscriber Main - Initiates the Mismatched QOS Subscriber Node

# Import the Mismatched Subscriber class from the node itself

import rclpy

from group1_gp1.mismatch_sub import Mismatch


def main(args=None) -> None:
    """Main function to spin the mismatch_sub node."""
    # Initialize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = Mismatch("Daredevil")
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
            rclpy.shutdown
