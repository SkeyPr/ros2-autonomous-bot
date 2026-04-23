# 10-Slide Presentation Script with Speaker Notes

## Slide 1: Title and Problem Statement
### Slide Content
- Vision-Guided Autonomous Construction Safety Robot
- Problem statement: construction cone and barrel detection on dynamic construction sites
- Stack: ROS2 Humble, Gazebo, Nav2, SLAM Toolbox, dual perception pipeline

### Speaker Notes
This work addresses a high-impact site safety problem: robust detection of temporary construction markers and conversion of those detections into safer autonomous motion. Construction cones and barrels are dynamic by nature, so map-only autonomy is insufficient. Our platform combines perception, localization, and navigation to create real-time hazard awareness.

---

## Slide 2: Why This Problem Matters
### Slide Content
- Dynamic environment with frequent layout changes
- Temporary markers are safety-critical but non-static
- Static maps become stale quickly
- Autonomous systems require semantic hazard awareness

### Speaker Notes
Construction operations continuously reshape the scene, often within minutes. Cones and barrels communicate operational risk zones, but those zones are not persistent in map data. A robot that cannot perceive these updates may plan technically valid yet operationally unsafe paths. This project closes that gap.

---

## Slide 3: Project Objectives
### Slide Content
- Real-time detection of construction markers
- Metric 3D localization from depth + intrinsics
- Detection-to-action pipeline for navigation safety
- Safety policy triggers: caution, danger, critical response
- KPI-driven validation for technical and operational impact

### Speaker Notes
The objective is not only to detect objects in images, but to produce decisions. We estimate object position in 3D, then use that spatial information to constrain motion behavior. The system is evaluated with measurable KPIs so that safety claims are evidence-based.

---

## Slide 4: System Overview
### Slide Content
- Robot: differential drive with LiDAR and RGB-D camera
- Simulation: Gazebo construction scenarios with cone/barrel assets
- Mapping/localization: SLAM Toolbox + AMCL
- Navigation: Nav2 global and local planning stack
- Perception: dual branch (classical HSV + YOLOv8) with depth-assisted localization

### Speaker Notes
The robot is modeled with a differential-drive base, 2D LiDAR, and an RGB-D camera. SLAM and localization establish global context, while Nav2 executes motion planning. Perception is intentionally dual-branch: a lightweight classical cone detector for baseline benchmarking and a learned YOLO branch for scalable multi-class detection.

---

## Slide 5: Perception Pipeline
### Slide Content
1. Subscribe to RGB and depth topics
2. Classical branch: HSV threshold + morphology + contour/shape checks
3. Learned branch: YOLO inference on RGB frames
4. Extract object center from accepted detections
5. Read depth at object center
6. Back-project to 3D using camera intrinsics
7. Publish object positions as ROS messages

### Speaker Notes
In the classical branch, orange segmentation is followed by morphology and geometric validation to reduce noise and enforce cone-like structure. In the learned branch, YOLO predicts class and bounding box candidates. For validated detections, we compute center-point depth and back-project to metric XYZ. These outputs are published for visualization, analytics, and navigation coupling.

---

## Slide 6: Navigation and Safety Behavior
### Slide Content
- Baseline: Nav2 planner/controller with costmap-based obstacle handling
- Safety-marker integration layer (next milestone)
- Proposed zone policy:
  - Caution: controlled speed reduction
  - Danger: controlled stop + replanning
  - Critical: immediate halt + event alert

### Speaker Notes
The navigation core is already operational. The strategic extension is semantic behavior control based on marker proximity. This allows the robot to treat cones and barrels as operational cues rather than generic obstacles, improving policy-level safety decisions.

---

## Slide 7: Model Strategy and Data Plan
### Slide Content
- Current status: dual approaches implemented and runnable
- Classical HSV branch: transparent cone baseline, low compute
- YOLO branch: primary path for cone/barrel learned detection
- Data priorities: occlusion, illumination shift, clutter, scale diversity
- Validation: per-class and per-approach benchmarking

### Speaker Notes
Keeping both branches strengthens technical rigor. The classical method provides a reproducible baseline and interpretable failure analysis. The learned method provides scalability and better generalization. The evaluation plan compares both and positions YOLO as the primary production candidate for full cone-and-barrel scope.

---

## Slide 8: Evaluation Metrics
### Slide Content
- Detection quality: precision, recall, mAP50, mAP50-95
- Runtime: branch-level latency + end-to-end latency + FPS
- Spatial performance: 3D localization error
- Safety performance: hazard-aware avoidance/replan success
- Reliability: false positives, false negatives, and uptime

### Speaker Notes
Accuracy alone does not guarantee safe behavior. We evaluate detection quality, processing speed, and spatial error together, then verify real navigation impact through scenario-based trials. This ensures the system is both technically strong and operationally relevant.

---

## Slide 9: Timeline, Risks, and Mitigation
### Slide Content
- Week 1-2: package hardening and parameterization
- Week 3-4: cone+barrel YOLO retraining and threshold tuning
- Week 5-6: detection-to-behavior Nav2 integration
- Week 7-8: comparative benchmarking and final reporting
- Key risks: sim-to-real shift, false alerts, class confusion, lighting sensitivity

### Speaker Notes
The plan is sequenced to reduce technical risk early. We first stabilize reproducibility and configuration quality, then expand model capability, then connect perception to control. Risk mitigation combines data strategy, threshold tuning, and temporal consistency checks.

---

## Slide 10: Conclusion and Expected Impact
### Slide Content
- End-to-end perception-to-action architecture demonstrated in simulation
- Dual-approach perception increases robustness and benchmarking credibility
- Clear KPI-driven path from prototype to pilot deployment
- Future direction: site trials, semantic costmaps, expanded safety object classes

### Speaker Notes
This project delivers more than object detection; it delivers an autonomy capability aligned with construction safety workflows. By combining spatial perception with navigation logic, the system provides a practical foundation for safer robot operation in dynamic work zones.

---

## Optional Closing Line
This system turns temporary construction markers into real-time, safety-aware navigation decisions.
