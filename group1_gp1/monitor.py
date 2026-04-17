# ENPM605 Project GP1 - Scenario 2
# Group 1
# monitor.py - subscribes to robot output to track information, publishes aggregated info.

# Import JSON needed for publishing messages.
import json

# Import necessary dependencies.
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class Monitor(Node):
    """Class for monitor's node which subscribes to /fleet/status and publishes to /fleet/report."""

    def __init__(self, node_name: str) -> None:
        """Initializer function for the monitor sub/pub node.

        Args:
            node_name (str): The name to be set for this node with super().__init__().
        """
        # Initialize this node using node_name as the name.
        super().__init__(node_name)

        # Define the publisher QoS profile required for the /fleet/report topic.
        self._qos_pub = QoSProfile(
            depth=1, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.VOLATILE
        )
        # Define the subscriber QoS profile required for the /fleet/status topic.
        self._qos_sub = QoSProfile(
            depth=3, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE
        )
        # Use a MutuallyExclusiveCallbackGroup so subscription callbacks do not run
        # concurrently. Necessary because class is updating shared robot tracking dictionaries.
        self._sub_callback_group = MutuallyExclusiveCallbackGroup()

        # Use a ReentrantCallbackGroup so the periodic report timer is independent
        # from the subscription callback. This allows it to run without blocking other callbacks.
        self._pub_callback_group = ReentrantCallbackGroup()

        # Creates a publisher object for /fleet/report using the defined QoS profile.
        self._publisher = self.create_publisher(String, "/fleet/report", self._qos_pub)
        # Creates a subscriber object for /fleet/status using the defined QoS profile.
        self._subscriber = self.create_subscription(
            String,
            "/fleet/status",
            self._subscriber_callback,
            self._qos_sub,
            callback_group=self._sub_callback_group,
        )

        # Initialize dict for each robot's last completed task.
        self._robot_last_task = {"robot_1": None, "robot_2": None, "robot_3": None}
        # Initialize dict for each robot's number of completed tasks.
        self._robot_completed = {"robot_1": 0, "robot_2": 0, "robot_3": 0}
        # Initialize dict for each robot's clock.
        self._robot_status_ts = {
            "robot_1": self.get_clock().now(),
            "robot_2": self.get_clock().now(),
            "robot_3": self.get_clock().now(),
        }
        # Fire the _timer_callback every 2.0 s while the node is spinning.
        self._timer = self.create_timer(
            2.0, self._timer_callback, callback_group=self._pub_callback_group
        )

    def _subscriber_callback(self, msg: String) -> None:
        """Receives data from the 3 robots via /fleet/status and tracks the data.

        Args:
            msg (String): The JSON message received from /fleet/status.
        """

        # Unpack the message into a dictionary.
        info = json.loads(msg.data)

        # Update the robot timestamp for the last received message.
        self._robot_status_ts[info["robot_id"]] = self.get_clock().now()

        # If the robot is complete with its task and that task different from their last completed task...
        if info["status"] == "done" and info["task"] != self._robot_last_task[info["robot_id"]]:
            # ...increase the completed tasks.
            self._robot_completed[info["robot_id"]] += 1
            # Then save the name of this task.
            self._robot_last_task[info["robot_id"]] = info["task"]

    def _timer_callback(self) -> None:
        """Publishes a system status message to /fleet/report every 2 seconds."""

        # Create a message object from the _robot_completed dictionary.
        msg = String()
        # Dump the object as JSON in msg's data.
        msg.data = json.dumps(self._robot_completed)

        # Warn if any robot has not reported in 5 seconds.
        # Get the current time.
        current_time = self.get_clock().now()
        # Iterate through the robot clock dict.
        for key, value in self._robot_status_ts.items():
            if Duration(seconds=5.0) <= current_time - value:
                self.get_logger().warn(f"{key} has not reported in 5 seconds!")

        # Publish the message to /fleet/report.
        self._publisher.publish(msg)
        # Log the number of tasks completed for each robot to the terminal.
        self.get_logger().info(
            f"Fleet report -- robot_1: {self._robot_completed['robot_1']}, robot_2: {self._robot_completed['robot_2']}, robot_3: {self._robot_completed['robot_3']}"
        )
