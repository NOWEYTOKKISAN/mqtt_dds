from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler
from launch.substitutions import LaunchConfiguration
from launch.events import Shutdown
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node

def generate_launch_description():
    message_size = LaunchConfiguration("message_size")
    publish_rate = LaunchConfiguration("publish_rate")
    duration = LaunchConfiguration("duration")

    pub_node = Node(
        package="ros2_dds_experiment",
        executable="pub_node",
        name="dds_publisher",
        output="screen",
        parameters=[{
            "message_size": message_size,
            "publish_rate": publish_rate
        }]
    )

    sub_node = Node(
        package="ros2_dds_experiment",
        executable="sub_node",
        name="dds_subscriber",
        output="screen",
        parameters=[{
            "duration": duration
        }]
    )

    cpu_logger_pub = Node(
        package="ros2_dds_experiment",
        executable="pub_cpu_logger",
        name="pub_cpu_logger",
        output="screen"
    )

    cpu_logger_sub = Node(
        package="ros2_dds_experiment",
        executable="sub_cpu_logger",
        name="sub_cpu_logger",
        output="screen"
    )

    return LaunchDescription([
        DeclareLaunchArgument("message_size", default_value="1024"),
        DeclareLaunchArgument("publish_rate", default_value="10.0"),
        DeclareLaunchArgument("duration", default_value="15.0"),
        pub_node,
        sub_node,
        cpu_logger_pub,
        cpu_logger_sub,
        RegisterEventHandler(
            OnProcessExit(
                target_action=sub_node,
                on_exit=[EmitEvent(event=Shutdown())]
            )
        )
    ])
