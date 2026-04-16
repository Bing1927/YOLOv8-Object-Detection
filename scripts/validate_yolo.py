import os
import random
try:
    import cv2
except ImportError:
    print("Warning: cv2 is not installed. Please install opencv-python to run this script.")
    exit(1)

VOC_CLASSES = [
    "aeroplane", "bicycle", "bird", "boat", "bottle", 
    "bus", "car", "cat", "chair", "cow", 
    "diningtable", "dog", "horse", "motorbike", "person", 
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

def draw_yolo_boxes(image_path, label_path):
    import numpy as np
    # Read image (handles Unicode paths)
    img_data = np.fromfile(image_path, dtype=np.uint8)
    img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Could not read {image_path}")
        return None
        
    h, w, _ = img.shape
    
    # Read labels
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Label file not found: {label_path}")
        return img
        
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
            
        cls_id = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        box_w = float(parts[3])
        box_h = float(parts[4])
        
        # Convert relative YOLO back to absolute coordinates
        x1 = int((x_center - box_w / 2) * w)
        y1 = int((y_center - box_h / 2) * h)
        x2 = int((x_center + box_w / 2) * w)
        y2 = int((y_center + box_h / 2) * h)
        
        # Draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 边界防溢出判断（如果 y1 太靠上，就把文字写在框里面，否则写在框上面）
        text_y = y1 - 10 if y1 > 20 else y1 + 25 
        
        # Draw label
        cls_name = VOC_CLASSES[cls_id]
        cv2.putText(img, cls_name, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    return img

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, '..')
    val_images_dir = os.path.join(base_dir, 'data', 'yolo_format', 'images', 'val')
    val_labels_dir = os.path.join(base_dir, 'data', 'yolo_format', 'labels', 'val')
    
    if not os.path.exists(val_images_dir):
        print(f"Validation images directory not found: {val_images_dir}")
        return
        
    images = [f for f in os.listdir(val_images_dir) if f.endswith('.jpg')]
    if not images:
        print("No images found in validation set.")
        return
        
    print(f"Found {len(images)} images in validation set. Visualizing a random sample...")
    
    # Select 5 random images
    samples = random.sample(images, min(5, len(images)))
    
    output_dir = os.path.join(base_dir, 'results', 'validation_samples')
    os.makedirs(output_dir, exist_ok=True)
    
    for img_name in samples:
        img_path = os.path.join(val_images_dir, img_name)
        txt_name = img_name.replace('.jpg', '.txt')
        lbl_path = os.path.join(val_labels_dir, txt_name)
        
        img_with_boxes = draw_yolo_boxes(img_path, lbl_path)
        if img_with_boxes is not None:
            out_path = os.path.join(output_dir, img_name)
            import numpy as np
            _, img_encode = cv2.imencode('.jpg', img_with_boxes)
            img_encode.tofile(out_path)
            print(f"Saved validation sample: {out_path}")

if __name__ == '__main__':
    main()
