import rclpy
import rclpy.node as rcl

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
        cur_obj = 'bottle'
        self.blackboard['current_object'] = cur_obj

        # initialize blackboard (TODO: from JSON)
        self.blackboard[cur_obj] = [0.21, 0.045]
        self.blackboard['focal_length'] = 0.0025
        self.blackboard['image_size'] = [640, 480]
        self.blackboard['sensor_size'] = [3.673e-3, 2.738e-3]
        self.blackboard['fov'] = [95, 70]

        # subtree nodes

        self.root = BehaviorTree.Iterator(name='try_until_detection', maxAttempts=5, blackboard=self.blackboard)
        
        seq = BehaviorTree.Sequence(name='seq')

        get_obj = BTClient(name='get_obj', srv_obj=DetectObjects, srv_name='detect_objects')

        compute_heading = computeHeading()

        # level order initialisation
        self.root.child = seq
        seq.add_child(get_obj)
        seq.add_child(compute_heading)
    
        # tick length parameter for ticking the behavior tree
        self.declare_parameter('tick_length', 1.0)
        TICK_LENGTH = self.get_parameter('tick_length').get_parameter_value().double_value

        self.timer = self.create_timer(TICK_LENGTH, self.evaluate)

    def evaluate(self):
        result = self.root.evaluate()
        self.get_logger().info(f'Root node {self.root.name} EVALUATED to {result}')
        self.destroy_node()



def main(args=None):
    rclpy.init(args=args)
    
    root = BTRoot()

    # behavior tree root node is ticked by internal timer
    # returning true makes the node self destruct
    # spin() handles callbacks incurred by timer object
    rclpy.spin(root)

    root.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


    


            



