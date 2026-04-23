# Executive Proposal

## Project Title
Vision-Guided Autonomous Safety Robot for Construction Cone and Barrel Awareness

## Problem Statement
Construction cone and barrel detection on construction sites.

## Executive Summary
This project proposes a ROS2-based autonomous safety robot that perceives temporary construction markers and converts those observations into actionable navigation intelligence. The system is implemented in Gazebo simulation and combines SLAM, localization, path planning, and perception. A key technical strength is the use of two complementary perception approaches: a classical HSV-based cone detector for lightweight baseline performance and a YOLOv8-based detector/localizer for scalable learned perception.

Current implementation demonstrates:
1. Autonomous mapping and localization pipeline (SLAM Toolbox + AMCL + Nav2 integration).
2. Classical cone detection using HSV masking, morphology, contour checks, and structural validation.
3. Learned detection workflow using YOLO-based inference.
4. Depth-assisted 3D localization of detections using camera intrinsics.

The next milestone is full cone-and-barrel operational integration with behavior-level responses such as controlled slowdown, stop, and reroute.

## Business Need and Strategic Value
Construction zones are dynamic environments where temporary markers are frequently repositioned. Static maps cannot capture these short-cycle changes, creating a safety gap for autonomous operation.

Expected value for site operations:
1. Faster hazard recognition in changing work zones.
2. Reduced risk of unsafe robot motion near workers and active equipment.
3. Better compliance traceability through event logging.
4. Data-driven safety monitoring for supervisors and project managers.

## Project Objectives
1. Detect cones and barrels in real time from onboard perception streams.
2. Estimate object positions in metric 3D coordinates.
3. Feed perception outputs into navigation decision-making.
4. Trigger risk-aware behavior policies near marked hazards.
5. Produce measurable KPIs for technical and operational validation.

## Technical Scope
### In Scope
1. Simulation-first validation in Gazebo construction scenarios.
2. Classical HSV pipeline for cone-focused baseline detection.
3. YOLO pipeline for learned object detection and future multi-class expansion.
4. 3D localization from depth + intrinsics projection.
5. Integration path from detection outputs to Nav2 behavior control.
6. End-to-end benchmarking and reporting.

### Out of Scope (Current Phase)
1. Production-grade field deployment on live sites.
2. Multi-robot orchestration and fleet-level coordination.
3. Regulatory certification and formal safety compliance audits.

## Current System Capabilities (Implemented)
1. Full autonomous stack in ROS2 Humble with SLAM, localization, and Nav2 planning.
2. Differential-drive robot model with LiDAR and RGB-D sensing in Gazebo.
3. Classical detector node publishing annotated output and 3D cone positions.
4. YOLO visualization node for learned perception output.
5. YOLO + depth localization node publishing 3D cone positions.
6. Construction-themed world assets with cone/barrel obstacles for evaluation.

## Architecture Overview
1. RGB, depth, and camera intrinsic data are subscribed from ROS topics.
2. Classical branch performs HSV segmentation, denoising, contour extraction, and shape-based filtering.
3. Learned branch performs YOLO inference and confidence-based detection.
4. Accepted detections are mapped from image coordinates to 3D camera-frame points.
5. Detection outputs are published for visualization, logging, and downstream planning logic.
6. Navigation policy layer (next phase) consumes hazard points to enforce safe motion behavior.

## KPI Framework
1. Detection quality: precision, recall, mAP50, mAP50-95 (class-wise and approach-wise).
2. Runtime performance: inference latency, end-to-end latency, throughput (FPS).
3. Spatial quality: mean and percentile 3D localization error.
4. Safety impact: hazard-aware reroute/avoidance success rate.
5. Reliability: false positives, false negatives, and node uptime.

Recommended acceptance targets:
1. Cone precision >= 0.90 across validation scenarios.
2. Barrel precision >= 0.90 after two-class YOLO retraining.
3. End-to-end perception latency < 100 ms on target runtime hardware.
4. Localization error <= 0.30 m in defined operating range.
5. Hazard-aware navigation success >= 95% in benchmark scenarios.

## Delivery Roadmap
### Phase 1: Technical Hardening (Week 1-2)
1. Finalize package metadata and dependency declaration.
2. Remove hardcoded paths through ROS parameters.
3. Standardize launch and run workflows for reproducibility.

### Phase 2: Barrel Expansion (Week 3-4)
1. Build balanced cone+barrel dataset.
2. Retrain YOLO with two-class target schema.
3. Tune thresholds and validate with confusion matrix analysis.

### Phase 3: Behavior Coupling (Week 5-6)
1. Convert object detections into semantic hazard zones.
2. Integrate zone policy with Nav2 behavior control.
3. Validate stop/slow/reroute behavior under dynamic conditions.

### Phase 4: Verification and Reporting (Week 7-8)
1. Run comparative trials (classical vs learned branch).
2. Compile KPI dashboards and scenario-level findings.
3. Package final presentation, report, and demonstration script.

## Risks and Mitigation Strategy
1. Simulation-to-real transfer gap.
   Mitigation: domain randomization and real-data fine-tuning.
2. Lighting sensitivity in classical HSV branch.
   Mitigation: adaptive thresholds and fallback to learned branch.
3. Multi-class confusion in cluttered scenes.
   Mitigation: class-balanced training and hard-negative mining.
4. False alarms affecting operational flow.
   Mitigation: temporal filtering and confidence hysteresis.
5. Deployment fragility from environment-specific paths.
   Mitigation: launch-configurable model/topic parameters.

## Planned Deliverables
1. Professional baseline benchmark for classical HSV cone detection.
2. Two-class YOLO model pipeline aligned to cone/barrel objectives.
3. Parameterized ROS2 perception nodes with clean launch integration.
4. Hazard-aware behavior integration design and validation report.
5. Executive presentation package and academic report package.

## Presentation Structure (Recommended)
1. Problem context and safety motivation.
2. System architecture and implementation maturity.
3. Dual-approach perception design rationale.
4. KPI methodology and validation strategy.
5. Risks, roadmap, and deployment pathway.
6. Business and safety impact.

## Report Structure (Recommended)
1. Abstract and introduction.
2. Problem framing and objectives.
3. Architecture and methodology.
4. Experimental design and metrics.
5. Results and comparative analysis.
6. Limitations, risks, and future work.
7. Conclusion and deployment outlook.