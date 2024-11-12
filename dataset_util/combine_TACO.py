import os
import shutil
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine all images from batch directories into a single directory.")
    parser.add_argument('source_directory', type=str, help="Path to the source directory containing batch folders")
    parser.add_argument('destination_directory', type=str, help="Path to the destination directory for combined images")

    args = parser.parse_args()
    source_directory = args.source_directory
    destination_directory = args.destination_directory

    os.makedirs(destination_directory, exist_ok=True)

    # Iterate over each batch subdirectory
    for batch in os.listdir(source_directory):
        batch_path = os.path.join(source_directory, batch)
        
        # Check if the path is a directory
        if os.path.isdir(batch_path):
            # Iterate over each image in the batch directory
            for image_file in os.listdir(batch_path):
                image_path = os.path.join(batch_path, image_file)
                
                # Ensure the current file is a file (not a subdirectory)
                if os.path.isfile(image_path):
                    # Move the image to the destination directory
                    shutil.move(image_path, os.path.join(destination_directory, image_file))

    print("All images have been combined into the destination directory.")
