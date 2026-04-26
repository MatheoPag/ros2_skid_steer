import os
import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='my_robot').find("my_robot")
    urdfModelPath = os.path.join(pkgPath, 'urdf/robot.urdf')
    rviz_config = os.path.join(pkgPath, 'config', 'config.rviz')
    
    controllers_yaml = os.path.join(pkgPath, 'config', 'controllers.yaml')
    with open(urdfModelPath, 'r') as file:
        robot_desc = file.read().replace(
            '__CONTROLLERS_YAML__', controllers_yaml
        )

    params = {'robot_description': robot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        output='screen',
        parameters=[params, {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package = "joint_state_publisher",
        executable = "joint_state_publisher",
        name = "joint_state_publisher",
        parameters=[params],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration("gui"))
    )
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package = "joint_state_publisher_gui",
        executable = "joint_state_publisher_gui",
        name = "joint_state_publisher_gui",
        condition=launch.conditions.IfCondition(LaunchConfiguration("gui"))
    )
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        condition=launch.conditions.IfCondition(LaunchConfiguration("rviz"))
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name="rviz", default_value="True", description="This is a flag for rviz"),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='False', description="time for gazebo"),
        launch.actions.DeclareLaunchArgument(name="gui", default_value="True", description="This is a flag for joint_state_publisher_gui"),
        launch.actions.DeclareLaunchArgument(name="robot", default_value=urdfModelPath, description="Path to the urdf model file"),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])