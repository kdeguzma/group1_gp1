# ENPM605 Project GP1 - Scenario 2
# Group 1
# robot_3.py - Subscribes to /fleet/tasks, publishes to /fleet/status, and filters messages for id.

# Import JSON needed for publishing messages.
import json

# Import necessary dependencies.
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rclpy.subscription import Subscription
from rclpy.timer import Timer
from std_msgs.msg import String


class RobotThree(Node):
    """Class for robot_3's node which subscribes to /fleet/tasks and publishes to /fleet/status."""

    def __init__(self) -> None:
        """Initializer function for the robot_3 sub/pub node."""
        # Initialize the node with the name "robot_3".
        super().__init__("robot_3")
        # Initialize the counter.
        self._counter: float = 0
        # Initialize the status.
        self._status: str = "idle"
        # Initialize the robot ID.
        self._robot_id: str = "robot_3"
        # Initialize the current task.
        self._task: str | None = None
        # This is needed so both callbacks don't run at the same time and cause race conditions.
        self._callback_group = MutuallyExclusiveCallbackGroup()
        # Define the subscriber QoS profile required for the /fleet/tasks topic.
        qos_sub = QoSProfile(
            depth=5,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
        )
        # Define the publisher QoS profile required for the /fleet/status topic.
        qos_pub = QoSProfile(
            depth=3,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
        )

        # Creates a subscriber object for /fleet/tasks using the defined QoS profile.
        self._subscriber: Subscription = self.create_subscription(
            # Message type: WE NEED TO MAKE SURE THIS MATCHES dispatcher's MESSAGE TYPE.
            String,
            # Topic name: WE NEED TO MAKE SURE THIS MATCHES dispatcher's TOPIC NAME.
            "/fleet/tasks",
            # Callback.
            self._subscriber_callback,
            # QoS profile. WE NEED TO MAKE SURE dispatcher USES A COMPATIBLE QoS POLICY WITH THIS NODE.
            qos_sub,
            # Only one callback can run at a time.
            callback_group=self._callback_group,
        )
        # Creates a publisher object for /fleet/status using the defined QoS profile. No callback here.
        self._publisher: Publisher = self.create_publisher(
            # Message type: WE NEED TO MAKE SURE THIS MATCHES monitor's and debug_logger's MESSAGE TYPE.
            String,
            # Topic name: WE NEED TO MAKE SURE THIS MATCHES monitor's and debug_logger's TOPIC NAME.
            "/fleet/status",
            # QoS profile: WE NEED TO MAKE SURE monitor and debug_logger USE COMPATIBLE QoS POLICIES WITH THIS NODE.
            qos_pub,
        )
        # Fire the _publisher_callback every 0.1 s while the node is spinning.
        self.timer: Timer = self.create_timer(
            0.1,
            self._timer_callback,
            # Only one callback can run at a time.
            callback_group=self._callback_group,
        )

    def _timer_callback(self) -> None:
        """Publishes to /fleet/status the robot's id, status, and task."""

        # If there's no tasks, exit this function using return.
        if self._task is None:
            return
        # Timer tick resolution of 0.1 chosen to account for robot_3's 0.3 s requirement.
        self._counter += 0.1

        # If block for when the robot is still busy.
        # Simulate fast 0.3 s sleep.
        if self._counter < 0.3:
            # Set the status to busy.
            self._status = "busy"
            # Create a message object.
            message = String()
            # Create a dict payload.
            payload = {"robot_id": self._robot_id, "status": self._status, "task": self._task}
            # Dump the payload dict as JSON in message's data.
            message.data = json.dumps(payload)
            # Publish the message in JSON format.
            self._publisher.publish(message)
            # Return if the robot is not done.
            return

        # Block for when the robot is done.
        # THE LOGGER INFO IS NOT THE SAME AS THE MESSAGE BEING PUBLISHED!!!
        # Display in terminal the task completed.
        self.get_logger().info(f"Task {self._task} complete")
        # Set the status to done.
        self._status = "done"
        # Repeat the same steps from the if block once done.
        message = String()
        payload = {"robot_id": self._robot_id, "status": self._status, "task": self._task}
        message.data = json.dumps(payload)
        self._publisher.publish(message)

        # Clear the task after publishing.
        self._task = None

    def _subscriber_callback(self, message: String) -> None:
        """Receives task messages from /fleet/tasks, filters tasks for id, and logs.

        Args:
            message (String): The JSON message received from the /fleet/tasks topic.
        """

        try:
            # Load the JSON from /fleet/tasks.
            data = json.loads(message.data)
            # Get the robot_id value from the message.
            robot_id = data.get("robot_id")
            # Get the task value from the message.
            task = data.get("task")

            # Filter out tasks that are not robot_3's ID.
            if (
                robot_id != self._robot_id
            ):  # or self._task is not None: # Commented out: Prevent accepting new tasks while busy.
                return

            # Otherwise, accept and set the task as robot_3's attribute.
            self._task = task
            # Change the status to "busy".
            self._status = "busy"
            # Reset the counter.
            self._counter = 0

            # Log the task info to the terminal.
            self.get_logger().info(f"Received task {task} -- executing...")
        # If the JSON is invalid, raise this exception.
        except json.JSONDecodeError:
            self.get_logger().warn("Invalid JSON received")
