from struct import pack
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

username = os.path.expanduser('~')

def generate_launch_description():
    package_dir = username+'/ros2_ws/src/iwr6843aop_pub/'
    robot_description_path = os.path.join(package_dir, 'urdf/my_urdf.urdf')    
    
    urdf_model = LaunchConfiguration('urdf_model')
    
    urdf_model_arg = DeclareLaunchArgument(
        name='urdf_model', 
        default_value=robot_description_path,
        description='Path to urdf file'
    )

    return LaunchDescription([
    
        urdf_model_arg,

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
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters = [{"robot_state_description": Command(['xacro ', LaunchConfiguration('urdf_model')])}],
            arguments=[robot_description_path]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        )
    ])
