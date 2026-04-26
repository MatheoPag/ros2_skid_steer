import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():

    package_name='my_robot'

    rviz = LaunchConfiguration('rviz')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','display.launch.py'
                )]), launch_arguments={
                    'use_sim_time': 'True',
                    'rviz': rviz,
                }.items()
    )

    rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Lancer RViz (false pour Gazebo seul)',
    )

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(
            get_package_share_directory('gazebo_ros'),
            'worlds',
            'empty.world',
        ),
        )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py',
            )
        ),
        launch_arguments={
            'world': world,
        }.items(),
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'my_robot',
            '-z', '0.23',
        ],
        output='screen',
    )

    spawn_after_gazebo = TimerAction(period=2.0, actions=[spawn_entity])

    return LaunchDescription([
        rviz_arg,
        rsp,
        world_arg,
        gazebo,
        spawn_after_gazebo,
    ])