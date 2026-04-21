# YOLOv8n vs YOLOv8s Comparison Summary

## Experimental Setup

Both models use the Pascal VOC 2007 dataset converted to YOLO format, with imgsz=640, batch=16, and epochs=50. YOLOv8n is treated as the baseline model, while YOLOv8s is the larger comparison model trained for this project.

## Metric Comparison

| Model | Role | Epochs | Batch | Precision | Recall | mAP50 | mAP50-95 | Result CSV |
|---|---|---:|---:|---:|---:|---:|---:|---|
| YOLOv8n | Baseline | 50 | 16 | 0.78427 | 0.67406 | 0.75183 | 0.53150 | models/baseline/runs/detect/train8/results.csv |
| YOLOv8s | Comparison model | 50 | 16 | 0.78708 | 0.70484 | 0.77526 | 0.56279 | models/YOLOv8s/results.csv |

## Difference: YOLOv8s - YOLOv8n

| Metric | Absolute Difference | Relative Change |
|---|---:|---:|
| Precision | +0.00281 | small increase |
| Recall | +0.03078 | +4.57% |
| mAP50 | +0.02343 | +3.12% |
| mAP50-95 | +0.03129 | +5.89% |

## Notes

- YOLOv8s achieved higher recall, mAP50, and mAP50-95 than YOLOv8n under the same dataset, image size, batch size, and target epoch count.
- The improvement in mAP50-95 suggests YOLOv8s provides better localization quality across stricter IoU thresholds, not only better loose-threshold detection.
- YOLOv8s is a larger model than YOLOv8n, so the accuracy gain is expected to come with higher model complexity and greater GPU memory demand.
- Training time should not be used as a direct speed comparison in this table, because the YOLOv8s run used a strict resume/cooling strategy on the local laptop GPU, while the YOLOv8n baseline was produced under a different execution condition.
- For final reporting, use accuracy metrics as the main comparison and describe runtime only with this hardware-condition caveat.

## Key File Locations

| Content | Path |
|---|---|
| YOLOv8n baseline results | models/baseline/runs/detect/train8/results.csv |
| YOLOv8s model results | models/YOLOv8s/results.csv |
| YOLOv8s best weight | models/YOLOv8s/weights/best.pt |
| YOLOv8s result figures | results/YOLOv8s/ |
| Comparison CSV | results/comparison/YOLOv8n_vs_YOLOv8s_metrics.csv |
