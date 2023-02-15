#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from visualization_msgs.msg import *
import csv
import roslib

RADIUS = 0.05

class draw_training_node:
    def __init__(self):
        rospy.init_node("draw_node", anonymous=True)
        # self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/change_dataset_balance/'
        self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/'
        # self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/use_dl_output/'
        self.path_pub = rospy.Publisher('move_base/DWAPlannerROS/local_plan', Path, queue_size=10)
        self.points7_pub = rospy.Publisher('point7', MarkerArray, queue_size=10)
        self.path_data = Path()
        self.points7 = MarkerArray()
        self.point7_count = 0
        self.path_data.header.frame_id = "map"
        self.pose_list = [[],[]]
        self.make_points()
        

    
    def make_points(self):
        self.points7.markers = []
        num = 0

        with open(self.path + 'path.csv', 'r') as f:
            is_first = True
            for row in csv.reader(f):
                if is_first:
                    is_first = False
                    continue

                # str_x, str_y = row
                no, str_x, str_y = row
                x, y = float(str_x), float(str_y)
        # with open(self.path + 'corner/traceable_pos.csv', 'r') as f:
        #     for row in csv.reader(f):
        #
        #         str_x, str_y,str_the = row
        #         x, y = float(str_x), float(str_y)
        #
        #
                point_marker = Marker()

                point_marker.header.frame_id = "map"
                point_marker.type = Marker.CYLINDER
                point_marker.action = point_marker.ADD

                point_marker.scale.x = 2 * RADIUS
                point_marker.scale.y = 2 * RADIUS
                point_marker.scale.z = 0.01

                point_marker.color.a = 1.0

                point_marker.pose.position.x = x + 100 #x
                point_marker.pose.position.y = y + 100 #y
                point_marker.pose.position.z = 0.0

                point_marker.pose.orientation.x = 0.0
                point_marker.pose.orientation.y = 0.0
                point_marker.pose.orientation.z = 0.0
                point_marker.pose.orientation.w = 1.0

                point_marker.color.r = 0.4
                point_marker.color.g = 0.0
                point_marker.color.b = 0.0
                point_marker.id = self.point7_count
                self.point7_count += 1
                self.points7.markers.append(point_marker)

    def loop(self):
        self.path_pub.publish(self.path_data)
        self.points7_pub.publish(self.points7)
    
if __name__ == '__main__':
    rg = draw_training_node()
    r = rospy.Rate(1 / 0.5)
    while not rospy.is_shutdown():
        rg.loop()
        r.sleep()
