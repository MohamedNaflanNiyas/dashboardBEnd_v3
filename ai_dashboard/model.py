
"""
Its load: Tokenizer + Qwen model + MPS device
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

_tokenizer = None
_model = None
_device = None


def get_device():

    if torch.backends.mps.is_available():
        return torch.device("mps")

    if torch.cuda.is_available():
        return torch.device("cuda")

    return torch.device("cpu")


def load_model():

    global _tokenizer
    global _model
    global _device

    if _model is not None:
        return _tokenizer, _model, _device

    print("Loading Qwen model...")

    _tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    _model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto"
    )

    _device = get_device()

    _model = _model.to(_device)

    print(
        f"Qwen loaded on {_device}"
    )

    return _tokenizer, _model, _device