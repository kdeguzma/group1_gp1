# ENPM605 Project GP1 - Scenario 2
# Group 1
# Monitor Main - Initiates the Monitor Node

# Import the Monitor class from the node itself.

import rclpy
from rclpy.executors import MultiThreadedExecutor

from group1_gp1.monitor import Monitor


def main(args=None) -> None:
    """Main function to spin the monitor node."""
    # Initialize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = Monitor("monitor")

    # Used a MultiThreadedExecutor so the node can service requests from
    # different groups at the same time.
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)

    # Spin the node.
    try:
        executor.spin()
    # Ctrl+C stops the node.

    except KeyboardInterrupt:
        node.get_logger().info("Shutting down.")

    # Clean up and shut down the node when done.
    finally:
        node.destroy_node()
        # Account for ROS 2 already shutting down.
        if rclpy.ok():
            rclpy.shutdown
