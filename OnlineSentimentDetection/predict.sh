#!/usr/bin/env bash
# @Author: Zeen Song
# @Date:   2020-4-26
# @Last Modified by:   zeen.song
# @Last Modified time: 2020-4-26

# Do the sentiment prediction for restaurant related comments
if [ $# != 1 ]; then
   echo "usage: predict.sh <task name>"
   echo "e.g.:  predict.sh restaurant"
   exit 1;
fi
TASK_NAME=$1
MODEL_NAME=albert_${TASK_NAME}
CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
export CUDA_VISIBLE_DEVICES="0"

cd models/ALBERT
echo "Start predict..."
python3 predict.py \
  --model_type=albert \
  --model_name_or_path=$CURRENT_DIR/models/albert_${TASK_NAME}/ \
  --task_name=$TASK_NAME \
  --data_dir=$CURRENT_DIR/data/${TASK_NAME}/ \
  --max_seq_length=128 \
  --output_dir=$CURRENT_DIR/data/${TASK_NAME}/ \