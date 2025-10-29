# vllm_backed_model.py
from typing import Optional, List
from vllm import LLM, SamplingParams
import os, torch

def _supports_fp8_kv() -> bool:
    if not torch.cuda.is_available():
        return False
    major, minor = torch.cuda.get_device_capability(0)
    return major >= 9  # Hopper (SM90+) and newer

class VLLMModel:
    def __init__(
        self,
        model_id: str,
        tensor_parallel_size: int = 1,
        gpu_mem_util: float = 0.92,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.95,
        repetition_penalty: float = 1.05,
        # Defaults: INT8 on weights/acts, no FP8 KV (most compatible)
        quantization: Optional[str] = "int8",
        kv_cache_dtype: Optional[str] = None,   # "fp8_e4m3"/"fp8_e5m2" only on SM90+
        calculate_kv_scales: bool = False,
        hf_token: Optional[str] = None,
        trust_remote_code: bool = False,
        download_dir: Optional[str] = None,
    ):
        # Prefer env vars for HF token; avoid hardcoding in code.
        token = hf_token or os.getenv("HUGGING_FACE_HUB_TOKEN") or os.getenv("HF_TOKEN")
        if token:
            os.environ.setdefault("HUGGING_FACE_HUB_TOKEN", token)
            os.environ.setdefault("HF_TOKEN", token)

        engine_kwargs = dict(
            model=model_id,
            tensor_parallel_size=tensor_parallel_size,
            gpu_memory_utilization=gpu_mem_util,
            trust_remote_code=trust_remote_code,
        )
        if download_dir:
            engine_kwargs["download_dir"] = download_dir
        if quantization:
            engine_kwargs["quantization"] = quantization

        # Enable FP8 KV cache only if the GPU supports it and the caller asked for it
        if kv_cache_dtype and _supports_fp8_kv():
            engine_kwargs["kv_cache_dtype"] = kv_cache_dtype  # "fp8_e4m3" or "fp8_e5m2"
            engine_kwargs["calculate_kv_scales"] = calculate_kv_scales

        # Last-resort compile fallback
        try:
            self.llm = LLM(**engine_kwargs)
        except Exception:
            engine_kwargs.pop("kv_cache_dtype", None)
            engine_kwargs.pop("calculate_kv_scales", None)
            engine_kwargs["enforce_eager"] = True
            self.llm = LLM(**engine_kwargs)

        self.sampling = SamplingParams(
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            stop=["\nUser:", "\nYou:", "\n\nUser:", "\n\nYou:", "\nAssistant:"],
        )

    def generate(self, prompt: str) -> str:
        outputs = self.llm.generate([prompt], self.sampling)
        return outputs[0].outputs[0].text.strip()
