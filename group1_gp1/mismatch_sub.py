# ENPM605 Project GP1 - Scenario 2
# Group 1
# mismatch_sub.py - A demonstration of a subscriber node with a QoS mismatch.

# Import JSON needed for publishing messages.
import json

# Import necessary dependencies.
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class Mismatch(Node):
    """A subscriber node which has a mismatch to show QoS incompatablity (RELIABLE vs BEST_EFFORT)"""

    ## Running this node will create QoS warnings. A "RELIABLE" QoS subscriber cannot receive
    # from a "BEST_EFFORT" publisher. Using ros2 topic info /fleet/status -v one can see all the
    # publishers and subscribers and their QOS types. This allows programmer to determine where
    # the QoS mismatch is.

    def __init__(self, node_name: str) -> None:
        """Initializer function for the mismatch_sub node class.

        Args:
            node_name (str): The name to be set for this node with super().__init__().
        """
        # Initialize this node using node_name as the name.
        super().__init__(node_name)

        # Define the subscriber QoS profile required for the /fleet/status topic.
        self._qos_sub = QoSProfile(
            depth=3, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.VOLATILE
        )

        # Use a MutuallyExclusiveCallbackGroup so subscription callbacks do not run
        # concurrently. Necessary because class is updating shared robot tracking dictionaries.
        self._sub_callback_group = MutuallyExclusiveCallbackGroup()

        # Use a ReentrantCallbackGroup so the periodic report timer is independent
        # from the subscription callback. This allows it to run without blocking other callbacks.
        self._pub_callback_group = ReentrantCallbackGroup()

        # Creates a subscriber object for /fleet/status using the defined QoS profile.
        self._subscriber = self.create_subscription(
            String,
            "/fleet/status",
            self._subscriber_callback,
            self._qos_sub,
            callback_group=self._sub_callback_group,
        )

        # Initialize the last message with the clock.
        self._last_message = self.get_clock().now()

    def _subscriber_callback(self, msg: String) -> None:
        """Updates the last message timestamp when it receives a message from /fleet/status.

        Args:
            msg (String): The message received from the /fleet/status topic.
        """

        # Unpack the message into a dictionary.
        info = json.loads(msg.data)

        # Update the robot timestamp for the last received message.
        self._last_message = self.get_clock().now()

        self.get_logger().info("----------MISMATCH HAS RECEIVED A MESSAGE!----------")
