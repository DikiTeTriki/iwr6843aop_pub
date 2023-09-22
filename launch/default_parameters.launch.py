from struct import pack
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros.actions
from launch_ros.actions import Node
import launch
from ament_index_python.packages import get_package_share_directory
import os

from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

username = os.path.expanduser('~')

def generate_launch_description():
    package_dir = username+'/ros2_ws/src/iwr6843aop_pub/'    
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    urdf_file_name = 'my_urdf.urdf.xml'
    urdf_path = os.path.join(package_dir, 'urdf', urdf_file_name)
    with open(urdf_path, 'r') as infp:
        robot_description = infp.read()
    
    urdf_model = LaunchConfiguration('urdf_model', default=robot_description)
    
    rsp = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters = [{'use_sim_time':use_sim_time, "robot_state_description": robot_description}],
        arguments=[urdf_path]
        )
        
    rsp = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters = [{'use_sim_time':use_sim_time}],
        arguments=[urdf_path]
    )

    return LaunchDescription([
    
        rsp,
        
        Node(
            package="iwr6843aop_pub",
            executable="pcl_pub",
            parameters=[
                {'cfg_path': username+'/ros2_ws/src/iwr6843aop_pub/cfg_files/xwr68xx_AOP_profile_2023_08_31T12_02_53_714.cfg'},
            	{'cli_port': '/dev/ttyUSB0'},
           	{'data_port': '/dev/ttyUSB1'},
           	{'frame_id': 'radar_1_link'}
            ]
    	),
    	Node(
            package="iwr6843aop_pub",
            executable="pcl_pub",
            parameters=[
                {'cfg_path': username+'/ros2_ws/src/iwr6843aop_pub/cfg_files/xwr68xx_AOP_profile_2023_08_31T12_02_53_714.cfg'},
            	{'cli_port': '/dev/ttyUSB2'},
            	{'data_port': '/dev/ttyUSB3'},
            	{'frame_id': 'radar_2_link'}
            ]
    	),
    	Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        )
    ])
