import rclpy
import rclpy.node as rcl
import yaml
from ament_index_python.packages import get_package_share_directory
import os

# behaviortree package
import behavior_tree.BehaviorTree as BehaviorTree
from behavior_tree.publisher_member_function import BTPublisher
from behavior_tree.subscriber_member_function import BTSubscriber
from behavior_tree.client_member_function import BTClient

# chimera_camera package custom interfaces
from custom_interfaces.srv import DetectObjects

# cortex behaviors
from cortex.behavior.compute_heading import computeHeading

# ROS node wrapper around behavior tree for ticking
class BTRoot(rcl.Node):
    def __init__(self, name='bt_root'):
        rcl.Node.__init__(self, name)
        

        self.blackboard = BehaviorTree.Blackboard()

        # recieve target object from main behaviortree
        self.declare_parameter('current_object', 'bottle')
        cur_obj = self.get_parameter('current_object').get_parameter_value().string_value
        self.get_logger().info(f'Current object is set to: {cur_obj}')
        
        self.blackboard['current_object'] = cur_obj

        # yaml filepaths
        package_share_directory = get_package_share_directory('cortex')

        # get current object dimensions
        with open(os.path.join(package_share_directory, 'config','object_properties.yaml')) as f:
            file = yaml.safe_load(f)
            try:
                self.blackboard[cur_obj] = file[cur_obj]
            except KeyError:
                self.get_logger().error(f'No object propertie for {cur_obj}. Defaulting to cup (nalgene bottle)')

        # get camera properties
        with open(os.path.join(package_share_directory, 'config','camera_properties.yaml')) as f:
            file = yaml.safe_load(f)
            self.blackboard['focal_length'] = file['focal_length']
            self.blackboard['image_size'] = file['image_size']
            self.blackboard['sensor_size'] = file['sensor_size']
            self.blackboard['fov'] = file['fov']

        # subtree nodes

        self.root = BehaviorTree.Iterator(name='try_until_detection', maxAttempts=5, blackboard=self.blackboard)
        
        seq = BehaviorTree.Sequence(name='seq')

        get_obj = BTClient(name='get_obj', srv_obj=DetectObjects, srv_name='detect_objects')

        compute_heading = computeHeading()

        # no errror handling required; if compute_heading fails 1st time the seq is terminated
        def format_data():
            c_o = self.blackboard['current_object']
            c_o_d = self.blackboard['current_object_distance']
            c_o_h = self.blackboard['current_object_heading']
            return f'current object: {c_o} | \n distance: {c_o_d} | \n heading: {c_o_h}'

        publish_metadata = BTPublisher('publish_metadata', 'image_metadata', format_data)

        # level order initialisation
        self.root.child = seq
        seq.add_child(get_obj)
        seq.add_child(compute_heading)
        seq.add_child(publish_metadata)
    
        # tick length parameter for ticking the behavior tree
        self.declare_parameter('tick_length', 1.0)
        TICK_LENGTH = self.get_parameter('tick_length').get_parameter_value().double_value

        self.timer = self.create_timer(TICK_LENGTH, self.evaluate)

    def evaluate(self):
        result = self.root.evaluate()
        self.get_logger().info(f'Root node {self.root.name} EVALUATED to {result}')



def main(args=None):
    rclpy.init(args=args)
    
    root = BTRoot()

    # behavior tree root node is ticked by internal timer
    # returning true makes the node self destruct
    # spin() handles callbacks incurred by timer object
    rclpy.spin(root)

    #root.evaluate()

    root.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


    


            



