import json
import os
import shutil
import argparse

def load_images_from_folder(folder, output_path):
    file_names = []
    count = 0

    # Ensure the destination directory exists
    destination_dir = os.path.join(output_path, "images")
    os.makedirs(destination_dir, exist_ok=True)

    for filename in os.listdir(folder):
        source = os.path.join(folder, filename)
        destination = os.path.join(destination_dir, f"img{count}.jpg")

        try:
            shutil.move(source, destination)
        except shutil.SameFileError:
            pass

        file_names.append(filename)
        count += 1

    return file_names


def get_img_ann(image_id, data):
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        return None

def get_img(filename, data):
    for img in data['images']:
        if img['file_name'] == filename:
            return img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change COCO json format to YOLO yormat")
    parser.add_argument('input_path', type=str, help="Path to the source directory containing the image dataset")
    parser.add_argument('output_path', type=str, help="Path to the target directory containing the output YOLO dataset")
    parser.add_argument('annotation_file', type=str, help="Name of the file containing COCO annotation")

    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    annotation_file = args.annotation_file
    
    f = open(annotation_file)
    data = json.load(f)
    f.close()
    
    files = load_images_from_folder(input_path, output_path)

    count = 0

    labels_dir = os.path.join(output_path, "labels")
    os.makedirs(labels_dir, exist_ok=True)
    for filename in files:
        # Extracting image 
        img = get_img(filename, data)
        if img == None:
            continue
        img_id = img['id']
        img_w = img['width']
        img_h = img['height']

        # Get Annotations for this image
        img_ann = get_img_ann(img_id, data)

        if img_ann:
            file_object = open(os.path.join(labels_dir, f"img{count}.txt"), "a")

            for ann in img_ann:
                current_category = ann['category_id'] - 1 # As yolo format labels start from 0 
                current_bbox = ann['bbox']
                x = current_bbox[0]
                y = current_bbox[1]
                w = current_bbox[2]
                h = current_bbox[3]
                
                # Finding midpoints
                x_centre = (x + (x+w))/2
                y_centre = (y + (y+h))/2
                
                # Normalization
                x_centre = x_centre / img_w
                y_centre = y_centre / img_h
                w = w / img_w
                h = h / img_h
                
                # Limiting upto fix number of decimal places
                x_centre = format(x_centre, '.6f')
                y_centre = format(y_centre, '.6f')
                w = format(w, '.6f')
                h = format(h, '.6f')
                    
                # Writing current object 
                file_object.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")

            file_object.close()
            count += 1
