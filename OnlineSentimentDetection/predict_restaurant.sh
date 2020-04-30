#!/usr/bin/env bash
# @Author: Zeen Song
# @Date:   2020-4-26
# @Last Modified by:   zeen.song
# @Last Modified time: 2020-4-26

# Do the sentiment prediction for restaurant related comments

TASK_NAME="restaurant"
MODEL_NAME="albert_restaurant"
CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
export CUDA_VISIBLE_DEVICES="0"

cd models
echo "Start predict..."
python3 predict.py \
  --model_type=albert \
  --model_name_or_path=$CURRENT_DIR/ALBERT/albert_${TASK_NAME}/ \
  --task_name=$TASK_NAME \
  --data_dir=$CURRENT_DIR/../data/${TASK_NAME}/ \
  --max_seq_length=128 \
  --output_dir=$CURRENT_DIR/../data/${TASK_NAME}/ \