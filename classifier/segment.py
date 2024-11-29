import cv2
import math
import os

def find_overlapping_regions(src_label_path, max_dist=200):
    overlap = {}
    with open(src_label_path, 'r') as file:
        src_file = [line.strip() for line in file]
        for i in range(len(src_file)):
            parts = src_file[i].split()
            if parts[0] == '1':
                for j in range(len(src_file)):
                    intersect = False
                    if src_file[j].split()[0] == '0':
                        intersect = is_intersect(src_file[i].split(), 
                                    src_file[j].split(), max_dist)
                    if intersect:
                        if i in overlap.keys():
                            overlap[i].append(j)
                        else:
                            overlap[i] = [j]
    return overlap


def is_intersect(bbox1, bbox2, max_dist):
    x_radius1 = (float(bbox1[3]) / 2) + max_dist
    y_radius1 = (float(bbox1[4]) / 2) + max_dist
    x_max1 = float(bbox1[1]) + x_radius1
    x_min1 = float(bbox1[1]) - x_radius1
    y_max1 = float(bbox1[2]) - y_radius1
    y_min1 = float(bbox1[2]) + y_radius1
    
    x_radius2 = (float(bbox2[3]) / 2)
    y_radius2 = (float(bbox2[4]) / 2)
    x_max2 = float(bbox2[1]) + x_radius2
    x_min2 = float(bbox2[1]) - x_radius2
    y_max2 = float(bbox2[2]) - y_radius2
    y_min2 = float(bbox2[2]) + y_radius2

    intersect =  not (x_max1 <= x_min2 or x_max2 <= x_min1 or
                y_max1 <= y_min2 or y_max2 <= y_min1)
    print(intersect)
    return intersect

def crop_regions(image_path, region_dict, label_file, index, output_dir):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    idx = 0
    regions = []
    out = None
    for trash, people in region_dict.items():
        min_x = math.inf
        max_x = 0
        min_y = math.inf
        max_y = 0
        objs = []
        objs.append(trash)
        objs.extend(people)
        for obj in objs: 
            bbox = label_file[obj].split()
            obj_x_radius = (float(bbox[3]) / 2)
            obj_y_radius = (float(bbox[4]) / 2)
            centroid_x = float(bbox[1]) * width
            centroid_y = (1 - (float(bbox[2]))) * height
            min_x_cdt = centroid_x - obj_x_radius
            max_x_cdt = centroid_x + obj_x_radius
            min_y_cdt = centroid_y - obj_y_radius
            max_y_cdt = centroid_y + obj_y_radius
            if min_x_cdt < min_x:
                min_x = min_x_cdt
            if min_y_cdt < min_y:
                min_y = min_y_cdt
            if max_x_cdt > max_x:
                max_x = max_x_cdt
            if max_y_cdt > max_y:
                max_y = max_y_cdt
        regions.append((min_x, max_x, min_y, max_y))
        cropped = img[min_y:max_y, min_x:max_x]
        out = os.path.join(output_dir, f"result_{index}_{idx}.jpg")
        cv2.imwrite(out, cropped)
    print(f"Cropped image {image_path} and saved result to {out}")
    return regions

