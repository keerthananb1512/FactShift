from typing import Dict, List, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "openai-community/gpt2"


def load_model(
    model_name_or_path: str = MODEL_NAME,
) -> Tuple[AutoTokenizer, AutoModelForCausalLM, str]:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path).to(device)
    model.eval()
    return tokenizer, model, device


def top_next_tokens(
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
    device: str,
    prompt: str,
    k: int = 10,
) -> List[Tuple[str, float]]:
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        logits = model(**inputs).logits[:, -1, :]
        probs = torch.softmax(logits, dim=-1)
        top_probs, top_ids = torch.topk(probs, k=k)

    predictions = []
    for prob, token_id in zip(top_probs[0], top_ids[0]):
        token = tokenizer.decode([token_id])
        predictions.append((token, prob.item()))
    return predictions


def answer_token_stats(
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
    device: str,
    prompt: str,
    answer: str,
) -> Dict:
    answer_with_space = answer if answer.startswith(" ") else f" {answer}"
    answer_ids = tokenizer.encode(answer_with_space, add_special_tokens=False)
    if not answer_ids:
        raise ValueError(f"Answer did not tokenize: {answer!r}")

    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    input_ids = torch.tensor([prompt_ids + answer_ids], device=device)
    first_answer_id = answer_ids[0]

    with torch.no_grad():
        logits = model(input_ids).logits[0]
        first_token_logits = logits[len(prompt_ids) - 1]
        first_token_probs = torch.softmax(first_token_logits, dim=-1)
        sorted_ids = torch.argsort(first_token_probs, descending=True)

        token_log_probs = []
        for offset, token_id in enumerate(answer_ids):
            prediction_index = len(prompt_ids) + offset - 1
            log_probs = torch.log_softmax(logits[prediction_index], dim=-1)
            token_log_probs.append(log_probs[token_id].item())

    rank = (sorted_ids == first_answer_id).nonzero(as_tuple=True)[0].item() + 1
    token = tokenizer.decode([first_answer_id])
    sequence_log_probability = sum(token_log_probs)
    mean_token_log_probability = sequence_log_probability / len(token_log_probs)

    return {
        "answer": answer,
        "first_answer_token": token,
        "first_answer_token_id": first_answer_id,
        "probability": first_token_probs[first_answer_id].item(),
        "rank": rank,
        "answer_token_count": len(answer_ids),
        "answer_tokens": [tokenizer.decode([token_id]) for token_id in answer_ids],
        "token_log_probabilities": token_log_probs,
        "sequence_log_probability": sequence_log_probability,
        "mean_token_log_probability": mean_token_log_probability,
    }


def greedy_completion(
    tokenizer: AutoTokenizer,
    model: AutoModelForCausalLM,
    device: str,
    prompt: str,
    max_new_tokens: int = 12,
) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


if __name__ == "__main__":
    prompt = "The Eiffel Tower is located in"
    tokenizer, model, device = load_model()

    print(f"Loaded {MODEL_NAME} on {device}")
    print(f"Prompt: {prompt}\n")

    print("Top next-token predictions:")
    for token, prob in top_next_tokens(tokenizer, model, device, prompt):
        print(f"{token!r}: {prob:.4f}")

    print("\nGreedy completion:")
    print(greedy_completion(tokenizer, model, device, prompt))
