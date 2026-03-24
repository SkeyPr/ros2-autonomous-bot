#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge
from ultralytics import YOLO
import numpy as np
import cv2

class ConeLocalizer(Node):
    def __init__(self):
        super().__init__('cone_localizer')
        self.bridge = CvBridge()
        self.model = YOLO('/home/ubuntu/botws/models/best.pt')

        # Camera intrinsics — populated from /camera/camera_info
        self.fx = self.fy = self.cx = self.cy = None

        # Subscribers
        self.create_subscription(CameraInfo, '/camera/camera_info', self.camera_info_cb, 10)
        self.create_subscription(Image, '/camera/image_raw', self.rgb_cb, 10)
        self.create_subscription(Image, '/camera/depth/image_raw', self.depth_cb, 10)

        # Publishers
        self.image_pub = self.create_publisher(Image, '/cone_localizer/image', 10)
        self.point_pub = self.create_publisher(PointStamped, '/cone_position', 10)

        # Storage for latest frames
        self.latest_depth = None

        self.get_logger().info('Cone Localizer node started')

    def camera_info_cb(self, msg):
        # K matrix: [fx, 0, cx, 0, fy, cy, 0, 0, 1]
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]

    def depth_cb(self, msg):
        self.latest_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    def rgb_cb(self, msg):
        if self.latest_depth is None or self.fx is None:
            return  # Wait until we have depth and intrinsics

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(frame, verbose=False)
        annotated = results[0].plot()

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            u = (x1 + x2) // 2  # bounding box center x
            v = (y1 + y2) // 2  # bounding box center y

            # Bounds check
            h, w = self.latest_depth.shape[:2]
            if not (0 <= u < w and 0 <= v < h):
                continue

            Z = float(self.latest_depth[v, u])

            if not np.isfinite(Z) or Z <= 0.0:
                continue  # Invalid depth reading

            # Back-project to 3D
            X = (u - self.cx) * Z / self.fx
            Y = (v - self.cy) * Z / self.fy

            # Publish 3D point
            point_msg = PointStamped()
            point_msg.header = msg.header
            point_msg.point.x = X
            point_msg.point.y = Y
            point_msg.point.z = Z

            self.point_pub.publish(point_msg)

            # Annotate image
            label = f'Z={Z:.2f}m'
            cv2.putText(annotated, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.circle(annotated, (u, v), 5, (0, 0, 255), -1)

            self.get_logger().info(f'Cone at X={X:.2f} Y={Y:.2f} Z={Z:.2f}m')

        out_msg = self.bridge.cv2_to_imgmsg(annotated, encoding='bgr8')
        out_msg.header = msg.header
        self.image_pub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ConeLocalizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()