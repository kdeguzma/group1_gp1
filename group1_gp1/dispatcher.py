# ENPM605 Project GP1 - Scenario 2
# Group 1
# dispatcher.py - Publish task assignments to /fleet/tasks for robots 1-3.

# Import JSON needed for publishing messages.
import json

# Import necessary dependencies.
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class Dispatcher(Node):
    """A publisher-only node which assigns tasks to robots."""

    def __init__(self, node_name: str) -> None:
        """Initializer function for the dispatcher node.

        Args:
            node_name (str): The name to be set for this node with super().__init__().
        """
        # Initialize this node using node_name as the name.
        super().__init__(node_name)
        # Define the QoS profile required for the /fleet/tasks topic.
        self._qos = QoSProfile(
            depth=5,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        # Creates a publisher object for /fleet/tasks using the defined QoS profile.
        self._publisher = self.create_publisher(String, "/fleet/tasks", self._qos)
        # Fire the _timer_callback every 1.0 s while the node is spinning.
        self._timer = self.create_timer(1.0, self._timer_callback)
        # Initialize robot dict.
        self._robots = {0: "robot_1", 1: "robot_2", 2: "robot_3"}
        # Initialize tasks dict.
        self._tasks = {0: "deliver_", 1: "pick_", 2: "check_", 3: "quantity_"}
        # Initialize task locations dict.
        self._locations = {0: "dock", 1: "shelf_A4", 2: "shelf_B1", 3: "shelf_Cf", 4: "shelf_E2"}
        # Initialize index.
        self._index = 0
        # Show the initial logger message on the terminal.
        self.get_logger().info("Dispatcher reporting for duty")

    def _timer_callback(self) -> None:
        """Publishes to /fleet/tasks a task message cycling through robots, tasks, and locations."""
        # Iterate through robots, tasks, and locations dicts based on index.
        robot = self._robots[self._index % 3]
        task = self._tasks[self._index % 4]
        location = self._locations[self._index % 5]

        # Create the message as a String object.
        msg = String()
        # Dump the dict as JSON in msg's data.
        msg.data = json.dumps({"robot_id": robot, "task": task + location})

        # Publish the message,
        self._publisher.publish(msg)
        # Display in terminal the task assigned.
        self.get_logger().info(f"Assigned task {task}{location} to {robot}")

        # Increment the index.
        self._index += 1
