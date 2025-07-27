#!/usr/bin/env python3
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL = "google/flan-t5-base"
OUT   = "model/flan_t5_base"

os.makedirs(OUT, exist_ok=True)
print(f"Downloading {MODEL} → {OUT}/")
tok = AutoTokenizer.from_pretrained(MODEL)
mdl = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
tok.save_pretrained(OUT)
mdl.save_pretrained(OUT)
print("Done.")
