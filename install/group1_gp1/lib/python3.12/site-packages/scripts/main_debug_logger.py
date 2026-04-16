# ENPM605 Project GP1 - Scenario 2
# Group 1
# Debug Logger Main - Initiates a Debug Logger Node

# Import the Debug Logger class from the node itself

import rclpy
from group1_gp1.debug_logger import DebugLogger

def main(args=None) -> None:
    """Main function to spin the node."""
    # Initizlize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = DebugLogger("debugger")
    #spin the node.
    try:
        rclpy.spin(node)
    # Ctrl+C stops the node.
    
    except KeyboardInterrupt:
        print("Node stopped.")
    
    finally:
        node.destroy_node()
        rclpy.shutdown