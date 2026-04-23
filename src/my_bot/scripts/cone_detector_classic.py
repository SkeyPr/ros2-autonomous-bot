#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge
import cv2
import numpy as np

class ConeDetectorClassic(Node):
    def __init__(self):
        super().__init__('cone_detector_classic')
        self.bridge = CvBridge()

        self.fx = self.fy = self.cx = self.cy = None

        self.lower_orange = np.array([5, 150, 150])
        self.upper_orange = np.array([20, 255, 255])

        self.latest_depth = None

        self.create_subscription(CameraInfo, '/camera/camera_info', self.camera_info_cb, 10)
        self.create_subscription(Image, '/camera/image_raw', self.rgb_cb, 10)
        self.create_subscription(Image, '/camera/depth/image_raw', self.depth_cb, 10)

        self.image_pub = self.create_publisher(Image, '/cone_classic/image', 10)
        self.point_pub = self.create_publisher(PointStamped, '/cone_classic/position', 10)

        self.get_logger().info('Classic cone detector started')

    def camera_info_cb(self, msg):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]

    def depth_cb(self, msg):
        self.latest_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    def is_valid_cone(self, frame, hsv, x, y, w, h):
        img_h, img_w = frame.shape[:2]

        # Check 1: Aspect ratio
        aspect_ratio = h / w
        if aspect_ratio < 0.8:
            return False

        # Check 2: Dark base below orange region
        base_y_start = min(y + h, img_h - 1)
        base_y_end   = min(y + h + int(h * 0.3), img_h)

        if base_y_end <= base_y_start:
            return False

        base_region = hsv[base_y_start:base_y_end, x:x + w]
        if base_region.size == 0:
            return False

        dark_mask = base_region[:, :, 2] < 60
        dark_ratio = np.sum(dark_mask) / dark_mask.size

        if dark_ratio < 0.25:
            return False

        # Check 3: Orange denser in upper half than lower half
        mid_y = y + h // 2
        upper_region = hsv[y:mid_y, x:x + w]
        lower_region = hsv[mid_y:y + h, x:x + w]

        if upper_region.size == 0 or lower_region.size == 0:
            return False

        upper_orange_mask = cv2.inRange(upper_region, self.lower_orange, self.upper_orange)
        lower_orange_mask = cv2.inRange(lower_region, self.lower_orange, self.upper_orange)

        upper_orange_ratio = np.sum(upper_orange_mask > 0) / upper_region[:, :, 0].size
        lower_orange_ratio = np.sum(lower_orange_mask > 0) / lower_region[:, :, 0].size

        if upper_orange_ratio < lower_orange_ratio * 0.5:
            return False

        return True

    def rgb_cb(self, msg):
        if self.latest_depth is None or self.fx is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Step 1 — HSV mask for orange
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)

        # Step 2 — Clean up noise
        kernel_small = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small)

        # Step 3 — Dilate vertically to merge orange bands into one blob
        kernel_merge = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 40))
        mask_merged = cv2.dilate(mask, kernel_merge, iterations=1)

        # Step 4 — Close remaining holes
        kernel_close = np.ones((7, 7), np.uint8)
        mask_merged = cv2.morphologyEx(mask_merged, cv2.MORPH_CLOSE, kernel_close)

        # Step 5 — Find contours on merged mask
        contours, _ = cv2.findContours(mask_merged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        annotated = frame.copy()

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 800 or area > 80000:
                continue

            x, y, w, h = cv2.boundingRect(cnt)

            # Solidity check
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            if hull_area == 0:
                continue
            solidity = area / hull_area
            if solidity < 0.5:
                continue

            # Structural validation
            if not self.is_valid_cone(frame, hsv, x, y, w, h):
                continue

            # Center
            u = x + w // 2
            v = y + h // 2

            # Depth lookup
            dh, dw = self.latest_depth.shape[:2]
            if not (0 <= u < dw and 0 <= v < dh):
                continue

            Z = float(self.latest_depth[v, u])
            if not np.isfinite(Z) or Z <= 0.0:
                continue

            # Back-project to 3D
            X = (u - self.cx) * Z / self.fx
            Y = (v - self.cy) * Z / self.fy

            # Publish
            pt = PointStamped()
            pt.header = msg.header
            pt.point.x = X
            pt.point.y = Y
            pt.point.z = Z
            self.point_pub.publish(pt)

            # Annotate
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 165, 255), 2)
            cv2.circle(annotated, (u, v), 5, (0, 0, 255), -1)
            cv2.putText(annotated, f'cone Z={Z:.2f}m', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

            # Debug visuals
            base_y_start = min(y + h, frame.shape[0] - 1)
            base_y_end   = min(y + h + int(h * 0.3), frame.shape[0])
            cv2.rectangle(annotated, (x, base_y_start), (x + w, base_y_end), (255, 0, 0), 1)
            mid_y = y + h // 2
            cv2.line(annotated, (x, mid_y), (x + w, mid_y), (0, 255, 255), 1)

            self.get_logger().info(f'Cone at X={X:.2f} Y={Y:.2f} Z={Z:.2f}m')

        out = self.bridge.cv2_to_imgmsg(annotated, encoding='bgr8')
        out.header = msg.header
        self.image_pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = ConeDetectorClassic()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()