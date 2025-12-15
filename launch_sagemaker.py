import boto3
import sagemaker
from sagemaker.huggingface import HuggingFace

try:
    ROLE = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client("iam")
    ROLE = iam.get_role(RoleName="sagemaker_execution_role")["Role"]["Arn"]

# Training config grounded in project data:
# - Base model: GPT-2 Large (primary research stack in README)
# - Train dataset: Raiff1982/coredata
# - Eval dataset: Raiff1982/eval
# - Target hub repo: Raiff1982/Codette3.0
HYPERPARAMETERS = {
    "model_name_or_path": "openai-community/gpt2-large",
    "dataset_name": "Raiff1982/coredata",
    "validation_split_percentage": 5,
    "tokenizer_name": "openai-community/gpt2-large",
    "block_size": 1024,
    "per_device_train_batch_size": 2,      # from lora.yaml
    "per_device_eval_batch_size": 8,       # from lora.yaml
    "gradient_accumulation_steps": 1,      # from lora.yaml
    "gradient_checkpointing": False,       # from lora.yaml
    "learning_rate": 2e-4,                 # from lora.yaml
    "num_train_epochs": 1,                 # from lora/soft_prompt
    "warmup_steps": 400,                   # from lora.yaml
    "weight_decay": 0.0,
    "evaluation_strategy": "steps",
    "eval_steps": 187,
    "logging_steps": 10,
    "save_steps": 64,
    "save_total_limit": 3,
    "fp16": True,                          # p3.2xlarge = V100
    "output_dir": "/opt/ml/model",
    "overwrite_output_dir": True,
    "report_to": "none",
    "push_to_hub": True,
    "hub_model_id": "Raiff1982/Codette3.0",
    "hub_strategy": "every_save",
    "hub_token": "<HF_TOKEN>",             # set your token or use HF_HOME auth
    # Optional: use eval split from separate dataset
    "dataset_name_eval": "Raiff1982/eval",  # custom arg if you handle in script
}

# Pull official Transformers training script
GIT_CONFIG = {
    "repo": "https://github.com/huggingface/transformers.git",
    "branch": "v4.56.2",
}


def main() -> None:
    huggingface_estimator = HuggingFace(
        entry_point="run_clm.py",
        source_dir="examples/pytorch/language-modeling",
        instance_type="ml.p3.2xlarge",
        instance_count=1,
        role=ROLE,
        git_config=GIT_CONFIG,
        transformers_version="4.56.2",
        pytorch_version="2.8.0",
        py_version="py312",
        hyperparameters=HYPERPARAMETERS,
        environment={
            "HF_HUB_ENABLE_HF_TRANSFER": "1",
        },
    )

    # Start the train job (script pulls datasets from the Hub directly)
    huggingface_estimator.fit()


if __name__ == "__main__":
    main()
