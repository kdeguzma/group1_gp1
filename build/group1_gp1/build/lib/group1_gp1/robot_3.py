import json

from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rclpy.subscription import Subscription
from rclpy.timer import Timer
from std_msgs.msg import String


class RobotThree(Node):
    """Class for robot_3's node which subscribes to /fleet/tasks."""

    def __init__(self) -> None:
        """Initializer function for the robot_3 subscriber node."""
        super().__init__("robot_3")
        self._counter: float = 0
        self._status: str = "idle"
        self._robot_id: str = "robot_3"
        self._task: str | None = None
        # This is needed so both callbacks don't run at the same time and cause race conditions.
        self._callback_group = MutuallyExclusiveCallbackGroup()
        # Define the QoS profile required for the /fleet/tasks topic.
        
        qos_sub = QoSProfile(
            depth=5,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
        )
        qos_pub = QoSProfile(
            depth=3,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
        )
        
        # Creates a subscriber object for /fleet/tasks.
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
        # Creates a publisher object for /fleet/status. No callback here.
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
        """Timer callback for this node, publishes this node's information."""

        # If there's no tasks, exit this function using return.
        if self._task is None:
            return
        # Timer tick resolution of 0.1 chosen to account for robot_3's 0.3 s requirement.
        self._counter += 0.1

        if self._counter < 0.3:
            self._status = "busy"
            message = String()
            payload = {"robot_id": self._robot_id, "status": self._status, "task": self._task}

            # Publish the message in JSON format.
            message.data = json.dumps(payload)
            self._publisher.publish(message)
            return
        # THE LOGGER INFO IS NOT THE SAME AS THE MESSAGE BEING PUBLISHED!!!
        self.get_logger().info(f"Task {self._task} complete")
        self._status = "done"
        message = String()
        payload = {"robot_id": self._robot_id, "status": self._status, "task": self._task}
        message.data = json.dumps(payload)
        self._publisher.publish(message)

        # Clear the task after publishing.
        self._task = None

    def _subscriber_callback(self, message: String) -> None:
        """Subscriber callback for this node, receives task messages from /fleet/tasks.

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
            # Change the status to "busy".
            self._task = task
            self._status = "busy"
            self._counter = 0

            # Log the task info to the terminal.
            self.get_logger().info(f"Received task {task} -- executing...")
        # If the JSON is invalid, raise this exception.
        except json.JSONDecodeError:
            self.get_logger().warn("Invalid JSON received")
