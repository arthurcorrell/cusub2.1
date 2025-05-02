from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cortex',
            executable='compute_heading_test',
            name='bt_root', 
            parameters=[{'current_object':'cup', 'camera_id':'front', 'tick_length':2.0}]
        ),
        Node(
            package='chimera_camera',
            executable='camera_node_raw',
            name='WebCam',
            parameters=[{'camera_port':0, 'fps':30, 'camera_id':'front'}]
        ),
        Node(
            package='chimera_camera',
            executable='camera_node_raw',
            name='SubCam1',
            parameters=[{'camera_port':2, 'fps':15, 'camera_id':'bottom'}]
        ),
        Node(
            package='chimera_camera',
            executable='camera_node',
            name='CameraPublisher',
            parameters=[{'display_output':True}]
        ),
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen',
            parameters=[
                {'port': 8765}  # optional: default is 8765
            ]
        )
    ])