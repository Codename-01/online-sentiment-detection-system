# -*- coding: utf-8 -*-
# @Author: Zeen Song
# @Date:   2020-04-26
# @Last Modified by:   zeen.song
# @Last Modified time: 2020-04-26
from __future__ import absolute_import, division, print_function

import argparse
import os
import torch
from .transformers import (WEIGHTS_NAME, BertConfig,
                          BertForSequenceClassification, BertTokenizer,
                          RobertaConfig, XLNetConfig,
                          XLNetForSequenceClassification,
                          XLNetTokenizer,
                          AlbertForSequenceClassification)

from .processors import clue_output_modes as output_modes
from .processors import clue_processors as processors
from .run_classifier import predict

ALL_MODELS = sum((tuple(conf.pretrained_config_archive_map.keys()) for conf in (BertConfig, XLNetConfig,
                                                                                RobertaConfig)), ())
MODEL_CLASSES = {
    ## bert ernie bert_wwm bert_wwwm_ext
    'bert': (BertConfig, BertForSequenceClassification, BertTokenizer),
    'xlnet': (XLNetConfig, XLNetForSequenceClassification, XLNetTokenizer),
    'roberta': (BertConfig, BertForSequenceClassification, BertTokenizer),
    'albert': (BertConfig, AlbertForSequenceClassification, BertTokenizer)
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parse required argument
    parser.add_argument("--data_dir", default=None, type=str, required=True,
                        help="The input data dir. Should contain the .tsv files (or other data files) for the task.")
    parser.add_argument("--model_type", default=None, type=str, required=True,
                        help="Model type selected in the list: " + ", ".join(MODEL_CLASSES.keys()))
    parser.add_argument("--task_name", default=None, type=str, required=True,
                        help="The name of the task to train selected in the list: " + ", ".join(processors.keys()))
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--model_name_or_path", default=None, type=str, required=True,
                        help="Path to pre-trained model or shortcut name selected in the list: " + ", ".join(
                            ALL_MODELS))
    # parse other argument
    parser.add_argument("--local_rank", type=int, default=-1,
                        help="For distributed training: local_rank")
    parser.add_argument("--max_seq_length", default=128, type=int,
                        help="The maximum total input sequence length after tokenization. Sequences longer "
                             "than this will be truncated, sequences shorter will be padded.")
    args = parser.parse_args()

    if args.local_rank == -1:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        args.n_gpu = torch.cuda.device_count()
    else:  # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
        torch.cuda.set_device(args.local_rank)
        device = torch.device("cuda", args.local_rank)
        torch.distributed.init_process_group(backend='nccl')
        args.n_gpu = 1
    args.device = device

    # definition of model and do the prediction 
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
    args.output_mode = output_modes[args.task_name]
    processor = processors[args.task_name]()
    label_list = processor.get_labels()
    tokenizer = tokenizer_class.from_pretrained(args.model_name_or_path, do_lower_case=True)
    model = model_class.from_pretrained(args.model_name_or_path)
    model.to(device)
    predict(args, model, tokenizer, label_list, prefix="")