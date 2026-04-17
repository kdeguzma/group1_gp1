# ENPM605 Project GP1 - Scenario 2
# Group 1
# debug_logger.py - Subscribes and logs all messages.

# Import JSON needed for publishing messages.
import json

# Import necessary dependencies.
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class DebugLogger(Node):
    """Debugger subscriber-only node which outputs the information when active."""

    def __init__(self, node_name: str) -> None:
        """Initializer function for debug_logger node.

        Args:
            node_name (str): The name to be set for this node with super().__init__().
        """
        # Initialize this node using node_name as the name.
        super().__init__(node_name)

        # Define the subscriber QoS profile required for the /fleet/tasks topic.
        self._qos_tasks = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        # Define the subscriber QoS profile required for the /fleet/status topic.
        self._qos_status = QoSProfile(
            depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE
        )
        # Creates a subscriber object for /fleet/tasks using the defined QoS profile.
        self._subscriber_tasks = self.create_subscription(
            String, "/fleet/tasks", self._subscriber_callback_tasks, self._qos_tasks
        )
        # Creates a subscriber object for /fleet/status using the defined QoS profile.
        self._subscriber_status = self.create_subscription(
            String, "/fleet/status", self._subscriber_callback_status, self._qos_status
        )

    def _subscriber_callback_tasks(self, msg: String) -> None:
        """Receives messages from the /fleet/tasks topic and outputs to the terminal."""

        # Unpack the message into a dictionary.
        info = json.loads(msg.data)

        # Log the unpacked message to the terminal.
        self.get_logger().info(f"T: {self.get_clock().now()}, M: {info}")

    def _subscriber_callback_status(self, msg: String) -> None:
        """Receives messages from the /fleet/status topic and outputs to the terminal."""

        # Unpack the message into a dictionary.
        info = json.loads(msg.data)

        # Log the unpacked message to the terminal.
        self.get_logger().info(f"T: {self.get_clock().now()}, M: {info}")
