# 10-Slide Presentation Script with Speaker Notes

## Slide 1: Title and Problem Statement
### Slide Content
- CV Mini Project: Cone and Barrel Detection for Construction Safety
- Problem statement: robust real-time marker detection under dynamic scene conditions
- CV focus: classical vision (HSV) vs deep learning (YOLOv8) + depth-based localization

### Speaker Notes
This is our Computer Vision mini project focused on detecting construction cones and barrels in realistic, changing environments. We frame the work as a CV comparison study with deployment context: a classical HSV pipeline versus a YOLOv8 learned detector, both connected to depth-assisted spatial estimation.

---

## Slide 2: CV Problem Framing
### Slide Content
- Domain challenges:
  - illumination variation and shadows
  - partial occlusion and clutter
  - scale variation with distance
  - similar-colored distractors
- Requirement: high recall with controlled false positives

### Speaker Notes
From a CV perspective, this is a difficult detection task because scenes are unconstrained. Lighting, background texture, and object scale continuously change. Our design objective is to sustain robust detection quality while keeping inference fast enough for real-time robotics.

---

## Slide 3: Project Objectives (CV-Centric)
### Slide Content
- Build and evaluate two CV pipelines on the same input stream
- Compare interpretability, robustness, and runtime cost
- Produce 2D detections and 3D object positions
- Quantify quality with precision, recall, mAP, and error analysis
- Identify failure modes and mitigation strategy

### Speaker Notes
The project is not only about obtaining boxes on images; it is about measurable CV performance under realistic constraints. We evaluate both a handcrafted and a learned approach, then analyze where each method succeeds or fails.

---

## Slide 4: Input Data and Perception Architecture
### Slide Content
- Input topics:
  - RGB image stream
  - aligned depth image stream
  - camera intrinsics from camera info
- Dual perception branches:
  - Classical HSV-based cone detector
  - YOLOv8 learned detector/localizer
- Common output: annotated image + 3D point estimates

### Speaker Notes
Both branches consume the same RGB-D sensing stack so the comparison is fair. The architecture allows us to isolate CV behavior and evaluate method-specific performance without changing upstream sensing.

---

## Slide 5: Classical CV Pipeline (HSV)
### Slide Content
1. Convert RGB to HSV color space
2. Threshold orange range for cone candidate mask
3. Morphology: open, dilate, close to suppress noise and merge regions
4. Contour extraction + geometric filtering (area, solidity, aspect ratio)
5. Structural validation (dark-base and upper/lower orange distribution checks)
6. Depth lookup at detection center and 3D back-projection

### Speaker Notes
This branch is highly interpretable. Every decision can be traced to thresholding and shape heuristics, which is useful for debugging and baseline benchmarking. The tradeoff is sensitivity to illumination and scene color variation.

---

## Slide 6: Learned CV Pipeline (YOLOv8)
### Slide Content
- Model: custom YOLOv8n weights
- Inference on RGB frames with confidence-based detections
- Bounding boxes used for visualization and center-point extraction
- Depth-assisted 3D localization from each accepted box
- Scalable path to multi-class detection (cone + barrel)

### Speaker Notes
The YOLO branch is the primary path for robust, scalable detection. Compared to handcrafted logic, it handles more appearance variability and is better suited for cone-and-barrel multi-class targets. We then attach the same depth-based projection stage for 3D localization.

---

## Slide 7: 3D Localization Formulation
### Slide Content
- From 2D pixel to 3D camera coordinates using intrinsics
- Inputs: pixel center $(u, v)$, depth $Z$, intrinsics $(f_x, f_y, c_x, c_y)$
- Equations:
  - $X = \frac{(u-c_x)Z}{f_x}$
  - $Y = \frac{(v-c_y)Z}{f_y}$
  - $Z = Z$
- Output: metric 3D point for downstream reasoning

### Speaker Notes
This stage converts detection from image space to actionable spatial information. It is a key CV contribution of the project because it bridges perception and geometric understanding.

---

## Slide 8: CV Evaluation and Benchmarking
### Slide Content
- Detection metrics:
  - precision, recall, mAP50, mAP50-95
  - per-class and per-approach reporting
- Runtime metrics:
  - branch latency and FPS
- Spatial metrics:
  - 3D localization error versus distance
- Error analysis:
  - false positives, false negatives, confusion trends

### Speaker Notes
We evaluate not only overall scores but also failure behavior. That includes where and why each branch fails, such as lighting extremes or clutter, and how those errors affect practical usability.

---

## Slide 9: Comparative Findings and CV Tradeoffs
### Slide Content
- Classical HSV branch:
  - strengths: fast, transparent, low compute
  - limitations: lighting sensitivity, color distractors
- YOLO branch:
  - strengths: stronger generalization, multi-class scalability
  - limitations: data dependence, training effort
- Decision: retain both; prioritize YOLO for cone+barrel expansion

### Speaker Notes
This comparison is central to the mini project. We use the classical method as a baseline and interpretability reference, while YOLO is the forward path for robust multi-class detection.

---

## Slide 10: Conclusion (CV Mini Project Outcomes)
### Slide Content
- Demonstrated two CV approaches on the same robotics task
- Delivered 2D detection + 3D localization pipeline
- Established metric-driven evaluation framework
- Future CV work:
  - two-class retraining and calibration
  - temporal tracking
  - domain adaptation for real-site deployment

### Speaker Notes
Our key contribution as a CV mini project is a comparative, end-to-end perception framework with geometric localization. It is technically grounded, measurable, and directly extensible to stronger real-world detection performance.

---

## Optional Closing Line
This CV project transforms raw RGB-D input into reliable, spatially grounded construction-marker intelligence.
