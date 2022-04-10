#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class UsbCamSensor(object):
    def __init__(self):
        self.image_sub_topic = '/usb_cam/image_raw'
        self.img_sub = rospy.Subscriber(self.image_sub_topic, Image, self.camera_callback)
        self.bridge_ob = CvBridge()
        height = 512
        width = 512
        self.cv_img = np.zeros((height,width,3), np.uint8)
        

    def camera_callback(self, data):
        try:
            self.cv_img = self.bridge_ob.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

    def get_image(self):
        return self.cv_img


