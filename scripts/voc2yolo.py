import os
import xml.etree.ElementTree as ET
import shutil
import random

# Configuration
VOC_CLASSES = [
    "aeroplane", "bicycle", "bird", "boat", "bottle", 
    "bus", "car", "cat", "chair", "cow", 
    "diningtable", "dog", "horse", "motorbike", "person", 
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

def convert_box(size, box):
    """
    Convert absolute VOC bounding box (xmin, ymin, xmax, ymax) 
    to YOLO relative bounding box (x_center, y_center, width, height).
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    
    # Calculate center x and y
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    
    # Calculate width and height
    w = box[1] - box[0]
    h = box[3] - box[2]
    
    # Normalize
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(voc_dir, image_id, output_label_path):
    in_file = open(os.path.join(voc_dir, f'Annotations/{image_id}.xml'), 'r', encoding='utf-8')
    out_file = open(output_label_path, 'w', encoding='utf-8')
    
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        
        # Skip difficult objects or classes not in our list
        if cls not in VOC_CLASSES or int(difficult) == 1:
            continue
            
        cls_id = VOC_CLASSES.index(cls)
        xmlbox = obj.find('bndbox')
        
        # VOC is 1-based indexing
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
             
        bb = convert_box((w, h), b)
        out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")
    
    in_file.close()
    out_file.close()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, '..')
    
    voc_dir = os.path.join(base_dir, 'data', 'VOCdevkit', 'VOC2007')
    yolo_dir = os.path.join(base_dir, 'data', 'yolo_format')
    
    if not os.path.exists(voc_dir):
        print(f"Error: {voc_dir} not found. Please run download_voc.py first.")
        return

    # Target directories
    dirs = ['images/train', 'images/val', 'labels/train', 'labels/val']
    for d in dirs:
        os.makedirs(os.path.join(yolo_dir, d), exist_ok=True)
        
    print("Converting VOC to YOLO format...")

    # For 2007, trainval contains train and val indices. 
    # Let's read the main train/val splits from ImageSets
    splits = {'train': 'train.txt', 'val': 'val.txt'}
    
    for split_name, txt_file in splits.items():
        split_txt = os.path.join(voc_dir, 'ImageSets', 'Main', txt_file)
        if not os.path.exists(split_txt):
            print(f"Warning: {split_txt} not found.")
            continue
            
        with open(split_txt, 'r') as f:
            image_ids = [x.strip() for x in f.readlines()]
            
        for image_id in image_ids:
            # Source image
            src_img = os.path.join(voc_dir, f'JPEGImages/{image_id}.jpg')
            if not os.path.exists(src_img):
                continue
                
            # Copy image
            dst_img = os.path.join(yolo_dir, f'images/{split_name}/{image_id}.jpg')
            if not os.path.exists(dst_img):
                shutil.copyfile(src_img, dst_img)
            
            # Convert and write label
            dst_lbl = os.path.join(yolo_dir, f'labels/{split_name}/{image_id}.txt')
            convert_annotation(voc_dir, image_id, dst_lbl)
            
    print(f"Conversion complete! YOLO format dataset saved at: {yolo_dir}")

if __name__ == '__main__':
    main()
