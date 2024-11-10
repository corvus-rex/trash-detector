source .env
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Download Roboflow's dataset
roboflow login
bash $SCRIPT_DIR/TACO_TN_UAV/downloader.sh
bash $SCRIPT_DIR/coco_human/downloader.sh
bash $SCRIPT_DIR/people_detection/downloader.sh

python $SCRIPT_DIR/dataset_util/cocosplit.py --having-annotations --multi-class -s 0.7 $SCRIPT_DIR/TACO/data/annotations.json $SCRIPT_DIR/TACO/data/annot_train.json $SCRIPT_DIR/TACO/data/annot_test.json
