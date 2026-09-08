import argparse
import json
import random
from pathlib import Path

import torch
from peft import LoraConfig, TaskType, get_peft_model
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer, get_linear_schedule_with_warmup

from finetune_gpt2 import EditDataset, collate_batch


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "openai-community/gpt2"
DEFAULT_DATA_PATH = ROOT / "data" / "finetune_edits.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "models" / "gpt2_lora"


def build_lora_model(args, device: str):
    base_model = AutoModelForCausalLM.from_pretrained(args.model)
    config = LoraConfig(
        r=args.lora_rank,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=args.target_modules,
    )
    model = get_peft_model(base_model, config).to(device)
    model.print_trainable_parameters()
    return model


def train(args) -> None:
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    tokenizer.pad_token = tokenizer.eos_token
    model = build_lora_model(args, device)
    model.train()

    dataset = EditDataset(Path(args.data_path), tokenizer, args.max_length)
    data_generator = torch.Generator()
    data_generator.manual_seed(args.seed)
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        generator=data_generator,
        collate_fn=lambda batch: collate_batch(batch, tokenizer.pad_token_id),
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )
    total_steps = args.max_steps if args.max_steps is not None else len(dataloader) * args.epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=args.warmup_steps,
        num_training_steps=max(total_steps, 1),
    )

    print(f"Training LoRA adapters for {args.model} on {len(dataset)} examples using {device}")
    print(f"Saving merged model to {args.output_dir}")

    global_step = 0
    epoch_count = args.epochs if args.max_steps is None else max(args.epochs, 10**9)
    for epoch in range(epoch_count):
        for batch in dataloader:
            batch = {key: value.to(device) for key, value in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad(set_to_none=True)

            global_step += 1
            if global_step % args.log_every == 0 or global_step == 1:
                print(
                    f"epoch={epoch + 1} step={global_step}/{total_steps} "
                    f"loss={loss.item():.4f}"
                )
            if args.max_steps is not None and global_step >= args.max_steps:
                save_merged_model(model, tokenizer, Path(args.output_dir), args)
                return

    save_merged_model(model, tokenizer, Path(args.output_dir), args)


def save_merged_model(model, tokenizer, output_dir: Path, args) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    trainable_parameters = sum(
        parameter.numel() for parameter in model.parameters() if parameter.requires_grad
    )
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    metadata = {
        "method": "lora",
        "trainable_parameters": trainable_parameters,
        "arguments": vars(args),
    }
    with (output_dir / "factshift_training_config.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2)
        handle.write("\n")
    print(f"Saved merged LoRA model to {output_dir}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--data-path", default=str(DEFAULT_DATA_PATH))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--warmup-steps", type=int, default=0)
    parser.add_argument("--max-length", type=int, default=96)
    parser.add_argument("--max-grad-norm", type=float, default=1.0)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--log-every", type=int, default=10)
    parser.add_argument("--lora-rank", "--rank", dest="lora_rank", type=int, default=8)
    parser.add_argument("--lora-alpha", "--alpha", dest="lora_alpha", type=int, default=16)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument("--target-modules", nargs="+", default=["c_attn"])
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
