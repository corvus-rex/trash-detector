from . import segment
import csv
import math
import os

def extract_global_features(label_gt_dir, label_yolo_dir, csv_file):
    if os.path.isfile(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]  # Each row is a dictionary

        current_label_gt = ''
        gt_x = 0
        gt_y = 0
        gt_w = 0
        gt_h = 0
        gt_class = 0

        current_label_yolo = ''
        person_x = 0
        person_y = 0
        person_w = 0
        person_h = 0

        for el in data:
            obj_num = int(el['unproc_person_id'].replace(".jpg", ""))
            if el['file_name'] != current_label_gt:
                current_label_gt = os.path.join(label_gt_dir, el['file_name'].replace(".jpg", ".txt"))
                with open(current_label_gt, mode='r') as label_file:
                    lines_gt = [line.strip() for line in label_file]
                    if len(lines_gt) > 0:
                        parts = lines_gt[0].split()
                        gt_x = parts[1]
                        gt_y = parts[2]
                        gt_w = parts[3]
                        gt_h = parts[4]
                        gt_class = parts[0]
                    else: 
                        gt_x = None
                        gt_y = None
                        gt_w = None
                        gt_h = None
                        gt_class = None
            if el['file_name'] != current_label_yolo:
                current_label_yolo = os.path.join(label_yolo_dir, el['file_name'].replace(".jpg", ".txt"))
                with open(current_label_yolo, mode='r') as bbox_file:
                    lines_bbox = [line.strip() for line in bbox_file]
            
            parts_bbox = lines_bbox[obj_num].split()
            person_x = float(parts_bbox[1])
            person_y = float(parts_bbox[2])
            person_w = float(parts_bbox[3])
            person_h = float(parts_bbox[4])

            nearest_trash_x = None
            nearest_trash_y = None
            nearest_trash_w = None
            nearest_trash_h = None

            dist = math.inf
            for line_bbox in lines_bbox:
                if line_bbox.split()[0] == '1':
                    dist_temp = math.sqrt((float(line_bbox.split()[1]) - person_x)**2 + (float(line_bbox.split()[2]) - person_y)**2)
                    if dist_temp < dist:
                        nearest_trash_x = float(line_bbox.split()[1])
                        nearest_trash_y = float(line_bbox.split()[2])
                        nearest_trash_w = float(line_bbox.split()[3])
                        nearest_trash_h = float(line_bbox.split()[4])
                        dist = dist_temp

            el['gt_x'] = gt_x
            el['gt_y'] = gt_y
            el['gt_w'] = gt_w
            el['gt_h'] = gt_h
            el['gt_class'] = gt_class

            el['person_x'] = person_x
            el['person_y'] = person_y
            el['person_w'] = person_w
            el['person_h'] = person_h

            el['nearest_trash_x'] = nearest_trash_x
            el['nearest_trash_y'] = nearest_trash_y
            el['nearest_trash_w'] = nearest_trash_w
            el['nearest_trash_h'] = nearest_trash_h
        
        if (len(data) > 0):
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
