# ENPM605 Project GP1 - Scenario 2
# Group 1
# Mismatched Subscriber Main - Initiates the Mismatched QOS Subscriber Node

# Import the Mismatched Subscriber class from the node itself

import rclpy
from group1_gp1.mismatch_sub import Mismatch

def main(args=None) -> None:
    """Main function to spin the node."""
    # Initizlize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = Mismatch("Daredevil")
    #spin the node.
    try:
        rclpy.spin(node)
    # Ctrl+C stops the node.
    
    except KeyboardInterrupt:
        print("Node stopped.")
    
    finally:
        node.destroy_node()
        rclpy.shutdown