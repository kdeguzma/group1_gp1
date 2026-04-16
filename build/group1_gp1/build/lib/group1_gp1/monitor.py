# ENPM605 Project GP1 - Scenario 2
# Group 1
# Monitor - subscribes to robot output to track information, publishes aggregated info

import json

from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class Monitor(Node):
    """A subscriber node which tracks completed tasks per robot and last status"""

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name)
        self._qos_pub = QoSProfile(
            depth=1, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.VOLATILE
        )
        self._qos_sub = QoSProfile(
            depth=3, reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE
        )
        self._sub_callback_group = MutuallyExclusiveCallbackGroup()
        self._pub_callback_group = ReentrantCallbackGroup()
        self._publisher = self.create_publisher(String, "/fleet/report", self._qos_pub)
        self._subscriber = self.create_subscription(
            String,
            "/fleet/status",
            self._subscriber_callback,
            self._qos_sub,
            callback_group=self._sub_callback_group,
        )

        self._robot_last_task = {"robot_1": None, "robot_2": None, "robot_3": None}
        self._robot_completed = {"robot_1": 0, "robot_2": 0, "robot_3": 0}
        self._robot_status_ts = {
            "robot_1": self.get_clock().now(),
            "robot_2": self.get_clock().now(),
            "robot_3": self.get_clock().now(),
        }

        self._timer = self.create_timer(
            2.0, self._timer_callback, callback_group=self._pub_callback_group
        )

    def _subscriber_callback(self, msg: String) -> None:
        """Receives data from the 3 robots and tracks the data"""

        # unpack message into a dictionary
        info = json.loads(msg.data)

        # update robot timestamp for last received message
        self._robot_status_ts[info["robot_id"]] = self.get_clock().now()

        # is robot complete with its task? Is that task different from their last completed task?
        if info["status"] == "done" and info["task"] != self._robot_last_task[info["robot_id"]]:
            # increase completed tasks
            self._robot_completed[info["robot_id"]] += 1
            # save the name of this task
            self._robot_last_task[info["robot_id"]] = info["task"]

    def _timer_callback(self) -> None:
        """Publishes a system status message every 2 seconds"""

        # create message from _robot_completed dictionary
        msg = String()
        msg.data = json.dumps(self._robot_completed)

        # warn if any robot has not reported in 5 seconds
        current_time = self.get_clock().now()
        for key, value in self._robot_status_ts.items():
            if Duration(seconds=5.0) <= current_time - value:
                self.get_logger().warn(f"{key} has not reported in 5 seconds!")

        # publish message to topic/log
        self._publisher.publish(msg)

        # Get the number of completed tasks for each robot from the dictionary.
        robot_1_no_tasks = self._robot_completed["robot_1"]
        robot_2_no_tasks = self._robot_completed["robot_2"]
        robot_3_no_tasks = self._robot_completed["robot_3"]
        self.get_logger().info(
            f"Fleet report -- robot_1: {robot_1_no_tasks} tasks, robot_2: {robot_2_no_tasks} tasks, robot_3: {robot_3_no_tasks} tasks"
        )
