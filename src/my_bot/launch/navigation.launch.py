import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    declare_map = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(
            get_package_share_directory('my_bot'),
            'maps', 'map.yaml'
        ),
        description='Full path to map yaml file'
    )

    declare_params = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(
            get_package_share_directory('my_bot'),
            'config', 'nav2_params.yaml'
        ),
        description='Full path to nav2 params file'
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('nav2_bringup'),
                         'launch', 'bringup_launch.py')
        ]),
        launch_arguments={
            'map': map_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file
        }.items()
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_map,
        declare_params,
        nav2
    ])