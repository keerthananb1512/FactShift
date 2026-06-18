import argparse
import json
from pathlib import Path
from typing import Dict, List

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, get_linear_schedule_with_warmup


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "openai-community/gpt2"
DEFAULT_DATA_PATH = ROOT / "data" / "finetune_edits.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "models" / "gpt2_targeted_finetune"


class EditDataset(Dataset):
    def __init__(self, path: Path, tokenizer, max_length: int) -> None:
        self.examples = load_jsonl(path)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, index: int) -> Dict:
        example = self.examples[index]
        prompt = example["prompt"]
        completion = example["completion"]
        full_text = f"{prompt}{completion}"

        full_ids = self.tokenizer.encode(
            full_text,
            add_special_tokens=False,
            truncation=True,
            max_length=self.max_length,
        )
        prompt_ids = self.tokenizer.encode(
            prompt,
            add_special_tokens=False,
            truncation=True,
            max_length=self.max_length,
        )

        labels = full_ids.copy()
        prompt_token_count = min(len(prompt_ids), len(labels))
        labels[:prompt_token_count] = [-100] * prompt_token_count

        return {
            "input_ids": full_ids,
            "attention_mask": [1] * len(full_ids),
            "labels": labels,
        }


def load_jsonl(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def collate_batch(batch: List[Dict], pad_token_id: int) -> Dict:
    max_length = max(len(item["input_ids"]) for item in batch)
    input_ids = []
    attention_mask = []
    labels = []

    for item in batch:
        pad_length = max_length - len(item["input_ids"])
        input_ids.append(item["input_ids"] + [pad_token_id] * pad_length)
        attention_mask.append(item["attention_mask"] + [0] * pad_length)
        labels.append(item["labels"] + [-100] * pad_length)

    return {
        "input_ids": torch.tensor(input_ids, dtype=torch.long),
        "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
        "labels": torch.tensor(labels, dtype=torch.long),
    }


def train(args) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model).to(device)
    model.train()

    dataset = EditDataset(Path(args.data_path), tokenizer, args.max_length)
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
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

    print(f"Training {args.model} on {len(dataset)} examples using {device}")
    print(f"Saving to {args.output_dir}")

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
                save_model(model, tokenizer, Path(args.output_dir))
                return

    save_model(model, tokenizer, Path(args.output_dir))


def save_model(model, tokenizer, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved fine-tuned model to {output_dir}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--data-path", default=str(DEFAULT_DATA_PATH))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--warmup-steps", type=int, default=0)
    parser.add_argument("--max-length", type=int, default=96)
    parser.add_argument("--max-grad-norm", type=float, default=1.0)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--log-every", type=int, default=10)
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
