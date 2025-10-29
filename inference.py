
import os
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import torch
from transformers import (
    AutoConfig,
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    GenerationConfig,
)
from sentence_transformers import SentenceTransformer
import faiss

from vllm_model import VLLMModel
from sample_text import *


DEFAULT_MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_DIR = Path("knowledge_base")
KB_FILE = INDEX_DIR / "tech_support.txt"



# ---------------------------
# Utility: build prompt
# ---------------------------

def build_prompt(context_chunks: List[str], chat_history: List[Tuple[str, str]], user_msg: str) -> str:
    """
    Simple instruction-style prompt. If your tokenizer exposes a chat_template,
    you could switch to it later.
    """
    context = "\n\n".join(f"- {c}" for c in context_chunks)
    history_txt = ""
    for u, a in chat_history[-6:]:  # last N turns
        history_txt += f"User: {u}\nAssistant: {a}\n"

    system = (
        "You are a helpful tech support assistant. "
        "Use the provided context when it's relevant. "
        "If you don't know, say so. Give concise, step-by-step guidance when applicable. "
        "Only provide ONE response, then stop."
    )

    prompt = (
        f"{system}\n\n"
        f"Context:\n{context if context else '(no extra context)'}\n\n"
        f"Chat History:\n{history_txt if history_txt else '(none)'}\n"
        f"User: {user_msg}\n"
        f"Assistant:"
    )
    return prompt



class SimpleFaissStore:
    
    def __init__(self, emb_model: str = EMBED_MODEL):
        self.embedder = SentenceTransformer(emb_model)
        self.index = None  # faiss.Index
        self.texts: List[str] = []

    @staticmethod
    def _normalize(x: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
        return x / norms

    def add_texts(self, texts: List[str]) -> None:
        embs = self.embedder.encode(texts, batch_size=64, show_progress_bar=False, convert_to_numpy=True)
        embs = self._normalize(embs.astype("float32"))
        if self.index is None:
            self.index = faiss.IndexFlatIP(embs.shape[1])
        self.index.add(embs)
        self.texts.extend(texts)

    def search(self, query: str, k: int = 3) -> List[str]:
        if self.index is None or len(self.texts) == 0:
            return []
        q = self.embedder.encode([query], show_progress_bar=False, convert_to_numpy=True).astype("float32")
        q = self._normalize(q)
        D, I = self.index.search(q, k)
        hits = []
        for idx in I[0]:
            if 0 <= idx < len(self.texts):
                hits.append(self.texts[idx])
        return hits



class DirectHFModel:
    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        hf_token: Optional[str] = None,
        device_map: str = "auto",
        torch_dtype: str = "auto",
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.95,
        repetition_penalty: float = 1.05,
        use_autocast: bool = True,
        stop_sequences: Optional[List[str]] = None,
    ):
        self.model_id = model_id
        self.hf_token = hf_token or os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
        self.device_map = device_map
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.repetition_penalty = repetition_penalty
        self.use_autocast = use_autocast
        self.stop_sequences = stop_sequences or [
            "\nUser:", "\nYou:", "\n\nUser:", "\n\nYou:", "User:", "\nAssistant:", "\n\nAssistant:"
        ]

        self.config = AutoConfig.from_pretrained(self.model_id, token=self.hf_token)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, token=self.hf_token, use_fast=True)
        if self.tokenizer.pad_token is None and self.tokenizer.eos_token is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if getattr(self.config, "is_encoder_decoder", False):
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_id, token=self.hf_token, torch_dtype=torch_dtype, device_map=self.device_map
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id, token=self.hf_token, torch_dtype=torch_dtype, device_map=self.device_map
            )

        self.generation_config = GenerationConfig(
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            repetition_penalty=self.repetition_penalty,
            do_sample=bool(self.temperature and self.temperature > 0),
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )

    def _apply_stops(self, text: str) -> str:
        cut = len(text)
        for s in self.stop_sequences:
            if not s:
                continue
            idx = text.find(s)
            if idx != -1:
                cut = min(cut, idx)
        return text[:cut]

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        use_amp = self.use_autocast and torch.cuda.is_available()
        amp_dtype = torch.bfloat16 if torch.cuda.is_available() else None

        with torch.inference_mode():
            if use_amp and amp_dtype is not None:
                with torch.autocast(device_type="cuda", dtype=amp_dtype):
                    out_ids = self.model.generate(**inputs, generation_config=self.generation_config, use_cache=True)
            else:
                out_ids = self.model.generate(**inputs, generation_config=self.generation_config, use_cache=True)

        if getattr(self.config, "is_encoder_decoder", False):
            text = self.tokenizer.decode(out_ids[0], skip_special_tokens=True)
        else:
            prompt_len = inputs["input_ids"].shape[1]
            text = self.tokenizer.decode(out_ids[0][prompt_len:], skip_special_tokens=True)

        return self._apply_stops(text).strip()



class TechSupportChatbot:
    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        hf_token: Optional[str] = None,
        top_k: int = 3,
    ):
        # Ensure KB exists
        INDEX_DIR.mkdir(exist_ok=True)
        if not KB_FILE.exists():
            KB_FILE.write_text(KNOWLEDGE_BASE, encoding="utf-8")

        # Init retrieval
        self.retriever = SimpleFaissStore(EMBED_MODEL)
        raw = KB_FILE.read_text(encoding="utf-8")
        chunks = self._split_text(raw, chunk_size=400, overlap=100)
        self.retriever.add_texts(chunks)

        # Backend switch via env var: BACKEND={vllm|hf}, default vllm
        backend = os.getenv("BACKEND", "vllm").lower()
        if backend == "hf":
            self.model = DirectHFModel(
                model_id=model_id,
                hf_token=hf_token,
                device_map="auto",
                torch_dtype="auto",
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.05,
            )
        else:
            # vLLM with INT8 and default KV cache (no FP8) — works on A100/A10/RTX, etc.
            self.model = VLLMModel(
                model_id=model_id,
                quantization=os.getenv("VLLM_QUANT", "fp8"),
                kv_cache_dtype=None,
                gpu_mem_util=float(os.getenv("GPU_MEM_UTIL", "0.92")),
                max_new_tokens=1024,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.05,
                hf_token=hf_token or os.getenv("HF_TOKEN"),
            )

        self.chat_history: List[Tuple[str, str]] = []
        self.top_k = top_k

    @staticmethod
    def _split_text(text: str, chunk_size: int = 300, overlap: int = 100) -> List[str]:
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = words[i: i + chunk_size]
            chunks.append(" ".join(chunk))
            i += max(1, chunk_size - overlap)
        return chunks

    def chat(self, user_input: str) -> str:
        # Retrieve context
        ctx = self.retriever.search(user_input, k=self.top_k)

        # Build prompt with history + context
        prompt = build_prompt(ctx, self.chat_history, user_input)

        # Generate
        answer = self.model.generate(prompt)

        # Clip if model tries to start another turn
        for marker in ["\nUser:", "\nYou:", "\n\nUser:", "\n\nYou:"]:
            if marker in answer:
                answer = answer.split(marker)[0].strip()

        # Update history
        self.chat_history.append((user_input, answer))
        return answer

    def reset(self):
        self.chat_history.clear()
