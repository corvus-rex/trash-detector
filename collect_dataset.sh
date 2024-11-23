source .env
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Download Roboflow's dataset
roboflow login
roboflow download -f yolov11 -l $SCRIPT_DIR/TACO_TN_UAV trash-recognition-fixed/taco_tn_uav
roboflow download -f yolov11 -l $SCRIPT_DIR/coco_human/data shreks-swamp/coco-dataset-limited--person-only
roboflow download -f yolov11 -l $SCRIPT_DIR/people_detection/data leo-ueno/people-detection-o4rdr

# Download TACO's dataset
python $SCRIPT_DIR/TACO/download.py

# Combine TACO's dataset batches into single directory
python $SCRIPT_DIR/dataset_util/combine_TACO.py $SCRIPT_DIR/TACO/data $SCRIPT_DIR/TACO/data/imgs

# Remove any reference to 'batch_' within the directory
python $SCRIPT_DIR/dataset_util/clean_annot.py $SCRIPT_DIR/TACO/data/annotations.json $SCRIPT_DIR/TACO/data/annotations.json

# Split the TACO annotation into training and testing 
python $SCRIPT_DIR/dataset_util/cocosplit.py --having-annotations --multi-class -s 0.7 $SCRIPT_DIR/TACO/data/annotations.json $SCRIPT_DIR/TACO/data/imgs/annot_train.json $SCRIPT_DIR/TACO/data/imgs/annot_test.json

# Convert COCO training data to YOLO format
python $SCRIPT_DIR/dataset_util/coco2yolo.py $SCRIPT_DIR/TACO_TN_UAV/data/train $SCRIPT_DIR/TACO_TN_UAV/data/yolo_train $SCRIPT_DIR/TACO_TN_UAV/data/train/_annotations.coco.json
python $SCRIPT_DIR/dataset_util/coco2yolo.py $SCRIPT_DIR/coco_human/data/train $SCRIPT_DIR/coco_human/data/yolo_train $SCRIPT_DIR/coco_human/data/train/_annotations.coco.json
python $SCRIPT_DIR/dataset_util/coco2yolo.py $SCRIPT_DIR/people_detection/data/train $SCRIPT_DIR/people_detection/data/yolo_train $SCRIPT_DIR/people_detection/data/train/_annotations.coco.json
python $SCRIPT_DIR/dataset_util/coco2yolo.py $SCRIPT_DIR/TACO/data/imgs $SCRIPT_DIR/TACO/data/yolo_imgs $SCRIPT_DIR/TACO/data/annot_train.json
