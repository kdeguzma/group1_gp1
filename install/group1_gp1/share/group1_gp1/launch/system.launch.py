from launch import LaunchDescription
from launch.actions import GroupAction, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    enable_debug = LaunchConfiguration("enable_debug")
    enable_mismatch = LaunchConfiguration("enable_mismatch")
    start_robot2 = LaunchConfiguration("robot_2")
    
    dispatcher = Node(
        package="group1_gp1", executable="dispatcher",
        output="screen", emulate_tty=True,
    )

    monitor = Node(
        package="group1_gp1", executable="monitor",
        output="screen", emulate_tty=True,
    )
    
    robot_1 = Node(
    package="group1_gp1", executable="robot_1",
    output="screen", emulate_tty=True,
    )
    
    robot_2 = Node(
    package="group1_gp1", executable="robot_2",
    output="screen", emulate_tty=True,
    condition = IfCondition(start_robot2)
    )
    
    robot_3 = Node(
    package="group1_gp1", executable="robot_3",
    output="screen", emulate_tty=True,
    )
    
    debug_logger = Node(
    package="group1_gp1", executable="debug_logger",
    output="screen", emulate_tty=True,
    condition = IfCondition(enable_debug),
    )
    
    mismatch_subscriber = Node(
    package="group1_gp1", executable="mismatch_sub",
    output="screen", emulate_tty=True,
    condition = IfCondition(enable_mismatch),
    )  
    

    admin_group = GroupAction([dispatcher, monitor])
    robot_group = GroupAction([robot_1, robot_2, robot_3])
    
    

    ld = LaunchDescription([DeclareLaunchArgument("enable_debug",
        default_value="false",
        description="Launch the debug logger node",
        ),
        DeclareLaunchArgument("enable_mismatch",
        default_value="false",
        description="Launch the mismatch subscriber node",
        ),
        DeclareLaunchArgument("robot_2",
        default_value="true",
        description="Launch the robot_2 node",
        )])
    
    ld.add_action(admin_group)
    ld.add_action(robot_group)
    ld.add_action(debug_logger)    
    ld.add_action(mismatch_subscriber)

    return ld