# ENPM605 Project GP1 - Scenario 2
# Group 1
# system.launch.py - File to launch multiple nodes for debugging.

# Import necessary dependencies.
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from launch import LaunchDescription


def generate_launch_description():
    """Function for launching multiple files using the ros2 command in the terminal."""

    # Define the debug and mismatch configurations for testing conditions in the terminal.
    enable_debug = LaunchConfiguration("enable_debug")
    enable_mismatch = LaunchConfiguration("enable_mismatch")

    # Needed to demonstrate queue buildup.
    start_robot2 = LaunchConfiguration("start_robot_2")

    # Set the dispatcher node.
    dispatcher = Node(
        package="group1_gp1",
        executable="dispatcher",
        output="screen",
        emulate_tty=True,
    )
    # Set the monitor node.
    monitor = Node(
        package="group1_gp1",
        executable="monitor",
        output="screen",
        emulate_tty=True,
    )
    # Set the robot_1 node.
    robot_1 = Node(
        package="group1_gp1",
        executable="robot_1",
        output="screen",
        emulate_tty=True,
    )
    # Set the robot_2 node and add the IfCondition for queue buildup.
    robot_2 = Node(
        package="group1_gp1",
        executable="robot_2",
        output="screen",
        emulate_tty=True,
        condition=IfCondition(start_robot2),
    )
    # Set the robot_3 node.
    robot_3 = Node(
        package="group1_gp1",
        executable="robot_3",
        output="screen",
        emulate_tty=True,
    )
    # Set the debug_logger node.
    debug_logger = Node(
        package="group1_gp1",
        executable="debug_logger",
        output="screen",
        emulate_tty=True,
        condition=IfCondition(enable_debug),
    )
    # Set the mismatch_subscriber node.
    mismatch_subscriber = Node(
        package="group1_gp1",
        executable="mismatch_sub",
        output="screen",
        emulate_tty=True,
        condition=IfCondition(enable_mismatch),
    )
    # Set groups for helping with debugging.
    admin_group = GroupAction([dispatcher, monitor])
    robot_group = GroupAction([robot_1, robot_2, robot_3])

    # Define the LaunchDescription.
    ld = LaunchDescription(
        [
            DeclareLaunchArgument(
                "enable_debug",
                default_value="false",
                description="Launch the debug logger node",
            ),
            DeclareLaunchArgument(
                "enable_mismatch",
                default_value="false",
                description="Launch the mismatch subscriber node",
            ),
            DeclareLaunchArgument(
                "start_robot_2",
                default_value="true",
                description="Launch the robot_2 node",
            ),
        ]
    )

    # Add the set nodes and groups to the LaunchDescription, then return.
    ld.add_action(admin_group)
    ld.add_action(robot_group)
    ld.add_action(debug_logger)
    ld.add_action(mismatch_subscriber)

    return ld
