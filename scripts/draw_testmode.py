#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import *
import csv
import roslib

RADIUS = 0.03

class draw_training_node:
    def __init__(self):
        rospy.init_node("draw_node", anonymous=True)
        # self.path = roslib.packages.get_pkg_dir('draw_nav_cloning') + '/data/analysis/'
        # self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/change_dataset_balance/'
        # self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/change_dataset_balance/'
        self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/use_dl_output/'
        # self.path = roslib.packages.get_pkg_dir('nav_cloning') + '/data/analysis/follow_path/'
        # self.result_path = "/home/kiyooka/Downloads/result_change_dataset_balance/"
        self.result_path = "/home/kiyooka/Downloads/result_use_dl_output/"
        # self.result_path = "/home/kiyooka/Downloads/result_follow_path/"
        self.path_pub = rospy.Publisher('move_base/DWAPlannerROS/local_plan', Path, queue_size=10)
        self.points1_pub = rospy.Publisher('point', MarkerArray, queue_size=10)
        self.pose_list = [[],[]]
        self.path_data = Path()
        self.points1 = MarkerArray()
        self.path_data.header.frame_id = "map"
        self.points1.markers = []
        self.points1_count = 0
        self.make_path()
        self.trajectory()

    def make_path(self):
        # with open(self.path + 'training.csv', 'r') as f:
        # with open(self.path + 'traceable_pos.csv', 'r') as f:
        with open(self.path + 'path.csv', 'r') as f:
        # with open('/home/kiyooka/Downloads/training.csv', 'r') as f:
        # with open('/home/kiyooka/catkin_ws/src/nav_cloning/data/analysis/path.csv') as f:
            is_first = True
            for row in csv.reader(f):
                if is_first:
                    is_first = False
                    continue
                # str_x, str_y, str_the, traceable = row
                # str_x, str_y, str_the = row
                # str_episode, mode, distance,str_x, str_y, str_the = row
                path_num,str_x, str_y = row
                # if mode == "training":
                x, y = float(str_x), float(str_y)
                pose = PoseStamped()
                pose.header.frame_id = "map"
                pose.pose.position.x = x + 100
                pose.pose.position.y = y + 100
                self.pose_list[0].append(x)
                self.pose_list[1].append(y)
                if len(self.pose_list[0]) %7 == 4:
                    self.path_data.poses.append(pose)

    def trajectory(self):
        list_step = []
        list_x = []
        list_y = []
        list_count = []
        list_collision = []
        list_timer = []


        with open(self.result_path + '2-3_50/training.csv', 'r') as f:
            # is_first = True
            for row in csv.reader(f):
                str_step, mode ,distance, str_x, str_y,str_the = row
                x, y = float(str_x) + 100, float(str_y) + 100
                # if mode == "training":
                if mode == "test":
                    point_marker = Marker()
                    point_marker.header.frame_id = "map"
                    point_marker.type = Marker.CYLINDER
                    point_marker.action = point_marker.ADD
                    point_marker.scale.x = 2 * RADIUS
                    point_marker.scale.y = 2 * RADIUS
                    point_marker.scale.z = 0.01
                    point_marker.color.a = 1.0
                    point_marker.pose.position.x = x
                    point_marker.pose.position.y = y
                    point_marker.pose.position.z = 0.0
                    point_marker.pose.orientation.x = 0.0
                    point_marker.pose.orientation.y = 0.0
                    point_marker.pose.orientation.z = 0.0
                    point_marker.pose.orientation.w = 1.0
                    point_marker.color.r = 0.0
                    point_marker.color.g = 0.0
                    point_marker.color.b = 0.0
                    point_marker.id = self.points1_count
                    self.points1_count += 1
                    self.points1.markers.append(point_marker)
    def loop(self):
        # self.path_pub.publish(self.path_data)
        self.points1_pub.publish(self.points1)
    
if __name__ == '__main__':
    rg = draw_training_node()
    r = rospy.Rate(1 / 0.5)
    while not rospy.is_shutdown():
        rg.loop()
        r.sleep()
