#!/usr/bin/env python3.6

import rospy
import anki_vector
import cv_bridge
import numpy

import cv2

from sensor_msgs.msg import Image

class Camera(object):
    def __init__(self, async_robot, publish_rate=10, image_frame_id='camera_link'):
        self.async_robot = async_robot
        self.rate = rospy.Rate(publish_rate)
        self.image_frame_id = image_frame_id
        self.image_publisher = rospy.Publisher("~camera", Image, queue_size=1)
        self.publish_camera_feed()

    def publish_camera_feed(self):
        bridge = cv_bridge.CvBridge()

        while not rospy.is_shutdown():
            raw_image = numpy.asarray(self.async_robot.camera.latest_image.raw_image)
            # image = bridge.cv2_to_imgmsg(numpy.asarray(self.async_robot.camera.latest_image), encoding="rgb8") # convert PIL.Image to ROS Image
            image = bridge.cv2_to_imgmsg(raw_image, encoding="rgb8") # convert PIL.Image to ROS Image
            image.header.stamp = rospy.Time.now()
            image.header.frame_id = self.image_frame_id
            self.image_publisher.publish(image)

            # make sure to publish at required rate
            self.rate.sleep()

if __name__=="__main__":
    rospy.init_node("camera")
    async_robot = anki_vector.AsyncRobot(enable_camera_feed=True)
    async_robot.connect()
    Camera(async_robot)
    rospy.spin()

