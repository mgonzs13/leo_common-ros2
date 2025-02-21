# MIT License
#
# Copyright (c) 2025 Miguel Ángel González Santamarta
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    DeclareLaunchArgument,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    bringup_dir = get_package_share_directory("leo_navigation")
    launch_dir = os.path.join(bringup_dir, "launch/navigation")

    stdout_linebuf_envvar = SetEnvironmentVariable("RCUTILS_LOGGING_BUFFERED_STREAM", "1")

    params_file = os.path.join(bringup_dir, "config", "nav2.yaml")

    launch_rviz = LaunchConfiguration("launch_rviz")
    launch_rviz_cmd = DeclareLaunchArgument(
        "launch_rviz",
        default_value="True",
        description="Whether launch rviz",
    )

    slam = LaunchConfiguration("slam")
    slam_cmd = DeclareLaunchArgument(
        "slam",
        default_value="False",
        description="Whether run a SLAM",
    )

    map_yaml_file = LaunchConfiguration(
        "map",
        default=os.path.join(
            bringup_dir, "maps/apartamento_leon", "apartamento_leon_gimp_con_mesa_tv.yaml"
        ),
    )
    map_yaml_cmd = DeclareLaunchArgument(
        "map",
        default_value=map_yaml_file,
        description="Full path to map yaml file to load",
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if True",
    )

    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_x_cmd = DeclareLaunchArgument(
        "initial_pose_x",
        default_value="1.336",
        description="Initial pose x",
    )

    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_y_cmd = DeclareLaunchArgument(
        "initial_pose_y",
        default_value="6.544",
        description="Initial pose y",
    )

    initial_pose_z = LaunchConfiguration("initial_pose_z")
    initial_pose_z_cmd = DeclareLaunchArgument(
        "initial_pose_z",
        default_value="0.0",
        description="Initial pose z",
    )

    initial_pose_yaw = LaunchConfiguration("initial_pose_yaw")
    initial_pose_yaw_cmd = DeclareLaunchArgument(
        "initial_pose_yaw",
        default_value="0.0",
        description="Initial pose yaw",
    )

    bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(launch_dir, "bringup.launch.py")),
        launch_arguments={
            "launch_rviz": launch_rviz,
            "slam": slam,
            "params_file": params_file,
            "map": map_yaml_file,
            "use_sim_time": use_sim_time,
            "initial_pose_x": initial_pose_x,
            "initial_pose_y": initial_pose_y,
            "initial_pose_z": initial_pose_z,
            "initial_pose_yaw": initial_pose_yaw,
            "cmd_vel_topic": "/cmd_vel",
        }.items(),
    )

    odom_to_tf = Node(
        package="odom_to_tf_ros2",
        executable="odom_to_tf",
        name="odom_to_tf",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "odom_topic": "wheel_odom_with_covariance",
                "child_frame_id": "base_footprint",
            }
        ],
    )

    ld = LaunchDescription()

    ld.add_action(stdout_linebuf_envvar)

    ld.add_action(launch_rviz_cmd)
    ld.add_action(slam_cmd)
    ld.add_action(map_yaml_cmd)
    ld.add_action(use_sim_time_cmd)
    ld.add_action(initial_pose_x_cmd)
    ld.add_action(initial_pose_y_cmd)
    ld.add_action(initial_pose_z_cmd)
    ld.add_action(initial_pose_yaw_cmd)

    ld.add_action(bringup_cmd)
    ld.add_action(odom_to_tf)

    return ld
