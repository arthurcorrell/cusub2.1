from launch import LaunchDescription
from launch_ros.actions import Node
import os
import subprocess
from launch.actions import TimerAction

def list_working_video_devices():
    devices = []
    dev_dir = '/dev'
    for entry in os.listdir(dev_dir):
        if entry.startswith('video') and entry != 'video0':
            dev_path = os.path.join(dev_dir, entry)
            try:
                subprocess.check_output(
                    ['v4l2-ctl', '-D', '-d', dev_path],
                    stderr=subprocess.STDOUT
                )
                devices.append(int(dev_path[-1]))
            except subprocess.CalledProcessError:
                continue  # skip non-functional devices
    return devices


def generate_launch_description():
    camera_nodes = []
    devices = list_working_video_devices()

    print(f'FOUND DEVICES \n {devices}')

    devices = [4, 8, 2, 6]
    for dev_idx, id in zip(devices, ['front', 'rear', 'top', 'bottom']):
        cam_name = f'SubCam{dev_idx}'
        node = Node(
                package='chimera_camera',
                executable='camera_node_raw',
                name=cam_name,
                parameters=[{'camera_port':dev_idx, 'fps':15, 'camera_id':id}]
        )
        camera_nodes.append(node)
    
    fg_bridge = Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen',
            parameters=[
                {'port': 8765}  # optional: default is 8765
            ]
        )
    camera_nodes.append(fg_bridge)
    
        
    return LaunchDescription(camera_nodes)