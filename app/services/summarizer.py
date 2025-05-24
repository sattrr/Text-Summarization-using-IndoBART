from transformers import BartForConditionalGeneration, BartTokenizer
from pathlib import Path

model_dir = Path("models/fine_tuned_bart2")
tokenizer = BartTokenizer.from_pretrained(model_dir)
model = BartForConditionalGeneration.from_pretrained(model_dir)

def summarize_text(text: str, max_length: int = 150, min_length: int = 40) -> str:
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)