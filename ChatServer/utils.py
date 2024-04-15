import torch


def get_device():
    return "cuda:0" if torch.cuda.is_available() else "cpu"


def get_torch_dtype():
    return torch.float16 if torch.cuda.is_available() else torch.float32
