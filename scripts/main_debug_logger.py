# ENPM605 Project GP1 - Scenario 2
# Group 1
# Debug Logger Main - Initiates a Debug Logger Node

# Import the Debug Logger class from the node itself

import rclpy

from group1_gp1.debug_logger import DebugLogger


def main(args=None) -> None:
    """Main function to spin the debug_logger node."""
    # Initialize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = DebugLogger("debugger")
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
