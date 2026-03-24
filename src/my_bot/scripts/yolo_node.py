#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2


class YoloNode(Node):

    def __init__(self):
        super().__init__('yolo_node')
        self.bridge = CvBridge()
        self.model = YOLO('/home/ubuntu/botws/models/best.pt')

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/yolo/image_detected',
            10
        )

        self.get_logger().info('YOLO node started, waiting for images...')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(frame, verbose=False)
        annotated_frame = results[0].plot()
        detected_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding='bgr8')
        detected_msg.header = msg.header
        self.publisher.publish(detected_msg)


def main(args=None):
    rclpy.init(args=args)
    node = YoloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()