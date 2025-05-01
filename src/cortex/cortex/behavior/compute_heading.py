
# behaviortree package
import behavior_tree.BehaviorTree as BehaviorTree

from rclpy.logging import get_logger


class computeHeading(BehaviorTree.Action):
    def __init__(self):
        BehaviorTree.Action.__init__(self, name='compute_heading', action=self.compute_heading)
        self.logger = get_logger('compute_heading')

    def compute_heading(self):
        # see https://www.scantips.com/lights/subjectdistance.html for more info

        obj_names = self.blackboard['object_names']
        cur_obj = self.blackboard['current_object']

        if len(obj_names) == 0:
            return False
        
        if cur_obj not in obj_names:
            return False
        
        index = 0
        for i, o in enumerate(obj_names):
            if o == cur_obj:
                index = i
                self.logger.info(f'Detected {cur_obj} in frame')
                break


        # bounding box coordinates of top left and bottom right
        tl, br = self.blackboard['top_left'][index*2:(index*2)+2], self.blackboard['bottom_right'][index*2:(index*2)+2]


        # bounding box x, y dims in pixels - object must not be tilted skewed or foreshortened
        px, py = br[0]-tl[0], br[1]-tl[1]

        # object size on image sensor
        rx, ry = self.blackboard['image_size']
        sx, sy = self.blackboard['sensor_size']
        x, y = (px / rx) * sx, (py / ry) * sy

        # size of currently tracked object; supplied by parent tree
        f = self.blackboard['focal_length']
        X, Y = self.blackboard[cur_obj]

        # pinhole projection formula
        # average distance based on height and width estimations
        d1 = (((X * f) / x)  + ((Y * f) / y)) / 2

        self.blackboard['current_object_distance'] = d1

        # difference between object and image center in pixels
        cx, cy = self.blackboard['object_positions_x'][index], self.blackboard['object_positions_y'][index]
        dx, dy = cx - (rx/2), cy - (ry/2)
        x_fov, y_fov = self.blackboard['fov']
        theta_x, theta_y = (dx / rx) * x_fov, (dy / ry) * y_fov

        self.blackboard['current_object_heading'] = [theta_x, theta_y]

        return True

    
def main(args=None):

    # take picture: ffmpeg -f v4l2 -s 640x480 -i /dev/video2 -frames:v 1 /tmp/webcam.jpg

    blackboard = BehaviorTree.Blackboard()
    cur_obj = 'bottle'
    blackboard['current_object'] = cur_obj
    blackboard[cur_obj] = [0.21, 0.045]

    blackboard['focal_length'] = 0.0025
    blackboard['image_size'] = [640, 480]
    blackboard['sensor_size'] = [3.673e-3, 2.738e-3]
    blackboard['fov'] = [95, 70]

    compute_heading = computeHeading(blackboard)

    compute_heading.evaluate()



if __name__ == '__main__':
    main()


    


            



