# ENPM605 Project GP1 - Scenario 2
# Group 1
# Dispatcher Main - Initiates the Dispatcher Node

# Import the Dispatcher class from the node itself

import rclpy
from group1_gp1.dispatcher import Dispatcher

def main(args=None) -> None:
    """Main function to spin the node."""
    # Initizlize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = Dispatcher("dispatcher")
    #spin the node.
    try:
        rclpy.spin(node)
    # Ctrl+C stops the node.
    
    except KeyboardInterrupt:
        print("Node stopped.")
    
    finally:
        node.destroy_node()
        rclpy.shutdown