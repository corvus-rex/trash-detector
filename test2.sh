source .env
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Convert COCO training data to YOLO format
# python $SCRIPT_DIR/dataset_util/coco2yolo.py $SCRIPT_DIR/TACO/data/imgs $SCRIPT_DIR/TACO/data/yolo_imgs $SCRIPT_DIR/TACO/data/imgs/annot_train.json

roboflow download -f yolov11 -l $SCRIPT_DIR/taco/data divya-lzcld/taco-mqclx