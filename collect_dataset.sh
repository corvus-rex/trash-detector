source .env
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Download Roboflow's dataset
roboflow login
bash $SCRIPT_DIR/TACO_TN_UAV/downloader.sh
bash $SCRIPT_DIR/coco_human/downloader.sh
bash $SCRIPT_DIR/people_detection/downloader.sh

# Download TACO's dataset
python $SCRIPT_DIR/TACO/download.py

# Combine TACO's dataset batches into single directory
python $SCRIPT_DIR/dataset_util/combine_TACO.py $SCRIPT_DIR/TACO/data $SCRIPT_DIR/TACO/data/imgs

# Split the TACO annotation into training and testing 
python $SCRIPT_DIR/dataset_util/cocosplit.py --having-annotations --multi-class -s 0.7 $SCRIPT_DIR/TACO/data/annotations.json $SCRIPT_DIR/TACO/data/annot_train.json $SCRIPT_DIR/TACO/data/annot_test.json

# Convert training data to YOLO format