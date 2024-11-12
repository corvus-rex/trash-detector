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

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)
    for batch in os.listdir(source_directory):
        if batch.startswith("batch_"):
            batch_path = os.path.join(source_directory, batch)
            
            if os.path.isdir(batch_path):
                batch_number = batch.split("_")[-1]

                for image_file in os.listdir(batch_path):
                    image_path = os.path.join(batch_path, image_file)
                    
                    if os.path.isfile(image_path):
                        new_file_name = f"{batch_number}_{os.path.splitext(image_file)[0]}.jpg"
                        destination_path = os.path.join(destination_directory, new_file_name)

                        shutil.copy(image_path, destination_path)

    print(f"All images have been combined and renamed in the '{destination_directory}' directory.")
