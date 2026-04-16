# ENPM605 Project GP1 - Scenario 2
# Group 1
# Monitor Main - Initiates the Monitor Node

# Import the Monitor class from the node itself

import rclpy
from group1_gp1.monitor import Monitor
from rclpy.executors import MultiThreadedExecutor

def main(args=None) -> None:
    """Main function to spin the node."""
    # Initizlize rclpy and build the node by calling the class.
    rclpy.init(args=args)
    node = Monitor("monitor")
    
    # Used a MultiThreadedExecutor so the node can service requests from
    # different groups at the same time.
    executor = MultiThreadedExecutor(num_threads = 4)
    executor.add_node(node)
    
    #spin the node.
    try:
        executor.spin()
    # Ctrl+C stops the node.
    
    except KeyboardInterrupt:
        print("Exception: Node stopped.")
    
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown