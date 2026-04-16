# ENPM605 Project GP1 - Scenario 2
# Group 1
# Dispatcher - publish task assignments to /fleet/tasks for robots 1-3

import json

from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class Dispatcher(Node):
    """A publisher which assigns tasks to robots"""

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name)

        self._qos = QoSProfile(
            depth=5,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._publisher = self.create_publisher(String, "/fleet/tasks", self._qos)
        self._timer = self.create_timer(1.0, self._timer_callback)
        self._robots = {0: "robot_1", 1: "robot_2", 2: "robot_3"}
        self._tasks = {0: "deliver_", 1: "pick_", 2: "check_", 3: "quantity_"}
        self._locations = {0: "dock", 1: "shelf_A4", 2: "shelf_B1", 3: "shelf_Cf", 4: "shelf_E2"}
        self._index = 0
        self.get_logger().info("Dispatcher reporting for duty")

    def _timer_callback(self) -> None:
        """Publishes a task message cycling through robots, tasks, and locations"""
        # Iterate through robots and locations based on index
        robot = self._robots[self._index % 3]
        task = self._tasks[self._index % 4]
        location = self._locations[self._index % 5]

        # create the message
        msg = String()
        msg.data = json.dumps({"robot_id": robot, "task": task + location})

        # have publisher issue the message
        self._publisher.publish(msg)
        self.get_logger().info(f"Assigned task {task}{location} to {robot}\n")
        
        #increment index
        self._index += 1
