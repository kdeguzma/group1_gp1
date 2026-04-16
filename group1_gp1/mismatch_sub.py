# ENPM605 Project GP1 - Scenario 2
# Group 1
# Monitor - subscribes to robot output to track information, publishes aggregated info

import json

from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class Mismatch(Node):
    """A subscriber node which has a mismatch to show QoS incompatablity (RELAIBLE vs BEST_EFFORT)"""
    
    ## Running this node will create QoS warnings. A "RELIABLE" QoS subscriber cannot receive 
    # from a "BEST_EFFORT" publisher. Using ros2 topic info /fleet/status -v one can see all the 
    # publishers and subscribers and their QOS types. This allows programmer to determine where 
    # the QoS mismatch is.

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name)

        self._qos_sub = QoSProfile(
            depth=3, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.VOLATILE
        )
        
        self._sub_callback_group = MutuallyExclusiveCallbackGroup()
        self._pub_callback_group = ReentrantCallbackGroup()
        self._subscriber = self.create_subscription(
            String,
            "/fleet/status",
            self._subscriber_callback,
            self._qos_sub,
            callback_group=self._sub_callback_group,
        )       

        self._last_message = self.get_clock().now()

    def _subscriber_callback(self, msg: String) -> None:
        """Updates last message timestamp when it receives a message"""

        # unpack message into a dictionary
        info = json.loads(msg.data)

        # update robot timestamp for last received message
        self._last_message = self.get_clock().now()
        
        self.get_logger().info(f"----------MISMATCH HAS RECEIVED A MESSAGE!----------")

        
