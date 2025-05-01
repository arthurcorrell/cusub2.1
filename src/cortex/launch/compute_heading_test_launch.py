from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cortex',
            namespace='test',
            executable='compute_heading_test',
            name='bt_root', 
            parameters=[{'current_object':'cup', 'tick_length':2.0}]
        ),
        Node(
            package='chimera_camera',
            namespace='test',
            executable='camera_node',
            name='CameraPublisher',
            parameters=[{'camera_port':0, 'display_output':True}]
        ),
        Node(
            package='chimera_camera',
            namespace='test',
            executable='camera_node_raw',
            name='CameraPublisherRaw',
            parameters=[{'camera_port':2, 'fps':15}]
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