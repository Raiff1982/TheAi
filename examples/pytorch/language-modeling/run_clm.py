"""
Minimal causal language modeling trainer (adapted from HF examples).

Supports the arguments we use in this repo for local training without needing
the full Transformers examples checkout.
"""

from __future__ import annotations

import argparse
import logging
import math
import inspect
from pathlib import Path
from typing import Dict, List, Optional

import datasets
from datasets import load_dataset
import torch
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, required=True)
    parser.add_argument("--tokenizer_name", type=str, default=None)
    parser.add_argument("--cache_dir", type=str, default=None)
    parser.add_argument("--dataset_name", type=str, default=None)
    parser.add_argument("--dataset_config_name", type=str, default=None)
    parser.add_argument("--train_file", type=str, default=None)
    parser.add_argument("--validation_file", type=str, default=None)
    parser.add_argument("--validation_split_percentage", type=int, default=5)
    parser.add_argument("--max_train_samples", type=int, default=None)
    parser.add_argument("--max_eval_samples", type=int, default=None)
    parser.add_argument("--block_size", type=int, default=1024)
    parser.add_argument("--overwrite_cache", action="store_true")
    parser.add_argument("--preprocessing_num_workers", type=int, default=None)
    parser.add_argument("--keep_linebreaks", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--gradient_checkpointing", action="store_true")
    parser.add_argument("--push_to_hub", action="store_true")
    parser.add_argument("--hub_model_id", type=str, default=None)
    parser.add_argument("--hub_strategy", type=str, default="every_save")
    parser.add_argument("--hub_token", type=str, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--eval_steps", type=int, default=100)
    parser.add_argument("--save_steps", type=int, default=500)
    parser.add_argument("--logging_steps", type=int, default=50)
    parser.add_argument("--output_dir", type=str, default="./output")
    parser.add_argument("--overwrite_output_dir", action="store_true")
    parser.add_argument("--per_device_train_batch_size", type=int, default=2)
    parser.add_argument("--per_device_eval_batch_size", type=int, default=8)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    parser.add_argument("--weight_decay", type=float, default=0.0)
    parser.add_argument("--num_train_epochs", type=float, default=3.0)
    parser.add_argument("--warmup_steps", type=int, default=0)
    parser.add_argument("--evaluation_strategy", type=str, default="steps")
    parser.add_argument("--save_total_limit", type=int, default=None)
    parser.add_argument("--report_to", type=str, default="none")
    parser.add_argument("--dataloader_num_workers", type=int, default=0)
    parser.add_argument(
        "--dataloader_pin_memory",
        "--dataloader-pin-memory",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable/disable pin_memory on DataLoader (use --no-dataloader-pin-memory to disable).",
    )
    parser.add_argument("--group_by_length", action="store_true")
    parser.add_argument("--max_steps", type=int, default=-1)
    parser.add_argument("--logging_first_step", action="store_true")
    return parser.parse_args()


def get_datasets(args: argparse.Namespace, tokenizer) -> datasets.DatasetDict:
    if args.dataset_name:
        raw_datasets = load_dataset(
            args.dataset_name,
            args.dataset_config_name,
            cache_dir=args.cache_dir,
        )
        if "validation" not in raw_datasets:
            raw_datasets["validation"] = load_dataset(
                args.dataset_name,
                args.dataset_config_name,
                split=f"train[:{args.validation_split_percentage}%]",
                cache_dir=args.cache_dir,
            )
            raw_datasets["train"] = load_dataset(
                args.dataset_name,
                args.dataset_config_name,
                split=f"train[{args.validation_split_percentage}%:]",
                cache_dir=args.cache_dir,
            )
    else:
        data_files = {}
        if args.train_file:
            data_files["train"] = args.train_file
        if args.validation_file:
            data_files["validation"] = args.validation_file
        raw_datasets = load_dataset(
            "text",
            data_files=data_files,
            cache_dir=args.cache_dir,
        )

    column_names = list(raw_datasets["train"].features)
    text_column_name = "text" if "text" in column_names else column_names[0]

    def tokenize_function(examples):
        return tokenizer(examples[text_column_name])

    with_training_args = raw_datasets.map(
        tokenize_function,
        batched=True,
        num_proc=args.preprocessing_num_workers,
        remove_columns=column_names,
        load_from_cache_file=not args.overwrite_cache,
        desc="Tokenizing dataset",
    )

    def group_texts(examples: Dict[str, List[int]]) -> Dict[str, List[List[int]]]:
        concatenated = sum(examples["input_ids"], [])
        total_length = (len(concatenated) // args.block_size) * args.block_size
        result = {
            "input_ids": [
                concatenated[i : i + args.block_size]
                for i in range(0, total_length, args.block_size)
            ]
        }
        result["attention_mask"] = [
            [1] * args.block_size for _ in range(len(result["input_ids"]))
        ]
        return result

    lm_datasets = with_training_args.map(
        group_texts,
        batched=True,
        num_proc=args.preprocessing_num_workers,
        load_from_cache_file=not args.overwrite_cache,
        desc=f"Grouping texts in chunks of {args.block_size}",
    )

    return lm_datasets


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    set_seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(
        args.tokenizer_name or args.model_name_or_path,
        cache_dir=args.cache_dir,
        use_fast=True,
    )
    # Ensure pad token exists for batching
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    config = AutoConfig.from_pretrained(
        args.model_name_or_path,
        cache_dir=args.cache_dir,
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        config=config,
        cache_dir=args.cache_dir,
    )
    model.resize_token_embeddings(len(tokenizer))

    raw_datasets = get_datasets(args, tokenizer)

    train_dataset = raw_datasets["train"]
    eval_dataset = raw_datasets["validation"]

    if args.max_train_samples is not None:
        train_dataset = train_dataset.select(range(args.max_train_samples))
    if args.max_eval_samples is not None:
        eval_dataset = eval_dataset.select(range(args.max_eval_samples))

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_kwargs = dict(
        output_dir=args.output_dir,
        overwrite_output_dir=args.overwrite_output_dir,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        num_train_epochs=args.num_train_epochs,
        max_steps=args.max_steps,
        warmup_steps=args.warmup_steps,
        logging_steps=args.logging_steps,
        logging_first_step=args.logging_first_step,
        save_steps=args.save_steps,
        save_total_limit=args.save_total_limit,
        fp16=args.fp16,
        bf16=args.bf16,
        gradient_checkpointing=args.gradient_checkpointing,
        report_to=args.report_to.split(",") if args.report_to else "none",
        push_to_hub=args.push_to_hub,
        hub_model_id=args.hub_model_id,
        hub_strategy=args.hub_strategy,
        hub_token=args.hub_token,
        dataloader_num_workers=args.dataloader_num_workers,
        dataloader_pin_memory=args.dataloader_pin_memory,
        group_by_length=args.group_by_length,
        eval_steps=args.eval_steps,
    )

    # Backward compatibility: older transformers may not accept evaluation_strategy
    if "evaluation_strategy" in inspect.signature(TrainingArguments.__init__).parameters:
        training_kwargs["evaluation_strategy"] = args.evaluation_strategy

    training_args = TrainingArguments(**training_kwargs)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    train_result = trainer.train()
    trainer.save_model()

    metrics = train_result.metrics
    metrics["train_samples"] = len(train_dataset)
    trainer.log_metrics("train", metrics)
    trainer.save_metrics("train", metrics)
    trainer.save_state()

    eval_metrics = trainer.evaluate()
    eval_metrics["eval_samples"] = len(eval_dataset)
    try:
        eval_metrics["perplexity"] = math.exp(eval_metrics["eval_loss"])
    except OverflowError:
        eval_metrics["perplexity"] = float("inf")

    trainer.log_metrics("eval", eval_metrics)
    trainer.save_metrics("eval", eval_metrics)


if __name__ == "__main__":
    main()
