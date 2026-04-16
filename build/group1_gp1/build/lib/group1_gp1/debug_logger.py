# ENPM605 Project GP1 - Scenario 2
# Group 1
# Debug Logger - Subscribes and logs all messages

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from std_msgs.msg import String
import json

class DebugLogger(Node):
    """Debugger which outputs information when active"""
    
    def __init__(self, node_name:str)->None:
        super().__init__(node_name)
        
        self._qos_tasks = QoSProfile(depth = 1, reliability = ReliabilityPolicy.RELIABLE, durability = DurabilityPolicy.TRANSIENT_LOCAL)
        self._qos_status = QoSProfile(depth = 1, reliability = ReliabilityPolicy.BEST_EFFORT, durability = DurabilityPolicy.VOLATILE)
        self._subscriber_tasks = self.create_subscription(String,"/fleet/tasks",self._subscriber_callback_tasks, self._qos_tasks)
        self._subscriber_status = self.create_subscription(String,"/fleet/status",self._subscriber_callback_status, self._qos_status)
        
    def _subscriber_callback_tasks(self, msg:String)->None:
        """ Receives messages from the /fleet/tasks topic and output to terminal"""

        #unpack message into a dictionary
        info = json.loads(msg.data)
        
        self.get_logger().info(f"T: {self.get_clock().now()}, M: {info}")

    def _subscriber_callback_status(self, msg:String) -> None:
        """ Receives messages from the /fleet/status topic and output to terminal"""
    
        #unpack message into dictionary
        info = json.loads(msg.data)
        
        self.get_logger().info(f"T: {self.get_clock().now()}, M: {info}")