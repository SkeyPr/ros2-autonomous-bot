# Full Academic Report Draft

## Title
Vision-Guided Autonomous Detection and Localization of Construction Cones and Barrels for Safe Mobile Robot Navigation in Dynamic Construction Sites

## Abstract
Construction sites are dynamic, safety-critical environments in which temporary markers such as cones and barrels define operational boundaries. Because marker placement changes frequently, static-map-only autonomy cannot guarantee safe decision-making. This report presents a ROS2-based autonomous robotic framework for real-time marker perception and depth-assisted 3D localization, designed to support safer navigation behavior in changing work zones. The implementation combines Gazebo simulation, SLAM Toolbox, AMCL localization, Nav2 planning/control, and two complementary perception pipelines: a classical HSV-based cone detector and a YOLOv8 learned detector/localizer. Current results demonstrate working dual-path cone perception and metric 3D localization; the next development stage focuses on robust cone-and-barrel learned detection and behavior-level hazard response (slowdown, stop, reroute). A KPI-driven evaluation methodology is defined across detection quality, latency, localization accuracy, and navigation safety outcomes. The contribution is an end-to-end, reproducible perception-to-action architecture tailored to construction safety workflows.

## 1. Introduction
### 1.1 Background
Mobile robots are increasingly used in industrial and construction workflows for inspection, logistics, and surveillance. Construction sites, however, are less structured than factory floors and involve temporary, frequently changing safety markers such as cones and barrels.

### 1.2 Problem Statement
Construction cone and barrel detection on construction sites.

### 1.3 Motivation
When robots rely only on pre-built maps, temporary safety markers may be ignored, creating unsafe motion plans near active work zones. Robust autonomous operation therefore requires scene-level semantic perception and responsive navigation policies that adapt to real-time marker observations.

### 1.4 Objectives
1. Detect construction cones and barrels in real time.
2. Estimate the 3D position of detected objects.
3. Integrate detections with autonomous navigation policies.
4. Trigger safe behavior based on hazard proximity.
5. Benchmark performance with reproducible KPIs.

## 2. Related Work and Technical Context
Autonomous navigation in ROS2 commonly combines SLAM/localization, global planning, and local control. For visual detection, two common families are classical color/shape pipelines and deep-learning detectors. Classical HSV pipelines are fast and interpretable but sensitive to lighting and domain changes. Deep-learning detectors such as YOLO are widely adopted for real-time vision tasks due to favorable speed-accuracy tradeoffs and stronger generalization. In construction-like domains, the key challenge is bridging object perception with actionable robot behavior under dynamic scene changes.

This project adopts both families deliberately. The classical branch provides a transparent baseline for cone detection and failure analysis, while the learned branch provides a scalable path toward robust multi-class perception, including barrel detection.

## 3. System Architecture
### 3.1 Hardware and Simulation Model
The robot is modeled as a differential-drive base with:
1. LiDAR for scan-based mapping and obstacle awareness.
2. RGB-D camera for object detection and depth-assisted localization.
3. Gazebo physics simulation in construction-themed worlds containing cones and barrels.

### 3.2 Software Stack
1. ROS2 Humble: middleware and node communication.
2. Gazebo: simulation and sensor generation.
3. SLAM Toolbox: online asynchronous mapping.
4. AMCL: probabilistic localization on a saved map.
5. Nav2: path planning, control, and behavior orchestration.
6. OpenCV-based classical HSV pipeline for cone detection.
7. YOLOv8: learned object detection inference.
8. OpenCV and cv_bridge: ROS-image interoperability.

### 3.3 Data Flow
1. Camera publishes RGB and depth streams.
2. Classical branch performs HSV thresholding, morphology, and contour validation.
3. Learned branch performs YOLO inference.
4. Localization node maps accepted detections to 3D coordinates.
5. Navigation consumes hazard points and adjusts motion behavior.

In the current implementation, detection outputs are published for visualization and localization; behavior-level hazard coupling is treated as the next integration milestone.

## 4. Methodology
### 4.1 Perception Methods

#### 4.1.1 Classical HSV-Based Cone Detection
The classical detector converts RGB frames to HSV color space and applies orange-range thresholding. Morphological opening, vertical dilation, and closing are used to suppress noise and merge fragmented cone regions. Candidate contours are validated using area, solidity, aspect ratio, and structural color heuristics (including dark-base and upper/lower orange-distribution checks). This branch is computationally lightweight, interpretable, and suitable as a cone-focused baseline.

#### 4.1.2 YOLO-Based Learned Detection
A YOLO-based detector processes RGB frames and outputs class labels, confidence scores, and bounding boxes. In the current codebase, YOLO is used both for image annotation and depth-assisted localization. This branch is the primary path for scalable multi-class detection, including cone and barrel classes after two-class model retraining. For each accepted detection, the center pixel is sampled in the depth frame.

### 4.2 3D Localization Method
Using camera intrinsic parameters \((f_x, f_y, c_x, c_y)\), a pixel \((u,v)\) with depth \(Z\) is back-projected:

$$
X = \frac{(u-c_x)Z}{f_x}, \quad
Y = \frac{(v-c_y)Z}{f_y}, \quad
Z = Z
$$

The resulting point is published as a 3D ROS message for downstream planning.

### 4.3 Navigation Integration
Detected objects are converted into semantic zones:
1. Caution zone: reduce linear velocity.
2. Danger zone: stop and request local/global replanning.
3. Critical zone: immediate halt and alert trigger.

At present, this policy is proposed architecture rather than fully implemented closed-loop behavior logic.

### 4.4 Training Strategy
1. Build class-balanced cone+barrel dataset.
2. Apply augmentations for lighting and viewpoint variability.
3. Validate class-wise performance using held-out scene splits.
4. Tune confidence and NMS thresholds for safety-critical recall.

The present trained model emphasizes cone detection performance; barrel robustness is an explicit next-stage objective.

## 5. Experimental Setup
### 5.1 Environment
Experiments are conducted in Gazebo worlds with varied cone/barrel placement, including cluttered and partially occluded conditions.

### 5.2 Test Scenarios
1. Static marker detection under nominal lighting.
2. Mixed marker scenes with clutter and occlusions.
3. Marker-adjacent goal navigation.
4. Dynamic obstacle interactions with marker-presence constraints.

### 5.3 Metrics
1. Detection: precision, recall, mAP50, mAP50-95 (per class, per approach).
2. Runtime: average and percentile latency, FPS.
3. Localization: mean absolute 3D error.
4. Navigation: successful hazard-avoidance and reroute rate.
5. Reliability: false positives per minute, node uptime.

## 6. Results (Draft Structure)
### 6.1 Perception Performance
Report comparative table by approach:
1. Classical HSV branch: cone precision/recall, false positives, latency.
2. YOLO branch: cone precision/recall/mAP and barrel precision/recall/mAP.

Recommended analysis notes:
1. Compare failure cases by lighting condition and distance.
2. Include qualitative examples where one branch succeeds and the other fails.
3. Report confidence-threshold sensitivity for safety-focused operating points.

### 6.2 Runtime Performance
Report:
1. Classical branch latency.
2. YOLO inference latency.
3. End-to-end pipeline latency.
4. Throughput in FPS.

### 6.3 Localization Quality
Report:
1. Mean and median localization error.
2. Error versus distance from sensor.

### 6.4 Navigation Safety Impact
Compare baseline navigation vs hazard-aware navigation:
1. Near-collision events.
2. Emergency stop frequency.
3. Goal completion success.

If behavior integration is still pending at submission time, include this section as a planned evaluation protocol with partial pilot results.

## 7. Discussion
### 7.1 Strengths
1. End-to-end integration from detection to action.
2. Dual-approach perception enables baseline-versus-learned comparison.
3. Real-time capable architecture.
4. Modular ROS2 components suitable for extension.

### 7.2 Limitations
1. Potential sim-to-real performance gap.
2. Classical HSV branch is sensitive to lighting and color variations.
3. Sensitivity to depth noise and occlusion.
4. Class imbalance risks when expanding to barrel detection.

### 7.3 Practical Deployment Considerations
1. Calibrate camera and depth alignment on real hardware.
2. Add temporal tracking for stable detections.
3. Use map-layer fusion for persistent hazard memory.

## 8. Conclusion
This project establishes a practical and extensible architecture for construction marker awareness in autonomous mobile robots. By combining dual-path visual perception with depth-based 3D localization and a clear navigation-integration roadmap, the framework addresses a critical gap in dynamic construction environments. The proposed KPI methodology, comparative evaluation plan, and phased roadmap provide a credible path from simulation validation to pilot deployment.

## 9. Future Work
1. Real-world data collection and field trials.
2. Completion of behavior-layer coupling with Nav2.
3. Multi-class expansion to additional site safety objects.
4. Multi-robot cooperative hazard mapping.
5. Uncertainty-aware planning using detection confidence.

## 10. Proposed References (Fill with course-required style)
1. ROS2 documentation and Nav2 documentation.
2. SLAM Toolbox and AMCL official packages.
3. Ultralytics YOLOv8 technical resources.
4. Construction robotics and safety perception literature.

## Appendix A: Suggested Tables
1. Detector performance by class.
2. Latency and throughput summary.
3. Localization error breakdown by distance bin.
4. Navigation safety outcomes by scenario.

## Appendix B: Suggested Figures
1. System architecture diagram.
2. Detection examples with confidence scores.
3. 3D localization visualization in RViz.
4. Navigation trajectories with and without hazard-aware behavior.
