# Mini Project Report

## 1. Title of Project
Vision-Guided Detection and 3D Localization of Construction Cones and Barrels Using Classical and Deep Learning Computer Vision

## 2. Introduction
Construction sites are dynamic and safety-critical environments where temporary markers such as cones and barrels define working boundaries. Because these markers are frequently moved, static map-based autonomy alone is not sufficient. This mini project focuses on computer vision methods for real-time marker detection and depth-assisted 3D localization.

The system is developed in ROS2 Humble with Gazebo simulation and uses an RGB-D camera stream. Two CV approaches are implemented and compared:
1. Classical HSV-based cone detection with contour and structural validation.
2. YOLOv8-based learned detection/localization pipeline.

This comparison allows both interpretability (classical vision) and scalability (deep learning), while keeping the same sensing setup.

## 3. Problem Definition and Algorithm
### Problem Definition
Detect construction cones and barrels in real time from camera input and estimate their 3D positions so that the robot can use this information for safety-aware operation.

### Algorithm
#### A. Classical HSV-Based Algorithm (Cone-Focused)
1. Capture RGB and depth frames.
2. Convert RGB image to HSV.
3. Apply orange color threshold to create mask.
4. Apply morphology (open, dilate, close) to reduce noise and merge regions.
5. Extract contours and apply geometric filters (area, solidity, aspect ratio).
6. Apply structural checks (dark-base presence, upper/lower color distribution).
7. Compute bounding box center and read depth value.
8. Back-project 2D point to 3D using camera intrinsics.

#### B. YOLOv8-Based Algorithm
1. Capture RGB and depth frames.
2. Run YOLO inference on RGB image.
3. Obtain class label, confidence, and bounding box.
4. Compute bounding box center pixel.
5. Read depth value at center.
6. Back-project to 3D point using camera intrinsics.
7. Publish annotated image and 3D position output.

### 3D Projection Equation
Given pixel $(u,v)$, depth $Z$, and intrinsics $(f_x, f_y, c_x, c_y)$:

$$
X = \frac{(u-c_x)Z}{f_x}, \quad
Y = \frac{(v-c_y)Z}{f_y}, \quad
Z = Z
$$

## 4. Block Diagram
```text
RGB Image + Depth Image + Camera Info
					 |
					 v
		+------------------------+
		|   Perception Module    |
		|------------------------|
		| A) HSV Classical Path  |
		| B) YOLOv8 Learned Path |
		+------------------------+
					 |
					 v
		Detection (bbox/class/conf)
					 |
					 v
		 Depth-based 3D Localization
					 |
					 v
		Output Topics / Visualization
		(/cone_classic/image,
		 /yolo/image_detected,
		 /cone_classic/position,
		 /cone_position)
```

## 5. Methodology Used
### Development Environment
1. ROS2 Humble.
2. Gazebo simulation.
3. OpenCV, cv_bridge, NumPy.
4. Ultralytics YOLOv8.

### Experimental Method
1. Run both CV approaches on the same RGB-D input stream.
2. Compare detection quality and runtime behavior.
3. Evaluate localization outputs from depth projection.
4. Perform qualitative failure analysis (lighting, clutter, occlusion).

### Evaluation Parameters
1. Detection: precision, recall, mAP50, mAP50-95.
2. Runtime: latency and FPS.
3. Localization: 3D coordinate consistency/error.

## 6. Code of Project
### Key Files
1. `src/my_bot/scripts/cone_detector_classic.py` - Classical HSV detection + 3D localization.
2. `src/my_bot/scripts/yolo_node.py` - YOLO inference and visualization.
3. `src/my_bot/scripts/cone_localizer.py` - YOLO detection + depth-based 3D point publishing.

### Sample Code Snippet (HSV Masking)
```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
kernel_small = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small)
```

### Sample Code Snippet (YOLO Inference)
```python
results = self.model(frame, verbose=False)
annotated_frame = results[0].plot()
```

### Sample Code Snippet (3D Back-Projection)
```python
X = (u - self.cx) * Z / self.fx
Y = (v - self.cy) * Z / self.fy
```

## 7. Snapshots of Input and Output
### Input Snapshot
1. Raw camera scene from Gazebo world with cones/barrels.

### Output Snapshots
1. Navigation goal and robot execution:
	- `assets/navigation1.jpeg`
	- `assets/navigation2.jpeg`
2. C    one detection and localization visualization:
	- `assets/cone_detection.jpeg`

Note: Add these images in the final report PDF under this section with captions.

## 8. Result and Experimental Evaluation
### Observed Results
1. Classical HSV pipeline successfully detects cone-like orange objects under suitable lighting.
2. YOLO pipeline provides stronger generalization and is better suited for cone-and-barrel multi-class scaling.
3. Depth-assisted localization provides metric 3D point outputs for detected objects.

### Comparative Evaluation (Qualitative)
1. Classical approach:
	- Advantages: simple, interpretable, lightweight.
	- Limitations: sensitive to lighting and color distractors.
2. YOLO approach:
	- Advantages: robust to scene variation, scalable to multiple classes.
	- Limitations: depends on dataset quality and training.

### Metrics to Report (Fill with your measured values)
1. Precision: ______
2. Recall: ______
3. mAP50: ______
4. mAP50-95: ______
5. Average latency (ms): ______
6. FPS: ______
7. 3D localization error (m): ______

## 9. Conclusion and Future Work
### Conclusion
This mini project demonstrates a practical CV pipeline for construction marker awareness using two approaches: classical HSV-based detection and YOLOv8-based learned detection. Combined with depth-based 3D localization, the system produces actionable spatial outputs in real time and establishes a solid baseline for safety-focused autonomous robotics.

### Future Work
1. Retrain YOLO model for stronger cone-and-barrel class balance.
2. Add temporal tracking for smoother multi-frame detections.
3. Integrate detection outputs into behavior-level stop/slow/reroute control.
4. Validate on real-world captured data beyond simulation.

## 10. References
1. ROS2 Documentation. https://docs.ros.org
2. Nav2 Documentation. https://navigation.ros.org
3. SLAM Toolbox Package Documentation.
4. Ultralytics YOLO Documentation. https://docs.ultralytics.com
5. OpenCV Documentation. https://docs.opencv.org

## 11. Name and Roll No of Students and Signature
| S. No. | Name of Student | Roll No. | Signature |
|---|---|---|---|
| 1 | Akash Patel | 1032221882 | ____________________ |
| 2 | Suryabhaas Karmakar | 1032221820 | ____________________ |
| 3 | Akash Bopalkar | 10322210569 | ____________________ |

