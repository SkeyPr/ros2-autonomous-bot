# Viva-Ready Q&A Bank

## Section A: Fundamental Questions

### Q1. What is the core problem your project solves?
Answer:
The project addresses real-time construction marker awareness in dynamic work zones. Specifically, it detects cones and barrels, estimates their spatial position, and provides a pathway to convert those detections into navigation-safe robot behavior beyond static-map assumptions.

### Q2. Why are cones and barrels important in construction robotics?
Answer:
They represent temporary safety boundaries and work-zone indicators. Ignoring them can cause unsafe path planning, worker risk, and non-compliant robot operation.

### Q3. Why did you use ROS2?
Answer:
ROS2 provides modular node-based architecture, robust communication middleware, simulation compatibility, and a mature ecosystem for SLAM, navigation, and perception integration.

### Q4. Why YOLOv8 for detection?
Answer:
YOLOv8 provides a strong speed-accuracy tradeoff for real-time robotics. It is practical to train, efficient to deploy, and well suited for scaling from single-class to multi-class detection under changing scene conditions.

### Q5. Why include depth in addition to RGB detection?
Answer:
RGB provides object class and image coordinates, while depth enables metric localization in 3D space. Navigation and safety policies require physically meaningful distances, not only pixel-level detections.

### Q5A. Do you have one or two detection approaches in your system?
Answer:
The current codebase contains two approaches. The first is a classical HSV-based cone detector with morphology, contour filtering, and structural validation. The second is a YOLO-based learned detector/localizer, which is the primary path for scalable multi-class detection, including cone and barrel classes.

## Section B: Architecture and Method

### Q6. Explain your pipeline from sensor to action.
Answer:
RGB, depth, and camera-intrinsic streams are subscribed in ROS2. Perception runs through either the classical HSV branch or the YOLO branch. For accepted detections, center-point depth is sampled and back-projected to metric XYZ coordinates. These 3D outputs are published for visualization and planning integration, with behavior-level stop/slow/reroute policies defined as the next integration stage.

### Q7. How do you compute 3D coordinates from image pixels?
Answer:
For pixel \((u,v)\) and depth \(Z\), using intrinsics \((f_x, f_y, c_x, c_y)\):
\(X = (u-c_x)Z/f_x\), \(Y = (v-c_y)Z/f_y\), \(Z = Z\).
This maps camera image points into camera-frame metric coordinates.

### Q8. What role does Nav2 play?
Answer:
Nav2 provides the core autonomy framework for global planning, local control, and behavior orchestration. In this project, it forms the control backbone onto which detection-derived hazard logic is integrated.

### Q9. How does SLAM/localization relate to your detection task?
Answer:
SLAM and localization provide global robot pose and map context. Detection adds dynamic semantic context. Together, they support safer navigation in changing environments.

### Q10. Why simulation-first development?
Answer:
Simulation enables rapid prototyping, controlled scenario creation, repeatability, lower cost, and safer early-stage testing before hardware deployment.

### Q10A. Why keep both HSV and YOLO instead of only one?
Answer:
They serve complementary engineering goals. HSV is computationally lightweight, explainable, and useful as a controlled baseline for cone detection. YOLO is more robust in complex scenes and is the main path for scalable cone-and-barrel perception. Maintaining both supports rigorous benchmarking and practical fallback strategies.

## Section C: Evaluation and Results

### Q11. Which metrics did you use and why?
Answer:
Perception metrics: precision, recall, mAP50, mAP50-95 to quantify class-wise detection quality.
Runtime metrics: branch-level and end-to-end latency with FPS for real-time feasibility.
Localization metrics: 3D position error to evaluate spatial accuracy.
Navigation metrics: hazard-avoidance and reroute success to measure safety impact.

### Q12. How do you validate that detection improves navigation safety?
Answer:
By comparing baseline navigation against hazard-aware navigation in identical scenarios and measuring near-collision events, successful reroutes, emergency stops, and goal completion rates.

### Q13. What are your expected acceptance thresholds?
Answer:
Target thresholds are cone precision >= 0.90, barrel precision >= 0.90 after two-class retraining, end-to-end latency under 100 ms, localization error <= 0.30 m in working range, and >= 95% hazard-aware navigation success in benchmark scenarios.

### Q14. What if precision is high but recall is low?
Answer:
Low recall means missed hazards, which is risky in safety applications. I would prioritize recall improvements through dataset expansion, class balancing, and threshold tuning, while controlling false positives with temporal filtering.

### Q15. How do you handle false positives?
Answer:
I use threshold calibration, temporal consistency filtering across frames, and context-aware plausibility checks. The goal is to reduce unnecessary stops without sacrificing hazard recall.

## Section D: Design Choices and Trade-Offs

### Q16. Why not use LiDAR-only object detection?
Answer:
LiDAR provides geometry but weak class semantics for cones versus barrels in many setups. Camera-based detection provides stronger class discrimination, while LiDAR/depth adds spatial context.

### Q17. Why not use a heavier model for higher accuracy?
Answer:
Heavier models may improve accuracy but can violate real-time constraints. In mobile robotics, response latency is critical. YOLOv8n-class models are a practical balance.

### Q17A. When would you prefer HSV over YOLO at runtime?
Answer:
HSV is preferable when compute is constrained and the task is strictly cone-focused under controlled lighting. In heterogeneous scenes, variable illumination, or multi-class objectives, YOLO is generally the better operational choice.

### Q18. Why use center-pixel depth instead of full mask depth?
Answer:
Center-depth is computationally simple and fast for real-time prototypes. For improved robustness, future work can use depth median over a valid-pixel region or instance segmentation.

### Q19. What are the biggest failure modes?
Answer:
Major failure modes include occlusion, severe illumination shifts, depth noise at reflective or distant surfaces, class confusion in cluttered regions, and simulation-to-real visual domain mismatch.

### Q20. How would you improve robustness?
Answer:
I would expand real-world data coverage, apply stronger domain randomization, add temporal multi-object tracking, incorporate uncertainty-aware filtering, and enforce cross-sensor consistency checks.

## Section E: Deployment and Future Scope

### Q21. What is needed to move from simulation to real deployment?
Answer:
Camera-depth calibration, hardware timing validation, on-device benchmarking, field-data fine-tuning, and safety policy validation under operational constraints.

### Q22. How does this project contribute academically?
Answer:
It demonstrates an integrated perception-to-action framework for dynamic hazard markers and provides a reproducible KPI-driven methodology for evaluating safety-aware autonomous behavior.

### Q23. What is novel in your implementation?
Answer:
The novelty lies in integration quality rather than isolated algorithm invention: dual-approach perception, metric localization, and navigation-ready safety semantics are combined into one coherent construction-safety robotics pipeline.

### Q24. What would you do with 3 more months?
Answer:
I would run real-site pilots, add temporal multi-object tracking, implement semantic costmap layers, and perform comparative studies across model sizes and planning strategies.

### Q25. If asked to summarize your project in one sentence?
Answer:
This project enables an autonomous robot to see construction cones and barrels, understand where they are in 3D space, and navigate more safely because of that understanding.

## Quick Defense Tips
1. Always connect technical decisions to safety and real-time constraints.
2. Explain trade-offs openly: speed vs accuracy, recall vs false positives.
3. Use metric evidence whenever possible.
4. Acknowledge limitations and present concrete mitigation plans.
5. Distinguish clearly between what is implemented now and what is roadmap work.
6. End answers with deployment relevance and measurable impact.
