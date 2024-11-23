from pycocotools.coco import COCO
import json
import os
import shutil

def merge_coco_json(json_files, output_file):
    merged_annotations = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    image_id_offset = 0
    annotation_id_offset = 0
    category_id_offset = 0
    existing_category_ids = set()

    for idx, file in enumerate(json_files):
        coco = COCO(file)

        # Update image IDs to avoid conflicts
        for image in coco.dataset['images']:
            image['id'] += image_id_offset
            merged_annotations['images'].append(image)

        # Update annotation IDs to avoid conflicts
        for annotation in coco.dataset['annotations']:
            annotation['id'] += annotation_id_offset
            annotation['image_id'] += image_id_offset
            merged_annotations['annotations'].append(annotation)

        # Update categories and their IDs to avoid conflicts
        for category in coco.dataset['categories']:
            if category['id'] not in existing_category_ids:
                category['id'] += category_id_offset
                merged_annotations['categories'].append(category)
                existing_category_ids.add(category['id'])

        image_id_offset = len(merged_annotations['images'])
        annotation_id_offset = len(merged_annotations['annotations'])
        category_id_offset = len(merged_annotations['categories'])

    # Save merged annotations to output file
    with open(output_file, 'w') as f:
        json.dump(merged_annotations, f)


def merge_yolo(datasets, output_dir, taco_indices):
    # Create merged directories
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    image_counter = 0  # To handle file naming conflicts
    dataset_counter = 0

    for dataset in datasets:
        dataset_images = os.path.join(dataset, "images")
        dataset_labels = os.path.join(dataset, "labels")
        
        # Copy images and labels
        for image_file in os.listdir(dataset_images):
            src_image_path = os.path.join(dataset_images, image_file)
            new_image_name = f"{image_counter:06d}.jpg"  # Ensure unique name
            dst_image_path = os.path.join(images_dir, new_image_name)
            shutil.copy(src_image_path, dst_image_path)

            # Modify and copy corresponding label
            label_file = image_file.replace(".jpg", ".txt")
            src_label_path = os.path.join(dataset_labels, label_file)
            dst_label_path = os.path.join(labels_dir, new_image_name.replace(".jpg", ".txt"))
            
            if dataset_counter in taco_indices:
                if os.path.exists(src_label_path):
                    with open(src_label_path, 'r') as src_file, open(dst_label_path, 'w') as dst_file:
                        for line in src_file:
                            parts = line.split()
                            parts[0] = '1'  # Change the class ID to '1' if it's a TACO dataset
                            dst_file.write(" ".join(parts) + "\n")
            else:
                if os.path.exists(src_label_path):
                    with open(src_label_path, 'r') as src_file, open(dst_label_path, 'w') as dst_file:
                        for line in src_file:
                            parts = line.split()
                            parts[0] = '0'  # Change the class ID to '0' if it's a human dataset
                            dst_file.write(" ".join(parts) + "\n")

            image_counter += 1
        print(f"Dataset {dataset} completed, Counter: {dataset_counter}")
        dataset_counter += 1

    print(f"Datasets merged into: {output_dir}")
